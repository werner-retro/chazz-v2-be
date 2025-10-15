from __future__ import annotations
import os
import httpx
from fastapi import APIRouter, HTTPException
from app.models.sessionModels import SessionIn, SessionOut, ClientSecret

router = APIRouter(prefix="/api/session", tags=["session"])
REALTIME_SESSIONS_URL = "https://api.openai.com/v1/realtime/sessions"

@router.post("", response_model=SessionOut, summary="Create Realtime ephemeral session token")
def createSession(body: SessionIn) -> SessionOut:
    apiKey = os.getenv("OPENAI_API_KEY")
    if not apiKey:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not set")

    model = os.getenv("REALTIME_MODEL", "gpt-4o-realtime-preview")
    voice = os.getenv("REALTIME_VOICE", "alloy")

    try:
        resp = httpx.post(
            REALTIME_SESSIONS_URL,
            headers={"Authorization": f"Bearer {apiKey}", "Content-Type": "application/json"},
            json={
                "model": model,
                "voice": voice,
                "instructions": (
                    "You are a friendly, concise voice agent. "
                    "Keep replies to 1–2 short sentences; ask one question at a time; "
                    "end politely if the user says goodbye."
                ),
            },
            timeout=10.0,
        )
        resp.raise_for_status()
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="realtime session request failed")
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    data = resp.json()
    raw = data.get("client_secret") or {}
    clientSecret = ClientSecret(
        value=raw.get("value", ""),
        expiresAt=raw.get("expires_at"),
    )
    expiresIn = int(data.get("expires_in", 60))

    return SessionOut(clientSecret=clientSecret, expiresIn=expiresIn)
