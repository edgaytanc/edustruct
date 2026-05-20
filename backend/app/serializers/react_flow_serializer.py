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


def serialize_avl_tree(items: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """
    Serialize an AVL tree levelorder list into React Flow nodes and edges.

    Extends the binary-tree visual contract with AVL metadata:
    - height: internal one-based AVL height
    - visualHeight: zero-based height for UI explanations
    - balanceFactor: left subtree height minus right subtree height
    - isUnbalanced: True when abs(balanceFactor) > 1

    The function remains stateless and deterministic, matching the existing
    binary tree serializer layout so the frontend can reuse React Flow patterns.
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
        balance_factor = item.get("balanceFactor", 0)
        is_unbalanced = bool(item.get("isUnbalanced", abs(balance_factor) > 1))

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
                "height": item.get("height", 1),
                "visualHeight": item.get("visualHeight", max(item.get("height", 1) - 1, 0)),
                "balanceFactor": balance_factor,
                "isUnbalanced": is_unbalanced,
                "structure": "avl-tree",
            }
        )

        if parent_id is None:
            category = "root"
        elif is_unbalanced:
            category = "unbalanced"
        else:
            category = direction or "child"

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
                    edge_id=f"avl-tree-edge-{parent_id}-{node_id}",
                    source=parent_id,
                    target=node_id,
                    edge_type="smoothstep",
                    label=direction,
                    animated=False,
                    relationship=direction,
                )
            )

    return {"nodes": nodes, "edges": edges}



def serialize_btree(items: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """
    Serialize B-Tree level-order entries into React Flow nodes and edges.

    Expected item contract:
    - id: stable node id generated by the BTree structure
    - keys: ordered keys stored in the multi-key node
    - leaf: True when the node has no children
    - level: zero-based visual level
    - parentId: optional parent node id
    - childIndex: optional child slot from the parent
    - keyCount: number of keys in the B-Tree node

    B-Tree nodes are wider than binary nodes because a single visual node can
    represent multiple ordered keys. The layout groups nodes by level and keeps
    sibling order deterministic through childIndex and level-order position.
    """
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []

    if not items:
        return {"nodes": nodes, "edges": edges}

    level_counters: dict[int, int] = {}
    level_totals: dict[int, int] = {}
    for item in items:
        level = int(item.get("level", 0))
        level_totals[level] = level_totals.get(level, 0) + 1

    for item in items:
        level = int(item.get("level", 0))
        index_in_level = level_counters.get(level, 0)
        level_counters[level] = index_in_level + 1

        keys = list(item.get("keys") or [])
        node_id = str(item["id"])
        parent_id = item.get("parentId")
        child_index = item.get("childIndex")
        is_leaf = bool(item.get("leaf", False))
        key_count = int(item.get("keyCount", len(keys)))

        x = _btree_x_position(level=level, index_in_level=index_in_level, total_in_level=level_totals[level])
        y = BASE_Y + (level * VERTICAL_GAP)

        metadata = dict(item.get("metadata") or {})
        metadata.update(
            {
                "structure": "btree",
                "keys": keys,
                "leaf": is_leaf,
                "level": level,
                "parentId": parent_id,
                "parentKeys": item.get("parentKeys"),
                "childIndex": child_index,
                "keyCount": key_count,
                "maxKeys": item.get("maxKeys"),
            }
        )

        category = "root" if parent_id is None else "leaf" if is_leaf else "internal"
        label = item.get("label") or " | ".join(str(key) for key in keys)

        nodes.append(
            create_react_flow_node(
                node_id=node_id,
                label=label,
                x=x,
                y=y,
                node_type="btreeNode",
                category=category,
                metadata=metadata,
            )
        )

        if parent_id is not None:
            edge_label = str(child_index) if child_index is not None else None
            edges.append(
                create_react_flow_edge(
                    edge_id=f"btree-edge-{parent_id}-{node_id}",
                    source=parent_id,
                    target=node_id,
                    edge_type="smoothstep",
                    label=edge_label,
                    animated=False,
                    relationship="parent-child",
                )
            )

    return {"nodes": nodes, "edges": edges}


def _btree_x_position(level: int, index_in_level: int, total_in_level: int) -> int:
    """Return a centered deterministic x position for a B-Tree level."""
    if total_in_level <= 1:
        return BASE_X

    btree_horizontal_gap = HORIZONTAL_GAP + 80
    level_width = (total_in_level - 1) * btree_horizontal_gap
    return BASE_X - (level_width // 2) + (index_in_level * btree_horizontal_gap)


def serialize_hash_table(
    buckets: list[dict[str, Any]],
    metrics: dict[str, Any] | None = None,
    last_operation: dict[str, Any] | None = None,
) -> dict[str, list[dict[str, Any]]]:
    """
    Serialize hash-table buckets and chains into React Flow nodes and edges.

    Expected bucket contract:
    - bucketIndex: numeric bucket position
    - size: number of entries in the bucket
    - hasCollision: True when the bucket stores more than one entry
    - items: ordered entries with key, value, chainPosition and collision

    The visual layout places buckets vertically and chained entries horizontally,
    making separate chaining collisions explicit and easy to defend in class.
    """
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    metrics_payload = dict(metrics or {})
    last_operation_payload = dict(last_operation or {}) if last_operation else None
    highlighted_key = last_operation_payload.get("key") if last_operation_payload else None
    highlighted_bucket = last_operation_payload.get("bucketIndex") if last_operation_payload else None

    for bucket_position, bucket in enumerate(buckets):
        bucket_index = int(bucket.get("bucketIndex", bucket_position))
        items = list(bucket.get("items") or [])
        bucket_size = int(bucket.get("size", len(items)))
        has_collision = bool(bucket.get("hasCollision", bucket_size > 1))
        is_highlighted_bucket = highlighted_bucket == bucket_index
        bucket_node_id = f"hash-bucket-{bucket_index}"

        bucket_metadata = {
            "structure": "hash-table",
            "role": "bucket",
            "bucketIndex": bucket_index,
            "size": bucket_size,
            "hasCollision": has_collision,
            "isHighlighted": is_highlighted_bucket,
            "metrics": metrics_payload,
            "lastOperation": last_operation_payload,
        }

        if has_collision:
            bucket_category = "bucket-collision"
        elif bucket_size == 0:
            bucket_category = "bucket-empty"
        else:
            bucket_category = "bucket"

        nodes.append(
            create_react_flow_node(
                node_id=bucket_node_id,
                label=f"Bucket {bucket_index}",
                x=BASE_X,
                y=BASE_Y + (bucket_position * VERTICAL_GAP),
                node_type="hashBucket",
                category=bucket_category,
                metadata=bucket_metadata,
            )
        )

        previous_node_id = bucket_node_id
        for item_position, item in enumerate(items):
            key = str(item.get("key"))
            chain_position = int(item.get("chainPosition", item_position))
            item_collision = bool(item.get("collision", chain_position > 0))
            is_highlighted_item = highlighted_key == key
            item_node_id = f"hash-entry-{bucket_index}-{chain_position}-{key}"
            student_name = _hash_table_value_label(item.get("value"))
            label = f"{key}\n{student_name}" if student_name else key

            metadata = {
                "structure": "hash-table",
                "role": "entry",
                "bucketIndex": bucket_index,
                "key": key,
                "value": item.get("value"),
                "chainPosition": chain_position,
                "collision": item_collision,
                "bucketHasCollision": has_collision,
                "isHighlighted": is_highlighted_item,
                "lastOperation": last_operation_payload,
            }

            if is_highlighted_item:
                category = "highlighted-collision" if item_collision else "highlighted-entry"
            elif item_collision:
                category = "collision"
            else:
                category = "entry"

            nodes.append(
                create_react_flow_node(
                    node_id=item_node_id,
                    label=label,
                    x=BASE_X + ((chain_position + 1) * HORIZONTAL_GAP),
                    y=BASE_Y + (bucket_position * VERTICAL_GAP),
                    node_type="hashEntry",
                    category=category,
                    metadata=metadata,
                )
            )

            edges.append(
                create_react_flow_edge(
                    edge_id=f"hash-edge-{previous_node_id}-{item_node_id}",
                    source=previous_node_id,
                    target=item_node_id,
                    edge_type="smoothstep",
                    label="head" if previous_node_id == bucket_node_id else "next",
                    animated=item_collision or is_highlighted_item,
                    relationship="chain",
                )
            )
            previous_node_id = item_node_id

    return {"nodes": nodes, "edges": edges}


def _hash_table_value_label(value: Any) -> str:
    """Return a compact label for hash-table entry values."""
    if isinstance(value, dict):
        return str(value.get("full_name") or value.get("name") or value.get("student_id") or "")
    if value is None:
        return ""
    return str(value)
