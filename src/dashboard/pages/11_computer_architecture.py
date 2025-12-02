import streamlit as st
from src.dashboard.components.navigation import sidebar_navigation
from src.dashboard.components.mermaid import render_mermaid

st.set_page_config(page_title="Computer Architecture", page_icon="💻", layout="wide")
sidebar_navigation()

st.title("💻 Computer Architecture & The OS")

# --- LAYER 1: Intuition ---
st.header("1. Intuition: The Restaurant Kitchen 🍳")
st.markdown("""
Imagine your computer is a busy **Restaurant Kitchen**.

*   **CPU (The Chef)**: Super fast, but can only do one thing at a time.
*   **RAM (The Countertop)**: Fast access to ingredients. Small space. Cleared when lights go out.
*   **Disk (The Freezer)**: Huge storage, but slow. You have to walk to get things.
*   **Kernel (The Manager)**: Tells the Chef what to cook. Ensures no one steals ingredients.
*   **Process (The Order)**: "Table 4 wants Pasta". A set of instructions.
""")
st.markdown("---")

# --- LAYER 3: Structure ---
st.header("3. Structure: User Space vs Kernel Space 🧱")
render_mermaid("""
graph TD
    subgraph User_Space ["User Space (Unprivileged)"]
        App1["Chrome"]
        App2["Python Script"]
        App3["Docker Container"]
    end

    subgraph Boundary ["System Call Interface"]
        SysCall["The Gatekeeper"]
    end

    subgraph Kernel_Space ["Kernel Space (Privileged)"]
        Kernel["The Kernel (Boss)"]
        Drivers["Device Drivers"]
        Hardware["Physical Hardware"]
    end

    App2 -->|1. print('Hello')| SysCall
    SysCall -->|2. write()| Kernel
    Kernel -->|3. Draw Pixels| Hardware
""", height=400)

st.markdown("""
*   **User Space**: Where your apps live. They are **Sandboxed**. They cannot touch hardware directly.
*   **Kernel Space**: The only code allowed to touch the metal.
*   **System Call**: The *only* way an app can ask the Kernel for help (e.g., "Open file", "Send network packet").
""")
st.markdown("---")

# --- LAYER 5: Full Math ---
st.header("5. The Math: Virtual Memory 🧮")
st.markdown("How does the Kernel trick apps into thinking they have infinite RAM?")
st.markdown("**The Mapping Function:**")
st.latex(r"PhysicalAddress = PageTable(VirtualAddress)")

st.markdown("""
*   **Virtual Address**: What the app sees (e.g., `0x00A1`).
*   **Physical Address**: Where the data actually is in the RAM stick (e.g., `Row 99, Col 3`).
*   **Page Table**: A dictionary maintained by the Kernel.
    *   `{Process A: {0x00A1: RAM_Slot_5}}`
    *   `{Process B: {0x00A1: RAM_Slot_99}}`
*   **Result**: Two apps can use the *same* address (`0x00A1`) but point to *different* physical memory. **Total Isolation.**
""")
st.markdown("---")

# --- LAYER 9: Exercises ---
st.header("9. Exercises 📝")
st.info("""
1.  **Run**: Open a terminal and run `top`.
2.  **Find**: Which process is using the most CPU?
3.  **Identify**: Find the `PID` (Process ID). This is the number the Kernel uses to track the "Order Ticket".
""")
