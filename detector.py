import zmq
import time
import random
import json
from datetime import datetime
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

context = zmq.Context()
push_addr = config['detector']['push']

publisher = context.socket(zmq.PUSH)
publisher.connect(push_addr)
print(f"Detector: PUSH connected to {push_addr}")

try:
    while True:
        time.sleep(2)
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
