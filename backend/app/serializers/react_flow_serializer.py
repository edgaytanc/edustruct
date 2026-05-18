"""
React Flow serializers for EduStruct structures.

This module converts pure data-structure state into a visual JSON contract
compatible with React Flow. It does not depend on Flask or any HTTP concern.
"""

from __future__ import annotations

from typing import Any


HORIZONTAL_GAP = 220
VERTICAL_GAP = 140
BASE_X = 0
BASE_Y = 0


def create_react_flow_node(
    node_id,
    label,
    x=0,
    y=0,
    node_type="default",
    category=None,
    metadata=None,
):
    return {
        "id": str(node_id),
        "type": node_type,
        "position": {
            "x": x,
            "y": y,
        },
        "data": {
            "label": str(label),
            "category": category,
            "metadata": metadata or {},
        },
    }


def create_react_flow_edge(
    edge_id,
    source,
    target,
    edge_type="smoothstep",
    label=None,
    animated=False,
    relationship=None,
):
    return {
        "id": str(edge_id),
        "source": str(source),
        "target": str(target),
        "type": edge_type,
        "label": label,
        "animated": animated,
        "data": {
            "relationship": relationship,
        },
    }


def serialize_linked_list(items: list[Any]) -> dict[str, list[dict[str, Any]]]:
    """Serialize a linked list as HEAD -> items -> TAIL."""
    nodes = [
        create_react_flow_node(
            node_id="list-head-marker",
            label="HEAD",
            x=BASE_X,
            y=BASE_Y,
            category="head",
            metadata={"role": "head-marker"},
        )
    ]
    edges = []

    previous_id = "list-head-marker"

    for index, item in enumerate(items):
        node_id = f"list-node-{index}"
        category = _linear_item_category(index=index, total=len(items), first="head", last="tail")
        nodes.append(
            create_react_flow_node(
                node_id=node_id,
                label=item,
                x=BASE_X + ((index + 1) * HORIZONTAL_GAP),
                y=BASE_Y,
                category=category,
                metadata={
                    "role": "item",
                    "index": index,
                    "value": item,
                    "isHead": index == 0,
                    "isTail": index == len(items) - 1,
                },
            )
        )
        edges.append(
            create_react_flow_edge(
                edge_id=f"list-edge-{previous_id}-{node_id}",
                source=previous_id,
                target=node_id,
                animated=True,
                relationship="next",
            )
        )
        previous_id = node_id

    tail_x = BASE_X + ((len(items) + 1) * HORIZONTAL_GAP)
    nodes.append(
        create_react_flow_node(
            node_id="list-tail-marker",
            label="TAIL",
            x=tail_x,
            y=BASE_Y,
            category="tail",
            metadata={"role": "tail-marker"},
        )
    )
    edges.append(
        create_react_flow_edge(
            edge_id=f"list-edge-{previous_id}-list-tail-marker",
            source=previous_id,
            target="list-tail-marker",
            animated=True,
            relationship="next",
        )
    )

    return {"nodes": nodes, "edges": edges}


