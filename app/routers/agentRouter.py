from __future__ import annotations
from typing import Dict
from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.models.agentModels import AgentTurnIn, AgentTurnOut
from app.services.agentService import AgentService

router = APIRouter(prefix="/agent", tags=["agent"])

def getAgent(request: Request) -> AgentService:
    svc = getattr(request.app.state, "agent_service", None)
    if not isinstance(svc, AgentService):
        raise HTTPException(status_code=500, detail="Agent service not initialized")
    return svc

@router.post(
    "/turn",
    response_model=AgentTurnOut,
    summary="Run one agent turn (text-in → text-out)",
)
def agentTurn(body: AgentTurnIn, agent: AgentService = Depends(getAgent)) -> AgentTurnOut:
    try:
        result: Dict = agent.turn(userText=body.userText, conversationCtx=body.context or [])
        return AgentTurnOut(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent turn failed: {type(e).__name__}",
        )
