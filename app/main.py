from __future__ import annotations
from fastapi import FastAPI

from app.services.agentService import AgentService
from app.routers.agentRouter import router as agentRouter
from app.routers.sessionRouter import router as sessionRouter

app = FastAPI(title="Pizza Voice Agent (Mark 1)")
app.state.agent_service = AgentService()  # reads env internally
app.include_router(agentRouter)
app.include_router(sessionRouter)