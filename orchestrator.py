import subprocess
import time

print("Orchestrator: starting Detector and Reactor services...")

# Start Detector
detector_process = subprocess.Popen(["python3", "detector.py"])

# Start Reactor
reactor_process = subprocess.Popen(["python3", "reactor.py"])

# Start Event Logger Reactor
logger_reactor = subprocess.Popen(["python3", "logger_reactor.py"])
print(f"Started LoggerReactor, PID={logger_reactor.pid}", flush=True)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nOrchestrator: received Ctrl+C, shutting down...")
    detector_process.terminate()
    reactor_process.terminate()
    logger_reactor.terminate()
    detector_process.wait()
    reactor_process.wait()
    logger_reactor.wait()
    print("Orchestrator: all services stopped. Bye!")
