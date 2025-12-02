import streamlit as st
from src.dashboard.components.navigation import sidebar_navigation
from src.dashboard.components.mermaid import render_mermaid

st.set_page_config(page_title="Computer Architecture", page_icon="💻", layout="wide")
sidebar_navigation()

st.title("💻 Computer Architecture & The OS")

st.markdown("""
> **"Everything is a file."** - Unix Philosophy
> To understand Docker, you must understand the Operating System it lives on.
""")

# --- SECTION 1: THE HARDWARE (THE KITCHEN) ---
st.header("1. The Hardware: The Kitchen 🍳")
st.markdown("Your computer is a restaurant kitchen.")

col1, col2, col3 = st.columns(3)
with col1:
    st.info("**CPU (The Chef)**")
    st.markdown("The brain. It chops, cooks, and plates. It is super fast but can only do one thing at a time (per core).")
with col2:
    st.warning("**RAM (The Countertop)**")
    st.markdown("Where the Chef works. Fast access to ingredients. Small space. If the power goes out, the food is lost.")
with col3:
    st.success("**Disk (The Freezer)**")
    st.markdown("Where ingredients are stored. Huge space, but slow. The Chef has to walk to the back to get things.")

st.markdown("---")

# --- SECTION 2: THE KERNEL (THE MANAGER) ---
st.header("2. The Kernel: The Manager 👔")
st.markdown("""
The **Kernel** is the boss.
*   **Resource Management**: "Chef, stop chopping onions (App A) and start grilling steak (App B)." (**Scheduling**).
*   **Security**: "App A, you are NOT allowed to touch App B's ingredients." (**Memory Isolation**).
*   **Hardware Abstraction**: "I don't care if it's an SSD or HDD, just save this file."
""")

render_mermaid("""
graph TD
    App1["Chrome"] -->|System Call| Kernel
    App2["Spotify"] -->|System Call| Kernel

    subgraph OS ["Operating System"]
        Kernel["The Kernel"]
    end

    Kernel --> CPU
    Kernel --> RAM
    Kernel --> Disk
""", height=350)

st.markdown("---")

# --- SECTION 3: THE PROCESS (THE ORDER) ---
st.header("3. The Process: The Order 🧾")
st.markdown("""
A **Program** is a recipe book (static file on disk).
A **Process** is the Chef actually cooking that recipe (running in RAM).

Every Process has:
1.  **PID (Process ID)**: A unique ticket number (e.g., 1042).
2.  **Memory**: Its own private chunk of the Countertop.
3.  **File Descriptors**: Which files it has open.
""")

st.markdown("---")

# --- SECTION 4: SYSTEM CALLS (THE BELL) ---
st.header("4. System Calls: Ringing the Bell 🔔")
st.markdown("""
Apps are **Unprivileged**. They cannot touch the hardware directly.
If Chrome wants to save a file, it cannot write to the disk.
It must **ask the Kernel**.

1.  Chrome: "Hey Kernel, please write 'hello' to `test.txt`." (**write() syscall**)
2.  Kernel: "Do you have permission? Yes. Okay, I'll do it."
3.  Kernel: Writes to disk.
4.  Kernel: "Done."
""")

st.markdown("---")

# --- SECTION 5: EXERCISES ---
st.header("5. Exercises 📝")
st.info("""
1.  **Top**: Run `top` (or `htop`) in your terminal. Watch the Chef work.
2.  **Kill**: Find a PID and run `kill <PID>`. You just told the Manager to fire that order.
3.  **Files**: Run `ls -l /proc`. This is the Kernel exposing its internal state as files!
""")
