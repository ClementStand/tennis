import streamlit as st
from src.dashboard.components.navigation import sidebar_navigation
from src.dashboard.components.mermaid import render_mermaid

st.set_page_config(page_title="Docker Compose", page_icon="📦", layout="wide")
sidebar_navigation()

st.title("📦 Docker Compose: The Conductor")

st.markdown("""
> **"One container is a solo artist. A system is an orchestra."**
> Docker Compose is the sheet music that keeps everyone playing in sync.
""")

# --- SECTION 1: ORCHESTRATION 101 ---
st.header("1. Orchestration 101: The Problem 😫")
st.markdown("Imagine you have a full application. It needs:")
st.markdown("""
1.  A **Python Backend** (API).
2.  A **Postgres Database** (Storage).
3.  A **Redis Cache** (Speed).
""")

st.markdown("Without Compose, you have to type this **every single time**:")
st.code("""
docker run -d --name my-db postgres
docker run -d --name my-redis redis
docker run -d --name my-app --link my-db --link my-redis -p 80:80 my-image
""", language="bash")

st.error("This is painful. It's hard to remember, hard to share, and hard to update.")

st.markdown("---")

# --- SECTION 2: THE SOLUTION (YAML) ---
st.header("2. The Solution: Infrastructure as Code 📄")
st.markdown("""
We write a file called `docker-compose.yml`.
This file describes the **Desired State** of your system.
""")

col_code, col_explain = st.columns([1, 1])

with col_code:
    st.code("""
    version: '3.8'  # The grammar version

    services:       # The list of instruments

      backend:      # Service Name (DNS Name)
        build: .    # Build from current folder
        ports:
          - "5000:5000"
        depends_on:
          - db      # Wait for DB to start
        environment:
          DB_HOST: db

      db:           # Service Name (DNS Name)
        image: postgres:13
        volumes:
          - pgdata:/var/lib/postgresql/data

    volumes:        # Persistent Storage
      pgdata:
    """, language="yaml")

with col_explain:
    st.markdown("""
    *   **Services**: The containers we want to run.
    *   **Build**: "Build this Dockerfile" (instead of just downloading an image).
    *   **Depends On**: "Don't start the Backend until the DB is ready."
    *   **Volumes**: "Create a named storage box called `pgdata` so we don't lose data when the DB restarts."
    *   **Magic DNS**: The backend can just connect to `host="db"`. Docker makes that name work automatically.
    """)

st.markdown("---")

# --- SECTION 3: THE LIFECYCLE ---
st.header("3. The Lifecycle: Up and Down 🔄")

st.markdown("Compose gives you simple commands to manage the entire orchestra.")

col1, col2, col3 = st.columns(3)
with col1:
    st.success("**docker-compose up**")
    st.markdown("Creates networks, volumes, builds images, and starts containers. **Everything.**")
with col2:
    st.warning("**docker-compose down**")
    st.markdown("Stops containers and **removes** them. It cleans up the network. (It keeps volumes safe).")
with col3:
    st.info("**docker-compose logs -f**")
    st.markdown("Follows the logs of *all* services in one stream. Great for debugging.")

st.markdown("---")

# --- SECTION 4: NETWORKING MAGIC ---
st.header("4. Networking Magic 🪄")
st.markdown("Compose automatically creates a **Shared Network** for your app.")

render_mermaid("""
graph LR
    subgraph Compose_Network ["myapp_default (Network)"]
        BE["Backend Service"]
        DB["Database Service"]
        Redis["Redis Service"]
    end

    BE <-->|can ping 'db'| DB
    BE <-->|can ping 'redis'| Redis
    DB <--> Redis
""", height=250)

st.markdown("You don't need to create a bridge manually. Compose does it for you.")

st.markdown("---")

# --- SECTION 5: EXERCISES ---
st.header("5. Exercises 📝")
st.info("""
1.  **Create**: Save the YAML above as `docker-compose.yml`.
2.  **Run**: `docker-compose up -d` (Detached mode, runs in background).
3.  **Check**: `docker-compose ps`. See them running?
4.  **Stop**: `docker-compose down`. Poof! They are gone.
""")
