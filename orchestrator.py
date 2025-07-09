# orchestrator.py
import subprocess
import time
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

processes = []

def start_process(script, name):
    print(f"Orchestrator: starting {name} ({script})")
    p = subprocess.Popen(["python3", script])
    processes.append(p)
    print(f"  PID={p.pid}")

# Always start the Proxy
start_process(config['proxy']['file'], "Proxy")

# Always start the Detector
start_process(config['detector']['file'], "Detector")

# Start all Reactors from list
for reactor in config['reactors']:
    start_process(reactor['file'], f"Reactor ({reactor['name']})")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nOrchestrator: received Ctrl+C, shutting down...")
    for p in processes:
        p.terminate()
    for p in processes:
        p.wait()
    print("Orchestrator: all services stopped. Bye!")
