from app.models.agentModels import AgentRequest, AgentResponse

class AgentService:
    def handleInstruction(self, data: AgentRequest) -> AgentResponse:
        """
        Example service logic — replace with your actual agent handling later.
        """
        response_text = f"Received instruction: '{data.instruction}'"
        return AgentResponse(status="ok", output=response_text)