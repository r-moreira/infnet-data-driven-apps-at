import openai
from openai import OpenAI, OpenAIError
from typing import List, Dict
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