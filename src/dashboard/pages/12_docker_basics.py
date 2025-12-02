import streamlit as st
from src.dashboard.components.navigation import sidebar_navigation
from src.dashboard.components.mermaid import render_mermaid

st.set_page_config(page_title="Docker Basics", page_icon="🐳", layout="wide")
sidebar_navigation()

st.title("🐳 Docker Basics: Images & Containers")

# --- LAYER 1: Intuition ---
st.header("1. Intuition: The Matrix 💊")
st.markdown("""
Docker is **NOT** a Virtual Machine. It doesn't start a new computer.
It puts a **Mask** on a Process.

*   **Normal Process**: Walks down the street, sees the whole city, sees other people.
*   **Containerized Process**: Put in a simulation.
    *   It looks around: "I am the only person here." (**PID Namespace**)
    *   It looks at the map: "This city only has my house." (**Mount Namespace**)
    *   It looks at the clock: "It's a different timezone." (**UTS Namespace**)

It is a **Process with Blinders on**.
""")
st.markdown("---")

# --- LAYER 3: Structure ---
st.header("3. Structure: Layers 🍰")
st.markdown("Docker Images are like a stack of transparency sheets.")
render_mermaid("""
graph BT
    subgraph Container ["Container (Writable)"]
        L4["Layer 4: Writable (Logs, Temp Files)"]
    end

    subgraph Image ["Image (Read-Only)"]
        L3["Layer 3: App Code (app.py)"]
        L2["Layer 2: Python Interpreter"]
        L1["Layer 1: Ubuntu OS Files"]
    end

    L4 --> L3
    L3 --> L2
    L2 --> L1
""", height=400)

st.markdown("""
*   **Read-Only**: Layers 1-3 are locked. You can't change them.
*   **Copy-on-Write**: If you try to edit a file in Layer 1, Docker copies it to Layer 4 first.
*   **Efficiency**: If 10 containers use Python, they all **share** Layer 2. It's only stored once!
""")
st.markdown("---")

# --- LAYER 4: Step-by-Step ---
st.header("4. Step-by-Step: `docker run` 👣")
st.markdown("What happens when you type `docker run nginx`?")
st.markdown("""
1.  **Client**: Sends JSON to Docker Daemon.
2.  **Check**: "Do I have the `nginx` image?" -> No? Download layers from Hub.
3.  **Create**: Create a new Writable Layer (Layer 4).
4.  **Isolate**:
    *   Create new Namespaces (PID, Net, Mnt).
    *   Apply Cgroups (Limit CPU/RAM).
5.  **Start**: Tell Kernel "Start `nginx` inside this sandbox."
""")
st.markdown("---")

# --- LAYER 9: Exercises ---
st.header("9. Exercises 📝")
st.info("""
1.  **Run**: `docker run hello-world`.
2.  **Read**: Read the output text. It explains exactly what happened.
3.  **Check**: Run `docker ps -a`. Why is it "Exited"? (Because the process finished its job).
""")
