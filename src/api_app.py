from fastapi import FastAPI, Query
from fastapi.encoders import jsonable_encoder
from service.statsbomb_service import StatsBombService
from service.openai_client_service import OpenAIClientService
from dotenv import load_dotenv
from typing import Dict, Any, List
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from model.openai_model import ChatRequest, ChatResponse, ChatSummary
from model.stats_bomb_model import MatchEvents, PlayerProfile
import requests
import logging

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Carregar variáveis de ambiente
load_dotenv()

# Inicialização do app FastAPI
app = FastAPI()

# Tratamento global de exceções
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Request {request.url } got Internal Server Error: {exc}")
    
    # Exceção para HTTP 404 da lib StatsBombPy
    if isinstance(exc, requests.exceptions.HTTPError) and exc.response.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={"message": "Not Found"},
        )
    
    # Erros genéricos
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )


# Rotas principais

@app.get("/match")
def get_match(match_id: int, competition_id: int, season_id: int) -> Dict[str, Any]:
    """ 
        Retorna informações de uma partida específica.
        
        Parâmetros:
        - match_id: int
        - competition_id: int
        - season_id: int    
    """
    return StatsBombService.get_match_dict(match_id, competition_id, season_id)

@app.get("/match_summary") 
def get_match(match_id: int, competition_id: int, season_id: int) -> ChatSummary:
    """ 
        Retorna um resumo de uma partida específica.
        
        Parâmetros:
        - match_id: int
        - competition_id: int
        - season_id: int
    """
    
    match_dict = StatsBombService.get_match_dict(match_id, competition_id, season_id)
    
    # Open AI, por padrão, tem um limite de 200K de tokens no INPUT, não é possível enviar muitos eventos. 
    # A aplicação suporta passar quantos eventos quiser, porém devido a limitação, foi escolhido passar apenas eventos de chutes.
    events_dict = StatsBombService.get_events_dict(
        match_id,
        event_type_list=[
            MatchEvents.SHOT.value, 
        ]
    )
    summary = OpenAIClientService.get_match_summary(match_dict, events_dict)
    return {"summary": summary}

@app.get("/player_profile") 
def get_player_profile(match_id: int, player_name: str) -> Any:
    """
        Retorna o perfil de um jogador específico em uma partida.
        
        Parâmetros:
        - match_id: int
        - player_name: str
    """
    
    player_profile: PlayerProfile = StatsBombService.get_player_profile(match_id, player_name)
    return jsonable_encoder(player_profile)

# Rotas adicionais para testes

@app.post("/chat")
def get_chat_response(request: ChatRequest) -> ChatResponse:
    response = OpenAIClientService.get_chat_response(request.message)
    return {"message": response}

@app.get("/competitions")
def get_competitions() -> List[Dict[str, Any]]:
    return StatsBombService.get_competitions_dict()

@app.get("/matches")
def get_matches(competition_id: int, season_id: int) -> List[Dict[str, Any]]:
    return StatsBombService.get_matches_dict(competition_id, season_id)

@app.get("/events")
def get_events(
        match_id: int,
        event_type_list: List[str] = Query(None),
        player_name: str = None
    ) -> List[Dict[str, Any]]:  
    events = StatsBombService.get_events_dict(match_id, event_type_list, player_name)
    return jsonable_encoder(events, exclude_none=True)

@app.get("/lineups")
def get_lineups(match_id: int, team: str) -> List[Dict[str, Any]]:
    return StatsBombService.get_lineups_dict(match_id, team)