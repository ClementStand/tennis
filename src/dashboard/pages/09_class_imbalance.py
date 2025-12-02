import streamlit as st
import numpy as np
import plotly.graph_objects as go
from src.dashboard.components.navigation import sidebar_navigation

st.set_page_config(page_title="Class Imbalance", page_icon="⚖️", layout="wide")
sidebar_navigation()

st.title("⚖️ Class Imbalance: The needle in the haystack")

# --- LAYER 1: Intuition ---
st.header("1. Intuition: The Lazy Student 😴")
st.markdown("""
Imagine a test with 100 questions.
*   99 questions are "False".
*   1 question is "True".

A lazy student can just answer "False" to everything and get **99% Accuracy**.
But they failed to find the one thing that mattered.

In Tennis, upsets are rare. If a model always predicts "Favorite Wins", it will have high accuracy but is useless for betting on upsets.
""")
st.markdown("---")

# --- LAYER 5: Full Math ---
st.header("5. The Math: Weighted Loss 🧮")
st.markdown("How do we fix this? We punish the model more for missing the rare class.")

st.latex(r"L = - [ w_1 y \log(p) + w_0 (1-y) \log(1-p) ]")

st.markdown("""
*   Normally, $w_1 = w_0 = 1$.
*   If Class 1 is rare (1%), we set $w_1 = 100$.
*   Now, missing a Class 1 example costs **100x more** than missing a Class 0 example.
*   The model is forced to pay attention.
""")
st.markdown("---")

# --- Interactive Viz ---
st.header("10. Interactive Playground")

imbalance = st.slider("Imbalance Ratio (Minority Class %)", 1, 50, 10)
n_samples = 1000
n_minority = int(n_samples * (imbalance / 100))
n_majority = n_samples - n_minority

st.metric("Majority Class", n_majority)
st.metric("Minority Class", n_minority)
st.metric("Lazy Accuracy (Predict All Majority)", f"{n_majority/n_samples:.1%}")

st.page_link("pages/02_model_playground.py", label="🎮 Go to Playground", icon="🎮")
