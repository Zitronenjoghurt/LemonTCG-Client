import aiohttp
from pydantic import BaseModel
from typing import Optional, Type, TypeVar, Union, Any
from src.entities.config import Config
from src.api.models.base_response import MessageResponse

T = TypeVar('T', bound=BaseModel)

class ApiController():
    _instance = None
    BASE_URL = "https://tcg.lemon.industries"

    def __init__(self) -> None:
        if ApiController._instance is not None:
            raise RuntimeError("Tried to initialize multiple instances of ApiController.")

    @staticmethod
    def get_instance() -> 'ApiController':
        if ApiController._instance is None:
            ApiController._instance = ApiController()
        return ApiController._instance
    
    def generate_url(self, endpoint_path: list[str], **kwargs) -> str:
        endpoint = "/".join(endpoint_path)
        arguments = "&".join([f"{key}={value}" for key, value in kwargs.items()])
        if len(kwargs) > 0:
            return f"{self.BASE_URL}/{endpoint}?{arguments}"
        return f"{self.BASE_URL}/{endpoint}"
    
    def build_headers(self) -> dict:
        config = Config.load_state()
        if len(config.api_key) == 0:
            raise MissingApiKeyError()
        
        headers = {
            'X-API-Key': config.api_key
        }

        return headers

    async def handle_response(self, url: str, response: aiohttp.ClientResponse, expected_codes: list[int], response_model: Optional[Type[T]] = None)-> Union[T, list[Any], dict[str, Any]]:
        if response.status not in expected_codes:
            data = await response.text()
            raise UnexpectedResponseCodeError(url, response.status, data)
        else:
            data = await response.json()
            if response_model and isinstance(data, dict):
                return response_model.model_validate(data)
            else:
                return data

    async def get(self, endpoint_path: list[str], expected_codes: list[int], response_model: Optional[Type[T]] = None, **params) -> Union[T, list[Any], dict[str, Any]]:
        url = self.generate_url(endpoint_path, **params)

        async with aiohttp.ClientSession(headers=self.build_headers()) as session:
            async with session.get(url) as response:
                return await self.handle_response(url=url, response=response, expected_codes=expected_codes, response_model=response_model)
                
class MissingApiKeyError(Exception):
    def __init__(self):
        super().__init__("There is no specified API Key.")
                
class UnexpectedResponseCodeError(Exception):
    """Exception raised for unexpected response codes."""
    def __init__(self, url: str, status_code: int, response_body: str = "") -> None:
        self.url = url
        self.status_code = status_code
        self.response_body = response_body
        message = f"Unexpected response code {status_code} for URL: {url}."
        if response_body:
            message += f" Response body: {response_body}"
        super().__init__(message)