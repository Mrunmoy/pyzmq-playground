# `index.html` — Dashboard UI Walkthrough

This document explains your simple Dashboard HTML file, which connects to your FastAPI WebSocket backend and lets you control + view your ZeroMQ playground in real time.

---

## What does it do?

- Opens a **WebSocket connection** to `/ws` on page load.
- Displays incoming events in a `<pre>` box.
- Has buttons to send control events (e.g., `force_detect`) to the backend via `/trigger` POST requests.

---

## Code Sections

---

## **HTML Skeleton**

```html
<!DOCTYPE html>
<html>
<head>
    <title>pyzmq-playground Dashboard</title>
    <style>
        body { font-family: sans-serif; }
        #log { background: #111; color: #0f0; padding: 1em; height: 300px; overflow-y: scroll; white-space: pre; }
        button { margin: 5px; padding: 10px; }
    </style>
</head>
<body>
    ...
</body>
</html>
```

- Simple, minimal page.
- `#log` is your log box → shows incoming events with a nice scrolling area.
- Basic styling for a terminal-like look.

---

## **Log Box & Buttons**

```html
<h1>pyzmq-playground Dashboard</h1>

<div id="log"></div>

<button onclick="sendEvent('force_detect')">Force Detect</button>
<button onclick="sendEvent('force_alert')">Force Alert</button>
```

- `#log` → where your WebSocket appends events.
- Each button calls `sendEvent()` with a custom event name → you can add more as needed.

---

## **WebSocket Connection**

```html
<script>
    const ws = new WebSocket(`ws://${location.host}/ws`);

    ws.onopen = () => {
        logMessage('WebSocket connected!');
    };

    ws.onmessage = (event) => {
        logMessage(event.data);
    };

    ws.onclose = () => {
        logMessage('WebSocket closed.');
    };

    function logMessage(msg) {
        const log = document.getElementById('log');
        log.textContent += msg;
        log.scrollTop = log.scrollHeight;
    }
```

- Connects to `/ws` → same host & port as your Dashboard backend.
- When it receives a message, it appends it to the `#log` div.
- Auto-scrolls so you always see the latest message.

---

## **Trigger Event Function**

```html
    async function sendEvent(eventName) {
        await fetch('/trigger', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ event: eventName })
        });
        logMessage(`Triggered: ${eventName}\n`);
    }
</script>
```

- Calls `/trigger` HTTP endpoint with `{ event: "force_detect" }` (or whatever).
- The backend `web_dashboard.py` picks it up, wraps it in a timestamped JSON, and sends it into the bus.
- Adds an immediate log entry so you see that the button worked.

---

## Tips for tweaking

- Add more buttons → copy one, change `eventName`.
- Style the log box how you like → colors, fonts, height.
- You can add a clear log button if you want:

```html
<button onclick="document.getElementById('log').textContent = ''">Clear Log</button>
```

---

## Result

Your Dashboard is:
- 🟢 Live-updating with ZeroMQ events via websockets.
- 🟢 Fully reactive → pushes your buttons to influence the system.
- 🟢 Lightweight — runs anywhere with FastAPI + Uvicorn.

---

