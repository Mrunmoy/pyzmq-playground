import zmq
from datetime import datetime

LOG_FILE = "/app/events.log"

context = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://localhost:5556")
subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

print("LoggerReactor: waiting for events...")

try:
    while True:
        message = subscriber.recv_string()
        timestamp = datetime.utcnow().isoformat()
        log_line = f"{timestamp} - {message}\\n"
        with open(LOG_FILE, "a") as f:
            f.write(log_line)
        print(f"LoggerReactor: wrote '{message}' to {LOG_FILE}")
except KeyboardInterrupt:
    print("LoggerReactor: stopped by user.")
finally:
    subscriber.close()
    context.term()
