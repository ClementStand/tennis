import streamlit as st
from src.dashboard.components.navigation import sidebar_navigation
from src.dashboard.components.mermaid import render_mermaid

st.set_page_config(page_title="Docker Networking", page_icon="🌐", layout="wide")
sidebar_navigation()

st.title("🌐 Docker Networking: IPs, Ports & Bridges")
st.markdown("### Connecting the Boxes")

st.markdown("""
Networking is often the scariest part of Docker for beginners.
"Why can't I connect to localhost?" "What is 0.0.0.0?" "How do containers talk to each other?"

We are going to demystify this by looking at how data actually moves through the wires (virtual ones).
""")

# --- 1. TL;DR ---
st.info("""
**🚀 Big Picture (TL;DR)**

*   **IP Address**: The "Street Address" of a computer (or container). Every container gets its own unique internal IP.
*   **Port**: The "Door Number" at that address. Web servers usually listen behind Door 80.
*   **Bridge Network (`docker0`)**: A virtual "Switch" inside your laptop. All containers plug into this switch so they can talk to each other.
*   **NAT / Port Mapping (`-p`)**: A rule that forwards traffic from your Laptop's Door to the Container's Door.
*   **DNS**: The phonebook. It lets containers find each other by name (`db`) instead of memorizing changing IP addresses (`172.17.0.5`).
""")

st.markdown("---")

# --- 2. Intuition ---
st.header("1. Intuition: The Apartment Complex 🏢")

st.markdown("""
Imagine your Laptop is a giant **Apartment Complex**.

*   **The Host (Your Laptop)**: The building itself. It has a public address (e.g., `192.168.1.5` on your WiFi).
*   **The Containers**: Individual **Apartments** inside.
    *   They are private.
    *   They have their own internal intercom numbers (Internal IPs like `172.17.0.2`).
    *   People on the street **cannot** walk directly into an apartment. They can only enter the Building Lobby.

*   **The Port Mapping (`-p 8080:80`)**: The Concierge.
    *   You tell the Concierge: "If anyone knocks on the **Building's Main Door #8080**, please escort them directly to **Apartment A, Door #80**."
    *   Without this instruction, the packet hits the building wall and is dropped.

*   **The Bridge**: The Hallway.
    *   Apartment A can walk down the hall and knock on Apartment B's door directly. They don't need to go outside.
""")

st.markdown("---")

# --- 3. Architecture Diagram ---
st.header("2. The Network Architecture")
st.markdown("Visualizing the flow of data.")

render_mermaid("""
graph LR
    subgraph Internet
        User["User Browser"]
    end

    subgraph Host_Machine ["Your Laptop (Host IP: 192.168.1.5)"]
        NIC["Physical WiFi Card"]
        NAT["NAT / Port Forwarding Rule"]

        subgraph Docker_Bridge ["docker0 Bridge (172.17.0.1)"]
            Container1["Container A (Web) <br> IP: 172.17.0.2 <br> Port: 80"]
            Container2["Container B (DB) <br> IP: 172.17.0.3 <br> Port: 5432"]
        end
    end

    User -->|1. Request 192.168.1.5:8080| NIC
    NIC -->|2. Pass to| NAT
    NAT -->|3. Rewrite Destination -> 172.17.0.2:80| Container1
    Container1 -->|4. Internal Traffic| Container2
""", height=500)

st.markdown("""
**How to read this:**
1.  **External Traffic**: The user hits your laptop's IP.
2.  **NAT**: Docker uses `iptables` (Linux Firewall) to rewrite the packet. It changes the destination from "Laptop" to "Container A".
3.  **Bridge**: The packet crosses the virtual bridge to reach the container.
4.  **Internal Traffic**: Container A can talk to Container B directly using the Bridge. It never leaves the laptop.
""")

st.markdown("---")

# --- 4. Technical Mechanics ---
st.header("3. Technical Mechanics: Protocols & DNS")

st.subheader("A. TCP vs UDP")
st.markdown("""
*   **TCP (Transmission Control Protocol)**: The "Reliable" one.
    *   Used for Web (HTTP), Database, Email.
    *   "Did you get that? Yes. Okay, sending next part."
    *   Docker uses this 99% of the time.
*   **UDP (User Datagram Protocol)**: The "Fast" one.
    *   Used for Video Streaming, Gaming.
    *   "Here is data! Good luck!"

B. DNS (Domain Name System)
In Docker Compose, you don't use IPs. You use **Service Names**.
*   You name your database service `db`.
*   Your web app connects to `postgres://db:5432`.
*   Docker runs a tiny DNS server inside the network.
*   When Web asks "Who is `db`?", Docker answers "It's `172.17.0.3`".
*   **Why?** Because if `db` restarts, it might get a new IP (`172.17.0.99`), but the name `db` stays the same.
""")

st.markdown("---")

# --- 5. What Actually Happens When... ---
st.header("4. What Actually Happens When... 🕵️‍♂️")
st.markdown("Scenario: **Browser** visits **Container**.")

st.markdown("""
**Command**: `docker run -p 8080:80 nginx`

1.  **Browser**: You type `http://localhost:8080`.
2.  **OS Kernel**: Receives a TCP SYN packet on Port 8080.
3.  **IPTables (The Firewall)**:
    *   Docker installed a rule: `DNAT tcp --dport 8080 -j DNAT --to-destination 172.17.0.2:80`.
    *   The Kernel rewrites the packet header. Destination is now the Container IP.
4.  **Routing**:
    *   Kernel looks at the routing table. "172.17.x.x? That goes to the `docker0` interface."
5.  **Bridge**:
    *   The packet travels over the virtual wire (`veth`).
6.  **Container**:
    *   Nginx receives the packet on Port 80.
    *   It processes the request and sends a response.
7.  **Return Trip**:
    *   The response goes back to the Bridge -> Kernel.
    *   Kernel "Un-NATs" the packet (changes source back to localhost:8080).
    *   Browser receives the page.
""")

st.markdown("---")

# --- 6. Practical Commands ---
st.header("5. Practical Commands")

st.markdown("""
*   `docker network ls`: List all networks.
*   `docker network inspect bridge`: See exactly which containers are connected and their IPs.
*   `docker run --network my-net ...`: Attach a container to a specific network.
""")

st.markdown("---")

# --- 7. FAQ & Exercises ---
st.header("6. FAQ & Exercises")

with st.expander("Q: Why can't I access the container on Port 80 directly?"):
    st.markdown("""
    Because your laptop doesn't listen on Port 80. The container does.
    The container is in a separate "room". You must open the door (Port Mapping) to let traffic in.
    """)

with st.expander("Q: What is 127.0.0.1 vs 0.0.0.0?"):
    st.markdown("""
    *   **127.0.0.1 (Localhost)**: "Me Only". If a container listens here, it ignores the outside world.
    *   **0.0.0.0 (All Interfaces)**: "Everyone". Containers MUST listen here to accept traffic from the Bridge.
    """)

st.info("""
**🧠 Try it yourself:**
1.  Run `docker run -d -p 8080:80 nginx`.
2.  Go to `localhost:8080` in your browser. It works!
3.  Go to `localhost:80`. It fails (Connection Refused). Why? Because we didn't map port 80 on the host.
""")

st.success("Next: Managing networks manually is hard. Let's automate it with Docker Compose.")
st.page_link("pages/14_docker_compose.py", label="Go to Docker Compose", icon="📦")
