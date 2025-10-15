from __future__ import annotations
from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict

class HealthOut(BaseModel):
    model_config = ConfigDict(extra="forbid")  # required by Pydantic
    status: Literal["ok"]

class ErrorOut(BaseModel):
    model_config = ConfigDict(extra="forbid")
    error: str = Field(..., description="Short machine-friendly error code")
    detail: Optional[str] = None
