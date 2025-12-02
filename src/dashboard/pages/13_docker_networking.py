import streamlit as st
from src.dashboard.components.navigation import sidebar_navigation
from src.dashboard.components.mermaid import render_mermaid

st.set_page_config(page_title="Docker Networking", page_icon="🌐", layout="wide")
sidebar_navigation()

st.title("🌐 Docker Networking: IPs, Ports & Bridges")

# --- LAYER 1: Intuition ---
st.header("1. Intuition: The Apartment Complex 🏢")
st.markdown("""
*   **Your Laptop**: The Building. Address: `192.168.1.5`.
*   **Container**: An Apartment inside. Address: `172.17.0.2` (Internal).
*   **Port Mapping**: The Concierge.
    *   "If someone knocks on the **Main Door #8080**, take them to **Apartment 2, Door #80**."
*   **Bridge**: The Hallway. Apartments can visit each other without going outside.
""")
st.markdown("---")

# --- LAYER 3: Structure ---
st.header("3. Structure: The Bridge Network 🌉")
render_mermaid("""
graph LR
    User["User (Internet)"] -->|Port 8080| Laptop["Laptop (Host)"]
    Laptop -->|NAT Rule| Bridge["docker0 Bridge"]
    Bridge -->|Internal IP| C1["Container 1 (Web)"]
    Bridge -->|Internal IP| C2["Container 2 (DB)"]

    C1 -->|Direct Access| C2
""", height=300)

st.markdown("""
*   **docker0**: A virtual network switch inside your laptop.
*   **NAT**: Network Address Translation. Rewrites the destination IP on packets.
*   **DNS**: Docker keeps a phonebook. Container 1 can just say "Call `db`", and Docker looks up the IP.
""")
st.markdown("---")

# --- LAYER 4: Step-by-Step ---
st.header("4. Step-by-Step: The Packet's Journey 📦")
st.markdown("Scenario: You visit `localhost:8080`.")
st.markdown("""
1.  **Browser**: Sends packet to `localhost` (Your Laptop) on Port `8080`.
2.  **Kernel**: Sees packet. Checks **IPTables** (Firewall).
3.  **NAT**: Rule says "Redirect Port 8080 to `172.17.0.2:80`".
4.  **Rewrite**: Kernel changes the packet header.
5.  **Bridge**: Packet crosses the virtual wire to the Container.
6.  **Container**: Nginx receives packet on Port 80. "Hello!"
""")
st.markdown("---")

# --- LAYER 9: Exercises ---
st.header("9. Exercises 📝")
st.info("""
1.  **Run**: `docker run -d -p 8080:80 nginx`.
2.  **Visit**: `localhost:8080`. (It works).
3.  **Visit**: `localhost:80`. (It fails). Why? (We didn't open the Main Door #80).
""")