def serialize_queue(items: list[Any]) -> dict[str, list[dict[str, Any]]]:
    """Serialize a queue as FRONT -> items -> REAR."""
    nodes = [
        create_react_flow_node(
            node_id="queue-front-marker",
            label="FRONT",
            x=BASE_X,
            y=BASE_Y,
            category="front",
            metadata={"role": "front-marker"},
        )
    ]
    edges = []

    previous_id = "queue-front-marker"

    for index, item in enumerate(items):
        node_id = f"queue-node-{index}"
        category = _linear_item_category(index=index, total=len(items), first="front", last="rear")
        nodes.append(
            create_react_flow_node(
                node_id=node_id,
                label=item,
                x=BASE_X + ((index + 1) * HORIZONTAL_GAP),
                y=BASE_Y,
                category=category,
                metadata={
                    "role": "item",
                    "indexFromFront": index,
                    "value": item,
                    "isFront": index == 0,
                    "isRear": index == len(items) - 1,
                },
            )
        )
        edges.append(
            create_react_flow_edge(
                edge_id=f"queue-edge-{previous_id}-{node_id}",
                source=previous_id,
                target=node_id,
                animated=True,
                relationship="next",
            )
        )
        previous_id = node_id

    rear_x = BASE_X + ((len(items) + 1) * HORIZONTAL_GAP)
    nodes.append(
        create_react_flow_node(
            node_id="queue-rear-marker",
            label="REAR",
            x=rear_x,
            y=BASE_Y,
            category="rear",
            metadata={"role": "rear-marker"},
        )
    )
    edges.append(
        create_react_flow_edge(
            edge_id=f"queue-edge-{previous_id}-queue-rear-marker",
            source=previous_id,
            target="queue-rear-marker",
            animated=True,
            relationship="next",
        )
    )

    return {"nodes": nodes, "edges": edges}


def serialize_stack(items: list[Any]) -> dict[str, list[dict[str, Any]]]:
    """Serialize a stack vertically as TOP -> items from top to bottom."""
    nodes = [
        create_react_flow_node(
            node_id="stack-top-marker",
            label="TOP",
            x=BASE_X,
            y=BASE_Y,
            category="top",
            metadata={"role": "top-marker"},
        )
    ]
    edges = []

    previous_id = "stack-top-marker"

    for index, item in enumerate(items):
        node_id = f"stack-node-{index}"
        category = "top" if index == 0 else "item"
        nodes.append(
            create_react_flow_node(
                node_id=node_id,
                label=item,
                x=BASE_X,
                y=BASE_Y + ((index + 1) * VERTICAL_GAP),
                category=category,
                metadata={
                    "role": "item",
                    "indexFromTop": index,
                    "value": item,
                    "isTop": index == 0,
                },
            )
        )
        edges.append(
            create_react_flow_edge(
                edge_id=f"stack-edge-{previous_id}-{node_id}",
                source=previous_id,
                target=node_id,
                edge_type="straight",
                animated=False,
                relationship="below",
            )
        )
        previous_id = node_id

    return {"nodes": nodes, "edges": edges}


def _linear_item_category(index: int, total: int, first: str, last: str) -> str:
    if total == 1:
        return f"{first}-{last}"

    if index == 0:
        return first

    if index == total - 1:
        return last

    return "item"


def serialize_general_tree(items: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """
    Serialize a general tree levelorder list into React Flow nodes and edges.

    Expected item contract:
    - id: unique node id
    - label: visual label
    - category: faculty, career, cycle, course, etc.
    - level: zero-based visual level
    - parentId: optional parent id
    - metadata: optional extra data
    """
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    level_counters: dict[int, int] = {}

    for item in items:
        level = int(item.get("level", 0))
        index_in_level = level_counters.get(level, 0)
        level_counters[level] = index_in_level + 1

        x = BASE_X + (index_in_level * HORIZONTAL_GAP)
        y = BASE_Y + (level * VERTICAL_GAP)

        node_id = item["id"]
        category = item.get("category", "academic")
        metadata = dict(item.get("metadata") or {})
        metadata.update(
            {
                "level": level,
                "parentId": item.get("parentId"),
                "childrenCount": item.get("childrenCount", 0),
            }
        )

        nodes.append(
            create_react_flow_node(
                node_id=node_id,
                label=item.get("label", node_id),
                x=x,
                y=y,
                category=category,
                metadata=metadata,
            )
        )

        parent_id = item.get("parentId")
        if parent_id:
            edges.append(
                create_react_flow_edge(
                    edge_id=f"tree-edge-{parent_id}-{node_id}",
                    source=parent_id,
                    target=node_id,
                    edge_type="smoothstep",
                    animated=False,
                    relationship="parent-child",
                )
            )

    return {"nodes": nodes, "edges": edges}
