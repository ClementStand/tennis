import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.metrics import confusion_matrix, roc_curve, auc
from src.dashboard.components.navigation import sidebar_navigation

st.set_page_config(page_title="Validation & Metrics", page_icon="✅", layout="wide")
sidebar_navigation()

st.title("✅ Validation & Metrics: Keeping it Real")

# --- LAYER 1: Intuition ---
st.header("1. Intuition: The Exam 📝")
st.markdown("""
Training a model is like studying.
*   **Training Set**: The textbook questions. (You can memorize these).
*   **Test Set**: The final exam questions. (You've never seen these).
*   **Accuracy**: Getting 90% right.
*   **Precision/Recall**: What if the exam is 99% "True" and 1% "False"? Guessing "True" gets you 99% accuracy but you learned nothing. We need better metrics.
""")
st.markdown("---")

# --- LAYER 3: Structure ---
st.header("3. Structure: The Confusion Matrix 🔲")
st.markdown("Every prediction falls into one of 4 buckets:")
col1, col2 = st.columns(2)
with col1:
    st.success("**True Positive (TP)**: Predicted Win, Actually Win.")
    st.error("**False Positive (FP)**: Predicted Win, Actually Lose. (Type I Error).")
with col2:
    st.error("**False Negative (FN)**: Predicted Lose, Actually Win. (Type II Error).")
    st.success("**True Negative (TN)**: Predicted Lose, Actually Lose.")
st.markdown("---")

# --- LAYER 5: Full Math ---
st.header("5. The Math: Precision, Recall, F1 🧮")

st.subheader("A. Precision (Quality)")
st.markdown("Of all the matches I *said* were Wins, how many were actually Wins?")
st.latex(r"Precision = \frac{TP}{TP + FP}")

st.subheader("B. Recall (Quantity)")
st.markdown("Of all the *actual* Wins, how many did I find?")
st.latex(r"Recall = \frac{TP}{TP + FN}")

st.subheader("C. F1 Score (Harmonic Mean)")
st.markdown("Why not just average P and R? Because if P=0.01 and R=1.0, the average is 0.5 (misleading).")
st.markdown("The **Harmonic Mean** punishes extreme values.")
st.latex(r"F1 = 2 \cdot \frac{P \cdot R}{P + R}")

st.subheader("D. ROC & AUC")
st.markdown("ROC plots **True Positive Rate** vs **False Positive Rate** at *every possible threshold*.")
st.markdown("**AUC (Area Under Curve)**: The probability that the model ranks a random Positive example higher than a random Negative example.")
st.markdown("---")

# --- Interactive Viz ---
st.header("10. Interactive Playground")

# Generate synthetic data
y_true = np.random.randint(0, 2, 100)
y_scores = np.random.rand(100)
# Add some signal
y_scores = y_scores + (y_true * 0.5)
y_scores = y_scores / y_scores.max()

threshold = st.slider("Decision Threshold", 0.0, 1.0, 0.5)
y_pred = (y_scores >= threshold).astype(int)

cm = confusion_matrix(y_true, y_pred)

col1, col2 = st.columns(2)
with col1:
    st.markdown("### Confusion Matrix")
    fig_cm = go.Figure(data=go.Heatmap(
        z=cm, x=['Pred 0', 'Pred 1'], y=['Actual 0', 'Actual 1'],
        text=cm, texttemplate="%{text}", colorscale='Blues'
    ))
    st.plotly_chart(fig_cm, use_container_width=True)

with col2:
    st.markdown("### ROC Curve")
    fpr, tpr, _ = roc_curve(y_true, y_scores)
    roc_auc = auc(fpr, tpr)

    fig_roc = go.Figure()
    fig_roc.add_trace(go.Scatter(x=fpr, y=tpr, name=f'AUC = {roc_auc:.2f}'))
    fig_roc.add_trace(go.Scatter(x=[0, 1], y=[0, 1], line=dict(dash='dash'), name='Random'))
    fig_roc.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='markers', marker=dict(color='red', size=10), name='Current Threshold')) # Placeholder for point
    st.plotly_chart(fig_roc, use_container_width=True)

st.page_link("pages/02_model_playground.py", label="🎮 Go to Playground", icon="🎮")
