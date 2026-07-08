NODE_REGISTRY = {}

def register_node(node_type: str):
    def decorator(cls):
        NODE_REGISTRY[node_type] = cls
        return cls
    return decorator
