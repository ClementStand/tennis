import streamlit as st
from src.dashboard.components.navigation import sidebar_navigation
from src.dashboard.components.mermaid import render_mermaid

st.set_page_config(page_title="Git Collaboration", page_icon="🤝", layout="wide")
sidebar_navigation()

st.title("🤝 Git Collaboration: The Multiverse")

st.markdown("""
> **"Don't touch my code!"**
> How do 100 people work on the same project without overwriting each other?
> The answer is **Branching**.
""")

# --- SECTION 1: BRANCHING ---
st.header("1. The Multiverse: Branches 🌌")
st.markdown("""
**Objective**: Simultaneous stability and development.
*   **Main Branch**: The "Production" version. Always stable.
*   **Feature Branch**: An independent line of development. You can break things here safely.
""")

render_mermaid("""
graph LR
    M1((Main 1)) --> M2((Main 2))
    M2 --> M3((Main 3))

    M2 --> F1((Feature 1))
    F1 --> F2((Feature 2))

    style M1 fill:#e0f7fa
    style M2 fill:#e0f7fa
    style M3 fill:#e0f7fa
    style F1 fill:#fff9c4
    style F2 fill:#fff9c4
""", height=300)

st.code("""
# Create a new branch and switch to it
git checkout -b new-feature

# Switch back to main
git checkout main

# Delete a branch (Safe)
git branch -d feature-branch

# Force Delete (Dangerous - if not merged)
git branch -D feature-branch
""", language="bash")

# --- SECTION 2: MERGING STRATEGIES ---
st.header("2. Merging Strategies 🔀")
st.markdown("How do we bring the history back together?")

tab_ff, tab_merge, tab_rebase = st.tabs(["Fast-Forward", "Merge Commit", "Rebase"])

with tab_ff:
    st.subheader("Fast-Forward (FF)")
    st.markdown("""
    *   **Condition**: Main has NOT moved since you branched off.
    *   **Action**: Git just moves the `main` pointer forward.
    *   **Result**: Linear history. No "Merge Bubble".
    """)

with tab_merge:
    st.subheader("Merge Commit (--no-ff)")
    st.markdown("""
    *   **Condition**: Main HAS moved (diverged).
    *   **Action**: Git creates a new "Merge Commit" with two parents.
    *   **Result**: Preserves the history of the branch.
    """)
    render_mermaid("""
    graph LR
        M1 --> M2
        M2 --> M3
        M2 --> F1
        F1 --> F2
        F2 --> Merge
        M3 --> Merge
    """, height=200)

with tab_rebase:
    st.subheader("Rebase (Advanced)")
    st.markdown("""
    *   **Action**: Pick up your commits and move them to the tip of Main.
    *   **Result**: Perfectly linear history.
    *   **Warning**: Do NOT rebase shared branches!
    """)

# --- SECTION 3: FETCH vs PULL ---
st.header("3. Fetch vs Pull 📥")
st.markdown("How do we get updates from the Cloud?")

col1, col2 = st.columns(2)
with col1:
    st.info("**git fetch**")
    st.markdown("Downloads the data but **DOES NOT** touch your code.")
    st.markdown("Safe. Lets you inspect changes before merging.")
with col2:
    st.warning("**git pull**")
    st.markdown("`git fetch` + `git merge`.")
    st.markdown("Downloads AND tries to merge immediately.")
    st.markdown("Convenient, but can cause surprise conflicts.")

# --- SECTION 4: CONFLICTS ---
st.header("4. Conflicts ⚔️")
st.markdown("""
When two people edit the *same line* of the *same file*.
""")
st.code("""
<<<<<<< HEAD
print("Goodbye")
=======
print("Hello")
>>>>>>> feature-branch
""", language="python")
st.markdown("Delete the markers, choose the winner, and commit.")

# --- SECTION 5: PULL REQUESTS & FORKING ---
st.header("5. Pull Requests & Forking 🍴")

st.subheader("Single Repo PR")
st.markdown("You and your team share one repo. You make branches and PRs.")

st.subheader("Multi-Repo PR (Forking)")
st.markdown("""
You want to contribute to **Open Source** (e.g., Scikit-Learn). You don't have permission to push there.
1.  **Fork**: Copy their repo to YOUR GitHub account.
2.  **Clone**: Download your fork.
3.  **Branch & Commit**: Do your work.
4.  **Push**: Push to YOUR fork.
5.  **PR**: Ask the original owner to pull from your fork.
""")

# --- SECTION 6: EXERCISES ---
st.header("6. Exercises 📝")
st.info("""
1.  **Branch**: Create `experiment`. Make a commit.
2.  **FF Merge**: Go to `main`. Merge `experiment`. (Should be Fast-Forward).
3.  **Conflict**: Create `conflict-branch`. Change Line 1. Go to `main`. Change Line 1. Merge. Fix it.
4.  **Fetch**: Run `git fetch`. Run `git status`.
""")
