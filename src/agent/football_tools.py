from langchain.tools import tool
from service.statsbomb_service import StatsBombService
from model.stats_bomb_model import MatchEvents, PlayerProfile
from fastapi.encoders import jsonable_encoder
from typing import Dict
import json

@tool
def get_player_info(action_input: str) -> Dict:
    """   
        Get the player profile using match_id and player_name.
        
        Args:
        - action_input(str): The input data containing the match_id.
            format: {"match_id": 777, "player_name": "Some Player Name"}
        
        Returns:
        - dict: The player profile from the specified match or None if the player is not found.
    """
    
    try:
        match_id = json.loads(action_input)["match_id"]
        player_name = json.loads(action_input)["player_name"]
        
        player_profile: PlayerProfile = StatsBombService.get_player_profile(match_id, player_name)
        return player_profile.model_dump()
    except Exception as e:
        if "404" in str(e):
            return None
        raise e
    
@tool
def get_match_events(action_input: str) -> Dict:
    """   
        Get the match events using match_id, competition_id and season_id.
        
        Args:
        - action_input(str): The input data containing the match_id.
            format: {"match_id": int}
        
        Returns:
        - dict: The match events from the specified match.
    """
    
    # The application supports passing as many events as you want,
    #   but it was chosen to pass only shot events due to the large number of tokens
    events_dict = StatsBombService.get_events_dict(
        match_id = json.loads(action_input)["match_id"],
        event_type_list=[
            MatchEvents.SHOT.value, 
        ]
    )
    return jsonable_encoder(events_dict, exclude_none=True)
