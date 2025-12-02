import streamlit as st
from src.dashboard.components.navigation import sidebar_navigation
from src.dashboard.components.mermaid import render_mermaid

st.set_page_config(page_title="Docker Basics", page_icon="🐳", layout="wide")
sidebar_navigation()

st.title("🐳 Docker Basics: Images & Containers")
st.markdown("### The Magic of Isolation")

st.markdown("""
Now that we know a **Process** is just a program running on the OS, we can understand Docker.
Docker is **NOT** a Virtual Machine (VM). It doesn't start a whole new computer.
It is a way to run a Process with a **Mask** on, so it thinks it is the only thing in the world.
""")

# --- 1. TL;DR ---
st.info("""
**🚀 Big Picture (TL;DR)**

*   **Container**: A standard Process (like Python or Chrome) but isolated by the Kernel so it can't see other processes or files.
*   **Image**: A read-only template (The Recipe) used to create containers. It contains the OS files, code, and libraries.
*   **Dockerfile**: A text file with instructions to build an Image (The Recipe Card).
*   **Layers**: Images are built like a stack of transparency sheets. This makes them fast to download and build.
*   **Registry**: A library of images (like Docker Hub) where you can download recipes (e.g., `python`, `postgres`).
""")

st.markdown("---")

# --- 2. Intuition ---
st.header("1. Intuition: The Matrix & The Recipe 💊")

st.markdown("""
#### A. The Matrix (Namespaces)
Imagine you are a Process.
*   **Normal Process**: You walk down the street. You see other people (processes). You see the whole city (filesystem).
*   **Containerized Process**: The Kernel puts you in a **Simulation**.
    *   You look around: You are the *only* person on earth (PID Namespace).
    *   You look at the map: The city is different. It only has your house (Mount Namespace).
    *   You look at the clock: It might be a different timezone (UTS Namespace).
    *   **Reality**: You are still just a person walking on the same physical street, but your *perception* is completely controlled.

#### B. The Recipe & The Cake (Images vs Containers)
*   **The Image (Recipe)**: "Grandma's Chocolate Cake".
    *   It's just text and instructions. You can't eat it. You can email it to a friend.
    *   It is **Read-Only**. You don't scribble on the recipe card while baking.
*   **The Container (Cake)**: The physical cake in the oven.
    *   You create it *from* the recipe.
    *   You can bake 100 cakes from one recipe.
    *   If you burn one, you throw it away (delete container) and bake a new one. The recipe is safe.
""")

st.markdown("---")

# --- 3. Technical Mechanics ---
st.header("2. Technical Mechanics: Under the Hood")

st.subheader("A. How Isolation Works (Linux Primitives)")
st.markdown("""
Docker uses features already built into Linux. It just makes them easy to use.

1.  **Namespaces (Visibility)**: Controls what the process *sees*.
    *   **PID**: "I am Process #1." (Even if it's really Process #10543 on the host).
    *   **Network**: "I have my own IP address and ports."
    *   **Mount**: "I see a different root filesystem (`/`)."
2.  **Cgroups (Control Groups)**: Controls what the process *uses*.
    *   "You can only use 50% of the CPU."
    *   "You can only use 512MB of RAM."
    *   This prevents one container from crashing the whole server.
""")

st.subheader("B. The Union Filesystem (Layers)")
st.markdown("""
Docker Images are not big blobs. They are **Layers**.
Imagine clear plastic transparency sheets stacked on top of each other.

*   **Layer 1 (Base)**: Ubuntu OS files.
*   **Layer 2 (Add)**: Python executable.
*   **Layer 3 (Add)**: Your `app.py`.

When you look from the top, you see one combined picture.
**Why?** Efficiency. If you have 10 apps that use Python, they all **share** Layer 2. It's stored only once on disk!
""")

render_mermaid("""
graph BT
    subgraph Container ["Container (Writable)"]
        Layer4["Writable Layer (New Data/Logs)"]
    end

    subgraph Image ["Image (Read-Only)"]
        Layer3["Layer 3: Copy app.py"]
        Layer2["Layer 2: Install Python"]
        Layer1["Layer 1: Ubuntu Base"]
    end

    Layer4 --> Layer3
    Layer3 --> Layer2
    Layer2 --> Layer1
""", height=400)

