from fastapi.encoders import jsonable_encoder
import streamlit as st
from streamlit_option_menu import option_menu
from service.statsbomb_service import StatsBombService
from model.stats_bomb_model import MatchEvents, PlayerProfile
from typing import Dict, Tuple
import pandas as pd
import logging
import plotly.express as px
import plotly.graph_objects as go

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

@st.dialog("Error")
def global_error_dialog() -> None:
    st.error(f"Something went wrong :(")
    
@st.cache_data(ttl=3600)
def get_cached_competitions():
   return StatsBombService.get_competitions_dict()

def sidebar_option_view() -> Tuple[int | None, Dict | None, Dict | None]:
    with st.sidebar:
        selected_competition = None
        selected_season = None
        selected_match = None
        match_id = None
    
        st.title("Football Match Selector")
        competitions = get_cached_competitions()
    
        unique_competitions = {comp['competition_name']: comp for comp in competitions}.values()
        sorted_competitions = sorted(unique_competitions, key=lambda comp: comp['competition_name'])
        selected_competition = st.selectbox(
            "Choose a Competition",
            sorted_competitions,
            format_func=lambda comp: comp['competition_name']
        )
    
        if selected_competition:
            seasons = [comp for comp in competitions if comp['competition_name'] == selected_competition['competition_name']]
            sorted_seasons = sorted(seasons, key=lambda season: season['season_name'])
            selected_season = st.selectbox(
                "Choose a Season", sorted_seasons, 
                format_func=lambda season: season['season_name']
            )
        
            if selected_season:
                matches = StatsBombService.get_matches_dict(selected_competition['competition_id'], selected_season['season_id'])
                selected_match = st.selectbox(
                    "Choose a Match", matches,
                    format_func=lambda match: f"{match['home_team']} x {match['away_team']}" 
                )
                
                if selected_match:
                    match_id = selected_match['match_id']
                    
        return match_id, selected_season, selected_match


def main_view():
    match_id, competition_season, match = sidebar_option_view()

    st.markdown(f"<h3 style='text-align: center;'>{match['home_team']} vs {match['away_team']}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>{match['home_score']} x {match['away_score']}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: center;'> At {match['stadium']} - {match['match_date']}</h4>", unsafe_allow_html=True)
       
    st.divider()

    selected_option = option_menu(
        menu_title=None,
        options=["Match Events", "Player Profile", "AI Agent"], 
        icons=['lightning', 'file-earmark-person', "robot"], 
        default_index=0,
        orientation="horizontal"
    )

    if selected_option == "Match Events":
        selected_events = st.multiselect(
            "Match Events",
            MatchEvents.to_value_list()
        )
        
        if selected_events:
            events_dict = StatsBombService.get_events_dict(match_id, event_type_list=selected_events)
            
            df = pd.DataFrame(events_dict)
            df = df.dropna(axis=1, how='all')
            st.dataframe(df)
    
    elif selected_option == "Player Profile":        
        player_team = st.selectbox(
            "Choose a Team",
            [match['home_team'], match['away_team']]
        )
        
        if player_team:
            players = StatsBombService.get_lineups_dict(match_id, player_team)
            
            player = st.selectbox(
                "Choose a Player",
                players,
                format_func=lambda player: player['player_name']
            )
            
            if player:        
                player_profile: PlayerProfile = None
              
                st.markdown(f"<h3 style='text-align: center;'>{player['player_name']}</h3>", unsafe_allow_html=True)
                st.markdown(f"<h4 style='text-align: center;'>Jersey Number: {player['jersey_number']}</h4>", unsafe_allow_html=True)
                st.markdown(f"<h4 style='text-align: center;'>Country: {player['country']}</h4>", unsafe_allow_html=True)
                
                for position in player['positions']:
                    st.markdown(f"<h4 style='text-align: center;'>Position: {position['position']}, from: {position['from']} to: {position['to']}</h4>", unsafe_allow_html=True)
         
                try:
                    player_profile = StatsBombService.get_player_profile(match_id, player["player_name"])
                except Exception as e:
                    if "404" in str(e):
                        st.warning("Events not found for the selected player")
                        return 
                    raise e
                
                match_stats = player_profile.match_stats.model_dump()

                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=list(match_stats.keys()),
                    y=list(match_stats.values()),
                    marker_color='#28af0c'
                ))

                fig.update_layout(
                    title=f"Match Events for {player['player_name']}",
                    xaxis_title="Stat Type",
                    yaxis_title="Value",
                    xaxis_tickangle=-45
                )

                st.plotly_chart(fig)               
                
                with st.expander("Player Profile JSON"):
                    st.write(player_profile.model_dump())
    
    
    elif selected_option == "AI Agent":
        st.write("AI Agent")

try:
    main_view()
except Exception as e:
    logging.error(f"Error rendering View: {e}")
    global_error_dialog()
