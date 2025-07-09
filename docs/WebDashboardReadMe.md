# `web_dashboard.py` — Annotated Walkthrough

This document explains each section of your **FastAPI + WebSocket + ZeroMQ Dashboard** so you always know what’s happening and can tweak it with confidence.

---

## What does `web_dashboard.py` do?

- Hosts a **FastAPI web server** for the UI (served at `/`).
- Opens a **WebSocket** at `/ws` to stream live events to the browser.
- Subscribes to the **ZeroMQ unified PUB bus** to receive real-time events.
- Provides an HTTP `/trigger` endpoint so you can send control events from buttons.
- Uses **YAML config** + optional **ENV overrides** for multi-environment support.

---

## High-level code sections

### 1️⃣ **Imports**

```python
import asyncio
import json
from datetime import datetime
from pathlib import Path
import os

from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse

import zmq
import zmq.asyncio
import yaml
```

- 🟢 `asyncio` → run background event loop for ZeroMQ.
- 🟢 `os` → read ENV vars for multi-env overrides.
- 🟢 `zmq.asyncio` → non-blocking PUB/SUB.
- 🟢 `FastAPI` → web server, HTTP endpoints, WebSocket.
- 🟢 `yaml` → read `config.yaml`.

---

### **Load config + ENV overrides**

```python
with open("config.yaml") as f:
    config = yaml.safe_load(f)

# Get addresses from YAML
push_addr = config['dashboard']['push']
sub_addr = config['dashboard']['sub']

# Override with ENV if set
push_addr = os.getenv('DASHBOARD_PUSH_ADDR', push_addr)
sub_addr = os.getenv('DASHBOARD_SUB_ADDR', sub_addr)

print(f"Dashboard: PUSH → {push_addr}")
print(f"Dashboard: SUB → {sub_addr}")
```

- 🟢 Loads ZeroMQ addresses for PUSH (control events) and SUB (live bus).
- 🟢 Allows Docker to override with container hostnames.

---

### **Setup ZeroMQ sockets**

```python
ctx = zmq.asyncio.Context()

# SUB socket for incoming events
subscriber = ctx.socket(zmq.SUB)
subscriber.connect(sub_addr)
subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

# PUSH socket for sending control events
publisher = ctx.socket(zmq.PUSH)
publisher.connect(push_addr)
```

- 🟢 `subscriber` listens for events from Proxy PUB.
- 🟢 `publisher` sends `/trigger` button events to Proxy PULL.

---

### **FastAPI app + shared event queue**

```python
app = FastAPI()
event_queue = asyncio.Queue()
```

- 🟢 `event_queue` buffers new events → feeds WebSocket.

---

### **Root route → serves HTML**

```python
@app.get("/")
async def get():
    html = Path("index.html").read_text()
    return HTMLResponse(content=html)
```

- 🟢 When you open `/` → you get the Dashboard UI.
- 🟢 Keep your `index.html` separate for easy edits.

---

### **WebSocket `/ws` → push live events**

```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Dashboard: WebSocket connected.")
    try:
        while True:
            msg = await event_queue.get()
            await websocket.send_text(msg)
    except Exception as e:
        print(f"Dashboard: WebSocket closed: {e}")
    finally:
        await websocket.close()
```

- 🟢 Keeps sending any new event from the `event_queue` to the browser.
- 🟢 Runs forever until client disconnects.

---

### **HTTP `/trigger` → send control event**

```python
@app.post("/trigger")
async def trigger_event(request: Request):
    data = await request.json()
    event_name = data.get("event")
    if not event_name:
        return {"status": "error", "message": "Missing event name"}

    payload = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event": event_name
    }
    message = json.dumps(payload)
    publisher.send_string(message)
    print(f"Dashboard: sent control event → {message}")
    return {"status": "success"}
```

- 🟢 Buttons in `index.html` make `POST` requests here.
- 🟢 Creates a JSON payload with timestamp → `PUSH`es to Proxy.

---

### **On startup → background SUB loop**

```python
@app.on_event("startup")
async def start_subscriber():
    print("Dashboard: Starting ZeroMQ SUB loop.")
    async def sub_loop():
        while True:
            raw = await subscriber.recv_string()
            try:
                data = json.loads(raw)
                pretty = f"{data['timestamp']} — {data['event']}"
                await event_queue.put(pretty + "\n")
            except json.JSONDecodeError:
                await event_queue.put(raw + "\n")
    asyncio.create_task(sub_loop())
```

- 🟢 When FastAPI starts, it spawns a background task.
- 🟢 Listens for new ZeroMQ messages → puts them in the queue.
- 🟢 WebSocket clients get them instantly!

---

## What makes it robust?

✔️ Configurable for local + Docker with ENV overrides.  
✔️ Non-blocking async for both ZeroMQ and WebSocket.  
✔️ Simple to expand → add more buttons, routes, or event formats.  
✔️ Logs every step → you know when connections open, events push, or sockets fail.

---
