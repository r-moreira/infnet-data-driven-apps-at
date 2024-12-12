from pydantic import BaseModel
from typing import List, Dict, Any

class ChatRequest(BaseModel):
    message: str
    
class ChatResponse(BaseModel):
    message: str
    
class ChatSummary(BaseModel):
    summary: str
        
class ChatNarration(BaseModel):
    narration: str