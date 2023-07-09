from typing import Optional

from pydantic import BaseModel, Field


class ClearbitResponse(BaseModel):
    full_name: Optional[str] = Field(title="Имя пользователя")
    time_zone: Optional[str] = Field(title="Часовой пояс")
    country: Optional[str] = Field(title="Страна")
    city: Optional[str] = Field(title="Город")
