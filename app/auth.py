"""Google OAuth (Authlib) with a domain + email allow-list.

Env:
  GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET  OAuth client. If GOOGLE_CLIENT_ID is unset the app runs in DEV MODE:
                                           everyone is auto-logged-in as dev@localhost and a yellow banner says so.
  SESSION_SECRET                           signs the session cookie.
  ALLOWED_DOMAINS                          comma list, default "scaleworks.com". Needs hd claim == domain AND email
                                           domain == domain AND email_verified.
  ALLOWED_EMAILS                           comma list of individual addresses always allowed (email_verified needed).
  BASE_URL                                 public URL, used to build the redirect URI <BASE_URL>/auth/callback.
"""
import os
import secrets
from typing import Any, Dict, List, Optional, Tuple

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

DEV_EMAIL = "dev@localhost"
PUBLIC_PATHS = ("/login", "/login/google", "/auth/callback", "/logout", "/healthz")
PUBLIC_PREFIXES = ("/static/",)


def dev_mode() -> bool:
    return not os.environ.get("GOOGLE_CLIENT_ID")


def _csv(name: str, default: str = "") -> List[str]:
    return [x.strip().lower() for x in os.environ.get(name, default).split(",") if x.strip()]


def allowed_domains() -> List[str]:
    return _csv("ALLOWED_DOMAINS", "scaleworks.com")


def allowed_emails() -> List[str]:
    return _csv("ALLOWED_EMAILS")


def session_secret() -> str:
    s = os.environ.get("SESSION_SECRET")
    if s:
        return s
    # Fine for dev; in production set SESSION_SECRET or sessions reset on every restart.
    return secrets.token_urlsafe(32)


def is_allowed(userinfo: Dict[str, Any]) -> Tuple[bool, str]:
    email = (userinfo.get("email") or "").strip().lower()
    if not email:
        return False, "Google did not return an email address."
    verified = userinfo.get("email_verified")
    if verified not in (True, "true", "True", 1):
        return False, "Your Google email address is not verified."
    if email in allowed_emails():
        return True, "allow-listed email"
    domain = email.rsplit("@", 1)[-1]
    hd = (userinfo.get("hd") or "").strip().lower()
    if domain in allowed_domains() and hd == domain:
        return True, "allowed Google Workspace domain"
    return False, "{} is not allowed. Sign in with a {} Google Workspace account.".format(
        email, " or ".join(allowed_domains()) or "permitted")


def current_user(request: Request) -> Optional[str]:
    if dev_mode():
        return DEV_EMAIL
    user = request.session.get("user")
    return user.get("email") if user else None


def is_public(path: str) -> bool:
    return path in PUBLIC_PATHS or any(path.startswith(p) for p in PUBLIC_PREFIXES)


_oauth = None


def _get_oauth():
    global _oauth
    if _oauth is None:
        from authlib.integrations.starlette_client import OAuth
        _oauth = OAuth()
        _oauth.register(
            name="google",
            client_id=os.environ.get("GOOGLE_CLIENT_ID"),
            client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
            server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
            client_kwargs={"scope": "openid email profile"},
        )
    return _oauth


def _redirect_uri(request: Request) -> str:
    base = os.environ.get("BASE_URL", "").rstrip("/")
    if base:
        return base + "/auth/callback"
    return str(request.url_for("auth_callback"))


def build_router(templates) -> APIRouter:
    router = APIRouter()

    @router.get("/login", response_class=HTMLResponse)
    async def login(request: Request, error: str = ""):
        if dev_mode():
            return RedirectResponse("/", status_code=303)
        return templates.TemplateResponse(request, "login.html", {
            "error": error, "domains": allowed_domains(), "user": None, "dev_mode": False})

    @router.get("/login/google")
    async def login_google(request: Request):
        if dev_mode():
            return RedirectResponse("/", status_code=303)
        return await _get_oauth().google.authorize_redirect(request, _redirect_uri(request),
                                                            prompt="select_account")

    @router.get("/auth/callback", name="auth_callback")
    async def auth_callback(request: Request):
        if dev_mode():
            return RedirectResponse("/", status_code=303)
        try:
            token = await _get_oauth().google.authorize_access_token(request)
        except Exception as exc:  # state mismatch, denied consent, etc.
            return templates.TemplateResponse(request, "login.html", {
                "error": "Sign-in failed: {}".format(exc), "domains": allowed_domains(), "user": None,
                "dev_mode": False}, status_code=400)
        userinfo = dict(token.get("userinfo") or {})
        ok, why = is_allowed(userinfo)
        if not ok:
            request.session.pop("user", None)
            return templates.TemplateResponse(request, "login.html", {
                "error": why, "domains": allowed_domains(), "user": None, "dev_mode": False}, status_code=403)
        request.session["user"] = {"email": userinfo["email"].lower(), "name": userinfo.get("name", "")}
        nxt = request.session.pop("next", "/")
        if not isinstance(nxt, str) or not nxt.startswith("/") or nxt.startswith("//"):
            nxt = "/"
        return RedirectResponse(nxt, status_code=303)

    @router.get("/logout")
    async def logout(request: Request):
        request.session.clear()
        return RedirectResponse("/login" if not dev_mode() else "/", status_code=303)

    return router
