import zmq
import time
import random

context = zmq.Context()
publisher = context.socket(zmq.PUB)
publisher.bind("tcp://*:5556")

print("Detector: publishing events on tcp://*:5556")

try:
    while True:
        # Fake a detection with 30% probability
        if random.random() < 0.3:
            message = "object_detected"
            print(f"Detector: sending '{message}'")
            publisher.send_string(message)
        else:
            print("Detector: no detection")
        
        time.sleep(5)
except KeyboardInterrupt:
    print("\nDetector: stopped by user.")
finally:
    publisher.close()
    context.term()
