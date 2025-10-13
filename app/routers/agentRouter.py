from fastapi import APIRouter, Depends
from app.models.agentModels import AgentRequest, AgentResponse
from app.services.agentService import AgentService

router = APIRouter()

def getAgentService() -> AgentService:
    return AgentService()

@router.post(
    "/process",
    response_model=AgentResponse,
    summary="Process agent instruction",
    description="Takes an instruction and returns a response from the agent service."
)
def processAgentRequest(
    body: AgentRequest,
    service: AgentService = Depends(getAgentService)
):
    return service.handleInstruction(body)
