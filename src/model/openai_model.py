from pydantic import BaseModel
from typing import List, Dict

class ChatRequest(BaseModel):
    message: str
    
class ChatResponse(BaseModel):
    message: str
    
class ChatSummary(BaseModel):
    summary: str