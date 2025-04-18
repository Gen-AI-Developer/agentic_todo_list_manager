import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent_ai.Agent import chat


st.title("Todo Chat Assistant")

user_input = st.chat_input("Say something:")
if user_input:
    response = chat(user_input)
    st.chat_message(response)