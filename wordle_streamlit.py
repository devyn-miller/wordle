import streamlit as st
import random

# Load words from file
with open('words.txt', 'r') as file:
    words = [line.strip() for line in file.readlines()]

# Initialize session state variables if they don't exist
if 'word_length' not in st.session_state:
    st.session_state.word_length = 5
if 'max_guesses' not in st.session_state:
    st.session_state.max_guesses = 6
if 'current_attempt' not in st.session_state:
    st.session_state.current_attempt = 0
if 'target_word' not in st.session_state:
    st.session_state.target_word = random.choice(words)
if 'guesses' not in st.session_state:
    st.session_state.guesses = [''] * st.session_state.max_guesses

def check_word():
    guess = st.session_state.guesses[st.session_state.current_attempt].lower()
    if len(guess) != st.session