from httpx import Client

api_client: Client = Client()


async def get_api_client() -> Client:
    async with api_client:
        return api_client
