from __future__ import annotations
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class AgentTurnIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    conversationId: str = Field(..., description="Conversation/session id")
    userText: str = Field(..., description="Final transcript for this turn")
    storeId: str = Field(..., description="Active store id for scoping tools")
    userId: Optional[str] = None
    nowISO: Optional[str] = None
    context: Optional[List[Dict[str, Any]]] = Field(
        None, description="Optional prior messages [{'role':'user'|'assistant','content':'...'}]"
    )

class AgentTurnOut(BaseModel):
    model_config = ConfigDict(extra="forbid")
    replyText: str = Field(..., description="Assistant's textual reply for this turn")
