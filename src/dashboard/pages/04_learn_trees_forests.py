import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from src.dashboard.components.navigation import sidebar_navigation
from src.dashboard.components.model_cards import render_model_card
from src.dashboard.components.toy_datasets import generate_moons, generate_circles
from src.dashboard.components.mermaid import render_mermaid

st.set_page_config(page_title="Trees & Forests", page_icon="🌳", layout="wide")
sidebar_navigation()

st.title("🌳 Decision Trees & Random Forests")

# --- LAYER 1: Super Simple Intuition ---
st.header("1. Intuition: The Game of 20 Questions ❓")
st.markdown("""
Imagine you are playing "20 Questions". You want to guess what animal I am thinking of.
*   **Bad Question**: "Is it a Zebra?" (Too specific, likely "No", doesn't help much).
*   **Good Question**: "Is it a Mammal?" (Splits the possibilities in half).

A **Decision Tree** plays this game with data. It tries to find the **best possible question** to ask at every step to separate the Winners from the Losers.
""")

st.markdown("---")

# --- LAYER 2: Real-World Analogy ---
st.header("2. Analogy: The Doctor's Diagnosis 🩺")
st.markdown("""
A doctor diagnosing a patient follows a tree:
1.  **"Do you have a fever?"**
    *   **No**: "Does your knee hurt?" -> (Orthopedics)
    *   **Yes**: "Do you have a cough?"
        *   **Yes**: (Flu)
        *   **No**: (Infection)

At each step, the group of patients gets smaller and more similar (**purer**). The goal is to reach a "Leaf" where everyone has the same condition.
""")

st.markdown("---")

# --- LAYER 3: Structural Explanation ---
st.header("3. Structure: Nodes and Leaves 🌿")
render_mermaid("""
graph TD
    Root["Root Node <br> (All Data)"] -->|Split Condition| Node1["Internal Node"]
    Root -->|Split Condition| Node2["Internal Node"]
    Node1 --> Leaf1["Leaf Node <br> (Prediction: Win)"]
    Node1 --> Leaf2["Leaf Node <br> (Prediction: Lose)"]

    style Root fill:#e3f2fd
    style Leaf1 fill:#c8e6c9
    style Leaf2 fill:#ffcdd2
""", height=300)

st.markdown("""
*   **Root**: The starting point (all data).
*   **Split**: A question (e.g., `Rank < 10`).
*   **Leaf**: The end of the line. We make a prediction here (e.g., "Win").
*   **Impurity**: A measure of how "mixed" a node is. We want to minimize this.
""")

st.markdown("---")

# --- LAYER 4: Step-by-Step Breakdown ---
st.header("4. Step-by-Step Construction 🧱")
st.markdown("Let's build a tree manually using a tiny dataset.")

toy_data = pd.DataFrame({
    'Match': [1, 2, 3, 4, 5, 6],
    'RankDiff': [10, -5, 20, 50, -2, 5],
    'Surface': ['Clay', 'Grass', 'Clay', 'Hard', 'Grass', 'Hard'],
    'Winner': ['Win', 'Win', 'Lose', 'Lose', 'Win', 'Lose']
})
st.dataframe(toy_data, use_container_width=True)

st.markdown("""
**Goal**: Separate 3 Wins and 3 Losses.
**Current State**: 3W, 3L. (50/50 Mix).
""")

st.subheader("Step 1: Calculate Root Impurity")
st.latex(r"Gini = 1 - (p_{win}^2 + p_{loss}^2) = 1 - (0.5^2 + 0.5^2) = 0.5")

st.subheader("Step 2: Test Split A (Surface = Clay)")
st.markdown("""
*   **Left (Clay)**: Match 1 (Win), Match 3 (Lose). -> 1W, 1L. (Gini = 0.5).
*   **Right (Not Clay)**: 2W, 2L. (Gini = 0.5).
*   **Result**: No improvement. Bad split.
""")

st.subheader("Step 3: Test Split B (RankDiff < 0)")
st.markdown("""
*   **Left (RankDiff < 0)**: Match 2 (-5), Match 5 (-2). -> **2 Wins, 0 Losses**.
    *   Gini = $1 - (1.0^2 + 0.0^2) = 0.0$. (**Perfectly Pure!**)
*   **Right (RankDiff >= 0)**: Match 1, 3, 4, 6. -> **1 Win, 3 Losses**.
    *   Gini = $1 - (0.25^2 + 0.75^2) = 0.375$.
""")

st.subheader("Step 4: Choose Best Split")
st.success("Split B reduces impurity significantly. The Tree chooses 'RankDiff < 0' as the Root Question.")

st.markdown("---")

# --- LAYER 5: Full Math ---
st.header("5. The Math: Entropy & Gini 🧮")

st.subheader("A. Gini Impurity (The Standard)")
st.markdown("Used by CART (Classification and Regression Trees). It measures the probability of misclassifying a randomly chosen element.")
st.latex(r"Gini(D) = 1 - \sum_{i=1}^C p_i^2")

