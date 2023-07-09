from pydantic import BaseModel, Field


class ClearbitResponse(BaseModel):
    full_name: str = Field(title="Имя пользователя")
    time_zone: str = Field(title="Часовой пояс")
    country: str = Field(title="Страна")
    city: str = Field(title="Город")
