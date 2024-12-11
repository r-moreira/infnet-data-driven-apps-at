from statsbombpy import sb
from typing import List, Any, Dict
import json
import numpy as np
from fastapi.exceptions import HTTPException

def get_match_dict(match_id: int, competition_id: int, season_id: int) -> Dict[str, Any]:
    match = get_matches_dict(competition_id, season_id)
    for m in match:
        if m['match_id'] == match_id:
            return m
    raise HTTPException(status_code=404, detail="Match not found")

def get_competitions_json_string() -> str:
    return json.dumps(
        sb.competitions().to_dict(orient='records')
    )
    
def get_competitions_dict() -> List[Dict[str, Any]]:
    return sb.competitions().to_dict(orient='records')
    
def get_matches_json_string(competition_id: int, season_id: int) -> str:
    return json.dumps(
        sb.matches(competition_id=competition_id, season_id=season_id).to_dict(orient='records')
    )
    
def get_matches_dict(competition_id: int, season_id: int) -> List[Dict[str, Any]]:
    return sb.matches(competition_id=competition_id, season_id=season_id).to_dict(orient='records')

def get_events_json_string(match_id: int) -> str:
    return json.dumps(
        sb.events(match_id=match_id).to_dict(orient='records')
    )
    
def get_events_dict(match_id: int) -> List[Dict[str, Any]]:    
    events = sb.events(match_id=match_id).to_dict(orient='records')
    for event in events:
        for key, value in event.items():
            if isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
                event[key] = None
    return events

def get_lineups_json_string(match_id: int, team: str) -> str:
    return json.dumps(
        sb.lineups(match_id=match_id)[team].to_dict(orient='records')
    )
    
def get_lineups_dict(match_id: int, team: str) -> List[Dict[str, Any]]:
    return sb.lineups(match_id=match_id)[team].to_dict(orient='records')