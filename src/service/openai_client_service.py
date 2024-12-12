import openai
from openai import OpenAI, OpenAIError
from typing import List, Dict, Any
import logging
import os

class OpenAIClientError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

class OpenAIClientService:
    logger = logging.getLogger(__name__)
    
    @staticmethod
    def get_chat_response(user_message: str) -> str:
        OpenAIClientService.logger.info("Getting chat response.")
        
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            raise OpenAIClientError("OPEN AI API Key is required.")
        
        openai.api_key = api_key
        client: OpenAI = openai
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant."
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            )
            return response.choices[0].message.content
        except OpenAIError as e:
            OpenAIClientService.logger.error(f"Failed to get chat response: {e}")
            raise OpenAIClientError(f"Failed to get chat response: {e}")
        
        
    @staticmethod
    def get_match_summary(match_dict: List[Dict[str, Any]], events_dict: List[Dict[str, Any]]) -> str:
        OpenAIClientService.logger.info("Getting match summary.")
        
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            raise OpenAIClientError("OPEN AI API Key is required.")
        
        openai.api_key = api_key
        client: OpenAI = openai
        
        system_prompt = f"""
            You are a sports journalist writing a match summary for a sports website.
            
            Utilize the information below to write a summary of the match between the home team and the away team.
            
            Your summary should be concise and informative, listing the key events of the match, along match statistics and the final score.
            
            Match General Information: {match_dict}
            
            Match Events Information: {events_dict}
            
            ### Example Summary: 
                In an exhilarating match, the home team triumphed over the away team with a 2-1 victory.
                The home team took an early lead in the first half, thanks to a goal from their striker Pelé.
                The away team fought back and equalized in the second half with a goal from their midfielder David Luiz.
                However, the home team clinched the win with a decisive late goal from their winger Robinho.
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    }
                ]
            )
            return response.choices[0].message.content
        except OpenAIError as e:
            OpenAIClientService.logger.error(f"Failed to get chat response: {e}")
            raise OpenAIClientError(f"Failed to get chat response: {e}")