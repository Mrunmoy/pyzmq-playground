# detector.py
import zmq
import time
import random
import json
from datetime import datetime

context = zmq.Context()
publisher = context.socket(zmq.PUSH)
publisher.connect("tcp://localhost:6000")
print("Detector: PUSH connected to tcp://localhost:6000")

try:
    while True:
        time.sleep(5)
        detected = random.random() < 0.3
        if detected:
            payload = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "event": "object_detected"
            }
            message = json.dumps(payload)
            publisher.send_string(message)
            print(f"Detector: sent {message}")
        else:
            print("Detector: no detection")
except KeyboardInterrupt:
    print("Detector: stopped.")
finally:
    publisher.close()
    context.term()
