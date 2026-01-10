from fastapi import FastAPI, Request
from settings import settings

from scalar_fastapi import get_scalar_api_reference

from apps.info.router import info_router
from apps.users.router import users_router


def get_application() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        root_path="/api",
    )
    app.include_router(users_router, prefix="/users", tags=["Users"])

    if settings.DEBUG:
        app.include_router(info_router, prefix="/info", tags=["INFO"])

    @app.get("/scalar", include_in_schema=False)
    async def scalar_html(request: Request):
        return get_scalar_api_reference(
            openapi_url=request.scope.get("root_path", "") + app.openapi_url,
            title=app.title,
        )

    return app
