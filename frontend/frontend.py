import streamlit as st
from agent_ai.Agent import chat

user_input = st.text_input("Say something:")
if user_input:
    st.write(chat(user_input))
    st.write(chat(user_input))
    st.write(chat(user_input))