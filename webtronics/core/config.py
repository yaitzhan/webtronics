from typing import List, Union, Optional, Dict, Any

from pydantic import AnyHttpUrl, BaseSettings, validator, PostgresDsn, RedisDsn, EmailStr


class Settings(BaseSettings):
    PROJECT_NAME: str = "Webtronics"
    DEBUG: bool = True
    SECRET_KEY: str = "BMBSj8^LUa5W+X*gb99!5R2!pX4E#h@ja6hzmXA$kA=%!DV8$S--BEKmzLHT"
    API_ROUTE_STR: str = "api"
    CURRENT_API_VERSION: str = "v1"
    BACKEND_CORS_ORIGINS: Union[str, List[AnyHttpUrl]] = []

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_USER: str = "webtronics_user"
    POSTGRES_PASSWORD: str = "webtronics_password"
    POSTGRES_DB: str = "webtronics"
    POSTGRES_SCHEME: str = "postgresql+asyncpg"
    DB_URI: Optional[PostgresDsn] = None

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    CLEARBIT_API_KEY: str = ""

    EMAIL_HUNT_API_KEY: str = ""

    REDIS_URL: RedisDsn = "redis://localhost:6379/0"

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
            cls,  # noqa
            v: Union[str, List[str]],
    ) -> Union[str, List[str]]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        if isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @validator("DB_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme=values.get("POSTGRES_SCHEME"),
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    FIRST_SUPERUSER: EmailStr = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
