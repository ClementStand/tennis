import streamlit as st
from src.dashboard.components.navigation import sidebar_navigation
from src.dashboard.components.mermaid import render_mermaid

st.set_page_config(page_title="Git Collaboration", page_icon="🤝", layout="wide")
sidebar_navigation()

st.title("🤝 Git Collaboration: The Multiverse")

# --- LAYER 1: Intuition ---
st.header("1. Intuition: Parallel Universes 🌌")
st.markdown("""
*   **Branching**: Splitting the timeline.
    *   Universe A: You fix a bug.
    *   Universe B: Your friend adds a feature.
    *   They exist at the same time.
*   **Merging**: Colliding the universes back together.
    *   If you changed different things, it works.
    *   If you changed the *same line*, the universe breaks (**Conflict**). You must manually fix it.
""")
st.markdown("---")

# --- LAYER 3: Structure ---
st.header("3. Structure: The Merge 🔀")
render_mermaid("""
graph RL
    C3["Feature Commit"] --> C1["Base Commit"]
    C2["Bugfix Commit"] --> C1

    Merge["Merge Commit"] --> C3
    Merge --> C2

    Main["main"] --> Merge
""", height=300)

st.markdown("""
*   **Divergence**: History splits at C1.
*   **Convergence**: History rejoins at the Merge Commit.
*   **Merge Commit**: A special commit with **Two Parents**.
""")
st.markdown("---")

# --- LAYER 4: Step-by-Step ---
st.header("4. Step-by-Step: Resolving a Conflict ⚔️")
st.markdown("""
1.  **Pull**: You try to pull changes. Git stops. "CONFLICT".
2.  **Open File**: You see:
    ```
    <<<<<<< HEAD
    My Code
    =======
    Their Code
    >>>>>>> branch-name
    ```
3.  **Decide**: You delete the markers and choose the correct code.
4.  **Add**: `git add file.py`.
5.  **Commit**: `git commit`. This creates the Merge Commit.
""")
st.markdown("---")

# --- LAYER 9: Exercises ---
st.header("9. Exercises 📝")
st.info("""
1.  **Branch**: `git checkout -b feature`.
2.  **Change**: Edit a file. Commit.
3.  **Switch**: `git checkout main`.
4.  **Merge**: `git merge feature`.
""")
