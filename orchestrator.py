# orchestrator.py
import subprocess
import time

print("Orchestrator: starting Proxy, Detector, Reactor, and LoggerReactor services...")

# Start Orchestrator Proxy
proxy_process = subprocess.Popen(["python3", "orchestrator_proxy.py"])
print(f"Started Orchestrator Proxy, PID={proxy_process.pid}", flush=True)

# Start Detector
detector_process = subprocess.Popen(["python3", "detector.py"])
print(f"Started Detector, PID={detector_process.pid}", flush=True)

# Start Reactor
reactor_process = subprocess.Popen(["python3", "reactor.py"])
print(f"Started Reactor, PID={reactor_process.pid}", flush=True)

# Start Logger Reactor
logger_reactor_process = subprocess.Popen(["python3", "logger_reactor.py"])
print(f"Started LoggerReactor, PID={logger_reactor_process.pid}", flush=True)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nOrchestrator: received Ctrl+C, shutting down...")

    proxy_process.terminate()
    detector_process.terminate()
    reactor_process.terminate()
    logger_reactor_process.terminate()

    proxy_process.wait()
    detector_process.wait()
    reactor_process.wait()
    logger_reactor_process.wait()

    print("Orchestrator: all services stopped. Bye!")
