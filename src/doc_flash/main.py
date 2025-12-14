from fastapi import FastAPI

from doc_flash.api import routes
from doc_flash.api.dependencies import get_provider, get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Document code and generate behaviour markdown using pluggable LLM providers.",
    )

    app.include_router(routes.router)

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok", "provider": settings.llm_provider}

    @app.on_event("startup")
    async def warm_provider() -> None:
        # Fail fast if provider configuration is invalid.
        get_provider(settings)

    return app


app = create_app()
