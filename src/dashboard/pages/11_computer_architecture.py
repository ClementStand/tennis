import streamlit as st
from src.dashboard.components.navigation import sidebar_navigation
from src.dashboard.components.mermaid import render_mermaid

st.set_page_config(page_title="Computer Architecture", page_icon="💻", layout="wide")
sidebar_navigation()

st.title("💻 Computer Architecture & The OS")
st.markdown("### The Foundation of Everything")

st.markdown("""
Before we can understand Docker, Containers, or even Python, we must understand the machine they live on.
Most people treat their computer like a magic black box. Today, we are going to open the box.

We will learn how **Hardware**, the **Operating System (OS)**, and **Applications** talk to each other.
This knowledge is the "secret weapon" of great software engineers.
""")

# --- 1. TL;DR ---
st.info("""
**🚀 Big Picture (TL;DR)**

*   **Hardware (The Body)**: The physical parts. CPU (Brain), RAM (Short-term Memory), Disk (Long-term Storage).
*   **Kernel (The Subconscious)**: The core of the OS. It controls the hardware. No app can touch hardware without asking the Kernel first.
*   **User Space (The Conscious Mind)**: Where your apps live (Chrome, Spotify, Python). They are "untrusted" and isolated.
*   **System Call (The Request)**: The specific way an App asks the Kernel to do something (e.g., "Please save this file").
*   **Process (The Thought)**: A running program. It thinks it has the whole computer to itself, but the Kernel is lying to it.
""")

st.markdown("---")

# --- 2. Intuition ---
st.header("1. Intuition: The Restaurant Kitchen 🍳")

st.markdown("""
Imagine your computer is a busy **Restaurant Kitchen**.

*   **The Hardware = The Kitchen Equipment**
    *   **CPU**: The **Chef**. He chops, cooks, and plates. He is super fast but can only do one thing at a time.
    *   **RAM**: The **Countertop**. Ingredients here are ready to be used immediately. It's fast but small. If the power goes out, everything here is lost.
    *   **Disk**: The **Pantry/Freezer**. Huge storage, but slow. You have to walk over, find the box, and bring it to the counter.
    *   **Network**: The **Delivery Window**. Food goes out, supplies come in.

*   **The Kernel = The Kitchen Manager**
    *   The Chef (CPU) is too busy to decide *what* to cook.
    *   The **Manager (Kernel)** tells the Chef: "Slice onions for 2 seconds, then flip the burger, then check the soup."
    *   The Manager ensures no one steals someone else's ingredients (Memory Isolation).
    *   The Manager handles the Delivery Window (Network).

*   **The Process = The Recipe Ticket**
    *   An order comes in: "Table 4 wants Pasta."
    *   This is a **Process**. It's a set of instructions (Code) that needs resources (Ingredients) and time with the Chef (CPU).
""")

st.markdown("---")

# --- 3. Architecture Diagram ---
st.header("2. The Architecture Stack")
st.markdown("This is how the layers actually stack up in your machine.")

render_mermaid("""
graph TD
    subgraph User_Space ["User Space (Where Apps Live)"]
        Browser["Chrome Browser"]
        Python["Python Script"]
        Docker["Docker Container"]
        VSCode["VS Code"]
    end

    subgraph Boundary ["The System Call Interface"]
        SysCall["The Gatekeeper"]
    end

    subgraph Kernel_Space ["Kernel Space (The Boss)"]
        Kernel["OS Kernel (Linux/Windows/Mac)"]
        Scheduler["Scheduler (Decides who runs)"]
        MemMgr["Memory Manager"]
        Drivers["Device Drivers"]
    end

    subgraph Hardware ["Hardware (The Metal)"]
        CPU["CPU (Brain)"]
        RAM["RAM (Memory)"]
        Disk["Disk (Storage)"]
        NIC["Network Card"]
    end

    Browser -->|1. Request Write| SysCall
    Python -->|1. Request Network| SysCall

    SysCall -->|2. Validate & Pass| Kernel

    Kernel -->|3. Schedule| Scheduler
    Kernel -->|4. Execute| Drivers

    Drivers -->|5. Voltage| Hardware
""", height=600)

st.markdown("""
**How to read this diagram:**
1.  **Top (User Space)**: This is where YOU work. It's safe. If Python crashes here, the computer is fine.
2.  **Middle (Kernel Space)**: This is the danger zone. If code crashes here (Kernel Panic / Blue Screen), the whole machine dies.
3.  **The Line**: Notice the "System Call" boundary. Apps **cannot** cross this line directly. They must ask nicely.
""")

st.markdown("---")

