import streamlit as st
from src.dashboard.components.navigation import sidebar_navigation
from src.dashboard.components.mermaid import render_mermaid

st.set_page_config(page_title="Docker Advanced", page_icon="🚀", layout="wide")
sidebar_navigation()

st.title("🚀 Docker Advanced: System & Scale")

# --- SECTION 1: DOCKER SYSTEM ---
st.header("1. Docker System: Under the Hood 🔧")
st.markdown("""
Where does Docker store everything?
It uses a **Layered Filesystem** in `/var/lib/docker`.
""")

col1, col2, col3 = st.columns(3)
with col1:
    st.info("**Images**")
    st.markdown("Read-Only layers. Stored in `/var/lib/docker/images`.")
with col2:
    st.warning("**Containers**")
    st.markdown("Writable layers. Stored in `/var/lib/docker/containers`.")
with col3:
    st.success("**Volumes**")
    st.markdown("Persistent Data. Stored in `/var/lib/docker/volumes`.")

st.subheader("Data Persistence: Volumes")
st.markdown("Containers are ephemeral. If you delete them, data dies. **Volumes** save data.")

tab_vol, tab_bind = st.tabs(["Docker Volumes", "Bind Mounts"])

with tab_vol:
    st.markdown("**Managed by Docker.** Best for databases.")
    st.code("""
# Create
docker volume create my-data

# Use
docker run -v my-data:/var/lib/mysql mysql
    """, language="bash")

with tab_bind:
    st.markdown("**Managed by You.** Maps a folder on your laptop to the container. Best for code.")
    st.code("""
# Map current folder ($PWD) to /app
docker run -v $(pwd):/app python-app
    """, language="bash")

# --- SECTION 2: DOCKER HUB ---
st.header("2. Docker Hub: The App Store 🛒")
st.markdown("How do you share your images with the world?")

st.code("""
# 1. Login
docker login

# 2. Tag (Rename your image)
# Format: username/repository:tag
docker tag my-app oscar/tennis-app:v1

# 3. Push (Upload)
docker push oscar/tennis-app:v1

# 4. Pull (Download on another machine)
docker pull oscar/tennis-app:v1
""", language="bash")

st.markdown("**Private Repositories**: You can create private repos on Docker Hub (like private GitHub repos) to keep code safe.")

# --- SECTION 3: ORCHESTRATION ---
st.header("3. Orchestration: Scaling Up 🎼")
st.markdown("""
Docker Compose is great for **one** machine.
But what if you have **100 servers**? You need **Orchestration**.
""")

col_swarm, col_k8s = st.columns(2)

with col_swarm:
    st.subheader("Docker Swarm")
    st.markdown("""
    *   **Built-in**: Comes with Docker.
    *   **Simple**: Easy to set up.
    *   **Concepts**: Manager Nodes & Worker Nodes.
    """)
    st.code("docker swarm init", language="bash")

with col_k8s:
    st.subheader("Kubernetes (K8s)")
    st.markdown("""
    *   **The Standard**: Used by Google, Amazon, everyone.
    *   **Powerful**: Auto-scaling, Self-healing, Rolling updates.
    *   **Complex**: Steep learning curve.
    """)
    st.markdown("*   **Pods**: Groups of containers.")
    st.markdown("*   **Services**: Networking for Pods.")

# --- SECTION 4: EXERCISES ---
st.header("4. Exercises 📝")
st.info("""
1.  **Volume**: Create a volume. Run a container that writes a file to it. Delete container. Run new container with same volume. Is the file there?
2.  **Hub**: Tag an image with your username. Push it (if you have an account).
3.  **System**: Explore `/var/lib/docker` (if you are on Linux) or use `docker system df` to see disk usage.
""")
