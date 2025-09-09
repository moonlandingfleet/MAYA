import subprocess
import json
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow Android to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory agent state
AGENT_RUNNING = False

@app.get("/proposals")
def get_proposals():
    return [{
        "id": "A-01",
        "name": "Faucet-Harvester",
        "description": "Claims ETH from testnet faucets every 10 min.",
        "roi_hrs": 0.3,
        "risk": "low",
        "cost": 0
    }]

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

@app.get("/heartbeat")
def heartbeat():
    # Simulate re-indexing every 10 min
    return {
        "status": "alive",
        "last_indexed": time.ctime(),
        "agents_queued": 1,
        "running": 1 if AGENT_RUNNING else 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)