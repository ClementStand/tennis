import streamlit as st
import numpy as np
import plotly.graph_objects as go
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.dashboard.components.navigation import sidebar_navigation
from src.dashboard.components.mermaid import render_mermaid
from src.dashboard.components.toy_datasets import generate_moons, generate_circles, generate_linear

st.set_page_config(page_title="SVM & KNN", page_icon="📐", layout="wide")
sidebar_navigation()

st.title("📐 SVM & K-Nearest Neighbors")

tab1, tab2 = st.tabs(["Support Vector Machines (SVM)", "K-Nearest Neighbors (KNN)"])

# ==========================================
# SVM SECTION (THE GOLD STANDARD)
# ==========================================
with tab1:
    st.header("Support Vector Machines (SVM)")

    # --- 1. Core Model Definition ---
    st.subheader("1. Core Model Definition")
    st.markdown("""
    The Support Vector Machine (SVM) is a **Linear Classifier** that finds the "Best" line to separate data.

    **The Decision Function:**
    """)
    st.latex(r"f(x) = w^T x + b")
    st.markdown("""
    *   $x$: The input vector (e.g., Rank Diff, Points Diff).
    *   $w$: The **Weight Vector**. It points perpendicular to the decision boundary.
    *   $b$: The **Bias**. It shifts the line away from the origin.
    *   $f(x)$: The **Signed Distance** (unnormalized).

    **The Prediction:**
    """)
    st.latex(r"\hat{y} = \text{sign}(f(x))")
    st.markdown("""
    *   If $f(x) > 0$: Predict **Class +1 (Win)**.
    *   If $f(x) < 0$: Predict **Class -1 (Lose)**.
    """)

    # --- 2. Geometry / Structure ---
    st.subheader("2. Geometry: Signed Safety & The Margin Band")
    st.markdown("""
    We don't just want to be *correct*. We want to be **Safe**.

    *   **Signed Safety**: $y_i (w^T x_i + b)$.
        *   If $y=+1$ and score is $+5$, Safety = $+5$ (Safe).
        *   If $y=+1$ and score is $-5$, Safety = $-5$ (Wrong).
        *   If $y=-1$ and score is $-5$, Safety = $+5$ (Safe).

    **The Margin Band**:
    We want a "No Man's Land" between the classes.
    *   Positive Hyperplane: $w^T x + b = +1$
    *   Negative Hyperplane: $w^T x + b = -1$
    *   **Margin Width**: The physical distance between these two lines is $\frac{2}{||w||}$.
    """)

    render_mermaid("""
    graph TD
        N1["Data Points"] --> N2["Hyperplane (w*x + b = 0)"]
        N2 --> N3["Margin Band (+1 to -1)"]
        N3 --> N4["Maximize Width (2 / ||w||)"]
    """, height=200)

    # --- 3. Constraints / Objective / Loss ---
    st.subheader("3. The Optimization Problem")
    st.markdown("We have two conflicting goals:")
    st.markdown("1.  **Maximize the Margin**: Make the road as wide as possible. (Minimize $||w||$).")
    st.markdown(r"2.  **Respect the Data**: Keep points out of the No Man's Land. ($y_i(w^T x_i + b) \ge 1$).")

    st.markdown("**The Hard Margin Primal Problem:**")
    st.latex(r"\min_{w, b} \frac{1}{2} ||w||^2 \quad \text{subject to} \quad y_i (w^T x_i + b) \ge 1")

    st.markdown(r"""
    *   **Why Minimize $||w||$?** Because Margin Width = $2/||w||$. To make the fraction big, the denominator must be small.
    *   **Why $\ge 1$?** We enforce that every point must be *at least* distance 1 away from the decision line (in score space).
    """)

    # --- 4. Deeper Components (Slack & Hinge Loss) ---
    st.subheader("4. Soft Margin & Hinge Loss")
    st.markdown(r"""
    Real data is messy. Sometimes points *must* be inside the margin (or on the wrong side).
    We introduce **Slack Variables** ($\xi_i$).

    *   $\xi_i = 0$: Point is safe.
    *   $0 < \xi_i < 1$: Point is inside the margin (unsafe but correct).
    *   $\xi_i > 1$: Point is misclassified.

    **The Hinge Loss:**
    """)
    st.latex(r"L(y, f(x)) = \max(0, 1 - y \cdot f(x))")
    st.markdown("""
    *   If Safety $> 1$: Loss is 0. (Great!)
    *   If Safety $< 1$: Loss increases linearly. (Pay a penalty).

    **The Full Objective (Primal):**
    """)
    st.latex(r"J(w, b) = \frac{1}{2} ||w||^2 + C \sum_{i=1}^N \max(0, 1 - y_i(w^T x_i + b))")
    st.markdown("*   **C**: The 'Bossiness' of the data. High C = Strict (Hard Margin). Low C = Chill (Soft Margin).")

    # --- 5. What the Solution Looks Like ---
    st.subheader("5. The Solution: Support Vectors")
    st.markdown(r"""
    The magic of SVM is that the solution depends **only** on the difficult points.

    *   **Easy Points** (Safety $> 1$): $\xi = 0$. They don't matter. You can delete them and the line won't move.
    *   **Support Vectors** (Safety $\le 1$): These are the points "holding up" the margin.

    The weight vector $w$ is a linear combination of *only* the Support Vectors:
    """)
    st.latex(r"w = \sum_{i \in SV} \alpha_i y_i x_i")
    st.markdown("This means the model is **Sparse** and efficient.")

    # --- 6. Graphs and Visuals ---
    st.subheader("6. Visualization")

    col_viz, col_controls = st.columns([3, 1])
    with col_controls:
        C_param = st.slider("C (Regularization)", 0.01, 10.0, 1.0, key="svm_c")
        kernel = st.selectbox("Kernel", ["linear", "rbf", "poly"], key="svm_kernel")
        dataset = st.selectbox("Dataset", ["Moons", "Circles", "Linear"], key="svm_data")

    with col_viz:
        if dataset == "Moons":
            X, y = generate_moons(n_samples=200, noise=0.2)
        elif dataset == "Circles":
            X, y = generate_circles(n_samples=200, noise=0.1)
        else:
            X, y = generate_linear(n_samples=200, noise=0.2)

        clf = SVC(C=C_param, kernel=kernel, probability=True)
        clf.fit(X, y)

        # Grid for decision boundary
        x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
        y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
        xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02), np.arange(y_min, y_max, 0.02))

        if hasattr(clf, "decision_function"):
            Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
        else:
            Z = clf.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]

        Z = Z.reshape(xx.shape)

        fig = go.Figure()
        # Decision Boundary
        fig.add_trace(go.Contour(x=np.arange(x_min, x_max, 0.02), y=np.arange(y_min, y_max, 0.02), z=Z,
                                 colorscale='RdBu', showscale=True,
                                 contours=dict(start=-1, end=1, size=1, coloring='lines', showlabels=True)))

        # Data Points
        fig.add_trace(go.Scatter(x=X[y==0, 0], y=X[y==0, 1], mode='markers', name='Class -1', marker=dict(color='red', symbol='circle')))
        fig.add_trace(go.Scatter(x=X[y==1, 0], y=X[y==1, 1], mode='markers', name='Class +1', marker=dict(color='blue', symbol='x')))

        # Support Vectors (Highlight)
        sv = clf.support_vectors_
        fig.add_trace(go.Scatter(x=sv[:, 0], y=sv[:, 1], mode='markers', name='Support Vectors',
                                 marker=dict(color='yellow', size=12, line=dict(width=2, color='black'))))

        fig.update_layout(title=f"SVM Decision Boundary (C={C_param}, Kernel={kernel})", height=500)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("The Yellow points are the Support Vectors. They are the only ones that matter.")

    # --- 7. Hyperparameters ---
    st.subheader("7. Hyperparameters & Behavior")
    st.markdown("""
    *   **C (Cost)**:
        *   **High C**: "I trust this data perfectly." Tries to classify every point correctly. Risk of Overfitting.
        *   **Low C**: "This data is noisy." Allows some errors to get a wider margin. Better Generalization.
    *   **Kernel**:
        *   **Linear**: Straight line. Good for simple problems.
        *   **RBF (Radial Basis Function)**: Infinite dimensions. Good for complex, curvy boundaries.
        *   **Poly**: Polynomial curves.
    """)

    # --- 8. Super Summary ---
    st.subheader("8. Super Summary 🦸")
    st.info(r"""
    *   **Goal**: Find the widest possible road (Margin) between classes.
    *   **Math**: Minimize $||w||^2$ subject to $y_i f(x_i) \ge 1$.
    *   **Key Insight**: Only the "Support Vectors" (points on the edge) define the line.
    *   **Knobs**: $C$ controls the trade-off between "Wide Road" and "No Errors".
    """)

