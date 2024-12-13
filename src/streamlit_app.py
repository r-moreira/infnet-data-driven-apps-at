import streamlit as st
from streamlit_option_menu import option_menu
from service.statsbomb_service import StatsBombService
from typing import Dict, Tuple

@st.cache_data(ttl=3600)
def get_cached_competitions():
   return StatsBombService.get_competitions_dict()

def sidebar_option() -> Tuple[int | None, Dict | None, Dict | None]:
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


match_id, competition_season, match = sidebar_option()

selected_option = option_menu(None, ["Match Events", "Player Profile", "AI Agent"], 
    icons=['lightning', 'file-earmark-person', "robot"], 
    menu_icon="cast", default_index=0, orientation="horizontal")

st.divider()

st.markdown(f"<h3 style='text-align: center;'>{match['home_team']} vs {match['away_team']}</h3>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center;'>{match['home_score']} x {match['away_score']}</h3>", unsafe_allow_html=True)
st.markdown(f"<h4 style='text-align: center;'> At {match['stadium']} - {match['match_date']}</h4>", unsafe_allow_html=True)


