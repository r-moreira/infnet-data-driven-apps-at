from statsbombpy import sb
from typing import List, Any, Dict
import numpy as np
from fastapi.exceptions import HTTPException
import logging

class StatsBombService:
    logger = logging.getLogger(__name__)
    
    @staticmethod
    def get_match_dict(match_id: int, competition_id: int, season_id: int) -> Dict[str, Any]:
        StatsBombService.logger.info(f"Getting match for match_id {match_id}, competition_id {competition_id}, season_id {season_id}")
        
        match = StatsBombService.get_matches_dict(competition_id, season_id)
        for m in match:
            if m['match_id'] == match_id:
                return m
        raise HTTPException(status_code=404, detail="Match not found")

    @staticmethod
    def get_competitions_dict() -> List[Dict[str, Any]]:
        StatsBombService.logger.info("Getting competitions.")
        
        return sb.competitions().to_dict(orient='records')
        
    @staticmethod
    def get_matches_dict(competition_id: int, season_id: int) -> List[Dict[str, Any]]:
        StatsBombService.logger.info(f"Getting matches for competition_id {competition_id}, season_id {season_id}")
        
        return sb.matches(competition_id=competition_id, season_id=season_id).to_dict(orient='records')
        
    @staticmethod
    def get_events_dict(match_id: int, event_type_list: List[str] = None) -> List[Dict[str, Any]]:    
        StatsBombService.logger.info(f"Getting events for match_id {match_id}, event_type_list {event_type_list}")
        
        print(f"Getting events for match_id {match_id}, event_type_list {event_type_list}")
        
        events = sb.events(match_id=match_id).to_dict(orient='records')
        
        # Tratamento de valores NaN e Inf
        for event in events:
            for key, value in event.items():
                if isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
                    event[key] = None
        
        # Filtrar eventos específicos se necessário
        if event_type_list:          
            events = list(filter(lambda event: event['type'] in event_type_list, events))
            
        if not events:
            raise HTTPException(status_code=404, detail="Events not found")
                    
        return events

    @staticmethod
    def get_lineups_dict(match_id: int, team: str) -> List[Dict[str, Any]]:
        StatsBombService.logger.info(f"Getting lineups for match_id {match_id}, team {team}")
            
        return sb.lineups(match_id=match_id)[team].to_dict(orient='records')