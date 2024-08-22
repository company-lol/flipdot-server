# 📦 Flipdot Sign API

Welcome to the **Flipdot Sign API**! This repository contains a lightweight HTTP server for pushing JSON-serialized numpy arrays directly to the Hanover flipdot display. This project is designed to be simple, efficient, and user-friendly, allowing you to interface easily with the flipdot display using Python 3. 🚀

---

## 📜 Summary of Project

The Flipdot Sign API allows users to send pixel data to a Hanover flipdot display through a dedicated API endpoint (`/api/dots`). This API leverages the `pyflidot` library for communication with the display. By posting a JSON-encoded numpy array, users can control what is displayed on the flipdot.

### Key Features
- Easy-to-use JSON API for sending pixel data.
- Built-in simulator for debugging without physical hardware.
- Docker support for easy deployment and management.
- Configuration via a straightforward INI file format.

---

## ⚙️ How to Use

### Prerequisites
- Python 3.12 or higher installed.
- Docker (optional, but recommended for easier setup).

### Getting Started

1. **Clone the Repository**
   ```bash
   git clone https://github.com/harperreed/flipdot-server.git
   cd flipdot-server
   ```

2. **Edit the Configuration File**
   Copy the example configuration and update it according to your setup:
   ```bash
   cp config.ini.example config.ini
   vi config.ini
   ```
   Ensure you have the correct values for:
   ```ini
   [SERVER]
   HOST = 0.0.0.0
   PORT = 8080

   [FLIPDOTSIGN]
   COLUMNS = 96
   ROWS = 16
   ADDRESS = 1
   USB = "/dev/ttyUSB0"
   SIMULATOR = True
   ```

3. **Run the Server**
   - **Option 1: Local Installation**
   ```bash
   pip3 install -r requirements.txt
   python3 app.py
   ```
   - **Option 2: Using Docker**
   Ensure your Docker service is running, then execute:
   ```bash
   docker-compose build
   docker-compose up
   ```
   If connecting to a USB serial adapter, edit `docker-compose.yml` to uncomment and modify the device entry.

4. **Testing the API**
   You can test the API using cURL:
   ```bash
   curl -X POST -H "Content-Type: application/json" -d @nparray_test.json http://localhost:8080/api/dots
   ```

5. **Creating Numpy Arrays**
   To create a numpy array representing the flipdot's pixel matrix, refer to the example code snippet provided in the README.

### Example Code
```python
import numpy as np
import requests
import json

sign_columns = 96
sign_rows = 16

image_array = np.zeros((sign_rows, sign_columns), dtype=bool)  # False by default
image_array[0][0] = True  # Set a pixel

url = "http://localhost:8080/api/dots"
headers = {'Content-type': 'application/json'}
r = requests.post(url, data=json.dumps(image_array.tolist()), headers=headers)
```

---

## 💻 Tech Info

### Technologies Used
- **Python**: The primary programming language.
- **aiohttp**: Asynchronous web framework for handling requests.
- **numpy**: To handle pixel data in array format.
- **pyflipdot**: Library to interface with Hanover flipdot signs.
- **Docker**: For containerization and easier deployment.
- **Markdown2**: For rendering README documentation in HTML.

### Repository Structure
```
flipdot-server/
├── Dockerfile
├── LICENSE
├── README.md
├── app.py
├── config.ini.example
├── docker-compose.yml
├── flipdot/
│   ├── __init__.py
│   └── simulator.py
├── nparray_test.json
└── requirements.txt
```

---

We hope you find this project useful! If you have any suggestions, issues or would like to contribute, don't hesitate to reach out. Let's light up those flipdots! 💡
