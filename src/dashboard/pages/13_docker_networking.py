import streamlit as st
from src.dashboard.components.navigation import sidebar_navigation
from src.dashboard.components.mermaid import render_mermaid

st.set_page_config(page_title="Docker Networking", page_icon="🌐", layout="wide")
sidebar_navigation()

st.title("🌐 Docker Networking: From Zero to Hero")

st.markdown("""
Networking is often the most confusing part of Docker.
To understand it, we first need to understand how computers talk to each other **without** Docker.
""")

# --- SECTION 1: NETWORKING 101 ---
st.header("1. Networking 101: The Apartment Analogy 🏢")
st.markdown("""
Imagine a computer network is a **City**.

### 1.1. IP Address = The Building Address 📍
*   Every computer (Server, Laptop, Phone) has an **IP Address**.
*   It looks like `192.168.1.5`.
*   This tells the mailman (the Router) **which building** to deliver the message to.

### 1.2. Port = The Apartment Number 🚪
*   A building has many apartments. A computer has many **Ports**.
*   You don't just send a letter to "Building 123". You send it to "Building 123, **Apartment 80**".
*   **Standard Apartments**:
    *   **Port 80**: The Web Server (HTTP).
    *   **Port 443**: The Secure Web Server (HTTPS).
    *   **Port 5432**: The Postgres Database.
    *   **Port 3000**: Your React App.

### 1.3. Protocol = The Language 🗣️
*   Once the door opens, what language do you speak?
*   **HTTP**: "GET me this page." (Websites)
*   **TCP**: "Did you hear me? I'll repeat it." (Reliable)
*   **UDP**: "CATCH THIS!" (Fast, used for Video/Gaming)

### 1.4. Localhost = "Me" 🏠
*   **127.0.0.1** (or `localhost`) always means **"This Computer"**.
*   **CRITICAL CONCEPT**: When you are inside a Docker Container, `localhost` means **THE CONTAINER ITSELF**, not your laptop!
""")

st.divider()

# --- SECTION 2: DOCKER NETWORKING ---
st.header("2. Docker Networking: The Virtual Router 🔀")
st.markdown("""
When you install Docker, it creates a **Virtual Router** inside your computer.
It creates a hidden private network that your laptop can't see directly without help.
""")

tab_bridge, tab_dns, tab_host, tab_none = st.tabs(["1. Bridge (The Default)", "2. DNS (Magic Names)", "3. Host (Speed)", "4. None (Silence)"])

with tab_bridge:
    st.subheader("The Bridge Network")
    st.markdown("""
    *   **What is it?**: The default network driver.
    *   **Isolation**: Every container gets its own private IP (e.g., `172.17.0.2`).
    *   **The Wall**: By default, **nobody** from the outside (internet/laptop) can get in.
    *   **The Gate**: To let people in, you must open a specific port (**Port Mapping**).
    """)
    render_mermaid("""
    graph TD
        Internet((Internet)) --X Wall
        Laptop["Laptop (Host)"] --X Wall

        subgraph Docker Network
            Router["Docker Bridge (172.17.0.1)"]
            C1["Container A (172.17.0.2)"]
            C2["Container B (172.17.0.3)"]
        end

        Laptop <--> Router
        Router <--> C1
        Router <--> C2

        style Wall fill:#ffcccc,stroke:#ff0000
    """, height=250)

with tab_dns:
    st.subheader("DNS & Service Discovery")
    st.markdown("""
    **The Problem**: Container IPs change every time they restart. `172.17.0.2` might become `172.17.0.5`.

    **The Solution**: Use **Names**, not IPs.

    If you create a custom network, Docker provides an internal **DNS Server**.
    """)
    st.code("""
# 1. Create a network
docker network create my-net

# 2. Run a database named 'db'
docker run -d --name db --network my-net postgres

# 3. Run a web app
docker run -d --network my-net my-web-app
    """, language="bash")
    st.markdown("""
    Now, inside the web app, you connect to the database using the hostname: **`db`**.
    *   ❌ `host: '172.17.0.2'` (Bad, brittle)
    *   ✅ `host: 'db'` (Good, permanent)
    """)

with tab_host:
    st.subheader("Host Network")
    st.markdown("""
    *   **Concept**: Remove the isolation. The container shares the **Host's IP**.
    *   **Speed**: Faster (no routing overhead).
    *   **Risk**: If the container uses Port 80, your Laptop's Port 80 is taken. You can't run two.
    *   **Command**: `docker run --network host ...`
    """)

with tab_none:
    st.subheader("None Network")
    st.markdown("""
    *   **Concept**: No network card. Total silence.
    *   **Use Case**: Security. Batch jobs that process files and exit without needing internet.
    """)

st.divider()

# --- SECTION 3: PORT MAPPING ---
st.header("3. Port Mapping: The Portal 🌀")
st.markdown("""
Since containers are locked in a private network, how do we see the website running inside?
We must **Publish** a port.
""")

col1, col2 = st.columns(2)

with col1:
    st.code("docker run -p 8080:80 nginx", language="bash")
    st.markdown("""
    *   **-p**: Publish.
    *   **8080**: The Port on your **Laptop** (Host).
    *   **80**: The Port inside the **Container**.
    """)

with col2:
    st.markdown("""
    **Translation**:
    > "Hey Docker, if anyone knocks on my Laptop's door **8080**, please teleport them instantly to the Container's door **80**."
    """)

render_mermaid("""
graph LR
    User["User Browser"] -->|http://localhost:8080| LaptopPort["Laptop:8080"]
    LaptopPort -->|Magic Tunnel| ContainerPort["Container:80"]
    ContainerPort --> Nginx["Nginx Server"]

    style LaptopPort fill:#e3f2fd
    style ContainerPort fill:#e8f5e9
""", height=200)

# --- SECTION 4: COMMON MISTAKES ---
st.header("4. Common Mistakes ⚠️")
st.warning("""
1.  **Connecting to Localhost**:
    *   If your code inside a container tries to connect to `localhost:5432`, it is looking for a database **inside the same container**.
    *   If the DB is in another container, use its **Service Name** (e.g., `postgres`).
    *   If the DB is on your Laptop, use `host.docker.internal` (Mac/Windows).

2.  **Port Conflicts**:
    *   You cannot run two containers mapped to the same Host port (e.g., `-p 8080:80` and `-p 8080:3000`).
    *   Solution: Change the Host port (`-p 8081:3000`).
""")

# --- SECTION 5: EXERCISES ---
st.header("5. Exercises 📝")
st.info("""
1.  **The Ping Test**:
    *   Create a network: `docker network create test-net`
    *   Run two alpines:
        *   `docker run -dit --name c1 --network test-net alpine sh`
        *   `docker run -dit --name c2 --network test-net alpine sh`
    *   Attach to c1: `docker attach c1`
    *   Ping c2: `ping c2` (It works!)

2.  **The Port Test**:
    *   Run Nginx: `docker run -d -p 9090:80 nginx`
    *   Open Browser: Go to `localhost:9090`.
    *   Try `localhost:80`. (It won't work).
""")
