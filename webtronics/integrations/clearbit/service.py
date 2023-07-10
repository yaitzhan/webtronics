from typing import Optional
from urllib.parse import urljoin

import httpx

from webtronics.integrations.base import BearerApiKey
from webtronics.core.config import settings
from webtronics.integrations.clearbit.schemas import ClearbitResponse


class ClearbitClient:
    auth = BearerApiKey(api_key=settings.CLEARBIT_API_KEY)
    base_url = "https://person.clearbit.com/"

    timeout = 60

    async def get_person_user_data(self, email: str) -> Optional[ClearbitResponse]:
        params = {"email": email}
        url = urljoin(self.base_url, "/v2/people/find")

        async with httpx.AsyncClient(
                auth=self.auth,
                timeout=self.timeout
        ) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()

        response_data = response.json()
        if response_data.get("error") is None:
            data_in = {
                "full_name": response_data.get("name", {}).get("fullName"),
                "time_zone": response_data.get("timeZone"),
                "city": response_data.get("geo", {}).get("city"),
                "country": response_data.get("geo", {}).get("country"),
            }
            return ClearbitResponse(**data_in)
