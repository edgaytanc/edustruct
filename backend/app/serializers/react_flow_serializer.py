def create_react_flow_node(
    node_id,
    label,
    x=0,
    y=0,
    node_type="default",
    category=None,
    metadata=None
):
    return {
        "id": str(node_id),
        "type": node_type,
        "position": {
            "x": x,
            "y": y
        },
        "data": {
            "label": label,
            "category": category,
            "metadata": metadata or {}
        }
    }


def create_react_flow_edge(
    edge_id,
    source,
    target,
    edge_type="smoothstep",
    label=None,
    animated=False,
    relationship=None
):
    return {
        "id": str(edge_id),
        "source": str(source),
        "target": str(target),
        "type": edge_type,
        "label": label,
        "animated": animated,
        "data": {
            "relationship": relationship
        }
    }