# ==========================================
# KNN SECTION (PLATINUM STANDARD)
# ==========================================
with tab2:
    st.header("K-Nearest Neighbors (KNN): The Lazy Learner")

    # --- 1. Intuition ---
    st.subheader("1. Intuition: The Real Estate Agent")
    st.markdown(r"""
    Imagine you want to estimate the price of a house. What do you do?
    You look at the **3 nearest houses** that sold recently.
    *   House A (Next door): Sold for \$500k.
    *   House B (Across street): Sold for \$510k.
    *   House C (Down block): Sold for \$490k.

    **Prediction**: Your house is probably around \$500k.

    This is KNN.
    *   **"Tell me who your neighbors are, and I'll tell you who you are."**
    *   It assumes that similar things exist in close proximity.
    """)

    # --- 2. The Algorithm (Step-by-Step) ---
    st.subheader("2. The Algorithm: A Concrete Example")
    st.markdown("Let's classify a new tennis player **X**.")

    st.markdown("**The Database (Training Set):**")
    st.code("""
    Player A: Rank=10, Points=2000 -> WIN
    Player B: Rank=12, Points=1900 -> WIN
    Player C: Rank=50, Points=500  -> LOSE
    """, language="text")

    st.markdown("**The New Player X:** Rank=11, Points=1950.")

    st.markdown("**Step 1: Calculate Distances** (Euclidean)")
    st.latex(r"d(X, A) = \sqrt{(11-10)^2 + (1950-2000)^2} = \sqrt{1 + 2500} \approx 50.01")
    st.latex(r"d(X, B) = \sqrt{(11-12)^2 + (1950-1900)^2} = \sqrt{1 + 2500} \approx 50.01")
    st.latex(r"d(X, C) = \sqrt{(11-50)^2 + (1950-500)^2} = \sqrt{1521 + 2102500} \approx 1450")

    st.markdown("**Step 2: Find Neighbors (K=3)**")
    st.markdown("*   Neighbors = {A, B, C} (Since we only have 3).")
    st.markdown("*   Closest are A and B.")

    st.markdown("**Step 3: Vote**")
    st.markdown("*   A says WIN.")
    st.markdown("*   B says WIN.")
    st.markdown("*   C says LOSE.")
    st.markdown("**Result**: 2 vs 1. Prediction = **WIN**.")

    # --- 3. Distance Metrics ---
    st.subheader("3. Distance Metrics: How do we measure 'Close'?")
    st.markdown("The choice of ruler changes the result.")

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown("**Euclidean (L2 Norm)**")
        st.latex(r"d(x, y) = \sqrt{\sum (x_i - y_i)^2}")
        st.markdown("The straight line distance (As the crow flies). Good for physical space.")
    with col_d2:
        st.markdown("**Manhattan (L1 Norm)**")
        st.latex(r"d(x, y) = \sum |x_i - y_i|")
        st.markdown("The taxi driver distance (Grid city). Good for high dimensions.")

    # --- 4. The Curse of Dimensionality ---
    st.subheader("4. The Curse of Dimensionality 👻")
    st.markdown(r"""
    KNN fails when you have too many features (dimensions).

    *   **Intuition**: In 1D (Line), points are close. In 2D (Paper), they spread out. In 100D, the space is so vast that **all points are far away from each other**.
    *   **Consequence**: You need exponentially more data to fill the space.
    *   **Fix**: Use Dimensionality Reduction (PCA) before KNN.
    """)

    # --- 5. Weighted KNN ---
    st.subheader("5. Weighted KNN")
    st.markdown(r"""
    Should the neighbor 1km away have the same vote as the neighbor 1m away? **No.**

    **Inverse Distance Weighting:**
    """)
    st.latex(r"w_i = \frac{1}{d(x_{new}, x_i)}")
    st.markdown("Points that are closer shout louder. Points far away just whisper.")

    # --- 6. Visualization ---
    st.subheader("6. Visualization")

    col_viz_knn, col_controls_knn = st.columns([3, 1])
    with col_controls_knn:
        k_neighbors = st.slider("K (Neighbors)", 1, 20, 3, key="knn_k")
        weights = st.selectbox("Weights", ["uniform", "distance"], key="knn_weights")
        metric = st.selectbox("Metric", ["euclidean", "manhattan"], key="knn_metric")
        dataset_knn = st.selectbox("Dataset", ["Moons", "Circles"], key="knn_data")

    with col_viz_knn:
        if dataset_knn == "Moons":
            X_k, y_k = generate_moons(n_samples=200, noise=0.2)
        else:
            X_k, y_k = generate_circles(n_samples=200, noise=0.1)

        clf_k = KNeighborsClassifier(n_neighbors=k_neighbors, weights=weights, metric=metric)
        clf_k.fit(X_k, y_k)

        # Grid
        x_min_k, x_max_k = X_k[:, 0].min() - 0.5, X_k[:, 0].max() + 0.5
        y_min_k, y_max_k = X_k[:, 1].min() - 0.5, X_k[:, 1].max() + 0.5
        xx_k, yy_k = np.meshgrid(np.arange(x_min_k, x_max_k, 0.02), np.arange(y_min_k, y_max_k, 0.02))

        Z_k = clf_k.predict(np.c_[xx_k.ravel(), yy_k.ravel()])
        Z_k = Z_k.reshape(xx_k.shape)

        fig_k = go.Figure()
        fig_k.add_trace(go.Contour(x=np.arange(x_min_k, x_max_k, 0.02), y=np.arange(y_min_k, y_max_k, 0.02), z=Z_k,
                                   colorscale='RdBu', opacity=0.4, showscale=False))
        fig_k.add_trace(go.Scatter(x=X_k[y_k==0, 0], y=X_k[y_k==0, 1], mode='markers', marker=dict(color='red')))
        fig_k.add_trace(go.Scatter(x=X_k[y_k==1, 0], y=X_k[y_k==1, 1], mode='markers', marker=dict(color='blue')))

        fig_k.update_layout(title=f"KNN (K={k_neighbors}, Weights={weights})", height=500)
        st.plotly_chart(fig_k, use_container_width=True)

    # --- 8. Super Summary ---
    st.subheader("8. Super Summary 🦸")
    st.info(r"""
    *   **Goal**: Classify based on similarity.
    *   **Math**: $d(x, y) = \sqrt{\sum (x_i - y_i)^2}$.
    *   **Key Insight**: "Birds of a feather flock together."
    *   **Knobs**: $K$ (Smoothness), Weights (Distance vs Uniform), Metric (Euclidean vs Manhattan).
    """)
