import streamlit as st
from src.dashboard.components.navigation import sidebar_navigation
from src.dashboard.components.mermaid import render_mermaid

st.set_page_config(page_title="Git Basics", page_icon="🌿", layout="wide")
sidebar_navigation()

st.title("🌿 Git Basics: The Time Machine")

# --- LAYER 1: Intuition ---
st.header("1. Intuition: The Photographer 📸")
st.markdown("""
Building software is like building a Lego Castle.
*   **Working Directory**: The messy table.
*   **Staging Area**: You arrange a specific scene. "I want to take a photo of just the tower."
*   **Commit**: You take the photo.
    *   You write the date on the back.
    *   You put it in an album.
    *   **You can never change the photo**. It is history.
""")
st.markdown("---")

# --- LAYER 3: Structure ---
st.header("3. Structure: The DAG (Directed Acyclic Graph) 🕸️")
render_mermaid("""
graph RL
    C3["Commit 3 <br> (Add CSS)"] --> C2["Commit 2 <br> (Add HTML)"]
    C2 --> C1["Commit 1 <br> (Init)"]

    Main["Branch: main"] --> C3
    HEAD["HEAD (You are here)"] --> Main
""", height=300)

st.markdown("""
*   **Commit**: A snapshot. It points to its **Parent**.
*   **Branch**: A sticky note pointing to a specific commit.
*   **HEAD**: A pointer to "Where I am right now". Usually points to the Branch.
""")
st.markdown("---")

# --- LAYER 4: Step-by-Step ---
st.header("4. Step-by-Step: `git commit` 👣")
st.markdown("""
1.  **Hash**: Calculate SHA-1 hash of every file in Staging.
2.  **Blob**: Store file contents in `.git/objects`.
3.  **Tree**: Create a list of files and their hashes.
4.  **Commit Object**: Create a text file with:
    *   Tree Hash.
    *   Parent Hash.
    *   Message.
5.  **Update Branch**: Move the `main` sticky note to the new Commit.
""")
st.markdown("---")

# --- LAYER 9: Exercises ---
st.header("9. Exercises 📝")
st.info("""
1.  **Init**: `git init`.
2.  **Create**: `touch test.txt`.
3.  **Stage**: `git add test.txt`.
4.  **Commit**: `git commit -m "First"`.
5.  **Log**: `git log`. See your hash!
""")
