import zmq

# 1. Create ZeroMQ context
context = zmq.Context()

# 2. Create a SUB socket
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://localhost:5556")  # Same port as Detector
subscriber.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all messages

print("Reactor: waiting for events...")

try:
    while True:
        message = subscriber.recv_string()
        print(f"Reactor: received '{message}' → reacting!")
except KeyboardInterrupt:
    print("\nReactor: stopped by user.")
finally:
    subscriber.close()
    context.term()
