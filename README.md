# pyzmq-playground

A tiny playground to experiment with **ZeroMQ pub/sub**, orchestration, and event-driven microservices — inspired by the Aiko platform style.

---

## What is this?

This project is a simple example of a **reactive distributed system**:
- **Orchestrator:** Starts and supervises the services.
- **Detector:** Pretends to be a sensor or TinyML module — publishes `object_detected` events at random.
- **Reactor:** Subscribes to the Detector’s events and reacts when something is actually detected.

It’s minimal on purpose — so you can understand:
- How **ZeroMQ PUB/SUB** works.
- How services can communicate asynchronously.
- How to coordinate small, single-purpose processes.

---

## Project structure
```
pyzmq-playground/
├── orchestrator.py            # Starts and supervises Detector & Reactor
├── detector.py                # Publishes fake detection events at random
├── reactor.py                 # Subscribes & reacts to detection events
├── requirements.txt           # pyzmq dependency
├── .gitignore                 # Excludes venv/ and pycache/
└── README.md                  # This document
```

---

## Getting started

**Create a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # or venv\Scripts\activate  # Windows PowerShell
```

**Install dependencies**
```
pip install -r requirements.txt
```

**Run the Orchestrator**
```
python3 orchestrator.py
```

**You should see:**
- The Detector saying “no detection” or “sending 'object_detected'”
- The Reactor reacting only when an event is actually sent

```
(venv) $ python3 orchestrator.py
Orchestrator: starting Detector and Reactor services...
Detector: publishing events on tcp://*:5556
Detector: sending 'object_detected'
Reactor: waiting for events...
Detector: no detection
Detector: sending 'object_detected'
Reactor: received 'object_detected' → reacting!
Detector: no detection
^C
Orchestrator: received Ctrl+C, shutting down...
Detector: stopped by user.

Reactor: stopped by user.
Orchestrator: all services stopped. Bye!
$
```
---


## Running with Docker 🐳

This playground is fully containerized so you can run it anywhere!

### Build & run (attached mode)

From your project root:
```bash
docker-compose up --build
```

- Builds the Docker image and starts the orchestrator.
- The orchestrator runs `detector.py` and `reactor.py` inside the container.
- **Logs are shown live in the same terminal** — thanks to Python’s unbuffered output.

Stop it anytime with `Ctrl+C` — the orchestrator will shut down the Detector & Reactor cleanly.

### Run in the background (detached mode)

```bash
docker-compose up --build -d
```

View logs:
```bash
docker-compose logs -f playground
```

Stop and remove the container:
```bash
docker-compose down
```

There is a helper script to do it for you.

**Note:** Always run these commands in the folder containing `docker-compose.yml`.

---
s
## How it works
- ZeroMQ PUB/SUB: The Detector binds a PUB socket on tcp://*:5556.
- The Reactor connects a SUB socket to tcp://localhost:5556.
- Event loop: The Detector runs forever, simulating a detection with a 30% chance every 5 seconds.
- Orchestration: The Orchestrator runs both services in separate processes and shuts them down gracefully with Ctrl+C.

---

## Next ideas

- Dockerize it [done]s
- Add another Reactor that logs events to a file or database.
- Build a simple web dashboard to trigger and visualize detections live.


---

## 📚 Inspired by
This playground is inspired by Andy Gelme’s [Aiko Platform](https://github.com/geekscape) — a reactive microservice approach for IoT and edge systems.

---

License

MIT — feel free to fork, extend, and play!

🎉 Happy hacking!