import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.dashboard.components.navigation import sidebar_navigation

st.set_page_config(page_title="Gradient Descent", page_icon="📉", layout="wide")
sidebar_navigation()

st.title("📉 Optimization: The Engine of Learning")

# --- 1. Intuition ---
st.header("1. Intuition: The Hiker in the Fog 🌫️")
st.markdown(r"""
Imagine you are lost on a mountain at night. There is thick fog, so you can't see the village at the bottom.
You want to get down as fast as possible.

**What do you do?**
1.  **Feel the ground** with your foot.
2.  Find the direction that slopes **down** the steepest.
3.  Take a step in that direction.
4.  Repeat.

This is **Gradient Descent**.
*   **Mountain**: The Loss Function (Error).
*   **Altitude**: The value of the Loss (Lower is better).
*   **Coordinates (Lat/Long)**: The Weights ($w$) of your model.
*   **Steepness**: The Gradient ($\nabla J$).
""")

# --- 2. The Math (Step-by-Step) ---
st.header("2. The Math: Step-by-Step Walkthrough")
st.markdown(r"""
Let's trace exactly what happens during **one single step** of learning.

**Scenario**:
*   We have a simple model: $Loss = w^2$. (A parabola).
*   Current Weight: $w = 3$.
*   Learning Rate ($\eta$): $0.1$.

**Goal**: Reduce the Loss.
""")

col_step1, col_step2, col_step3 = st.columns(3)

with col_step1:
    st.markdown("### Step 1: Calculate Gradient")
    st.markdown(r"The Gradient is the derivative (slope).")
    st.latex(r"\frac{\partial Loss}{\partial w} = \frac{\partial}{\partial w} (w^2) = 2w")
    st.markdown(r"At $w=3$:")
    st.latex(r"\text{Gradient} = 2 \times 3 = \mathbf{6}")
    st.markdown("Positive slope means 'Uphill is to the Right'.")

with col_step2:
    st.markdown("### Step 2: Calculate Step")
    st.markdown(r"We want to go **Downhill** (Left).")
    st.latex(r"\text{Step} = - \eta \times \text{Gradient}")
    st.latex(r"\text{Step} = - 0.1 \times 6 = \mathbf{-0.6}")

with col_step3:
    st.markdown("### Step 3: Update Weight")
    st.latex(r"w_{new} = w_{old} + \text{Step}")
    st.latex(r"w_{new} = 3 - 0.6 = \mathbf{2.4}")
    st.markdown("New Loss: $2.4^2 = 5.76$ (Better than $3^2=9$!)")

st.success("We successfully descended from Loss=9 to Loss=5.76. Repeat this 100 times, and we reach $w=0$.")

# --- 3. Advanced Optimizers (Platinum Depth) ---
st.header("3. Advanced Optimizers: Adam & Friends")
st.markdown("Vanilla Gradient Descent is slow and dumb. Modern AI uses **Adam**.")

tab_mom, tab_adam, tab_sgd = st.tabs(["Momentum", "Adam (The King)", "Batch vs SGD"])

with tab_mom:
    st.subheader("Momentum: The Heavy Ball 🎳")
    st.markdown(r"""
    **Problem**: If the surface is flat (plateau), gradients are tiny. Learning stops.
    **Solution**: Give the optimizer **Mass**.

    If a heavy ball rolls down a hill, it gains **Velocity**. Even if the hill flattens out, the ball keeps rolling due to inertia.

    **The Math**:
    """)
    st.latex(r"v_{t} = \gamma v_{t-1} + \eta \nabla J(w_t)")
    st.latex(r"w_{t+1} = w_t - v_{t}")
    st.markdown(r"""
    *   $v_t$: The velocity vector. Accumulates past gradients.
    *   $\gamma$ (Gamma): Friction (usually 0.9). We keep 90% of our previous speed.
    """)

