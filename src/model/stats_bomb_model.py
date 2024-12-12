from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class PlayerEvents(Enum):
    PASS = 'Pass'
    BALL_RECEIPT = 'Ball Receipt*'
    CARRY = 'Carry'
    PRESSURE = 'Pressure'
    FOUL_COMMITTED = 'Foul Committed'
    FOUL_WON = 'Foul Won'
    DISPOSSESSED = 'Dispossessed'
    DUEL = 'Duel'
    DRIBBLED_PAST = 'Dribbled Past'
    DRIBBLE = 'Dribble'
    BLOCK = 'Block'
    INTERCEPTION = 'Interception'
    BALL_RECOVERY = 'Ball Recovery'
    MISCONTROL = 'Miscontrol'
    SHIELD = 'Shield'
    SHOT = 'Shot'
    GOAL_KEEPER = 'Goal Keeper'
    BAD_BEHAVIOUR = 'Bad Behaviour'
        
    def to_value_list() -> List:
        return [e.value for e in PlayerEvents]

class MatchEvents(Enum):
    STARTING_XI = 'Starting XI'
    HALF_START = 'Half Start'
    PASS = 'Pass'
    BALL_RECEIPT = 'Ball Receipt*'
    CARRY = 'Carry'
    PRESSURE = 'Pressure'
    FOUL_COMMITTED = 'Foul Committed'
    FOUL_WON = 'Foul Won'
    DISPOSSESSED = 'Dispossessed'
    DUEL = 'Duel'
    DRIBBLED_PAST = 'Dribbled Past'
    DRIBBLE = 'Dribble'
    CLEARANCE = 'Clearance'
    BLOCK = 'Block'
    INTERCEPTION = 'Interception'
    BALL_RECOVERY = 'Ball Recovery'
    MISCONTROL = 'Miscontrol'
    SHIELD = 'Shield'
    SHOT = 'Shot'
    GOAL_KEEPER = 'Goal Keeper'
    INJURY_STOPPAGE = 'Injury Stoppage'
    REFEREE_BALL_DROP = 'Referee Ball-Drop'
    HALF_END = 'Half End'
    SUBSTITUTION = 'Substitution'
    BAD_BEHAVIOUR = 'Bad Behaviour'
    TACTICAL_SHIFT = 'Tactical Shift'
    FIFTY_FIFTY = '50/50'
        
    def to_value_list() -> List:
        return [e.value for e in MatchEvents]
    
    
class MatchStats(BaseModel):
    total_passes: int
    total_ball_receipts: int
    total_carries: int
    total_pressures: int
    total_fouls_committed: int
    total_fouls_won: int
    total_dispossessed: int
    total_duels: int
    total_dribbled_past: int
    total_dribbles: int
    total_blocks: int
    total_interceptions: int
    total_ball_recoveries: int
    total_miscontrols: int
    total_shields: int
    total_shots: int
    total_goal_keeper: int
    total_bad_behaviour: int

class Position(BaseModel):
    position_id: int
    position: str
    from_time: Optional[str] = Field(None, alias='from')
    to_time: Optional[str] = Field(None, alias='to')
    from_period: Optional[int] = None
    to_period: Optional[int] = None
    start_reason: Optional[str] = None
    end_reason: Optional[str] = None

class PlayerInfo(BaseModel):
    player_id: int
    player_name: str
    player_nickname: Optional[str] = None
    jersey_number: int
    country: str
    cards: List[Any] = []
    positions: List[Position] 
    
class PlayerProfile(BaseModel):
    match_id: int
    match_stats: MatchStats
    player_info: PlayerInfo
    