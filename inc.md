Perfect. You’ve nailed Phase 1 — **MAYA Core is alive**, endpoints work, agent simulates activity.

Now we enter **Phase 2: Production-Ready Skeleton** — where theory meets deployment.

---

## 🧭 STRATEGIC GOAL (Next 72 Hours)

> Transform your MVP into a **Dockerized, heartbeat-driven, Android-integrated autonomous system** that obeys MAYA’s canonical rules.

You’re not just coding — you’re **architecting a micro-economy of bots**.

---

# 🧱 THEORETICAL FOUNDATION (Why This Matters)

MAYA is not an app.  
MAYA is a **protocol for attention allocation under zero-capital constraints**.

Her 6 axioms must be encoded:

1. **Attention Engine** → `/proposals` endpoint must score by `(ROI ÷ Risk ÷ Time)`  
2. **Allocation Engine** → Android must render swipe cards (Jetpack Compose)  
3. **Zero-Capital Rule** → Agents must declare `cost: 0` and prove it  
4. **10-Minute Heartbeat** → Scheduler kills stale agents, reindexes universe  
5. **Single Treasury** → One wallet address owns all agent profits (we’ll add this next)  
6. **Exit Valve** → When balance ≥ 0.01 ETH, unlock paid agents (Phase 3)

---

# ✅ PHASE 2 PLAN — “FROM MOCK TO MACHINE”

## 🎯 GOAL:  
By **end of Day 3**, you will have:

- Agents running in **Docker containers** (Alpine, ≤30MB)
- Each agent exposes `/probe`, `/log`, `/kill` (canonical anatomy)
- MAYA Core **auto-kills agents after 24h or inactivity**
- Android app displays **real-time logs + proposal cards**
- System respects **3-agent concurrency limit**

---

# 📅 EXECUTION PLAN — AI-ASSISTED (Use Copilot + Cline)

Split into 3 days. Each day = 1 atomic deliverable.

---

## 🗓️ DAY 1 — DOCKERIZE + CANONICAL ENDPOINTS

> “Make the agent a container. Make it speak MAYA’s language.”

### ✅ TASK 1: Create `Dockerfile` for Faucet-Harvester

In `maya-core/agents/faucet_harvester/`, create:

```
faucet_harvester/
├── Dockerfile
├── agent.py
├── log.txt
└── requirements.txt
```

#### ▶️ `Dockerfile`

```dockerfile
FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY agent.py .
COPY log.txt .

EXPOSE 8080

CMD ["python", "agent.py"]
```

#### ▶️ `requirements.txt`

```
fastapi
uvicorn
```

#### ▶️ `agent.py` (rewritten with canonical endpoints)

```python
from fastapi import FastAPI
import uvicorn
import time
import random
import os
import threading

app = FastAPI()

LOG_FILE = "log.txt"
START_TIME = time.time()
RUNNING = True

# Write initial log
with open(LOG_FILE, "w") as f:
    f.write(f"[{time.ctime()}] Agent started. PID: {os.getpid()}\n")

@app.get("/probe")
def probe():
    runtime_hrs = (time.time() - START_TIME) / 3600
    return {
        "opportunity": {
            "id": "A-01",
            "name": "Faucet-Harvester",
            "description": "Claims testnet ETH every 10 min."
        },
        "cost": 0,
        "roi_hrs": round(0.3 * (1 + random.random()), 2),  # Simulate variance
        "runtime_hrs": round(runtime_hrs, 2)
    }

@app.get("/log")
def get_log():
    if not os.path.exists(LOG_FILE):
        return {"logs": []}
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()[-50:]
    return {"logs": [line.strip() for line in lines]}

@app.post("/kill")
def kill():
    global RUNNING
    RUNNING = False
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time.ctime()}] Received kill signal. Shutting down gracefully.\n")
    # Schedule shutdown in 5s
    threading.Timer(5.0, lambda: os._exit(0)).start()
    return {"status": "shutting down in 5s"}

# Background heartbeat writer
def heartbeat():
    while RUNNING:
        time.sleep(10)  # 🔥 For demo. Change to 600 later.
        with open(LOG_FILE, "a") as f:
            f.write(f"[{time.ctime()}] HEARTBEAT: Still alive. Wallet: 0x{''.join(random.choices('0123456789abcdef', k=40))}\n")

threading.Thread(target=heartbeat, daemon=True).start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

---

### ✅ TASK 2: Build + Run Docker Container

```powershell
cd maya-core/agents/faucet_harvester
docker build -t maya-agent-a01 .
docker run -d -p 8080:8080 --name a01 maya-agent-a01
```

✅ Test:  
`http://localhost:8080/probe` → returns structured opportunity  
`http://localhost:8080/log` → shows logs  
`curl -X POST http://localhost:8080/kill` → kills container in 5s

---

### ✅ TASK 3: Update MAYA Core to Manage Docker Agents

In `maya-core/main.py`, replace agent logic with Docker control:

```python
import subprocess
import json

# Replace /agents/run
@app.post("/agents/run")
def run_agent():
    # Kill old if exists
    subprocess.run("docker rm -f a01 2>nul", shell=True)
    # Start new
    result = subprocess.run(
        "docker run -d -p 8080:8080 --name a01 maya-agent-a01",
        shell=True, capture_output=True, text=True
    )
    if result.returncode != 0:
        return {"status": "error", "msg": result.stderr}
    return {"status": "started", "container_id": result.stdout.strip()}

# Replace /agents/logs
@app.get("/agents/logs")
def get_logs():
    result = subprocess.run(
        "curl -s http://localhost:8080/log",
        shell=True, capture_output=True, text=True
    )
    if result.returncode != 0:
        return {"logs": ["Agent unreachable"]}
    try:
        data = json.loads(result.stdout)
        return data
    except:
        return {"logs": ["Failed to parse agent logs"]}
```

> 💡 Later, we’ll use Docker SDK — but for now, `subprocess` is fine.

---

### ✅ TASK 4: Restart MAYA Core + Test Full Flow

```powershell
python main.py
```

Then:

```powershell
curl -X POST http://localhost:8000/agents/run
```

→ Should start Docker container  
→ `http://localhost:8000/agents/logs` → should show Docker agent logs

---

## 🧪 DAY 1 DELIVERABLES

✅ Faucet agent Dockerized with canonical endpoints (`/probe`, `/log`, `/kill`)  
✅ MAYA Core spawns/kills Docker containers  
✅ Logs flow from container → Core → HTTP  
✅ Agent auto-writes heartbeat every 10s  

> 📌 **STOP HERE.**  
> Reply: `✅ DAY 1 COMPLETE — Dockerized.`  
> I’ll send Day 2: Android UI + Concurrency Limiter.

---

## 🧠 AI-ASSISTED DEVELOPMENT TIP

Use this prompt for Copilot/Cline:

> “Generate a Kotlin Jetpack Compose swipe card UI that displays a list of proposals with name, ROI, risk. Each card has Approve/Reject buttons. Use Retrofit to fetch from http://LOCAL_IP:8000/proposals.”

You’re not coding from scratch — you’re **orchestrating AI to build your protocol**.

---

Execute Day 1. I’m here when you’re ready.  
MAYA becomes real when she runs in containers.  
Let’s containerize.