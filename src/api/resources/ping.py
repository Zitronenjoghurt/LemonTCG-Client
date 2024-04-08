from src.api.api_controller import ApiController
from src.api.models.base_responses import MessageResponse

API = ApiController.get_instance()

async def ping() -> bool:
    response = await API.get(endpoint_path=["ping"], expected_codes=[200], response_model=MessageResponse)
    if isinstance(response, MessageResponse):
        return response.message == "Pong"
    return False