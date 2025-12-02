import streamlit as st
from src.dashboard.components.navigation import sidebar_navigation
from src.dashboard.components.mermaid import render_mermaid

st.set_page_config(page_title="Git Collaboration", page_icon="🤝", layout="wide")
sidebar_navigation()

st.title("🤝 Git Collaboration: Branches & Merging")
st.markdown("### Parallel Universes")

st.markdown("""
The real power of Git is not just saving history, but **Branching**.
Branching allows multiple people to work on the same project at the same time without interfering with each other.
""")

# --- 1. TL;DR ---
st.info("""
**🚀 Big Picture (TL;DR)**

*   **Branch**: A parallel version of the project. You create a branch to work on a new feature safely.
*   **Merge**: Combining two branches back together.
*   **Merge Conflict**: When two people change the *exact same line* of a file. Git asks you to choose the winner.
*   **Remote (Origin)**: The version of the repo on GitHub.
*   **Pull Request (PR)**: A formal request to merge your branch into the main codebase. It allows for code review.
""")

st.markdown("---")

# --- 2. Intuition ---
st.header("1. Intuition: The Multiverse 🌌")

st.markdown("""
Imagine you are writing a book.

*   **Main Universe (`main`)**: The published version of the book. It must always be perfect.
*   **Feature Universe (`feature-chapter-2`)**: You clone the universe and start writing Chapter 2.
    *   In this universe, Chapter 2 exists.
    *   In the Main Universe, it does not.
    *   You can make mistakes here. It doesn't affect the Main Universe.
*   **The Merge**: When you are done, you smash the two universes back together. Now the Main Universe has Chapter 2.
""")

st.markdown("---")

# --- 3. Architecture Diagram ---
st.header("2. The Graph: Diverging & Converging")
st.markdown("Visualizing how history splits and rejoins.")

render_mermaid("""
graph RL
    subgraph Feature_Branch ["Branch: feature-login"]
        C4["Commit C4 <br> (Write Login)"] --> C3["Commit C3 <br> (Create File)"]
    end

    subgraph Main_Branch ["Branch: main"]
        C5["Commit C5 <br> (Fix Typo)"] --> C2
    end

    C3 --> C2["Commit C2 <br> (Base)"]
    C2 --> C1["Commit C1"]

    Merge["Merge Commit C6 <br> (Combine C4 + C5)"] --> C4
    Merge --> C5

    style Merge fill:#ffecb3,stroke:#ff6f00,stroke-width:2px
""", height=400)

st.markdown("""
**How to read this:**
1.  **Divergence**: We started `feature-login` at C2. We made C3 and C4.
2.  **Parallel Work**: Meanwhile, someone else added C5 to `main`.
3.  **Convergence (Merge)**: We create **C6**.
    *   C6 is special. It has **Two Parents** (C4 and C5).
    *   It contains the sum of changes from both sides.
""")

st.markdown("---")

# --- 4. Merge Conflicts ---
st.header("3. Merge Conflicts: When Universes Collide 💥")

st.markdown("""
Git is smart. If Alice changes `file A` and Bob changes `file B`, Git merges them automatically.
**But what if you both edit Line 10 of `file A`?**

Git panics. It doesn't know whose version is correct. It stops and asks **YOU** to decide.
""")

st.code("""
<<<<<<< HEAD (Current Change)
The sky is blue.
=======
The sky is green.
>>>>>>> feature-branch (Incoming Change)
""", language="text")

st.markdown("""
**How to Fix:**
1.  Open the file in your editor (VS Code).
2.  Delete the markers (`<<<<`, `====`, `>>>>`).
3.  Pick the correct line (or rewrite it to say "The sky is teal").
4.  Save the file.
5.  `git add file_A`.
6.  `git commit`. This finishes the merge.
""")

st.markdown("---")

# --- 5. The Workflow (GitHub) ---
st.header("4. The Workflow: Pull Requests")
st.markdown("In a professional team, we rarely merge directly on our laptops. We use **GitHub**.")

st.markdown("""
1.  **Branch**: Create `feature-login` locally.
2.  **Commit**: Make your changes.
3.  **Push**: Send your branch to GitHub (`git push origin feature-login`).
4.  **Pull Request (PR)**: Go to GitHub.com. Click "Create Pull Request".
    *   This asks the team: "Can I merge `feature-login` into `main`?"
5.  **Review**: Teammates read your code, leave comments ("Fix this variable name").
6.  **Merge**: Once approved, click the big green "Merge" button on GitHub.
7.  **Pull**: Back on your laptop, run `git pull` to update your local `main`.
""")

st.markdown("---")

# --- 6. Practical Commands ---
st.header("5. Practical Commands")

st.markdown("""
*   `git branch feature-x`: Create a new branch.
*   `git checkout feature-x`: Switch to that branch.
*   `git checkout -b feature-x`: Create AND Switch (Shortcut).
*   `git merge feature-x`: Merge feature-x into your *current* branch.
*   `git push origin feature-x`: Upload branch to GitHub.
*   `git pull origin main`: Download latest changes from GitHub's main branch.
*   `git fetch`: Download changes but don't merge them yet (Safe mode).
""")

st.markdown("---")

# --- 7. FAQ & Exercises ---
st.header("6. FAQ & Exercises")

with st.expander("Q: What is 'Detached HEAD'?"):
    st.markdown("""
    It sounds scary, but it just means "You are looking at a specific commit, not a branch."
    If you make commits here, they belong to no branch. If you switch away, they are lost.
    **Fix**: `git checkout -b new-branch-name` to save your state to a branch.
    """)

st.info("""
**🧠 Try it yourself:**
1.  `git checkout -b test-branch`.
2.  Change a file. Commit.
3.  `git checkout main`.
4.  Look at the file. Your change is gone! (It's safe in the other universe).
5.  `git merge test-branch`.
6.  Look at the file. The change is back!
""")

st.success("You have completed the Software Development Syllabus! 🎓")
st.page_link("app.py", label="Back to Home", icon="🏠")
