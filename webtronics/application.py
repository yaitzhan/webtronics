from fastapi import FastAPI

from webtronics.core.config import settings
from webtronics.api.v1.api import router


app = FastAPI(
    debug=settings.DEBUG,
    title=settings.PROJECT_NAME,
    openapi_url="/docs/openapi.json",
    docs_url="/docs/swagger.yml"
)

app.include_router(
    router,
    prefix=f"/{settings.API_ROUTE_STR}/{settings.CURRENT_API_VERSION}",
    tags=[f"API {settings.CURRENT_API_VERSION}"]
)
