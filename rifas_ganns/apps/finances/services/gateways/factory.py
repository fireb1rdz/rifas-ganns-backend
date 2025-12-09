from typing import Type, Dict, Any, Callable 

CLASS_REGISTRY: Dict[str, Type] = {}

def auto_register(name: str = None) -> Callable:
    """
    Decorator to automatically register a class in CLASS_REGISTRY.
    If no name is provided, the class name is used.
    """
    def decorator(cls: Type) -> Type:
        key = name or cls.__name__
        if key in CLASS_REGISTRY:
            raise ValueError(f"Duplicate registration for key '{key}'")
        CLASS_REGISTRY[key] = cls
        return cls
    return decorator

class GatewayFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_instance(name):
        cls = CLASS_REGISTRY[name]
        if not cls:
            raise ValueError(f"Class not found: {cls}")
        return cls