# --- 4. Technical Mechanics ---
st.header("3. Technical Mechanics: How it Works")

st.subheader("A. The Process & Virtual Memory")
st.markdown("""
When you double-click an app, the OS creates a **Process**.
Crucially, the OS lies to the Process.
*   **The Lie**: "You have 100% of the RAM and CPU. Go wild."
*   **The Truth**: The Process is in a sandbox. It sees "Virtual Memory".
    *   When it tries to access address `0x1234`, the Kernel secretly maps that to "Real RAM Stick #2, Slot 5000".
    *   If Process A tries to touch Process B's memory, the Kernel sees the map doesn't match and kills Process A (`Segmentation Fault`).

**Why this matters for Docker:**
Docker Containers are just **Processes** with an even stricter sandbox. They aren't separate machines!

B. The System Call (Syscall)
The API of the Kernel. There are only about 300-400 system calls in Linux. Everything your computer does is a combination of these.
*   `fork()`: "Clone me." (How new processes start)
*   `exec()`: "Replace my brain with this new program."
*   `open()`: "Open this file."
*   `write()`: "Write data to this file (or screen)."
*   `socket()`: "Open a network connection."
""")

st.markdown("---")

# --- 5. What Actually Happens When... ---
st.header("4. What Actually Happens When... 🕵️‍♂️")
st.markdown("Let's trace the exact steps when you run a simple Python script.")

st.code("python hello.py", language="bash")

st.markdown("""
1.  **Shell Parsing**: You type the command in your terminal (Shell). The Shell parses the text.
2.  **Search**: The Shell looks for the `python` executable on your Disk (in your PATH).
3.  **Fork (The Clone)**:
    *   The Shell calls `fork()`.
    *   The OS creates a near-identical copy of the Shell process.
4.  **Exec (The Transformation)**:
    *   The *Child Process* calls `exec("python", "hello.py")`.
    *   The Kernel wipes the memory of this child and loads the Python Interpreter code from the Disk.
5.  **Initialization**:
    *   Python starts up. It asks the Kernel to `open("hello.py")`.
    *   It `read()`s the file contents into RAM.
6.  **Translation**:
    *   Python translates your code `print("Hello")` into machine instructions.
7.  **Output**:
    *   Python calls `write(1, "Hello", 5)`. (1 = Standard Output).
    *   The Kernel takes the bytes "Hello" and sends them to the Terminal Driver.
    *   The Terminal Driver draws the pixels on your screen.
8.  **Exit**:
    *   Python calls `exit(0)`.
    *   The Kernel sees the process is done. It marks the RAM as "Free" again.
    *   The Parent Shell wakes up and gives you the prompt back.
""")

st.markdown("---")

# --- 6. Practical Commands ---
st.header("5. Practical Commands")
st.markdown("How do we see this happening in real life?")

col1, col2 = st.columns(2)

with col1:
    st.subheader("`top` / `htop`")
    st.markdown("""
    Shows the **Kitchen Manager's Board**.
    *   Who is using the Chef (CPU)?
    *   Who is hogging the Countertop (RAM)?
    *   **PID**: Process ID (The Ticket Number).
    """)

with col2:
    st.subheader("`ps aux`")
    st.markdown("""
    Snapshot of all running processes.
    *   `USER`: Who started it?
    *   `PID`: The ID.
    *   `COMMAND`: What is it running?
    """)

st.markdown("---")

# --- 7. FAQ & Exercises ---
st.header("6. FAQ & Exercises")

with st.expander("Q: If I run 100 apps, why doesn't my CPU explode?"):
    st.markdown("""
    **Time Slicing.**
    The CPU is fast (3 Billion cycles per second).
    The Kernel lets App A run for 0.001 seconds, then pauses it, runs App B for 0.001 seconds, etc.
    It happens so fast that it *looks* like they are running at the same time.
    """)

with st.expander("Q: What is a 'Kernel Panic'?"):
    st.markdown("""
    It's when the Manager (Kernel) gets confused or corrupted.
    Since the Manager controls reality, if they go crazy, the only safe option is to **shut down everything immediately** to prevent data corruption.
    """)

st.info("""
**🧠 Try it yourself:**
1.  Open your terminal.
2.  Run `top` (or `htop` if you have it).
3.  Look at the `%CPU` column. Who is the hungriest process?
4.  Look at the `PID`. Every single thing has a number.
""")

st.success("Next: Now that we know what a Process is, let's see how Docker wraps a Process in a 'Container'.")
st.page_link("pages/12_docker_basics.py", label="Go to Docker Basics", icon="🐳")
