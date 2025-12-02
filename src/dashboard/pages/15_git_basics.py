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

# --- SECTION 1: OVERVIEW ---
st.header("1. Git Overview 🌍")
st.markdown("""
**What is Git?**
It is a **Distributed Version Control System (DVCS)**.
*   **Distributed**: Every user has a **complete copy** of the history on their laptop. You can work offline.
*   **Version Control**: It tracks changes over time.
*   **Snapshots**: Unlike other systems that save "deltas" (changes), Git takes a **Snapshot** of the entire project at every commit.

**Why use it?**
*   **Continuous Improvement**: Track every step of your project.
*   **Safety**: If you break something, you can "Undo" to a previous snapshot.
""")

# --- SECTION 2: INSTALLATION & CONFIG ---
st.header("2. Installation & Configuration ⚙️")
st.markdown("Before you start, you must tell Git who you are. This information is stamped onto every commit you make.")

st.code("""
# 1. Check if installed
git --version

# 2. Set your identity (Global = for all projects)
git config --global user.name "Your Name"
git config --global user.email "your.email@esade.edu"

# 3. Check settings
git config --list
""", language="bash")

# --- SECTION 3: THE FOUR AREAS ---
st.header("3. The Four Areas 🗺️")
st.markdown("Files move through four zones in Git:")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.error("**1. Working Directory**")
    st.markdown("Your actual folder. Where you edit code. (The Present).")
with col2:
    st.warning("**2. Staging Area**")
    st.markdown("The 'On Deck' circle. Files you `add` to be committed.")
with col3:
    st.success("**3. Local Repository**")
    st.markdown("Your `.git` folder. Where `commit` saves snapshots.")
with col4:
    st.info("**4. Remote Repository**")
    st.markdown("The Cloud (GitHub). Where you `push` to share.")

render_mermaid("""
graph LR
    WD["Working Dir"] -->|git add| Stage["Staging Area"]
    Stage -->|git commit| Local["Local Repo"]
    Local -->|git push| Remote["Remote (GitHub)"]
    Remote -->|git pull| WD
""", height=250)

# --- SECTION 4: BASIC COMMANDS ---
st.header("4. Basic Commands 🛠️")

tab_init, tab_status, tab_ignore = st.tabs(["Init & Clone", "Status & Add", ".gitignore"])

with tab_init:
    st.subheader("Starting a Project")
    st.markdown("""
    *   **`git init`**: Turns the current folder into a Git repository (creates hidden `.git` folder).
    *   **`git clone <url>`**: Downloads an existing repository from GitHub.
    """)
    st.code("git init", language="bash")

with tab_status:
    st.subheader("Checking State")
    st.markdown("""
    *   **`git status`**: The most important command. Tells you what is untracked, modified, or staged.
    *   **`git add <file>`**: Moves a file to Staging.
    *   **`git add .`**: Moves **ALL** changed files to Staging.
    *   **`git commit -m "message"`**: Saves the snapshot.
    """)
    st.code("""
# Check what's going on
git status

# Add a specific file
git add app.py

# Commit
git commit -m "Added login feature"
    """, language="bash")

with tab_ignore:
    st.subheader("Ignoring Files (.gitignore) 🙈")
    st.markdown("""
    Some files should **NEVER** be committed (Passwords, huge data files, temporary files).
    We list them in a special file called `.gitignore`.
    """)
    st.code("""
# .gitignore example

# Ignore all .txt files
*.txt

# Ignore the temp folder
temp/

# Ignore secrets
.env
    """, language="text")

# --- SECTION 5: REMOTE REPOSITORIES ---
st.header("5. Remote Repositories (GitHub) ☁️")
st.markdown("""
To share your code, you need a **Remote**.
*   **`origin`**: The default nickname for your remote repository.
""")

st.code("""
# 1. Link your local repo to GitHub
git remote add origin https://github.com/username/repo.git

# 2. Verify
git remote -v

# 3. Push your commits
git push -u origin main
""", language="bash")

# --- SECTION 6: EXERCISES ---
st.header("6. Exercises 📝")
st.info("""
1.  **Config**: Set your `user.name` and `user.email`.
2.  **Init**: Create a folder `lab1`, go inside, and run `git init`.
3.  **Ignore**: Create a file `secret.txt`. Create `.gitignore` and add `*.txt`. Run `git status`. Is it ignored?
4.  **Commit**: Create `hello.py`. `git add .`. `git commit -m "First commit"`.
5.  **Log**: Run `git log` to see your handiwork.
""")
