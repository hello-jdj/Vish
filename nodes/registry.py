NODE_REGISTRY = {}

def register_node(node_type: str, *, label=None, category="Other", description=""):
    def decorator(cls):
        NODE_REGISTRY[node_type] = {
            "class": cls,
            "label": label or cls.__name__,
            "category": category,
            "description": description,
        }
        return cls
    return decorator

def create_node(node_type):
    entry = NODE_REGISTRY.get(node_type)
    if not entry:
        raise ValueError(f"Unknown node type: {node_type}")
    return entry["class"]()
