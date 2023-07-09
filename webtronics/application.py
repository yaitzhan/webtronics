from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

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


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
