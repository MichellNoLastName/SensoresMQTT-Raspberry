# 🌐 Interfaz Gráfica MQTT con Sensores y Actuadores

Este proyecto implementa una interfaz gráfica en Python (usando `tkinter`) que permite:

- Visualizar datos de sensores conectados a un ESP32.
- Controlar actuadores como un servomotor y una matriz LED.
- Consultar coordenadas GPS y visualizar mapas estáticos desde Google Maps.
- Recibir alertas en tiempo real desde sensores de gas y proximidad.

---

## 🛠️ Tecnologías Usadas

| Tecnología | Descripción |
|-----------|-------------|
| 🐍 Python | Lenguaje principal |
| 📡 MQTT | Comunicación con ESP32 |
| 📷 OpenCV | Visualización de mapas |
| 🌐 Google Maps API | Mapa estático con coordenadas |
| 🪟 Tkinter | Interfaz gráfica |
| 💡 Sensores | DHT11, BH1750, DS18B20, HMC5883L, MQ9, LJ12A3 |

---

## 📦 Estructura del Proyecto

.
├── imageMaps.py
├── maps.py
├── main.py
├── GPSImage/
│ └── imageGPS.jpg
└── README.md

## 🧩 Características Principales

### 🔍 Monitoreo de Sensores

- Fecha y hora (GPS)
- Temperatura (DS18B20)
- Luminosidad (BH1750)
- Humedad (DHT11)
- Brújula (HMC5883L)
- Sensor Hall (ESP32 interno)
- Gas (MQ9) - ⚠️ *Genera alerta emergente*
- Proximidad metálica (LJ12A3) - ℹ️ *Genera alerta emergente*

### 🛰️ GPS y Google Maps

- Muestra coordenadas y altitud.
- Obtiene la dirección con `reverse geocoding`.
- Abre una imagen del mapa estático usando la API de Google Maps.

### 🕹️ Control de Actuadores

- **Servomotor**: Control por ángulo (0° a 180°).
- **Matriz LED**: Control de caracteres (`A` a `D`, `0` a `9`), más botón para limpiar.

### 🚨 Alertas Emergentes

- Gas LP / Monóxido (MQ9)
- Objeto metálico cercano (LJ12A3)

