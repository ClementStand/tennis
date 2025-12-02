import streamlit as st
from src.dashboard.components.navigation import sidebar_navigation
from src.dashboard.components.mermaid import render_mermaid

st.set_page_config(page_title="Git Advanced", page_icon="🧠", layout="wide")
sidebar_navigation()

st.title("🧠 Git Advanced: Under the Hood")

st.markdown("""
> **"I deleted everything by mistake!"**
> Don't panic. Git is a time machine.
> To master Git, you must understand its **Data Structure**.
""")

# --- SECTION 1: THE GRAPH MODEL (DAG) ---
st.header("1. The Graph Model (DAG) 🕸️")
st.markdown("""
Git is not just a list of files. It is a **Directed Acyclic Graph (DAG)**.
*   **Nodes**: Commits.
*   **Edges**: Arrows pointing to the **Parent** (Previous commit).
*   **Acyclic**: Time only moves forward (no loops).
""")

render_mermaid("""
graph RL
    C3["Commit C <br> (Child)"] --> C2["Commit B <br> (Parent)"]
    C2 --> C1["Commit A <br> (Grandparent)"]

    style C3 fill:#e1bee7
    style C2 fill:#ce93d8
    style C1 fill:#ba68c8
""", height=200)

# --- SECTION 2: REFERENCES (REFS) ---
st.header("2. References (Refs) 🏷️")
st.markdown("""
Commits have ugly names like `a1b2c3d`. Humans need names.
A **Ref** is just a sticky note pointing to a Commit Hash.
""")

col1, col2, col3 = st.columns(3)
with col1:
    st.info("**HEAD**")
    st.markdown("Pointer to **Where you are right now**.")
    st.markdown("Usually points to the current Branch.")
with col2:
    st.success("**Branch**")
    st.markdown("Pointer to the **Latest Commit** in a line of work.")
    st.markdown("Moves forward automatically when you commit.")
with col3:
    st.warning("**Tag**")
    st.markdown("Pointer to a **Specific Commit** (e.g., v1.0).")
    st.markdown("Does NOT move. It's permanent.")

st.subheader("Tags: Lightweight vs Annotated")
st.code("""
# Lightweight (Just a bookmark)
git tag v1.0

# Annotated (Has author, date, message - Like a commit)
git tag -a v1.0 -m "Release version 1.0"

# Push tags to remote
git push origin --tags
""", language="bash")

# --- SECTION 3: UNDOING THINGS ---
st.header("3. Undoing Things (The Panic Button) ↩️")
st.error("⚠️ WARNING: Never rewrite history that has been pushed to a shared repo!")

tab_amend, tab_revert, tab_reset = st.tabs(["Amend", "Revert", "Reset"])

with tab_amend:
    st.subheader("Amend: Fix the Last Commit")
    st.markdown("Did you forget to add a file? Or make a typo in the message?")
    st.code("""
git add forgotten_file.py
git commit --amend -m "Fixed message and added file"
    """, language="bash")

with tab_revert:
    st.subheader("Revert: The Safe Undo")
    st.markdown("""
    Creates a **New Commit** that is the exact opposite of the bad commit.
    *   Safe for shared repos.
    *   History is preserved.
    """)
    st.code("git revert <commit-hash>", language="bash")

with tab_reset:
    st.subheader("Reset: Time Travel")
    st.markdown("Moves the HEAD pointer back in time. **Destructive**.")

    st.markdown("**1. Soft Reset (`--soft`)**")
    st.markdown("*   Moves HEAD back.")
    st.markdown("*   Changes stay in **Staging Area**. (Ready to commit again).")

    st.markdown("**2. Mixed Reset (`--mixed`)**")
    st.markdown("*   Moves HEAD back.")
    st.markdown("*   Changes stay in **Working Dir**. (Unstaged).")

    st.markdown("**3. Hard Reset (`--hard`)**")
    st.markdown("*   Moves HEAD back.")
    st.markdown("*   **DESTROYS** all changes. (Dangerous!).")

    st.code("git reset --hard HEAD~1", language="bash")

# --- SECTION 4: REFLOG ---
st.header("4. Reflog: The Safety Net 🪂")
st.markdown("""
Deleted a branch by mistake? Hard reset too far?
**Git keeps a log of everywhere HEAD has been.**
Even "deleted" commits are still there for a few days.
""")

st.code("""
# 1. See history of moves
git reflog

# Output:
# a1b2c3d HEAD@{0}: reset: moving to HEAD~1
# 9999999 HEAD@{1}: commit: Bad commit

# 2. Rescue the lost commit
git checkout -b rescue-branch 9999999
""", language="bash")

# --- SECTION 5: EXERCISES ---
st.header("5. Exercises 📝")
st.info("""
1.  **Tag**: Create a tag `v0.1` on your current commit.
2.  **Amend**: Make a commit, then change the message using `--amend`.
3.  **Reset**: Make a dummy commit. `git reset --soft HEAD~1`. Where did the file go?
4.  **Reflog**: Run `git reflog`. Can you see your reset action?
""")
