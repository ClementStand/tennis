import streamlit as st
import numpy as np
import plotly.graph_objects as go
from src.dashboard.components.navigation import sidebar_navigation

st.set_page_config(page_title="Hyperparameters", page_icon="🎛️", layout="wide")
sidebar_navigation()

st.title("🎛️ Hyperparameters: Tuning the Radio")

# --- LAYER 1: Intuition ---
st.header("1. Intuition: The Radio Station 📻")
st.markdown("""
*   **Parameters ($w, b$)**: The music playing. The model learns this from the data.
*   **Hyperparameters**: The knobs on the radio (Volume, Bass, Treble). **YOU** set these before the music starts.
    *   If Bass is too high, the music sounds muddy (Underfitting).
    *   If Treble is too high, it hurts your ears (Overfitting).
    *   You need to tune the knobs to get the perfect sound.
""")
st.markdown("---")

# --- LAYER 3: Structure ---
st.header("3. Structure: Grid Search 🔍")
st.markdown("""
How do we find the best settings? We try them all!
1.  **Grid Search**: Try every combination. (Slow but thorough).
    *   Depth: [3, 5, 10]
    *   Trees: [10, 50, 100]
    *   Total: $3 \times 3 = 9$ models to train.
2.  **Cross-Validation**: For each setting, test it 5 times on different data chunks to be sure.
""")
st.markdown("---")

# --- LAYER 6: Diagrams ---
st.header("6. Visualization: Complexity vs Error 📉")

# Synthetic Complexity Curve
complexity = np.linspace(1, 10, 50)
train_err = 1 / complexity
test_err = 1 / complexity + (complexity * 0.05) # U-shape

fig = go.Figure()
fig.add_trace(go.Scatter(x=complexity, y=train_err, name="Training Error (Decreases forever)"))
fig.add_trace(go.Scatter(x=complexity, y=test_err, name="Test Error (U-Shape)"))
fig.update_layout(title="The Bias-Variance Tradeoff", xaxis_title="Model Complexity (e.g., Tree Depth)", yaxis_title="Error")
st.plotly_chart(fig, use_container_width=True)

st.success("The Sweet Spot is where the Test Error is lowest (the bottom of the U).")

st.page_link("pages/02_model_playground.py", label="🎮 Go to Playground", icon="🎮")
