from src.api.api_controller import ApiController
from src.api.models.base_responses import ErrorResponse
from src.api.models.e2ee_models import E2EEPublicKey, E2EEEncryptedPrivateKey
from src.context import Context
from src.utils.e2ee import generate_e2ee, decrypt_private_key, load_public_key, check_keys, PasswordError

API = ApiController.get_instance()
CONTEXT = Context.get_instance()

async def initialize_e2ee(password: str) -> None:
    if await check_e2ee_status():
        await fetch_private_key(password)
    else:
        await setup_e2ee(password)

    if not check_keys(CONTEXT.public_key, CONTEXT.private_key):
        CONTEXT.clear_keys()
        raise PasswordError()

async def setup_e2ee(password: str) -> None:
    info = generate_e2ee(password)
    header = {
        "X-Public-Key": info.public_key,
        "X-Encrypted-Private-Key": info.encrypted_private_key,
        "X-Salt-Hex": info.salt_hex
    }
    response = await API.post(endpoint_path=["e2ee"], header_data=header, expected_codes=[200, 400], response_models={200: E2EEPublicKey, 400: ErrorResponse})
    handle_response(response, 'setup E2EE')
    await initialize_e2ee(password)

async def check_e2ee_status() -> bool:
    response = await API.get(endpoint_path=["e2ee", "public"], expected_codes=[200, 400], response_models={200: E2EEPublicKey, 400: ErrorResponse})
    if isinstance(response, E2EEPublicKey):
        CONTEXT.update_public_key(key=load_public_key(response.key))
        return True
    return False

async def fetch_private_key(password: str) -> None:
    response = await API.get(endpoint_path=["e2ee", "private"], expected_codes=[200, 400], response_models={200: E2EEEncryptedPrivateKey, 400: ErrorResponse})
    handle_response(response, 'fetch your E2EE private key')
    if isinstance(response, E2EEEncryptedPrivateKey):
        CONTEXT.update_private_key(key=decrypt_private_key(response.key, response.salt_hex, password))

def handle_response(response, context: str):
    if isinstance(response, ErrorResponse):
        raise RuntimeError(f"An error occurred while trying to {context}: {response.detail}")