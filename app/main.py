"""Ledgerline Order-to-Cash operator: FastAPI app factory.

Run locally:  uvicorn app.main:app --reload
"""
import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app import auth, store
from app.web import chat as chat_web
from app.web import maya as maya_web
from app.web import rig as rig_web
from app.web.views import STATIC_DIR, _render, _user, build_router, templates


def create_app() -> FastAPI:
    app = FastAPI(title="Ledgerline AR Operator", docs_url=None, redoc_url=None, openapi_url=None)
    store.init_db()

    @app.middleware("http")
    async def require_login(request: Request, call_next):
        path = request.url.path
        if auth.is_public(path) or auth.current_user(request) or (
                path.startswith("/api/maya/") and maya_web.courier_ok(request)):
            return await call_next(request)
        if request.headers.get("HX-Request"):
            return PlainTextResponse("login required", status_code=401, headers={"HX-Redirect": "/login"})
        if request.method == "GET":
            nxt = path + (("?" + request.url.query) if request.url.query else "")
            request.session["next"] = nxt
            return RedirectResponse("/login", status_code=303)
        return JSONResponse({"detail": "login required"}, status_code=401)

    # Added after the auth middleware so it wraps it (outermost) and request.session is available inside.
    app.add_middleware(
        SessionMiddleware,
        secret_key=auth.session_secret(),
        session_cookie="ledgerline_session",
        same_site="lax",
        https_only=os.environ.get("BASE_URL", "").startswith("https://"),
        max_age=60 * 60 * 12,
    )

    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    app.include_router(auth.build_router(templates))
    app.include_router(rig_web.build_router())
    app.include_router(maya_web.build_router(_render, _user))
    app.include_router(chat_web.build_router())
    app.include_router(build_router())

    @app.get("/healthz", response_class=PlainTextResponse)
    async def healthz():
        return "ok"

    return app


app = create_app()
