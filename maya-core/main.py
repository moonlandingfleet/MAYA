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

# Treasury information
TREASURY_ADDRESS = "0xYourWalletAddressHere"  # Replace with real wallet
TREASURY_BALANCE = 0.0012  # Simulated for now

@app.get("/proposals")
def get_proposals():
    treasury_balance = 0.0012  # Later fetch real balance
    
    proposals = [
        {
            "id": "A-01",
            "name": "Faucet-Harvester",
            "description": "Claims ETH from testnet faucets every 10 min.",
            "roi_hrs": 0.3,
            "risk": "low",
            "cost": 0,
            "locked": False
        },
        {
            "id": "A-13",
            "name": "Liquidity-Miner",
            "description": "Provides liquidity to DEX pools for fees.",
            "roi_hrs": 5.0,
            "risk": "medium",
            "cost": 0.05,
            "locked": treasury_balance < 0.01
        }
    ]
    return proposals

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

@app.get("/treasury")
def get_treasury():
    return {
        "address": TREASURY_ADDRESS,
        "balance_eth": TREASURY_BALANCE,
        "agents_contributed": ["A-01"],
        "last_updated": time.ctime()
    }

@app.post("/agents/decide")
def agent_decide(agent_id: str, decision: str):
    global AGENT_RUNNING
    if decision == "continue":
        return {"status": "extended", "agent": agent_id}
    else:
        subprocess.run("docker kill a01", shell=True)
        AGENT_RUNNING = False
        return {"status": "terminated", "agent": agent_id}

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