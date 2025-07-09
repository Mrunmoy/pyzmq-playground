import zmq
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

# Find the logger reactor entry
logger_config = next(r for r in config['reactors'] if r['type'] == 'logger')

context = zmq.Context()
sub_addr = logger_config['sub']
log_file = logger_config['log_file']

subscriber = context.socket(zmq.SUB)
subscriber.connect(sub_addr)
subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

print(f"LoggerReactor: SUB connected to {sub_addr}")
print(f"LoggerReactor: logging to {log_file}")

with open(log_file, "a") as f:
    try:
        while True:
            message = subscriber.recv_string()
            f.write(message + "\n")
            f.flush()
            print(f"LoggerReactor: {message}")
    except KeyboardInterrupt:
        print("LoggerReactor: stopped.")