st.markdown("---")

# --- 4. What Actually Happens When... ---
st.header("3. What Actually Happens When... 🕵️‍♂️")
st.markdown("Command: `docker run -p 5000:80 nginx`")

st.markdown("""
1.  **CLI**: You type the command. The Docker Client sends a JSON request to the **Docker Daemon** (background boss).
2.  **Check Image**: Daemon checks: "Do I have `nginx` locally?"
    *   *No?* Go to Docker Hub. Download the layers.
    *   *Yes?* Use the cache.
3.  **Create Container**:
    *   Daemon creates a read-write layer on top of the image.
    *   It prepares the **Namespaces** (The Matrix).
4.  **Networking**:
    *   It creates a virtual network cable (`veth` pair).
    *   One end plugs into the container, the other into the `docker0` bridge.
    *   It assigns an internal IP (e.g., `172.17.0.2`).
    *   It sets up a **NAT Rule**: "Traffic on Host Port 5000 -> Container Port 80".
5.  **Start**:
    *   Daemon calls the Kernel: "Start `nginx` process, but wrap it in these Namespaces and Cgroups."
6.  **Run**:
    *   Nginx starts. It thinks it is PID 1. It thinks it has its own network. It listens on Port 80.
""")

st.markdown("---")

# --- 5. The Dockerfile ---
st.header("4. The Dockerfile")
st.markdown("How do we create our own recipes? We write a `Dockerfile`.")

col1, col2 = st.columns(2)

with col1:
    st.code("""
    # 1. The Base (Plate)
    FROM python:3.9-slim

    # 2. Setup (Bowl)
    WORKDIR /app

    # 3. Ingredients
    COPY requirements.txt .
    RUN pip install -r requirements.txt

    # 4. The Code
    COPY . .

    # 5. Bake
    CMD ["python", "app.py"]
    """, language="dockerfile")

with col2:
    st.markdown("""
    **Explanation:**
    1.  **FROM**: Start with a pre-made OS + Python image.
    2.  **WORKDIR**: Create a folder `/app` inside the image and go there.
    3.  **COPY/RUN**: Copy the dependency list and install them. *This creates a cached layer.*
    4.  **COPY**: Copy your actual code.
    5.  **CMD**: The default command to run when the container starts.
    """)

st.markdown("---")

# --- 6. Practical Commands ---
st.header("5. Practical Commands")

st.markdown("""
*   `docker build -t my-app .`: Read Dockerfile, bake the image, name it `my-app`.
*   `docker run -d -p 5000:5000 my-app`: Run the image in background (`-d`), mapping ports.
*   `docker ps`: List running containers (The Oven).
*   `docker images`: List available images (The Recipe Book).
*   `docker logs <container_id>`: See what the process printed to stdout.
*   `docker exec -it <container_id> bash`: Teleport inside the container (open a shell inside the Matrix).
""")

st.markdown("---")

# --- 7. FAQ & Exercises ---
st.header("6. FAQ & Exercises")

with st.expander("Q: Do containers persist data?"):
    st.markdown("""
    **No.** By default, if you delete a container, the "Writable Layer" is destroyed.
    To save data (like a database), you must use **Volumes** (we will cover this next).
    """)

with st.expander("Q: Why is Docker better than a VM?"):
    st.markdown("""
    **Speed and Size.**
    *   **VM**: Has a full OS kernel inside. Takes minutes to boot. GBs in size.
    *   **Container**: Shares the Host Kernel. Starts in milliseconds. MBs in size.
    """)

st.info("""
**🧠 Try it yourself:**
1.  Run `docker run hello-world`.
2.  Read the output. It explains exactly what happened!
3.  Run `docker ps -a`. You will see the container is "Exited". It ran, finished its job, and stopped.
""")

st.success("Next: The most confusing part... Networking. IPs, Ports, and Bridges.")
st.page_link("pages/13_docker_networking.py", label="Go to Docker Networking", icon="🌐")
