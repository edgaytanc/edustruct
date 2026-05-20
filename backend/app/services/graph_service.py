"""
Application service for the EduStruct course prerequisite graph.

The service coordinates graph use cases for the future REST layer while keeping
Graph independent from Flask and HTTP details. It builds the demo graph from the
existing course and prerequisite datasets.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from app.errors.exceptions import DatasetError, DuplicateKeyError, NotFoundError, ValidationError
from app.serializers.react_flow_serializer import serialize_graph
from app.structures.graph import Graph, GraphNode, GraphTraversalResult


class GraphService:
    """Service that exposes graph operations for course prerequisite maps."""

    def __init__(self, dataset_root: Optional[Path] = None) -> None:
        self._graph = Graph(directed=True)
        self._dataset_root = dataset_root or self._default_dataset_root()
        self._last_traversal: Optional[dict[str, Any]] = None
        self._last_search: Optional[dict[str, Any]] = None

    def state(self) -> dict[str, Any]:
        """Return current graph state and React Flow contract."""
        return self._build_result()

    def add_node(self, node_id: Any, value: Any = None) -> dict[str, Any]:
        """Add a course node to the graph."""
        normalized_id = self._validate_node_id(node_id)
        before = self._build_visual_snapshot()
        try:
            node = self._graph.add_node(normalized_id, value if value is not None else normalized_id)
        except ValueError as error:
            self._raise_structure_error(str(error), normalized_id)
            raise

        result = self._build_result(before=before)
        result["operation"] = "add-node"
        result["node"] = self._node_to_result(node)
        self._clear_visual_context()
        return result

    def add_edge(self, source_id: Any, target_id: Any) -> dict[str, Any]:
        """Add a directed prerequisite edge: prerequisite course -> unlocked course."""
        source = self._validate_node_id(source_id, field="sourceId")
        target = self._validate_node_id(target_id, field="targetId")
        before = self._build_visual_snapshot()
        try:
            created_source, created_target = self._graph.add_edge(source, target)
        except ValueError as error:
            self._raise_structure_error(str(error), source, target)
            raise

        result = self._build_result(before=before)
        result["operation"] = "add-edge"
        result["edge"] = {"source": created_source, "target": created_target}
        self._clear_visual_context()
        return result

    def search(self, node_id: Any) -> dict[str, Any]:
        """Search a course node by id."""
        normalized_id = self._validate_node_id(node_id)
        search_result = self._graph.search(normalized_id).to_dict()
        self._last_search = search_result
        result = self._build_result(search=search_result)
        result["operation"] = "search"
        result["query"] = normalized_id
        result["found"] = search_result["found"]
        result["search"] = search_result
        result["node"] = search_result["node"]
        return result

    def traverse(self, algorithm: Any, start_node_id: Any) -> dict[str, Any]:
        """Execute DFS or BFS and return traversal animation steps."""
        normalized_algorithm = self._validate_algorithm(algorithm)
        start = self._validate_node_id(start_node_id, field="startNodeId")
        try:
            traversal = self._graph.dfs(start) if normalized_algorithm == "DFS" else self._graph.bfs(start)
        except ValueError as error:
            self._raise_structure_error(str(error), start)
            raise

        traversal_payload = traversal.to_dict()
        self._last_traversal = traversal_payload
        self._last_search = None
        result = self._build_result(traversal=traversal_payload)
        result["operation"] = "traverse"
        result["traversal"] = traversal_payload
        result["order"] = traversal_payload["order"]
        result["steps"] = traversal_payload["steps"]
        return result

    def dfs(self, start_node_id: Any) -> dict[str, Any]:
        """Execute DFS from a start node."""
        return self.traverse("DFS", start_node_id)

    def bfs(self, start_node_id: Any) -> dict[str, Any]:
        """Execute BFS from a start node."""
        return self.traverse("BFS", start_node_id)

    def metrics(self) -> dict[str, Any]:
        """Return graph metrics."""
        result = self._build_result()
        result["metricsOnly"] = True
        return result

    def load_demo(self) -> dict[str, Any]:
        """Load the course prerequisite graph from courses.json and prerequisites.json."""
        before = self._build_visual_snapshot()
        courses = self._load_json_file("courses.json")
        prerequisites = self._load_json_file("prerequisites.json")

        if not isinstance(courses, list) or not isinstance(prerequisites, list):
            raise DatasetError(
                message="Los datasets de cursos y prerrequisitos deben ser listas JSON.",
                details=[{"files": ["courses.json", "prerequisites.json"], "issue": "MUST_BE_LISTS"}],
            )

        graph = Graph(directed=True)
        course_ids: set[str] = set()
        for index, course in enumerate(courses):
            if not isinstance(course, dict):
                raise DatasetError(
                    message="Cada curso del dataset debe ser un objeto JSON.",
                    details=[{"field": f"courses[{index}]", "issue": "MUST_BE_OBJECT"}],
                )
            course_id = self._validate_dataset_field(course, "id", f"courses[{index}].id")
            course_ids.add(course_id)
            graph.add_node(course_id, self._course_value(course))

        loaded_edges: list[dict[str, str]] = []
        for index, relation in enumerate(prerequisites):
            if not isinstance(relation, dict):
                raise DatasetError(
                    message="Cada prerrequisito del dataset debe ser un objeto JSON.",
                    details=[{"field": f"prerequisites[{index}]", "issue": "MUST_BE_OBJECT"}],
                )
            course_id = self._validate_dataset_field(relation, "course_id", f"prerequisites[{index}].course_id")
            prerequisite_id = self._validate_dataset_field(
                relation,
                "prerequisite_id",
                f"prerequisites[{index}].prerequisite_id",
            )
            if course_id not in course_ids or prerequisite_id not in course_ids:
                raise DatasetError(
                    message="El dataset de prerrequisitos referencia cursos inexistentes.",
                    details=[
                        {
                            "field": f"prerequisites[{index}]",
                            "courseId": course_id,
                            "prerequisiteId": prerequisite_id,
                            "issue": "UNKNOWN_COURSE_REFERENCE",
                        }
                    ],
                )
            graph.add_edge(prerequisite_id, course_id)
            loaded_edges.append({"source": prerequisite_id, "target": course_id})

        self._graph = graph
        self._clear_visual_context()
        result = self._build_result(before=before)
        result["operation"] = "load-demo"
        result["loaded"] = {"courses": len(courses), "prerequisites": len(loaded_edges)}
        result["context"] = "Grafo dirigido de prerrequisitos universitarios: prerrequisito -> curso habilitado"
        return result

    def reset(self) -> dict[str, Any]:
        """Clear graph state."""
        before = self._build_visual_snapshot()
        self._graph = Graph(directed=True)
        self._clear_visual_context()
        result = self._build_result(before=before)
        result["reset"] = True
        result["operation"] = "reset"
        return result

    def _build_result(
        self,
        before: Optional[dict[str, Any]] = None,
        traversal: Optional[dict[str, Any]] = None,
        search: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        traversal_payload = traversal if traversal is not None else self._last_traversal
        search_payload = search if search is not None else self._last_search
        visualization = self._build_visual_snapshot(traversal=traversal_payload, search=search_payload)
        graph_payload = self._graph_payload()
        return {
            "graph": graph_payload,
            "directed": self._graph.directed,
            "verticesCount": self._graph.vertices_count,
            "edgesCount": self._graph.edges_count,
            "isEmpty": self._graph.is_empty(),
            "nodes": visualization["nodes"],
            "edges": visualization["edges"],
            "before": before,
            "after": visualization,
            "traversal": traversal_payload,
            "search": search_payload,
            "lastOperation": self._graph.last_operation,
            "metrics": self._build_metrics(edges_count=len(visualization["edges"])),
        }

    def _build_visual_snapshot(
        self,
        traversal: Optional[dict[str, Any]] = None,
        search: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        return serialize_graph(graph=self._graph_payload(), traversal=traversal, search=search)

    def _graph_payload(self) -> dict[str, Any]:
        payload = self._graph.to_dict()
        for node in payload["nodes"]:
            node["inDegree"] = self._graph.in_degree(node["id"])
        return payload

    def _build_metrics(self, edges_count: int) -> dict[str, Any]:
        node_count = self._graph.vertices_count
        edge_count = self._graph.edges_count
        isolated_count = 0
        max_out_degree = 0
        max_in_degree = 0
        for node in self._graph.nodes():
            out_degree = node.degree()
            in_degree = self._graph.in_degree(node.id)
            max_out_degree = max(max_out_degree, out_degree)
            max_in_degree = max(max_in_degree, in_degree)
            if out_degree == 0 and in_degree == 0:
                isolated_count += 1

        return {
            "count": node_count,
            "verticesCount": node_count,
            "edgesCount": edge_count,
            "visualEdgesCount": edges_count,
            "connectedComponents": self._graph.connected_components_count(),
            "isolatedVertices": isolated_count,
            "maxOutDegree": max_out_degree,
            "maxInDegree": max_in_degree,
            "density": self._density(node_count, edge_count),
            "height": None,
            "balanceFactor": None,
            "collisions": None,
            "levels": None,
        }

    @staticmethod
    def _node_to_result(node: GraphNode) -> dict[str, Any]:
        return node.to_dict()

    @staticmethod
    def _density(vertices_count: int, edges_count: int) -> float:
        if vertices_count <= 1:
            return 0
        return round(edges_count / (vertices_count * (vertices_count - 1)), 4)

    def _load_json_file(self, filename: str) -> Any:
        path = self._dataset_root / filename
        if not path.exists():
            raise DatasetError(
                message="No se encontró el dataset requerido para el grafo.",
                details=[{"file": str(path), "issue": "FILE_NOT_FOUND"}],
            )
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise DatasetError(
                message="El dataset contiene JSON inválido.",
                details=[{"file": str(path), "issue": "INVALID_JSON", "error": str(error)}],
            ) from error

    @staticmethod
    def _course_value(course: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": course.get("id"),
            "code": course.get("code"),
            "name": course.get("name"),
            "credits": course.get("credits"),
            "cycleId": course.get("cycle_id"),
            "description": course.get("description"),
        }

    @staticmethod
    def _validate_dataset_field(item: dict[str, Any], key: str, field: str) -> str:
        value = item.get(key)
        if value is None or not str(value).strip():
            raise DatasetError(
                message="El dataset tiene campos obligatorios vacíos.",
                details=[{"field": field, "issue": "REQUIRED"}],
            )
        return str(value).strip()

    @staticmethod
    def _validate_node_id(node_id: Any, field: str = "nodeId") -> str:
        if node_id is None:
            raise ValidationError(
                message="El identificador del nodo es obligatorio.",
                details=[{"field": field, "issue": "REQUIRED"}],
            )
        normalized = str(node_id).strip()
        if not normalized:
            raise ValidationError(
                message="El identificador del nodo no puede estar vacío.",
                details=[{"field": field, "issue": "EMPTY_STRING"}],
            )
        return normalized

    @staticmethod
    def _validate_algorithm(algorithm: Any) -> str:
        normalized = str(algorithm or "").strip().upper()
        if normalized not in {"DFS", "BFS"}:
            raise ValidationError(
                message="El algoritmo de recorrido debe ser DFS o BFS.",
                details=[{"field": "algorithm", "issue": "INVALID_TRAVERSAL_ALGORITHM"}],
            )
        return normalized

    @staticmethod
    def _default_dataset_root() -> Path:
        return Path(__file__).resolve().parents[3] / "datasets"

    def _clear_visual_context(self) -> None:
        self._last_traversal = None
        self._last_search = None

    @staticmethod
    def _raise_structure_error(error_code: str, source: str, target: Optional[str] = None) -> None:
        details = [{"source": source, "target": target, "issue": error_code}]
        if error_code == "DUPLICATE_NODE" or error_code == "DUPLICATE_EDGE":
            raise DuplicateKeyError(message="El nodo o arista ya existe en el grafo.", details=details)
        if error_code in {"SOURCE_NODE_NOT_FOUND", "TARGET_NODE_NOT_FOUND", "START_NODE_NOT_FOUND"}:
            raise NotFoundError(message="El nodo solicitado no existe en el grafo.", details=details)
        raise ValidationError(message="Operación inválida para el grafo.", details=details)
