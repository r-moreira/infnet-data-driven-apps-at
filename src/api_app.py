from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from service import statsbomb_service
from dotenv import load_dotenv
from typing import Dict, Any, List
from fastapi.responses import JSONResponse
from fastapi.requests import Request
import requests

load_dotenv()
app = FastAPI()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Request {request.url } got Internal Server Error: {exc}")
    
    # Tratamento global da exceção para HTTP 404 da lib StatsBombPy
    if isinstance(exc, requests.exceptions.HTTPError) and exc.response.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={"message": "Not Found"},
        )
    
    # Tratamento global para erros genéricos
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )

@app.get("/competitions")
def get_competitions() -> List[Dict[str, Any]]:
    return statsbomb_service.get_competitions_dict()

@app.get("/match")
def get_match(match_id: int, competition_id: int, season_id: int) -> Dict[str, Any]:
    return statsbomb_service.get_match_dict(match_id, competition_id, season_id)

@app.get("/matches")
def get_matches(competition_id: int, season_id: int) -> List[Dict[str, Any]]:
    return statsbomb_service.get_matches_dict(competition_id, season_id)

@app.get("/events")
def get_events(match_id: int) -> List[Dict[str, Any]]:   
    events = statsbomb_service.get_events_dict(match_id)
    return jsonable_encoder(events, exclude_none=True)

@app.get("/lineups")
def get_lineups(match_id: int, team: str) -> List[Dict[str, Any]]:
    return statsbomb_service.get_lineups_dict(match_id, team)
