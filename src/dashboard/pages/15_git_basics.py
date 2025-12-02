import streamlit as st
from src.dashboard.components.navigation import sidebar_navigation
from src.dashboard.components.mermaid import render_mermaid

st.set_page_config(page_title="Git Basics", page_icon="🌿", layout="wide")
sidebar_navigation()

st.title("🌿 Git Basics: The Time Machine")
st.markdown("### The Save Button for History")

st.markdown("""
Git is the most important tool for a developer.
It is not just a backup. It is a **Time Machine** and a **Parallel Universe Generator**.
It allows you to save snapshots of your project, travel back to them, and work on multiple versions simultaneously.
""")

# --- 1. TL;DR ---
st.info("""
**🚀 Big Picture (TL;DR)**

*   **Repository (Repo)**: The database where Git stores your project history (the `.git` folder).
*   **Commit**: A permanent, immutable snapshot of the ENTIRE project at a specific moment.
*   **Hash (SHA-1)**: The unique ID of a commit (e.g., `a1b2c3d`). It is calculated based on the content.
*   **Branch**: A movable sticky note that points to a specific commit.
*   **HEAD**: A pointer to "Where you are right now". Usually points to the current Branch.
*   **Staging Area**: The "Loading Dock". You pick which files go into the next commit here.
""")

st.markdown("---")

# --- 2. Intuition ---
st.header("1. Intuition: The Photographer 📸")

st.markdown("""
Imagine you are building a Lego Castle.

1.  **Working Directory**: The table. You are adding bricks, moving things around. It's messy.
2.  **Staging Area (Index)**: You set up a specific scene. You say "I want to take a picture of *just* the tower, not the messy pile of bricks next to it."
3.  **Commit**: You take the photo.
    *   You print it out.
    *   You write the date and a message ("Added the North Tower") on the back.
    *   You put it in a photo album.
    *   **Crucial**: You can NEVER change this photo. If you want to change the tower, you must build a new version and take a *new* photo.

**Git is NOT a "Save" button.**
*   "Save" overwrites the file.
*   "Commit" saves a *new version* and keeps the old one forever.
""")

st.markdown("---")

# --- 3. Technical Mechanics ---
st.header("2. Technical Mechanics: The Graph (DAG)")

st.subheader("A. The Chain of History")
st.markdown("""
Git stores history as a **Directed Acyclic Graph (DAG)**.
Every commit points to its **Parent** (the commit before it).
""")

render_mermaid("""
graph RL
    C3["Commit C3 <br> (Add CSS)"] --> C2["Commit C2 <br> (Add HTML)"]
    C2 --> C1["Commit C1 <br> (Initial)"]

    style C3 fill:#f9f,stroke:#333,stroke-width:4px

    Main["Branch: main"] --> C3
    HEAD["HEAD"] --> Main
""", height=300)

st.markdown("""
**How to read this:**
1.  **C1** was the first commit.
2.  **C2** came after C1. C2 knows C1 is its parent.
3.  **C3** came after C2.
4.  **main** is just a label pointing to C3.
5.  **HEAD** says "We are currently looking at `main`".

**If we commit again:**
Git creates **C4**. It points C4 to C3. Then it moves the `main` label to C4.
""")

st.subheader("B. The Three States")
st.markdown("Files move through three zones.")

render_mermaid("""
graph LR
    Working["Working Directory <br> (Your Files)"] -->|git add| Staging["Staging Area <br> (The Index)"]
    Staging -->|git commit| Repo["Local Repository <br> (.git folder)"]
    Repo -->|git push| Remote["Remote <br> (GitHub)"]
""", height=300)

st.markdown("---")

# --- 4. What Actually Happens When... ---
st.header("3. What Actually Happens When... 🕵️‍♂️")
st.markdown('Command: `git commit -m "Fix bug"`')

st.markdown("""
1.  **Hash Content**: Git calculates the SHA-1 hash of every file in the Staging Area.
2.  **Create Blobs**: It compresses the file contents and stores them as "Blob Objects" in the `.git/objects` folder.
3.  **Create Tree**: It creates a "Tree Object" (like a folder listing) that maps filenames to Blob hashes.
4.  **Create Commit**: It creates a "Commit Object". This text file contains:
    *   The Hash of the Tree (the snapshot).
    *   The Hash of the Parent Commit (history).
    *   Author (You), Date, and Message.
5.  **Update Branch**: Git updates the file `.git/refs/heads/main` to contain the new Commit Hash.
6.  **Update HEAD**: HEAD is still pointing to `main`, so it effectively moves forward.
""")

st.markdown("---")

# --- 5. Practical Commands ---
st.header("4. Practical Commands")

st.markdown("""
*   `git init`: Turn the current folder into a Repository (creates `.git`).
*   `git status`: **The most important command.** Tells you what is Modified, Staged, or Untracked.
*   `git add .`: Move all modified files to Staging.
*   `git commit -m "msg"`: Create a snapshot from Staging.
*   `git log --oneline --graph`: Show the history graph in text format.
*   `git checkout <hash>`: Time travel. Move HEAD to a specific commit to see how the project looked back then.
""")

st.markdown("---")

# --- 6. FAQ & Exercises ---
st.header("5. FAQ & Exercises")

with st.expander("Q: Does Git store the whole file or just the changes (diffs)?"):
    st.markdown("""
    **Myth**: Git stores diffs.
    **Fact**: Git stores **Snapshots**.
    If you change one line in a 1000-line file, Git stores a new copy of the *entire* file (compressed).
    It is smart about deduplication, but conceptually, it's a full snapshot.
    """)

st.info("""
**🧠 Try it yourself:**
1.  Run `git init` in a new folder.
2.  Create `hello.txt`.
3.  Run `git status`. See it is "Untracked".
4.  Run `git add hello.txt`. Run `git status`. See it is "Staged".
5.  Run `git commit -m "First"`. Run `git status`. Clean!
""")

st.success("Next: How do we work with other people? Branches and Merging.")
st.page_link("pages/16_git_collaboration.py", label="Go to Git Collaboration", icon="🤝")
