from httpx import Client

api_client: Client = Client()


def get_api_client() -> Client:
    with api_client:
        return api_client
