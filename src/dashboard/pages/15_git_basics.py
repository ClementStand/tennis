import streamlit as st
from src.dashboard.components.navigation import sidebar_navigation
from src.dashboard.components.mermaid import render_mermaid

st.set_page_config(page_title="Git Basics", page_icon="🌿", layout="wide")
sidebar_navigation()

st.title("🌿 Git Basics: The Time Machine")

st.markdown("""
> **"Final_Final_v2_REAL.docx"**
> We have all been there. Git solves the problem of "Saving Versions" forever.
""")

# --- SECTION 1: THE CONCEPT ---
st.header("1. The Concept: Snapshots 📸")
st.markdown("""
Git is not a "Save" button. It is a **Camera**.
*   **Save**: Overwrites the file. You lose the old version.
*   **Git Commit**: Takes a photo of the *entire project* at that moment. You can always go back to that photo.
""")

render_mermaid("""
graph LR
    V1["Commit 1: <br> Initial Code"] --> V2["Commit 2: <br> Added Login"]
    V2 --> V3["Commit 3: <br> Fixed Bug"]

    style V1 fill:#e0f7fa
    style V2 fill:#e0f7fa
    style V3 fill:#b2ebf2
""", height=200)

st.markdown("---")

# --- SECTION 2: THE THREE AREAS ---
st.header("2. The Three Areas 🗺️")
st.markdown("To understand Git, you must know where your files live.")

col1, col2, col3 = st.columns(3)
with col1:
    st.error("**1. Working Directory**")
    st.markdown("Your actual folder. Where you edit code. This is the **Present**.")
with col2:
    st.warning("**2. Staging Area**")
    st.markdown("The 'On Deck' circle. You pick which files you want to include in the next photo.")
with col3:
    st.success("**3. Repository (.git)**")
    st.markdown("The Photo Album. Where the snapshots are stored forever. This is **History**.")

render_mermaid("""
graph LR
    WD["Working Directory"] -->|git add| Stage["Staging Area"]
    Stage -->|git commit| Repo["Repository (.git)"]
    Repo -->|git checkout| WD
""", height=250)

st.markdown("---")

# --- SECTION 3: THE ANATOMY OF A COMMIT ---
st.header("3. The Anatomy of a Commit 🧬")
st.markdown("A Commit is not just a copy of files. It contains metadata.")
st.markdown("""
*   **Unique ID (SHA-1)**: A random string like `a1b2c3d`. This is the commit's name.
*   **Author**: Who did it?
*   **Message**: Why did they do it?
*   **Parent**: What happened before this? (This links commits together into a chain).
*   **Snapshot**: The state of all files.
""")

st.markdown("---")

# --- SECTION 4: BASIC WORKFLOW ---
st.header("4. The Workflow: Add, Commit, Push 🔄")

st.code("""
# 1. Initialize (Start a new album)
git init

# 2. Add files (Prepare the photo)
git add app.py
git add style.css

# 3. Commit (Take the photo)
git commit -m "Created the login page"

# 4. Push (Upload the album to the cloud/GitHub)
git push origin main
""", language="bash")

st.markdown("---")

# --- SECTION 5: EXERCISES ---
st.header("5. Exercises 📝")
st.info("""
1.  **Init**: Create a folder. Run `git init`. See the hidden `.git` folder? That's the brain.
2.  **Status**: Run `git status`. It tells you what is in the Working Directory vs Staging.
3.  **Log**: Run `git log`. See the history of your time travel.
""")
