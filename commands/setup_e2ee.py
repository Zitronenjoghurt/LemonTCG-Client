from src.api.resources.e2ee import initialize_e2ee

async def setup_e2ee():
    password = input("Provide your online password: ")
    await initialize_e2ee(password=password)