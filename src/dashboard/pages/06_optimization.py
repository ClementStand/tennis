import streamlit as st
import numpy as np
import plotly.graph_objects as go
from src.dashboard.components.navigation import sidebar_navigation

st.set_page_config(page_title="Gradient Descent", page_icon="📉", layout="wide")
sidebar_navigation()

st.title("📉 Optimization: Gradient Descent")

# --- LAYER 1: Intuition ---
st.header("1. Intuition: The Blind Hiker 🏔️")
st.markdown("""
Imagine you are on a mountain at night. It's pitch black. You want to get to the village at the bottom.
You can't see the path. What do you do?
1.  Feel the ground with your feet.
2.  Find which way is **down**.
3.  Take a small step.
4.  Repeat.

This is **Gradient Descent**.
*   **Mountain**: The Loss Function (Error).
*   **You**: The Model.
*   **Village**: The Optimal Weights (Lowest Error).
""")
st.markdown("---")

# --- LAYER 3: Structure ---
st.header("3. Structure: The Update Loop 🔄")
st.markdown("""
1.  **Calculate Gradient**: Find the slope ($\nabla J$).
2.  **Update Weights**: Move opposite to the slope.
    *   $w_{new} = w_{old} - \text{Step} \times \text{Slope}$
3.  **Repeat**: Until slope is zero.
""")
st.markdown("---")

# --- LAYER 5: Full Math ---
st.header("5. The Math: The Gradient Vector 🧮")

st.subheader("A. The Gradient")
st.markdown("The gradient $\nabla J(w)$ is a vector of partial derivatives. It always points **Uphill** (Steepest Ascent).")
st.latex(r"\nabla J(w) = \left[ \frac{\partial J}{\partial w_1}, \frac{\partial J}{\partial w_2}, \dots \right]")

st.subheader("B. The Update Rule")
st.markdown("Since we want to go **Downhill**, we subtract the gradient.")
st.latex(r"w \leftarrow w - \eta \nabla J(w)")
st.markdown("*   $\eta$ (Eta): Learning Rate. The size of the step.")

st.subheader("C. Convexity")
st.markdown("If the bowl is shaped like a perfect U (Convex), we are guaranteed to find the bottom. If it's wavy (Non-Convex), we might get stuck in a small valley (Local Minimum).")
st.markdown("---")

# --- LAYER 6: Diagrams (3D) ---
st.header("6. Visualization: The 3D Loss Surface 🧊")

# 3D Surface Data
x = np.linspace(-10, 10, 50)
y = np.linspace(-10, 10, 50)
X, Y = np.meshgrid(x, y)
Z = X**2 + Y**2  # Simple Bowl

fig_3d = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis', opacity=0.8)])
fig_3d.update_layout(title="Loss Surface J(w1, w2)", scene=dict(xaxis_title='w1', yaxis_title='w2', zaxis_title='Loss'), height=500)
st.plotly_chart(fig_3d, use_container_width=True)

st.markdown("---")

# --- LAYER 7: Micro-Examples ---
st.header("7. Micro-Examples 🧪")
st.markdown("**Function**: $J(w) = w^2$. **Gradient**: $2w$.")
st.markdown("**Start**: $w=3$. **Rate**: $\eta=0.1$.")
st.markdown("1. Grad = $2(3) = 6$.")
st.markdown("2. Step = $0.1 \times 6 = 0.6$.")
st.markdown("3. New w = $3 - 0.6 = 2.4$.")
st.markdown("4. Grad = $2(2.4) = 4.8$. (Slope got smaller!)")
st.markdown("---")

# --- Interactive Viz ---
st.header("10. Interactive Playground")
col1, col2 = st.columns([1, 3])
with col1:
    lr = st.slider("Learning Rate", 0.01, 1.1, 0.1)
    steps = st.slider("Steps", 1, 50, 10)

with col2:
    w_range = np.linspace(-10, 10, 100)
    J_range = w_range**2

    path_w = [8.0]
    path_J = [64.0]
    curr = 8.0
    for _ in range(steps):
        grad = 2 * curr
        curr = curr - lr * grad
        path_w.append(curr)
        path_J.append(curr**2)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=w_range, y=J_range, name="Loss"))
    fig.add_trace(go.Scatter(x=path_w, y=path_J, mode='markers+lines', name="Path", marker=dict(color='red')))
    st.plotly_chart(fig, use_container_width=True)

st.page_link("pages/02_model_playground.py", label="🎮 Go to Playground", icon="🎮")
