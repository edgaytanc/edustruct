def create_metrics(
    count=0,
    height=None,
    balance_factor=None,
    collisions=None,
    levels=None,
    edges_count=0
):
    return {
        "count": count,
        "height": height,
        "balanceFactor": balance_factor,
        "collisions": collisions,
        "levels": levels,
        "edgesCount": edges_count
    }
