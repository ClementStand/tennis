import streamlit as st
from src.dashboard.components.navigation import sidebar_navigation
from src.dashboard.components.mermaid import render_mermaid

st.set_page_config(page_title="Docker Compose", page_icon="📦", layout="wide")
sidebar_navigation()

st.title("📦 Docker Compose: The Conductor")

# --- LAYER 1: Intuition ---
st.header("1. Intuition: The Sheet Music 🎼")
st.markdown("""
*   **Docker Run**: Playing a solo. You have to manually start the drums, then the guitar, then the vocals.
*   **Docker Compose**: The Conductor's Score.
    *   "Start the Drums."
    *   "Start the Guitar."
    *   "Make sure they are on the same stage (Network)."
    *   "If the Drums crash, restart them."

It turns a manual process into a **Declarative** one. You describe *what* you want, not *how* to do it.
""")
st.markdown("---")

# --- LAYER 3: Structure ---
st.header("3. Structure: The YAML File 📄")
st.code("""
version: '3.8'
services:
  web:
    image: nginx
    ports:
      - "8080:80"
    depends_on:
      - db

  db:
    image: postgres
    environment:
      POSTGRES_PASSWORD: secret
""", language="yaml")

st.markdown("""
*   **Services**: The instruments (Containers).
*   **Networks**: The stage. (Compose creates a default network for you).
*   **Volumes**: The storage closet.
""")
st.markdown("---")

# --- LAYER 4: Step-by-Step ---
st.header("4. Step-by-Step: `docker-compose up` 👣")
st.markdown("""
1.  **Read**: Parse `docker-compose.yml`.
2.  **Network**: Create a new bridge network `myapp_default`.
3.  **Volumes**: Create persistent volumes.
4.  **Pull**: Download images if missing.
5.  **Start DB**: Start the database first (because `web` depends on it).
6.  **Start Web**: Start the web server.
7.  **DNS**: Add `db` and `web` to the internal DNS so they can find each other.
""")
st.markdown("---")

# --- LAYER 9: Exercises ---
st.header("9. Exercises 📝")
st.info("""
1.  **Create**: A file `docker-compose.yml` with the content above.
2.  **Run**: `docker-compose up`.
3.  **Verify**: Open `localhost:8080`.
4.  **Stop**: Press `Ctrl+C`.
5.  **Clean**: `docker-compose down`.
""")
