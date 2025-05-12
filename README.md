# 📦 3D Logistics Simulation

A three-dimensional logistics simulation that models the efficient arrangement of boxes inside a container using autonomous forklift agents. The system employs 3D bin packing algorithms and movement heuristics within a visually realistic environment, rendered through two versions: an OpenGL-based native renderer and a React Three Fiber web visualization.

## 🌟 Project Purpose

This project was developed to:

- Simulate a realistic logistics environment with background buildings, warehouse, and transport truck.
- Represent the optimal arrangement of boxes of various sizes inside a container, prioritizing stability and space efficiency.
- Visualize autonomous forklift agents executing concurrent tasks.
- Explore integration between computational logic (Julia, Python) and rendering engines (OpenGL, React Three).

This simulation serves as an educational and demonstrative tool for understanding agent-based simulations, optimization algorithms, and interactive 3D rendering.

---

## 🛠️ Technologies Used

### Backend and Packing Logic
- **Python + Flask** — REST API to connect packing logic with graphical simulators
- **Julia + Agents.jl** — Agent modeling and movement logic
- **3D-Bin-Packing Python Library** — External algorithm for 3D box arrangement
### Graphics and Simulation
- **OpenGL/PyGame (Python)** — Full 3D simulation with textured environment and free camera
- **React + Three Fiber (JS)** — Web visualization focused on logic and monitoring
### Project Tools
- Git + Bitbucket — Version control

---

## ⚙️ Features

- 3D simulation with animated forklifts, buildings, and container.
- Free camera control (WASD, arrows, `e/r` to follow forklifts).
- Transparent container for observing final arrangement.
- Autonomous forklift logic with priorities and state management.
- Three box types: 10x10x10, 50x50x50, 70x70x70.
- Post-processing of the packing result for visualization.

---

## 🧩 Project Structure

```
/cajas-kaggu
├── 3D-bin-packing/         # Python logic using 3DBinPacking
│   └── api.py              # Flask API with /setItemAndBox endpoint
├── Julia/                  # Agent and movement logic in Julia
│   └── webapi.jl           # Julia ↔ Python API and simulation bridge
├── OpenGL/                 # 3D native simulation
│   ├── main.py             # Main render script
│   ├── ClaseMontacarga.py  # Forklift agent class
│   ├── ClaseCaja.py        # Box behavior class
│   └── Ambiente.py         # Environment and textures
├── kaggu-fe/               # Web interface with React Three
│   ├── public/             # Static assets
│   └── src/                # Components and simulation logic
└── README.md               # Project documentation
```

---

## 🚀 How to Run

### 🔹 OpenGL (Full Simulation)
```bash
git clone https://bitbucket.org/proyectos-tec-itc/cajas-kaggu
cd cajas-kaggu
git checkout main
cd 3D-bin-packing && pip install -r requirements.txt && python api.py
cd ../Julia && julia webapi.jl
cd ../OpenGL && python main.py
```

### 🔹 React Three (Web Version)
```bash
git clone https://bitbucket.org/proyectos-tec-itc/cajas-kaggu
cd cajas-kaggu
git checkout luc_entrega
cd kaggu-fe
npm install
npm run dev
```

---

## 🧪 Testing & Quality

- Pathfinding validation and collision control for agents.
- Visual rendering tests (textures, 3D objects, sync with Julia).
- Modular and structured file organization.
- Manual testing of box arrangement logic with varied inputs.

---

## 👥 Team & Credits

Developed by students from Tecnológico de Monterrey, Campus Puebla:

- 🎓 Jonathan Arredondo
- 🎓 Kevin Núñez
- 🎓 Rusbel Morales
- 🎓 Pablo Coca

---

## 📄 License

This project was developed for educational purposes. All rights reserved by the authors and Tecnológico de Monterrey unless stated otherwise.
