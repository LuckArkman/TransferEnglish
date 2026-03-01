from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.core.config import settings

class ChatService:
    def __init__(self, model: str = "gemini-2.5-flash"):
        self.llm = ChatGoogleGenerativeAI(
            model=model, 
            temperature=0.7,
            google_api_key=settings.GOOGLE_API_KEY
        )
        self.system_prompt = (
            "You are a specialized English tutor for Portuguese speakers. "
            "Your goal is to achieve functional fluency in 6 months using Linguistic Transfer. "
            "Focus on using cognates (words similar in PT and EN) to build student confidence. "
            "Always respond in English, but use simple structures at first. "
            "If the student makes a phonetic error or uses a false cognate, gently guide them. "
            "Keep responses short and conversational, suitable for audio interaction."
        )

    async def get_response(self, history: List[Dict[str, str]], user_input: str, system_modifier: str = "") -> str:
        full_prompt = self.system_prompt
        if system_modifier:
            full_prompt += f"\n\nAdditional Instruction: {system_modifier}"
            
        messages = [SystemMessage(content=full_prompt)]
        
        # Add history
        for msg in history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
        
        # Add current user input
        messages.append(HumanMessage(content=user_input))
        
        response = await self.llm.ainvoke(messages)
        return response.content

chat_service = ChatService()
