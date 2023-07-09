from typing import Generator

import httpx


class BearerApiKey(httpx.Auth):
    def __init__(self, api_key: str):
        self.api_key = api_key
        if not api_key:
            raise Exception("API Key is mandatory.")

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        request.headers["Authorization"] = f"Bearer {self.api_key}"
        yield request
