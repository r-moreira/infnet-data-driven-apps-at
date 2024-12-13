import streamlit as st
from service.statsbomb_service import StatsBombService

st.title("Hello World")

st.json(StatsBombService.get_competitions_dict())

