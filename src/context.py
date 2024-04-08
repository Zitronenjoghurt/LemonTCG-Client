from typing import Any
from src.entities.config import Config

class Context():
    _instance = None

    def __init__(self) -> None:
        if Context._instance is not None:
            raise RuntimeError("Tried to initialize multiple instances of Context.")
        self.config = Config.load_state()
        self.private_key: Any = None
        self.public_keys: dict[str, Any] = {}
        
    @staticmethod
    def get_instance() -> 'Context':
        if Context._instance is None:
            Context._instance = Context()
        return Context._instance
    
    @property
    def api_key(self) -> str:
        return self.config.api_key