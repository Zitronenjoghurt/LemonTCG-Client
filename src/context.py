from typing import Any
from src.entities.config import Config

class Context():
    _instance = None

    def __init__(self) -> None:
        if Context._instance is not None:
            raise RuntimeError("Tried to initialize multiple instances of Context.")
        self.config = Config.load_state()
        self.public_key: Any = None
        self.private_key: Any = None
        self.cached_public_keys: dict[str, Any] = {}
        
    @staticmethod
    def get_instance() -> 'Context':
        if Context._instance is None:
            Context._instance = Context()
        return Context._instance
    
    @property
    def api_key(self) -> str:
        return self.config.api_key
    
    def update_public_key(self, key) -> None:
        if not self.public_key:
            self.public_key = key

    def update_private_key(self, key) -> None:
        if not self.private_key:
            self.private_key = key

    def clear_keys(self) -> None:
        self.public_key = None
        self.private_key = None