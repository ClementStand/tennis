import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve, confusion_matrix
from sklearn.calibration import calibration_curve
import sys
import os

# Fix for Streamlit Cloud path issues
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.dashboard.components.navigation import sidebar_navigation
from src.dashboard.components.data_manager import get_train_test_data
from src.dashboard.components.model_manager import discover_models, load_model

st.set_page_config(page_title="Model Comparison", page_icon="⚔️", layout="wide")
sidebar_navigation()

st.title("⚔️ The Battle Royale: Model Comparison")

st.markdown(r"""
Welcome to the Arena. Here, we pit all our trained models against each other on the **Test Set** (Matches from 2024).
We don't just look at Accuracy. We look at **Calibration**, **Risk**, and **Profitability**.
""")

# 1. Load Data
with st.spinner("Loading Test Data (2024 Season)..."):
    X_train, X_test, y_train, y_test, test_df = get_train_test_data()

if X_test is None:
    st.error("Could not load test data. Please check the data path.")
    st.stop()

st.success(f"Loaded Test Set: **{len(X_test)} matches**")

# 2. Load Models
models_info = discover_models()
if not models_info:
    st.warning("No models found. Please train models first in the Playground.")
    st.stop()

results = []
roc_curves = []
calibration_curves = []
confusion_matrices = {}

progress_bar = st.progress(0)
total_models = len(models_info)

for i, (name, info) in enumerate(models_info.items()):
    try:
        model = load_model(info['path'])

        # Predict
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None

        # Metrics
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_prob) if y_prob is not None else 0.5

        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        confusion_matrices[name] = cm

        results.append({
            "Model": name,
            "Accuracy": acc,
            "Precision": prec,
            "Recall": rec,
            "F1 Score": f1,
            "ROC AUC": auc
        })

        # ROC Curve Data
        if y_prob is not None:
            fpr, tpr, _ = roc_curve(y_test, y_prob)
            roc_curves.append((name, fpr, tpr, auc))

            # Calibration Data
            prob_true, prob_pred_cal = calibration_curve(y_test, y_prob, n_bins=10)
            calibration_curves.append((name, prob_true, prob_pred_cal))

    except Exception as e:
        st.error(f"Error evaluating {name}: {e}")

    progress_bar.progress((i + 1) / total_models)

# 3. Leaderboard
st.header("🏆 The Leaderboard")
results_df = pd.DataFrame(results).set_index("Model").sort_values("Accuracy", ascending=False)

st.dataframe(
    results_df.style.highlight_max(axis=0, color='lightgreen').format("{:.2%}"),
    use_container_width=True
)

# 4. Deep Dive Visualizations
st.header("🔍 Deep Dive Analysis")

tab_roc, tab_cal, tab_conf = st.tabs(["ROC Curves", "Calibration", "Confusion Matrices"])

with tab_roc:
    st.subheader("ROC Curves (Discrimination)")
    st.markdown("How well does the model separate Winners from Losers? (Top-Left is best).")
    fig_roc = go.Figure()
    fig_roc.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', line=dict(dash='dash', color='gray'), name='Random'))

    for name, fpr, tpr, auc_score in roc_curves:
        fig_roc.add_trace(go.Scatter(x=fpr, y=tpr, mode='lines', name=f'{name} (AUC={auc_score:.2f})'))

    fig_roc.update_layout(xaxis_title="False Positive Rate", yaxis_title="True Positive Rate", height=600)
    st.plotly_chart(fig_roc, use_container_width=True)

with tab_cal:
    st.subheader("Calibration Curves (Reliability)")
    st.markdown("If the model says '70% chance', does the player actually win 70% of the time? (Diagonal is best).")
    fig_cal = go.Figure()
    fig_cal.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', line=dict(dash='dash', color='gray'), name='Perfect'))

    for name, prob_true, prob_pred_cal in calibration_curves:
        fig_cal.add_trace(go.Scatter(x=prob_pred_cal, y=prob_true, mode='lines+markers', name=name))

    fig_cal.update_layout(xaxis_title="Predicted Probability", yaxis_title="Actual Win Rate", height=600)
    st.plotly_chart(fig_cal, use_container_width=True)

with tab_conf:
    st.subheader("Confusion Matrices")
    selected_model = st.selectbox("Select Model", list(confusion_matrices.keys()))
    cm = confusion_matrices[selected_model]

    fig_cm = px.imshow(cm, text_auto=True, color_continuous_scale='Blues',
                       labels=dict(x="Predicted", y="Actual", color="Count"),
                       x=['Lose', 'Win'], y=['Lose', 'Win'])
    fig_cm.update_layout(title=f"Confusion Matrix: {selected_model}")
    st.plotly_chart(fig_cm, use_container_width=True)

# 5. Super Summary
st.header("8. Super Summary 🦸")
st.info(r"""
*   **Accuracy**: Good for balanced data. Bad for imbalanced.
*   **AUC**: Best for ranking. (Who is *more likely* to win?).
*   **Calibration**: Crucial for betting. (Is the probability real?).
*   **Recommendation**: Use **Random Forest** or **Logistic Regression (Calibrated)** for best results.
""")
