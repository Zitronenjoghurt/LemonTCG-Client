from lemon_tcg.entities.base_save_state_entity import BaseSaveStateEntity
from src.utils.file_operations import construct_path

class Config(BaseSaveStateEntity):
    FILE_PATH = construct_path("src/config.json")
    api_key: str = ""