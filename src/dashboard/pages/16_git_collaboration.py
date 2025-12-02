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

# --- SECTION 1: THE MULTIVERSE (BRANCHING) ---
st.header("1. The Multiverse: Parallel Timelines 🌌")
st.markdown("""
Imagine you want to try a crazy experiment. You don't want to blow up the main lab.
So you create a **Parallel Universe**.
*   **Main Branch**: The stable, production code. The "Real World".
*   **Feature Branch**: Your playground. You can break things here. It doesn't affect Main.
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

st.markdown("---")

# --- SECTION 2: THE MERGE (CONVERGENCE) ---
st.header("2. The Merge: Bringing it Back 🔀")
st.markdown("""
You finished your experiment. It works! Now you want to bring it back to the Real World.
This is a **Merge**.
Git takes your changes from `Feature` and replays them onto `Main`.
""")

render_mermaid("""
graph LR
    M1((Main 1)) --> M2((Main 2))
    M2 --> M3((Main 3))
    M3 --> Merge((Merge))

    M2 --> F1((Feature 1))
    F1 --> F2((Feature 2))
    F2 --> Merge

    style Merge fill:#d1c4e9
""", height=300)

st.markdown("---")

# --- SECTION 3: CONFLICTS (THE BATTLE) ---
st.header("3. Conflicts: When Universes Collide ⚔️")
st.markdown("""
What if:
1.  **You** changed Line 10 of `app.py` to say `print("Hello")`.
2.  **Your Friend** changed Line 10 of `app.py` to say `print("Goodbye")`.
3.  You try to merge.

Git panics. **"I don't know which one is right!"**
This is a **Merge Conflict**.
""")

st.code("""
<<<<<<< HEAD
print("Goodbye")
=======
print("Hello")
>>>>>>> feature-branch
""", language="python")

st.markdown("""
**How to fix it:**
1.  Open the file.
2.  Delete the weird markers (`<<<<`, `====`, `>>>>`).
3.  Pick the code you want (or combine them).
4.  Save and Commit.
""")

st.markdown("---")

# --- SECTION 4: PULL REQUESTS (CODE REVIEW) ---
st.header("4. Pull Requests: The Gatekeeper 🛡️")
st.markdown("""
In professional teams, you don't just merge. You open a **Pull Request (PR)**.
*   "Hey team, I want to merge my Feature branch into Main."
*   The team reviews your code. "Change this variable name." "Fix this bug."
*   Once approved, you click the **Merge Button**.
""")

st.markdown("---")

# --- SECTION 5: EXERCISES ---
st.header("5. Exercises 📝")
st.info("""
1.  **Branch**: `git checkout -b new-feature`.
2.  **Change**: Make a change and commit it.
3.  **Switch**: `git checkout main`. Notice your change is GONE! (It's safe in the other universe).
4.  **Merge**: `git merge new-feature`. Now your change appears in Main.
""")
