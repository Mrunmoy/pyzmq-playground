import zmq
import zmq.asyncio
import asyncio
import yaml

# Load config
with open("config.yaml") as f:
    config = yaml.safe_load(f)

ctx = zmq.asyncio.Context()

# Bind PULL sockets
detector_addr = config['proxy']['detector_pull']
dashboard_addr = config['proxy']['dashboard_pull']
unified_pub_addr = config['bus']['unified_pub']

detector_pull = ctx.socket(zmq.PULL)
detector_pull.bind(detector_addr)
print(f"Proxy: PULL bound to {detector_addr} (Detector)")

dashboard_pull = ctx.socket(zmq.PULL)
dashboard_pull.bind(dashboard_addr)
print(f"Proxy: PULL bound to {dashboard_addr} (Dashboard)")

# PUB socket for unified bus
master_pub = ctx.socket(zmq.PUB)
master_pub.bind(unified_pub_addr)
print(f"Proxy: PUB bound to {unified_pub_addr} (Event bus)")

async def relay(source_pull, name):
    while True:
        msg = await source_pull.recv_string()
        print(f"Proxy: relaying from {name} → {msg}")
        master_pub.send_string(msg)

async def main():
    await asyncio.gather(
        relay(detector_pull, "Detector"),
        relay(dashboard_pull, "Dashboard")
    )

asyncio.run(main())
