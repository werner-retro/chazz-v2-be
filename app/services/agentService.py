from __future__ import annotations
import os
from typing import List, Dict, Any, Optional
from openai import OpenAI

class AgentService:
    """
    Minimal agent service for Mark 1.
    Reads OPENAI_API_KEY (and optional REALTIME_MODEL) directly from env.
    """

    def __init__(self, model: str | None = None):
        apiKey = os.getenv("OPENAI_API_KEY")
        if not apiKey:
            raise RuntimeError("OPENAI_API_KEY is not set")

        self.model = model or os.getenv("REALTIME_MODEL", "gpt-4o-mini")
        self.client = OpenAI(api_key=apiKey)
        self.instruction = (
            "You are a friendly, concise voice agent. "
            "Keep replies to 1–2 short sentences. Ask one question at a time. "
            "If you didn't catch something, ask briefly for a repeat. "
            "End politely if the user says goodbye."
        )

    def turn(self, userText: str, conversationCtx: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        messages: List[Dict[str, str]] = [{"role": "system", "content": self.instruction}]
        if conversationCtx:
            messages.extend(conversationCtx)
        messages.append({"role": "user", "content": userText})

        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.4,
            max_tokens=120,
        )
        replyText = resp.choices[0].message.content or ""
        return {"replyText": replyText}
