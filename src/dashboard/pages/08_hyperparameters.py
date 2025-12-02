import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.dashboard.components.navigation import sidebar_navigation

st.set_page_config(page_title="Hyperparameters", page_icon="🎛", layout="wide")
sidebar_navigation()

st.title("🎛 Hyperparameters & Cross-Validation")

# --- 1. Core Model Definition ---
st.header("1. Core Model Definition")
st.markdown(r"""
**Parameters** ($w, b$) are learned *during* training.
**Hyperparameters** are set *before* training. They control the architecture and learning process.

Examples:
*   **Capacity**: Tree Depth, Number of Neurons.
*   **Regularization**: C, Lambda, Dropout.
*   **Optimization**: Learning Rate, Batch Size.
""")

# --- 2. The Bias-Variance Tradeoff ---
st.header("2. The Bias-Variance Tradeoff")
st.markdown(r"""
The Holy Grail of ML is **Generalization**.
We decompose the Error into three parts:

1.  **Bias (Underfitting)**: The model is too stupid. It assumes the world is simple (linear) when it's complex (curved).
    *   *Solution*: Increase Complexity (More depth, more neurons).
2.  **Variance (Overfitting)**: The model is too smart. It memorizes the noise in the training set.
    *   *Solution*: Decrease Complexity, Add Regularization, Get More Data.
3.  **Irreducible Error**: The noise inherent in the universe. (You can't fix this).
""")

st.latex(r"E[\text{Total Error}] = \text{Bias}^2 + \text{Variance} + \text{Noise}")

# --- 3. Cross-Validation (Platinum Depth) ---
st.header("3. Cross-Validation: The Exam Analogy 📝")
st.markdown(r"""
How do we know if our model is good?

**The Analogy**:
*   **Training Set**: The Textbook. You study this to learn.
*   **Validation Set**: The Practice Exam. You use this to tune your study habits (Hyperparameters).
*   **Test Set**: The Final Exam. You only see this ONCE at the very end.

**The Golden Rule**: NEVER tune on the Test Set. That is cheating (Data Leakage).
""")

st.subheader("The Algorithms")
tab_kfold, tab_strat, tab_time = st.tabs(["K-Fold CV", "Stratified K-Fold", "Time Series Split"])

with tab_kfold:
    st.markdown("**K-Fold Cross-Validation**")
    st.markdown("""
    1.  Split data into $K$ equal chunks (Folds).
    2.  Train on $K-1$ folds.
    3.  Validate on the remaining 1 fold.
    4.  Repeat $K$ times, rotating the validation fold.
    5.  **Final Score**: Average of the $K$ scores.
    """)
    st.info("Robust because every data point gets to be in the validation set exactly once.")
    st.code("""
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
cv = KFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')

print(f"Average Accuracy: {scores.mean():.2f}")
    """, language="python")

with tab_strat:
    st.markdown("**Stratified K-Fold** (Crucial for Imbalanced Data)")
    st.markdown("""
    If you have 90% Class A and 10% Class B, a random split might give you a fold with **zero** Class B.
    **Stratified** splitting ensures each fold has the **same percentage** of samples for each class as the complete set.
    """)
    st.warning("ALWAYS use this for Classification problems.")
    st.code("""
from sklearn.model_selection import StratifiedKFold

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
# Usage is identical to KFold
scores = cross_val_score(model, X, y, cv=cv, scoring='f1')
    """, language="python")

with tab_time:
    st.markdown("**Time Series Split** (Crucial for Tennis/Finance)")
    st.markdown("""
    You cannot shuffle time!
    *   **Wrong**: Train on 2024, Validate on 2023. (Leakage: Future predicts Past).
    *   **Right**: Train on Jan-Mar, Validate on Apr. Train on Jan-Apr, Validate on May.
    """)
    st.code("""
from sklearn.model_selection import TimeSeriesSplit

cv = TimeSeriesSplit(n_splits=5)
for train_index, val_index in cv.split(X):
    X_train, X_val = X[train_index], X[val_index]
    y_train, y_val = y[train_index], y[val_index]
    # Train and Evaluate...
    """, language="python")

# --- 4. Search Strategies ---
st.header("4. Search Strategies")
st.markdown("How do we find the best settings? It's a search problem.")

tab_grid, tab_rand = st.tabs(["Grid Search", "Random Search"])

with tab_grid:
    st.subheader("Grid Search 🕸️")
    st.markdown("Try **EVERY** combination. Guaranteed to find the best, but slow.")
    st.code("""
from sklearn.model_selection import GridSearchCV

param_grid = {
    'C': [0.1, 1, 10],
    'kernel': ['linear', 'rbf']
}
grid = GridSearchCV(SVC(), param_grid, cv=5)
grid.fit(X_train, y_train)

print(grid.best_params_)
    """, language="python")

with tab_rand:
    st.subheader("Random Search 🎲")
    st.markdown("Try **RANDOM** combinations. Faster and often better.")
    st.code("""
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform

param_dist = {
    'C': uniform(0.1, 10),  # Any float between 0.1 and 10.1
    'kernel': ['linear', 'rbf']
}
rand = RandomizedSearchCV(SVC(), param_dist, n_iter=10, cv=5)
rand.fit(X_train, y_train)
    """, language="python")

# --- 6. Visualization ---
st.header("6. Visualization: The Validation Curve")

col_viz, col_controls = st.columns([3, 1])
with col_controls:
    complexity = st.slider("Model Complexity", 1, 100, 50)

with col_viz:
    x = np.linspace(1, 100, 100)
    # Bias decreases
    bias = 50 * np.exp(-0.05 * x)
    # Variance increases
    variance = 0.01 * x**2
    # Total
    total = bias + variance + 10

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=bias, name='Bias (Underfit)', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=x, y=variance, name='Variance (Overfit)', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=x, y=total, name='Total Error', line=dict(color='green', width=4)))

    # Current
    curr_bias = 50 * np.exp(-0.05 * complexity)
    curr_var = 0.01 * complexity**2
    curr_tot = curr_bias + curr_var + 10

    fig.add_trace(go.Scatter(x=[complexity], y=[curr_tot], mode='markers', marker=dict(size=15, color='black'), name='Your Model'))

    fig.update_layout(title="The Bias-Variance Tradeoff", xaxis_title="Complexity", yaxis_title="Error", height=500)
    st.plotly_chart(fig, use_container_width=True)

# --- 8. Super Summary ---
st.header("8. Super Summary 🦸")
st.info(r"""
*   **Goal**: Generalization.
*   **Cross-Validation**: The standard way to evaluate models reliably.
*   **Stratified**: Use for Classification.
*   **Time Series**: Use for Forecasting.
*   **Grid/Random Search**: Use to automate tuning.
""")
