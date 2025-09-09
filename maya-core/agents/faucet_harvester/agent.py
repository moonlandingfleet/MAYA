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