with tab_adam:
    st.subheader("Adam: Adaptive Moment Estimation 🧠")
    st.markdown(r"""
    Adam is the **Gold Standard**. It combines two great ideas:
    1.  **Momentum** (Keep moving forward).
    2.  **RMSProp** (Scale learning rate by volatility).

    **The Logic**:
    *   "If a parameter has huge gradients (very steep), **slow down** to be careful."
    *   "If a parameter has tiny gradients (very flat), **speed up** to make progress."

    **The Full Math (Simplified):**
    """)

    col_m, col_v = st.columns(2)
    with col_m:
        st.markdown("**1. First Moment (Momentum)**")
        st.markdown("Average of past gradients.")
        st.latex(r"m_t = \beta_1 m_{t-1} + (1-\beta_1) \nabla J")
    with col_v:
        st.markdown("**2. Second Moment (Variance)**")
        st.markdown("Average of past squared gradients (Volatility).")
        st.latex(r"v_t = \beta_2 v_{t-1} + (1-\beta_2) (\nabla J)^2")

    st.markdown("**3. The Update Rule**")
    st.latex(r"w_{t+1} = w_t - \frac{\eta}{\sqrt{v_t} + \epsilon} m_t")
    st.markdown(r"""
    *   We divide by $\sqrt{v_t}$.
    *   If variance $v_t$ is **High** (Steep/Volatile), we divide by a big number -> **Small Step**.
    *   If variance $v_t$ is **Low** (Flat/Stable), we divide by a small number -> **Big Step**.
    """)

with tab_sgd:
    st.subheader("Batch vs. Stochastic vs. Mini-Batch")
    st.markdown(r"""
    How much data do we look at before taking a step?

    1.  **Batch GD**: Look at **ALL** data. (Precise, but Slow).
        *   "I read the entire map before taking one step."
    2.  **Stochastic GD (SGD)**: Look at **ONE** sample. (Fast, but Noisy/Drunk).
        *   "I look at one tree, take a step. Look at another tree, take a step."
    3.  **Mini-Batch GD**: Look at **32 or 64** samples. (Best of both worlds).
        *   "I look at a small patch of terrain, then move."
    """)

# --- 6. Visualization ---
st.header("6. Visualization: The 3D Surface")

col_viz, col_controls = st.columns([3, 1])
with col_controls:
    lr = st.slider("Learning Rate", 0.01, 1.2, 0.1)
    steps = st.slider("Steps", 1, 100, 50)
    optimizer = st.selectbox("Optimizer", ["GD", "Momentum"])
    momentum = st.slider("Momentum (Gamma)", 0.0, 0.99, 0.9) if optimizer == "Momentum" else 0.0

with col_viz:
    # Surface Data
    x = np.linspace(-10, 10, 50)
    y = np.linspace(-10, 10, 50)
    X, Y = np.meshgrid(x, y)
    Z = X**2 + Y**2  # Simple Bowl

    # Path Calculation
    path_x = [8.0]
    path_y = [0.0]
    path_z = [64.0]

    curr_x = 8.0
    curr_y = 0.0
    vel_x = 0.0
    vel_y = 0.0

    for _ in range(steps):
        grad_x = 2 * curr_x
        grad_y = 2 * curr_y

        if optimizer == "Momentum":
            vel_x = momentum * vel_x + lr * grad_x
            vel_y = momentum * vel_y + lr * grad_y
            curr_x = curr_x - vel_x
            curr_y = curr_y - vel_y
        else:
            curr_x = curr_x - lr * grad_x
            curr_y = curr_y - lr * grad_y

        path_x.append(curr_x)
        path_y.append(curr_y)
        path_z.append(curr_x**2 + curr_y**2)

    fig = go.Figure()

    # Surface
    fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale='Viridis', opacity=0.8, showscale=False))

    # Path
    fig.add_trace(go.Scatter3d(x=path_x, y=path_y, z=path_z, mode='markers+lines',
                               marker=dict(size=4, color='red'), line=dict(color='red', width=4), name='Path'))

    fig.update_layout(title=f"Optimization Path ({optimizer})",
                      scene=dict(xaxis_title='w1', yaxis_title='w2', zaxis_title='Loss'), height=600)
    st.plotly_chart(fig, use_container_width=True)

# --- 7. How to do it in Python ---
st.header("7. How to do it in Python 🐍")
st.markdown("Most sklearn models hide the optimizer, but you can control it.")
st.code("""
from sklearn.linear_model import SGDClassifier, LogisticRegression

# Option A: Explicit Stochastic Gradient Descent
sgd = SGDClassifier(loss='log_loss', learning_rate='adaptive', eta0=0.01)
sgd.fit(X_train, y_train)

# Option B: Configuring the Solver in Logistic Regression
# 'lbfgs' is a quasi-Newton method (better than vanilla GD)
lr = LogisticRegression(solver='lbfgs', max_iter=1000)
lr.fit(X_train, y_train)
""", language="python")

# --- 8. Super Summary ---
st.header("8. Super Summary 🦸")
st.info(r"""
*   **Goal**: Find the bottom of the valley (Min Loss).
*   **Gradient**: The compass pointing Uphill. We go opposite.
*   **Learning Rate**: Step size. Too big = Explode. Too small = Slow.
*   **Adam**: The smart optimizer that adapts speed for each parameter.
""")
