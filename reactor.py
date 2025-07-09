import zmq
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

# Find the generic print reactor
print_reactor = next(r for r in config['reactors'] if r['type'] == 'print')

context = zmq.Context()
sub_addr = print_reactor['sub']

subscriber = context.socket(zmq.SUB)
subscriber.connect(sub_addr)
subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

print(f"Reactor: SUB connected to {sub_addr}")
print("Reactor: waiting for events...")

try:
    while True:
        message = subscriber.recv_string()
        print(f"Reactor: received → {message}")
except KeyboardInterrupt:
    print("Reactor: stopped.")
