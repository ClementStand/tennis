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

# --- SECTION 1: NETWORKING 101 (PRE-DOCKER) ---
st.header("1. Networking 101: The City Analogy 🏙️")
st.markdown("Before we touch Docker, we must understand how computers talk.")

col1, col2 = st.columns(2)
with col1:
    st.info("**1. The IP Address (The Building Address)**")
    st.markdown("""
    Every computer has an address.
    *   `192.168.1.5`: Your Laptop's address on the Wifi.
    *   `127.0.0.1` (**Localhost**): "Me". Always points to yourself.
    *   `0.0.0.0`: "Everyone". Listen to anyone who calls.
    """)

with col2:
    st.warning("**2. The Port (The Apartment Number)**")
    st.markdown("""
    One building (IP) has many apartments (Apps).
    *   **Port 80**: The Web Server Apartment.
    *   **Port 5432**: The Database Apartment.
    *   **Port 22**: The SSH Admin Apartment.

    To visit a website, you need **IP + Port**: `192.168.1.5:80`.
    """)

st.markdown("---")

# --- SECTION 2: THE DOCKER BRIDGE ---
st.header("2. The Docker Bridge: A Virtual Router 🌉")
st.markdown("""
When you install Docker, it creates a **Virtual Router** inside your laptop called `docker0`.
*   It creates a private network (usually `172.17.0.x`).
*   Your laptop is the **Gateway** (`172.17.0.1`).
*   Every container gets its own private IP (e.g., `172.17.0.2`).
""")

render_mermaid("""
graph TD
    Laptop["Laptop (Host) <br> 192.168.1.5"]

    subgraph Docker_Network ["Docker Bridge Network (172.17.0.x)"]
        Router["Virtual Router (docker0) <br> 172.17.0.1"]
        C1["Container A (Web) <br> 172.17.0.2"]
        C2["Container B (DB) <br> 172.17.0.3"]
    end

    Laptop <--> Router
    Router <--> C1
    Router <--> C2
    C1 <--> C2
""", height=350)

st.success("**Key Concept**: Containers can talk to each other directly using these internal IPs!")

st.markdown("---")

# --- SECTION 3: PORT MAPPING ---
st.header("3. Port Mapping: The Concierge 🛎️")
st.markdown("""
**The Problem**: The outside world (Internet) cannot see `172.17.0.2`. That IP is private.
**The Solution**: Port Mapping (`-p`).

We tell Docker:
> "If anyone knocks on the Laptop's **Port 8080**, forward them to the Container's **Port 80**."
""")

col_ex, col_diag = st.columns([1, 1])

with col_ex:
    st.code("docker run -p 8080:80 nginx", language="bash")
    st.markdown("""
    *   **8080 (Host Port)**: The public door. You can change this (e.g., to 3000 or 5000).
    *   **80 (Container Port)**: The private door. Nginx *must* listen on this. You usually can't change this without configuring Nginx.
    """)

with col_diag:
    render_mermaid("""
    graph LR
        User["User"] -->|Request| HostPort["Host:8080"]
        HostPort -->|Forwarding Rule| ContPort["Container:80"]
        ContPort --> App["Nginx App"]
    """, height=200)

st.markdown("---")

# --- SECTION 4: DNS (SERVICE DISCOVERY) ---
st.header("4. DNS: The Phonebook 📒")
st.markdown("""
**The Problem**: Container IPs (`172.17.0.2`) change every time you restart them.
**The Solution**: **DNS** (Domain Name System).

Docker maintains an internal phonebook.
*   You name a container `my-db`.
*   Docker says: "Okay, `my-db` is currently at `172.17.0.2`."
*   If `my-db` restarts and gets `172.17.0.99`, Docker updates the phonebook.

**Your Code**:
```python
# BAD: Hardcoded IP
connect("172.17.0.2")

# GOOD: Use the Container Name
connect("my-db")
```
""")

st.markdown("---")

# --- SECTION 5: EXERCISES ---
st.header("5. Exercises 📝")
st.info("""
1.  **Run**: `docker run -d --name my-web -p 8080:80 nginx`.
2.  **Inspect**: `docker inspect my-web`. Find the `IPAddress`. It will be something like `172.17.0.x`.
3.  **Ping**: Run another container: `docker run -it alpine ping my-web`. It works! Docker resolves the name `my-web` to the IP.
""")
