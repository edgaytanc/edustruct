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


def serialize_binary_tree(items: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """
    Serialize a binary tree levelorder list into React Flow nodes and edges.

    Expected item contract:
    - id: unique node id, usually str(value)
    - label: visual label
    - value: original comparable value
    - level: zero-based visual level
    - parentId: optional parent node id
    - direction: optional left/right relationship from parent
    - hasLeft / hasRight / childrenCount: optional structural metadata

    The layout keeps the root centered and separates children horizontally by
    level, producing a deterministic hierarchy suitable for React Flow.
    """
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []

    if not items:
        return {"nodes": nodes, "edges": edges}

    max_level = 0
    for item in items:
        level = int(item.get("level", 0))
        if level > max_level:
            max_level = level

    for item in items:
        level = int(item.get("level", 0))
        direction = item.get("direction")
        node_id = str(item["id"])
        parent_id = item.get("parentId")

        x = _binary_tree_x_position(item=item, max_level=max_level)
        y = BASE_Y + (level * VERTICAL_GAP)

        metadata = dict(item.get("metadata") or {})
        metadata.update(
            {
                "value": item.get("value"),
                "level": level,
                "parentId": parent_id,
                "parentValue": item.get("parentValue"),
                "direction": direction,
                "hasLeft": item.get("hasLeft", False),
                "hasRight": item.get("hasRight", False),
                "childrenCount": item.get("childrenCount", 0),
            }
        )

        category = "root" if parent_id is None else direction or "child"
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

        if parent_id is not None:
            edges.append(
                create_react_flow_edge(
                    edge_id=f"binary-tree-edge-{parent_id}-{node_id}",
                    source=parent_id,
                    target=node_id,
                    edge_type="smoothstep",
                    label=direction,
                    animated=False,
                    relationship=direction,
                )
            )

    return {"nodes": nodes, "edges": edges}


def _binary_tree_x_position(item: dict[str, Any], max_level: int) -> int:
    """Return deterministic horizontal position from BST path metadata."""
    level = int(item.get("level", 0))
    path = _binary_tree_path_code(item)
    remaining_depth = max(max_level - level, 0)
    slot_width = HORIZONTAL_GAP * (2 ** remaining_depth)
    offset = 0

    for index, direction in enumerate(path):
        depth_from_node = len(path) - index - 1
        step = HORIZONTAL_GAP * (2 ** depth_from_node)
        offset += -step if direction == "left" else step

    if level == 0:
        return BASE_X

    return BASE_X + (offset * max(slot_width // HORIZONTAL_GAP, 1))


def _binary_tree_path_code(item: dict[str, Any]) -> list[str]:
    """
    Build a best-effort path code for a levelorder binary-tree item.

    The BinaryTree structure provides only direct parent direction. To keep this
    serializer stateless and compatible with the current contract, it accepts an
    optional path field and falls back to repeating the direct direction by level.
    The fallback remains deterministic and visually separates left/right sides.
    """
    path = item.get("path")
    if isinstance(path, list) and all(direction in {"left", "right"} for direction in path):
        return path

    direction = item.get("direction")
    level = int(item.get("level", 0))

    if direction not in {"left", "right"} or level <= 0:
        return []

    return [direction] * level
