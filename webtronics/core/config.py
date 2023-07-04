from typing import List, Union, Optional, Dict, Any

from pydantic import AnyHttpUrl, BaseSettings, validator, PostgresDsn


class Settings(BaseSettings):
    PROJECT_NAME: str = "Webtronics"
    DEBUG: bool = True
    API_ROUTE_STR: str = "api"
    CURRENT_API_VERSION: str = "v1"
    BACKEND_CORS_ORIGINS: Union[str, List[AnyHttpUrl]] = []

    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_USER: str = "webtronics_user"
    DB_PASSWORD: str = "webtronics_password"
    DB_NAME: str = "webtronics"
    DB_SCHEME: str = "postgresql+asyncpg"
    DB_URI: Optional[PostgresDsn] = None

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
            cls,  # noqa
            v: Union[str, List[str]],
    ) -> Union[str, List[str]]:
        if isinstance(v, str) and not v.startswith('['):
            return [i.strip() for i in v.split(',')]
        if isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @validator("DB_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme=values.get("DB_SCHEME"),
            user=values.get("DB_USER"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_HOST"),
            port=values.get("DB_PORT"),
            path=f"/{values.get('DB_NAME') or ''}",
        )


settings = Settings()
