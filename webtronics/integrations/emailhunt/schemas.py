from typing import Optional
from pydantic import BaseModel


class EmailHuntResponse(BaseModel):
    email_status: Optional[str]
    email_score: Optional[int]
    email_disposable: Optional[bool]
    email_gibberish: Optional[bool]
