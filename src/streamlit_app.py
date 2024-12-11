import streamlit as st
from service import statsbomb_service

st.title("Hello World")

st.json(statsbomb_service.get_competitions())

