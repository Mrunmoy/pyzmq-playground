# web_dashboard.py
import asyncio
import json
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse

import zmq
import zmq.asyncio

ZMQ_INPUT_ADDRESS = "tcp://localhost:5556"  # Unified bus for incoming events
ZMQ_PUSH_ADDRESS = "tcp://localhost:6001"   # Outgoing to Proxy

ctx = zmq.asyncio.Context()

# SUB socket for incoming bus
subscriber = ctx.socket(zmq.SUB)
subscriber.connect(ZMQ_INPUT_ADDRESS)
subscriber.setsockopt_string(zmq.SUBSCRIBE, "")
print(f"Dashboard: SUB connected to {ZMQ_INPUT_ADDRESS}")

# PUSH socket for control events
publisher = ctx.socket(zmq.PUSH)
publisher.connect(ZMQ_PUSH_ADDRESS)
print(f"Dashboard: PUSH connected to {ZMQ_PUSH_ADDRESS}")

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
            message = await event_queue.get()
            await websocket.send_text(message)
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
