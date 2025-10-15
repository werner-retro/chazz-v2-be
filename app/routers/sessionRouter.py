# app/routers/sessionRouter.py
from __future__ import annotations
import os, httpx
from fastapi import APIRouter, HTTPException
from app.models.sessionModels import SessionIn, SessionOut, ClientSecret

router = APIRouter(prefix="/api/session", tags=["session"])  # ensure /api prefix

CLIENT_SECRETS_URL = "https://api.openai.com/v1/realtime/client_secrets"

@router.post("", response_model=SessionOut)
def createSession(body: SessionIn) -> SessionOut:
    apiKey = os.getenv("OPENAI_API_KEY")
    if not apiKey:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not set")

    # Must be a realtime-capable model; “gpt-realtime” or “gpt-4o-realtime-preview”
    model = os.getenv("REALTIME_MODEL", "gpt-realtime")

    try:
        resp = httpx.post(
            CLIENT_SECRETS_URL,
            headers={
                "Authorization": f"Bearer {apiKey}",
                "Content-Type": "application/json",
            },
            json={
                "session": {
                    "type": "realtime",
                    "model": model,
                }
            },
            timeout=10.0,
        )
        resp.raise_for_status()
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="client_secrets request failed")

    data = resp.json()
    # API returns { value: "ek_...", expires_at: <epoch>, ... }
    ek_value = data.get("value", "")
    expires_at = data.get("expires_at")
    expires_in = data.get("expires_in", 60)

    return SessionOut(
        clientSecret=ClientSecret(value=ek_value, expiresAt=expires_at),
        expiresIn=int(expires_in),
    )
