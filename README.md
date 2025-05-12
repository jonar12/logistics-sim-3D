# 📦 Simulación Logística 3D

Simulación logística tridimensional que modela el acomodo eficiente de cajas en un contenedor de una van de entrega de ultima milla mediante agentes montacargas autónomos. El sistema emplea algoritmos de empaquetado (3D-Bin-Packing) y heurísticas de movimiento en un entorno gráfico realista, utilizando dos versiones de visualización: una renderizada con OpenGL y otra basada en React Three para la web.

## 🌟 Propósito del Proyecto

Este proyecto fue desarrollado para:

- Simular un entorno logístico realista con ambientación, almacén y camión de transporte.
- Representar el acomodo óptimo de cajas de distintos tamaños en un contenedor, priorizando estabilidad y aprovechamiento del espacio.
- Visualizar la lógica de comportamiento de múltiples montacargas autónomos ejecutando tareas concurrentes.
- Explorar la integración entre algoritmos computacionales (Julia, Python) y motores gráficos (OpenGL, React Three).

Esta simulación sirve como herramienta educativa y demostrativa para entender simulaciones basadas en agentes, algoritmos de optimización, y renderizado 3D interactivo.

---

## 🛠️ Tecnologías Utilizadas

### Backend y Lógica de Empaquetado
- **Python + Flask** — API REST para comunicar la lógica de empaquetado con simuladores gráficos
- **Julia + Agents.jl** — Modelado de agentes montacargas y lógica de movimiento
- **3D-Bin-Packing** — Algoritmo externo para el acomodo óptimo de cajas tridimensionales

### Visualización Gráfica
- **OpenGL (Python)** — Simulación 3D nativa con ambientación completa, cámara libre y renderizado de texturas
- **React + Three Fiber (JS)** — Visualización web enfocada en la lógica del acomodo y monitoreo simplificado

### Herramientas de Proyecto
- Pygame + PyOpenGL — Entorno gráfico y manejo de cámara

---

## ⚙️ Características

- Simulación 3D con edificios, almacén y montacargas animados.
- Control de cámara libre (teclas `WASD`, flechas, `e/r` para seguir montacargas).
- Visualización transparente del contenedor para observar el acomodo.
- Lógica de movimiento autónomo con prioridades y estados de los montacargas.
- Variación de cajas (10x10x10, 50x50x50, 70x70x70) con posiciones finales calculadas.
- Posprocesamiento visual del resultado de empaquetado.

---

## 🧩 Estructura del Código

```
/cajas-kaggu
├── 3D-bin-packing/         # Lógica de acomodo en Python usando 3DBinPacking
│   └── api.py              # API Flask con endpoint /setItemAndBox
├── Julia/                  # Lógica de agentes y movimiento en Julia
│   └── webapi.jl           # Conexión Julia ↔ Python API y simulación
├── OpenGL/                 # Simulación 3D con cámara libre
│   ├── main.py             # Script principal de visualización
│   ├── ClaseMontacarga.py  # Modelado de agente
│   ├── ClaseCaja.py        # Modelado de cajas
│   └── Ambiente.py         # Ambientación, texturas y entorno 3D
├── kaggu-fe/               # Interfaz Web con React Three
│   ├── public/             # Archivos estáticos
│   └── src/                # Componentes y lógica de simulación
└── README.md               # Documentación del proyecto
```

---

## 🚀 Instrucciones de Ejecución

### 🔹 OpenGL (Versión Completa)
```bash
git clone https://bitbucket.org/proyectos-tec-itc/cajas-kaggu
cd cajas-kaggu
git checkout main
cd 3D-bin-packing && pip install -r requirements.txt && python api.py
cd ../Julia && julia webapi.jl
cd ../OpenGL && python main.py
```

### 🔹 React Three (Versión Web)
```bash
git clone https://bitbucket.org/proyectos-tec-itc/cajas-kaggu
cd cajas-kaggu
git checkout luc_entrega
cd kaggu-fe
npm install
npm run dev
```

---

## 🧪 Pruebas & Calidad

- Validación de trayectorias de los agentes con control de colisiones y límites.
- Pruebas de renderizado visual (texturas, objetos 3D, sincronización con Julia).
- Modularidad y separación de responsabilidades por archivo.
- Pruebas manuales de la lógica de acomodo con múltiples combinaciones de cajas.

---

## 👥 Equipo y Créditos

Desarrollado por estudiantes del Tecnológico de Monterrey, Campus Puebla:

- 🎓 Jonathan Arredondo
- 🎓 Kevin Núñez
- 🎓 Rusbel Morales
- 🎓 Pablo Coca
---

## 📄 Licencia

Este proyecto fue realizado con fines educativos. Todos los derechos pertenecen a los autores y al Tecnológico de Monterrey, salvo que se indique lo contrario.
