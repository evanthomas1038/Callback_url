import hashlib
import hmac
import os
from typing import Any

from fastapi import FastAPI, Header, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse


VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN", "")
APP_SECRET = os.getenv("META_APP_SECRET", "")

app = FastAPI(title="Meta Graph API Callback", version="1.0.0")


@app.get("/")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/webhook", response_class=PlainTextResponse)
def verify_webhook(
    hub_mode: str | None = Query(default=None, alias="hub.mode"),
    hub_verify_token: str | None = Query(default=None, alias="hub.verify_token"),
    hub_challenge: str | None = Query(default=None, alias="hub.challenge"),
) -> str:
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return hub_challenge or ""

    raise HTTPException(status_code=403, detail="Webhook verification failed")


@app.post("/webhook")
async def receive_webhook(
    request: Request,
    x_hub_signature_256: str | None = Header(default=None),
) -> dict[str, Any]:
    body = await request.body()

    if APP_SECRET:
        verify_signature(body, x_hub_signature_256)

    payload = await request.json()
    print(payload)

    return {"received": True}


@app.get("/oauth/callback")
def oauth_callback(code: str | None = None, error: str | None = None) -> dict[str, str | None]:
    if error:
        return {"status": "error", "error": error}

    return {"status": "ok", "code": code}


def verify_signature(body: bytes, signature_header: str | None) -> None:
    if not signature_header or not signature_header.startswith("sha256="):
        raise HTTPException(status_code=403, detail="Missing Meta signature")

    expected = hmac.new(
        APP_SECRET.encode("utf-8"),
        msg=body,
        digestmod=hashlib.sha256,
    ).hexdigest()
    received = signature_header.removeprefix("sha256=")

    if not hmac.compare_digest(expected, received):
        raise HTTPException(status_code=403, detail="Invalid Meta signature")
