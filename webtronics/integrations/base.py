from typing import Generator

import httpx


class BearerApiKey(httpx.Auth):
    def __init__(self, api_key: str):
        self.api_key = api_key
        if api_key is None:
            raise Exception("API Key is mandatory.")

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        request.headers["Authorization"] = f"Bearer {self.api_key}"
        yield request


class QueryApiKey(httpx.Auth):
    def __init__(self, api_key: str, query_parameter_name: str = None):
        self.api_key = api_key
        if api_key is None:
            raise Exception("API Key is mandatory.")
        self.query_parameter_name = query_parameter_name or "api_key"

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        request.url = request.url.copy_merge_params(
            {self.query_parameter_name: self.api_key}
        )
        yield request
