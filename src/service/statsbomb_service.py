from statsbombpy import sb
from typing import List, Any, Dict
import numpy as np
from fastapi.exceptions import HTTPException
from model.stats_bomb_model import PlayerProfile, MatchStats, PlayerInfo, Position
import logging

class StatsBombService:
    logger = logging.getLogger(__name__)
    
    @staticmethod
    def get_match_dict(match_id: int, competition_id: int, season_id: int) -> Dict[str, Any]:
        """
            Obtém informações de uma partida específica.
        """
        StatsBombService.logger.info(f"Getting match for match_id {match_id}, competition_id {competition_id}, season_id {season_id}")
        
        match = StatsBombService.get_matches_dict(competition_id, season_id)
        for m in match:
            if m['match_id'] == match_id:
                return m
        raise HTTPException(status_code=404, detail="Match not found")

    @staticmethod
    def get_competitions_dict() -> List[Dict[str, Any]]:
        """
            Obtém informações de competições.
        """
        StatsBombService.logger.info("Getting competitions.")
        
        return sb.competitions().to_dict(orient='records')
        
    @staticmethod
    def get_matches_dict(competition_id: int, season_id: int) -> List[Dict[str, Any]]:
        """
            Obtém informações de partidas.
        """
        StatsBombService.logger.info(f"Getting matches for competition_id {competition_id}, season_id {season_id}")
        
        return sb.matches(competition_id=competition_id, season_id=season_id).to_dict(orient='records')
        
    @staticmethod
    def get_events_dict(
            match_id: int,
            event_type_list: List[str] = None,
            player_name: str = None
        ) -> List[Dict[str, Any]]:    
        """
            Obtém eventos de uma partida específica.
        """
        
        StatsBombService.logger.info(f"Getting events for match_id {match_id}, event_type_list {event_type_list}, player_name {player_name}")
                
        events = sb.events(match_id=match_id).to_dict(orient='records')
        
        # Tratamento de valores NaN e Inf
        for event in events:
            for key, value in event.items():
                if isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
                    event[key] = None
        
        # Filtra eventos específicos se necessário
        if event_type_list:          
            events = list(filter(lambda event: event['type'] in event_type_list, events))
            
        # Filtra eventos de jogadores específicos se necessário
        if player_name:
            events = list(filter(lambda event: event['player'] == player_name, events))
      
        if not events:
            raise HTTPException(status_code=404, detail="Events not found")
                    
        return events

    @staticmethod
    def get_lineups_dict(match_id: int, team: str) -> List[Dict[str, Any]]:
        """
            Obtém escalações de uma partida específica.
        """
        StatsBombService.logger.info(f"Getting lineups for match_id {match_id}, team {team}")
            
        return sb.lineups(match_id=match_id)[team].to_dict(orient='records')
    
    @staticmethod
    def get_player_profile(match_id, player_name: str) -> PlayerProfile:
        """
            Obtém o perfil de um jogador em uma partida específica.
        """
        
        StatsBombService.logger.info(f"Getting player profile for player_name {player_name}")
        
        # Pega eventos do jogar em uma partida
        player_events_dict: List[Dict[str, Any]] = StatsBombService.get_events_dict(match_id, player_name=player_name)
        
        # Descobre o time do jogador
        player_team = None
        
        for event in player_events_dict:
            if event['player'] == player_name:
                if event['team'] is not None:
                    player_team = event['team']
                    break
            
        if player_team is None:
            raise HTTPException(status_code=404, detail="Player team not found")
        
        
        # Pega informações do jogador
        player_info_dict: List[Dict[str, Any]] = StatsBombService.get_lineups_dict(match_id, player_team)
        
        player_info: PlayerInfo = None
        
        for player in player_info_dict:
            if player['player_name'] == player_name:
                player_info = player
                break
            
        if player_info is None:
            raise HTTPException(status_code=404, detail="Player info not found")
        
        player_info = PlayerInfo(**player_info)
        
        # Pega estatísticas do jogador na partida
        match_stats: MatchStats = {
            "total_passes": 0,
            "total_ball_receipts": 0,
            "total_carries": 0,
            "total_pressures": 0,
            "total_fouls_committed": 0,
            "total_fouls_won": 0,
            "total_dispossessed": 0,
            "total_duels": 0,
            "total_dribbled_past": 0,
            "total_dribbles": 0,
            "total_blocks": 0,
            "total_interceptions": 0,
            "total_ball_recoveries": 0,
            "total_miscontrols": 0,
            "total_shields": 0,
            "total_shots": 0,
            "total_goal_keeper": 0,
            "total_bad_behaviour": 0,
        }
        
        for event in player_events_dict:
            event_type = event['type']
            player = event['player']
            
            if player == player_name:                
                if event_type == 'Pass':
                    match_stats["total_passes"] += 1
                elif event_type == 'Ball Receipt*':
                    match_stats["total_ball_receipts"] += 1
                elif event_type == 'Carry':
                    match_stats["total_carries"] += 1
                elif event_type == 'Pressure':
                    match_stats["total_pressures"] += 1
                elif event_type == 'Foul Committed':
                    match_stats["total_fouls_committed"] += 1
                elif event_type == 'Foul Won':
                    match_stats["total_fouls_won"] += 1
                elif event_type == 'Dispossessed':
                    match_stats["total_dispossessed"] += 1
                elif event_type == 'Duel':
                    match_stats["total_duels"] += 1
                elif event_type == 'Dribbled Past':
                    match_stats["total_dribbled_past"] += 1
                elif event_type == 'Dribble':
                    match_stats["total_dribbles"] += 1
                elif event_type == 'Block':
                    match_stats["total_blocks"] += 1
                elif event_type == 'Interception':
                    match_stats["total_interceptions"] += 1
                elif event_type == 'Ball Recovery':
                    match_stats["total_ball_recoveries"] += 1
                elif event_type == 'Miscontrol':
                    match_stats["total_miscontrols"] += 1
                elif event_type == 'Shield':
                    match_stats["total_shields"] += 1
                elif event_type == 'Shot':
                    match_stats["total_shots"] += 1
                elif event_type == 'Goal Keeper':
                    match_stats["total_goal_keeper"] += 1
                elif event_type == 'Bad Behaviour':
                    match_stats["total_bad_behaviour"] += 1
                else:
                    pass
                
        return PlayerProfile(match_id=match_id, match_stats=match_stats, player_info=player_info)