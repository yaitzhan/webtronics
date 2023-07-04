import uvicorn

from webtronics.core.config import settings


def run_dev_server() -> None:
    uvicorn.run(
        "webtronics.application:app",
        host="127.0.0.1",
        port=8080,
        reload=settings.DEBUG
    )


if __name__ == "__main__":
    run_dev_server()
