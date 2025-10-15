from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class ClientSecret(BaseModel):
    model_config = ConfigDict(extra="forbid")
    value: str = Field(..., description="Ephemeral token value")
    expiresAt: Optional[int] = Field(None, description="Unix epoch seconds when the token expires")

class SessionIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    clientId: str = Field(..., description="Opaque ID from FE for correlation/logging")

class SessionOut(BaseModel):
    model_config = ConfigDict(extra="forbid")
    clientSecret: ClientSecret
    expiresIn: int = Field(..., description="Seconds until token expiry")