st.subheader("B. Entropy (Information Theory)")
st.markdown("Used by ID3/C4.5. Measures the amount of 'surprise' or 'disorder'.")
st.latex(r"Entropy(D) = - \sum_{i=1}^C p_i \log_2(p_i)")

st.subheader("C. Information Gain")
st.markdown("The improvement achieved by a split.")
st.latex(r"Gain = I(Parent) - \sum \frac{N_{child}}{N_{parent}} I(Child)")
st.markdown("We maximize this Gain.")

st.subheader("D. Random Forest Variance")
st.markdown("Why do Forests work better? Variance Reduction.")
st.latex(r"Var(\text{Forest}) = \rho \sigma^2 + \frac{1-\rho}{n} \sigma^2")
st.markdown("""
*   $\sigma^2$: Variance of one tree.
*   $n$: Number of trees.
*   $\rho$: Correlation between trees.
*   **Bootstrapping** and **Random Features** reduce $\rho$, making the forest stronger.
""")

st.markdown("---")

# --- LAYER 6: Diagrams ---
st.header("6. Visualization: Forest Voting 🗳️")
render_mermaid("""
graph LR
    Input["New Match"] --> T1
    Input --> T2
    Input --> T3

    subgraph Forest
        T1["Tree 1"] -->|Vote| V1["Win"]
        T2["Tree 2"] -->|Vote| V2["Lose"]
        T3["Tree 3"] -->|Vote| V3["Win"]
    end

    V1 --> Final["Majority Vote: <br> WIN"]
    V2 --> Final
    V3 --> Final
""", height=300)

st.markdown("---")

# --- LAYER 7: Micro-Examples ---
st.header("7. Micro-Examples 🧪")
st.markdown("**Example: Entropy of a Coin Toss**")
st.markdown("*   **Fair Coin (50/50)**: $p=0.5$. Entropy = $-0.5 \log_2(0.5) - 0.5 \log_2(0.5) = 1.0$ (Max Uncertainty).")
st.markdown("*   **Rigged Coin (100/0)**: $p=1.0$. Entropy = $-1 \log_2(1) = 0$ (Zero Uncertainty).")

st.markdown("---")

# --- LAYER 8: FAQ ---
st.header("8. FAQ 🙋")
with st.expander("Q: How deep should the tree be?"):
    st.markdown("Deep trees (depth=20) memorize data (Overfitting). Shallow trees (depth=2) are too simple (Underfitting). We usually tune this parameter.")
with st.expander("Q: Why random features in Forests?"):
    st.markdown("If we didn't use random features, every tree would pick the 'Best' feature (e.g., Rank) at the top. All trees would look the same. Randomness forces them to look at other features, creating diversity.")

st.markdown("---")

# --- LAYER 9: Exercises ---
st.header("9. Exercises 📝")
st.info("""
1.  **Calculate**: A node has 4 Wins and 0 Losses. What is its Gini? (Hint: $1 - (1^2 + 0^2)$)
2.  **Draw**: Draw a tree for deciding "Should I bring an umbrella?" (Rain? -> Yes/No).
3.  **Think**: If you have 1000 identical trees, is the Forest better than 1 tree? (Hint: Look at the variance formula).
""")

st.markdown("---")

# --- Interactive Playground ---
st.header("10. Interactive Playground")

col1, col2 = st.columns([1, 3])
with col1:
    dataset_type = st.selectbox("Dataset", ["Moons", "Circles"])
    noise = st.slider("Noise", 0.0, 1.0, 0.3)
    model_type = st.radio("Model", ["Decision Tree", "Random Forest"])
    max_depth = st.slider("Max Depth", 1, 20, 5)
    n_estimators = st.slider("Trees", 1, 100, 10) if model_type == "Random Forest" else 1

with col2:
    if dataset_type == "Moons":
        X, y = generate_moons(noise=noise)
    else:
        X, y = generate_circles(noise=noise)

    if model_type == "Decision Tree":
        clf = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    else:
        clf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)

    clf.fit(X, y)

    # Plot
    x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02), np.arange(y_min, y_max, 0.02))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    fig = go.Figure()
    fig.add_trace(go.Contour(x=np.arange(x_min, x_max, 0.02), y=np.arange(y_min, y_max, 0.02), z=Z, colorscale='RdBu', opacity=0.4, showscale=False))
    fig.add_trace(go.Scatter(x=X[y==0, 0], y=X[y==0, 1], mode='markers', name='Class 0', marker=dict(color='red')))
    fig.add_trace(go.Scatter(x=X[y==1, 0], y=X[y==1, 1], mode='markers', name='Class 1', marker=dict(color='blue')))
    fig.update_layout(title=f"{model_type} Boundary", height=500)
    st.plotly_chart(fig, use_container_width=True)

st.page_link("pages/02_model_playground.py", label="🎮 Go to Playground", icon="🎮")
