from typing import Optional
from urllib.parse import urljoin

import httpx

from webtronics.integrations.base import QueryApiKey
from webtronics.core.config import settings
from webtronics.integrations.emailhunt.schemas import EmailHuntResponse


class EmailHuntClient:
    auth = QueryApiKey(api_key=settings.EMAIL_HUNT_API_KEY)
    base_url = settings.EMAIL_HUNT_HOST_URL

    timeout = 60

    async def verify_user_email(self, email: str) -> Optional[EmailHuntResponse]:
        params = {"email": email}
        url = urljoin(self.base_url, "/v2/email-verifier")

        async with httpx.AsyncClient(
                auth=self.auth,
                timeout=self.timeout
        ) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()

        response_data = response.json()
        data = response_data.get("data")
        if data and data.get("status") == "valid":
            data_in = {
                "email_status": data.get("status"),
                "email_score": int(data.get("score")),
                "email_disposable": data.get("disposable"),
                "email_gibberish": data.get("gibberish")
            }
            return EmailHuntResponse(**data_in)
