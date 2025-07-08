import subprocess
import time

print("Orchestrator: starting Detector and Reactor services...")

# Start Detector
detector_process = subprocess.Popen(["python3", "detector.py"])

# Start Reactor
reactor_process = subprocess.Popen(["python3", "reactor.py"])

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nOrchestrator: received Ctrl+C, shutting down...")
    detector_process.terminate()
    reactor_process.terminate()
    detector_process.wait()
    reactor_process.wait()
    print("Orchestrator: all services stopped. Bye!")
