from fastapi import FastAPI
from app.routers.agentRouter import router as agentRouter

app = FastAPI(
    title="Agent API",
    description="Base FastAPI app with a single router/service/model setup.",
    version="0.1.0",
)

app.include_router(agentRouter, prefix="/agent", tags=["Agent"])