import streamlit as st
from src.dashboard.components.navigation import sidebar_navigation
from src.dashboard.components.mermaid import render_mermaid

st.set_page_config(page_title="Docker Compose", page_icon="📦", layout="wide")
sidebar_navigation()

st.title("📦 Docker Compose: Orchestration")
st.markdown("### The Conductor of the Orchestra")

st.markdown("""
In the real world, apps are never just one container.
You have a **Frontend** (React), a **Backend** (Python), a **Database** (Postgres), and a **Cache** (Redis).

Starting these one by one with `docker run` is painful. You have to create networks, remember IPs, and start them in the right order.
**Docker Compose** automates this. It is a tool for defining and running multi-container applications.
""")

# --- 1. TL;DR ---
st.info("""
**🚀 Big Picture (TL;DR)**

*   **docker-compose.yml**: A text file (YAML) that describes your entire app stack (The Blueprint).
*   **Service**: A container definition in that file (e.g., "web", "db").
*   **Orchestration**: The act of coordinating multiple containers (starting, stopping, connecting them).
*   **Project Name**: Compose groups containers by project (usually the folder name) so they don't clash with other apps.
*   **Service Discovery**: Containers can talk to each other by **Name** (`ping db`), not IP.
""")

st.markdown("---")

# --- 2. Intuition ---
st.header("1. Intuition: The Construction Site 🏗️")

st.markdown("""
*   **Docker Run**: Like hiring one contractor to build a wall. You have to tell them exactly what to do, where to stand, and what tools to use.
*   **Docker Compose**: Like hiring a **General Contractor** (The Foreman).
    *   You give the Foreman a **Blueprint** (`docker-compose.yml`).
    *   The Blueprint says: "We need a Plumber, an Electrician, and a Carpenter."
    *   The Foreman handles the logistics: "Electrician, you start after the Carpenter is done."
    *   The Foreman ensures they can talk to each other (Networking).
""")

st.markdown("---")

# --- 3. The Blueprint (YAML) ---
st.header("2. The Blueprint (YAML)")
st.markdown("Let's analyze the famous **Voting App** architecture.")

col1, col2 = st.columns(2)

with col1:
    st.code("""
version: '3.8'

services:
  # 1. The Frontend
  vote:
    image: dockersamples/examplevotingapp_vote:before
    ports:
      - "5000:80"
    networks:
      - front-tier
    depends_on:
      - redis

  # 2. The Cache
  redis:
    image: redis:alpine
    networks:
      - front-tier
      - back-tier

  # 3. The Database
  db:
    image: postgres:15
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - back-tier

volumes:
  db-data:

networks:
  front-tier:
  back-tier:
    """, language="yaml")

with col2:
    st.markdown("""
    **Key Components:**
    *   **services**: The list of containers.
    *   **image**: The recipe to use.
    *   **ports**: Open doors to the host.
    *   **networks**: Which rooms can this container enter?
        *   `vote` is in `front-tier`.
        *   `db` is in `back-tier`.
        *   `vote` CANNOT talk to `db` directly! (Security).
    *   **volumes**: `db-data` ensures the database files survive if the `db` container dies.
    """)

st.markdown("---")

# --- 4. Architecture Diagram ---
st.header("3. The Architecture")
st.markdown("How the services connect.")

render_mermaid("""
graph TD
    subgraph Host ["Your Laptop"]
        Browser
    end

    subgraph Network ["Compose Network (voting_app_default)"]
        Vote["Service: vote <br> (Python)"]
        Redis["Service: redis <br> (Cache)"]
        Worker["Service: worker <br> (.NET)"]
        DB["Service: db <br> (Postgres)"]
    end

    Browser -->|localhost:5000| Vote
    Vote -->|redis://redis| Redis
    Worker -->|redis://redis| Redis
    Worker -->|postgres://db| DB

    style Vote fill:#e1f5fe
    style Redis fill:#ffebee
    style DB fill:#e8f5e9
""", height=500)

st.markdown("---")

# --- 5. What Actually Happens When... ---
st.header("4. What Actually Happens When... 🕵️‍♂️")
st.markdown("Command: `docker compose up -d`")

st.markdown("""
1.  **Parse**: Compose reads `docker-compose.yml`. It validates the syntax.
2.  **Project Name**: It looks at the folder name (e.g., `my_project`). It prefixes everything with this name (`my_project_web_1`).
3.  **Network**:
    *   It checks: "Does `my_project_default` network exist?"
    *   No? It creates a new Bridge Network.
4.  **Volumes**:
    *   It checks: "Does `db-data` volume exist?"
    *   No? It creates it on disk.
5.  **Pull/Build**:
    *   It downloads images for `redis` and `postgres`.
    *   It builds the `vote` image if `build: .` was specified.
6.  **Dependency Order**:
    *   It sees `depends_on`. It starts `redis` FIRST.
    *   It waits for `redis` to be running.
    *   Then it starts `vote`.
7.  **DNS Registration**:
    *   It adds `redis` and `db` to the internal DNS server.
    *   Now `vote` can resolve `redis` to an IP address.
""")

st.markdown("---")

# --- 6. Practical Commands ---
st.header("5. Practical Commands")

st.markdown("""
*   `docker compose up`: Start everything in the foreground (shows logs).
*   `docker compose up -d`: Start in background (Detached).
*   `docker compose down`: Stop containers AND remove networks (Clean slate).
*   `docker compose down -v`: Also delete Volumes (DANGER: Deletes database data).
*   `docker compose logs -f`: Follow logs of all services mixed together.
*   `docker compose ps`: List status of this project's services.
""")

st.markdown("---")

# --- 7. FAQ & Exercises ---
st.header("6. FAQ & Exercises")

with st.expander("Q: What is the difference between 'expose' and 'ports'?"):
    st.markdown("""
    *   **ports (`5000:80`)**: Opens the port to the **Host** (Your Laptop).
    *   **expose (`80`)**: Just documentation. It says "I listen on 80", but it DOES NOT open it to the host. Only other containers on the same network can reach it.
    """)

st.info("""
**🧠 Try it yourself:**
1.  Create a file `docker-compose.yml` with the content above.
2.  Run `docker compose up -d`.
3.  Run `docker compose ps`. See them running?
4.  Run `docker compose down`. Watch them disappear.
""")

st.success("Next: We have built the software. Now, how do we save the code? Enter Git.")
st.page_link("pages/15_git_basics.py", label="Go to Git Basics", icon="🌿")
