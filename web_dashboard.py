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

# Load config
with open("config.yaml") as f:
    config = yaml.safe_load(f)

# Default values from YAML
push_addr = config['dashboard']['push']
sub_addr = config['dashboard']['sub']

# Override if ENV VAR is set
push_addr = os.getenv('DASHBOARD_PUSH_ADDR', push_addr)
sub_addr = os.getenv('DASHBOARD_SUB_ADDR', sub_addr)

print(f"Dashboard: PUSH → {push_addr}")
print(f"Dashboard: SUB → {sub_addr}")

ctx = zmq.asyncio.Context()

# SUB for incoming bus
subscriber = ctx.socket(zmq.SUB)
subscriber.connect(sub_addr)
subscriber.setsockopt_string(zmq.SUBSCRIBE, "")
print(f"Dashboard: SUB connected to {sub_addr}")

# PUSH for control commands
publisher = ctx.socket(zmq.PUSH)
publisher.connect(push_addr)
print(f"Dashboard: PUSH connected to {push_addr}")

app = FastAPI()
event_queue = asyncio.Queue()

@app.get("/")
async def get():
    html = Path("index.html").read_text()
    return HTMLResponse(content=html)

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
