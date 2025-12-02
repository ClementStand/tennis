import streamlit as st
from src.dashboard.components.navigation import sidebar_navigation
from src.dashboard.components.mermaid import render_mermaid

st.set_page_config(page_title="Docker Networking", page_icon="🌐", layout="wide")
sidebar_navigation()

st.title("🌐 Docker Networking: The Invisible Cables")

st.markdown("""
> **"There is no place like 127.0.0.1"**
> But what does that actually mean? And how do Containers talk to each other?
""")

# --- SECTION 1: NETWORKING 101 ---
st.header("1. Networking 101: The Basics 🏙️")
st.markdown("""
Before Docker, we must understand the basics:
*   **IP Address**: The unique address of a machine (e.g., `192.168.1.5`).
*   **Port**: The specific door for an application (e.g., `80` for Web, `5432` for DB).
*   **Localhost**: `127.0.0.1` (Yourself).
""")

# --- SECTION 2: NETWORK MODES ---
st.header("2. Docker Network Modes 🔀")
st.markdown("Docker offers different ways to connect containers.")

tab_bridge, tab_host, tab_none, tab_custom = st.tabs(["Bridge (Default)", "Host", "None", "Custom"])

with tab_bridge:
    st.subheader("Bridge Network (The Virtual Router)")
    st.markdown("""
    *   **Default**: If you don't specify anything, this is used.
    *   **Isolation**: Containers get a private IP (e.g., `172.17.0.2`).
    *   **Communication**: They can talk to each other if you know the IP.
    *   **Access**: Outside world needs **Port Mapping** (`-p`) to get in.
    """)
    render_mermaid("""
    graph TD
        Laptop["Laptop (Host)"] <--> Router["Docker Bridge (docker0)"]
        Router <--> C1["Container A (172.17.0.2)"]
        Router <--> C2["Container B (172.17.0.3)"]
    """, height=200)

with tab_host:
    st.subheader("Host Network (No Isolation)")
    st.markdown("""
    *   **Concept**: The container shares the **Host's IP**.
    *   **Performance**: Faster (no routing overhead).
    *   **Risk**: Port conflicts! You can't run two Nginx containers on Port 80.
    *   **Command**: `docker run --network host ...`
    """)

with tab_none:
    st.subheader("None Network (Total Isolation)")
    st.markdown("""
    *   **Concept**: No network card. No Internet. No talking to anyone.
    *   **Use Case**: High security jobs (e.g., generating keys).
    *   **Command**: `docker run --network none ...`
    """)

with tab_custom:
    st.subheader("Custom Networks (The Best Way)")
    st.markdown("""
    *   **Concept**: Create your own private island.
    *   **Benefit**: **Automatic DNS**. You can ping containers by **Name**.
    """)
    st.code("""
# 1. Create Network
docker network create my-app-net

# 2. Run Containers
docker run --network my-app-net --name db postgres
docker run --network my-app-net --name web nginx

# 3. Magic
# Inside 'web', you can simply do: ping db
    """, language="bash")

# --- SECTION 3: PORT MAPPING ---
st.header("3. Port Mapping: The Concierge 🛎️")
st.markdown("""
**The Problem**: The outside world cannot see the Bridge Network.
**The Solution**: Forward a Host Port to a Container Port.
""")

st.code("docker run -p 8080:80 nginx", language="bash")
st.markdown("""
*   **8080**: Host Port (Public).
*   **80**: Container Port (Private).
""")

render_mermaid("""
graph LR
    User["User"] -->|Request| HostPort["Host:8080"]
    HostPort -->|Forwarding Rule| ContPort["Container:80"]
    ContPort --> App["Nginx App"]
""", height=200)

# --- SECTION 4: EXERCISES ---
st.header("4. Exercises 📝")
st.info("""
1.  **Bridge**: Run `docker run -d --name web nginx`. Inspect its IP.
2.  **Host**: Run `docker run --rm --network host alpine ip addr`. See? It has YOUR IP.
3.  **Custom**: Create a network. Connect two containers. Ping them by name.
""")
