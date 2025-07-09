import zmq
import zmq.asyncio
import asyncio

ctx = zmq.asyncio.Context()

# PULL sockets for incoming streams
detector_pull = ctx.socket(zmq.PULL)
detector_pull.bind("tcp://*:6000")
print("Orchestrator Proxy: PULL bound to tcp://*:6000 (Detector)")

dashboard_pull = ctx.socket(zmq.PULL)
dashboard_pull.bind("tcp://*:6001")
print("Orchestrator Proxy: PULL bound to tcp://*:6001 (Dashboard)")

# PUB socket for unified event bus
master_pub = ctx.socket(zmq.PUB)
master_pub.bind("tcp://*:5556")
print("Orchestrator Proxy: PUB bound to tcp://*:5556 (Event bus)")

async def relay(source_pull, name):
    while True:
        message = await source_pull.recv_string()
        print(f"Orchestrator Proxy: received from {name} → {message}")
        master_pub.send_string(message)

async def main():
    await asyncio.gather(
        relay(detector_pull, "Detector"),
        relay(dashboard_pull, "Dashboard")
    )

asyncio.run(main())
