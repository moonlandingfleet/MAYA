import subprocess
import json
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from web3 import Web3
from typing import Dict, Any

app = FastAPI()

# Allow Android to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Web3 connection (using Infura as an example)
# Replace with your Infura project ID or other Ethereum node provider
w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/2db6b9cd6ba745f3b98f07e264e57785"))

# In-memory agent state
AGENT_RUNNING = False

# Treasury information
TREASURY_ADDRESS = "0x16B3d93d02FB58f7aCe79157E74Eb275D2c3F734"  # Replace with real wallet
TREASURY_BALANCE = 0.0012  # Simulated for now

# Store wallet sessions
WALLET_SESSIONS = {}

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
    # Fetch real ETH balance for the treasury address
    try:
        if w3.is_connected():
            balance_wei = w3.eth.get_balance(TREASURY_ADDRESS)
            balance_eth = w3.from_wei(balance_wei, 'ether')
            real_balance = float(balance_eth)
        else:
            # Fallback to simulated balance if not connected
            real_balance = TREASURY_BALANCE
    except Exception as e:
        # Fallback to simulated balance if error occurs
        real_balance = TREASURY_BALANCE
    
    return {
        "address": TREASURY_ADDRESS,
        "balance_eth": real_balance,
        "agents_contributed": ["A-01"],
        "last_updated": time.ctime(),
        "wallet_connected": w3.is_connected()
    }

@app.get("/wallet/balance")
def get_wallet_balance(address: str):
    """Fetch real ETH balance for a given wallet address"""
    try:
        if w3.is_connected():
            balance_wei = w3.eth.get_balance(address)
            balance_eth = w3.from_wei(balance_wei, 'ether')
            return {
                "address": address,
                "balance_eth": float(balance_eth),
                "last_updated": time.ctime()
            }
        else:
            return {"error": "Not connected to Ethereum network"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/agents/decide")
def agent_decide(agent_id: str, decision: str):
    global AGENT_RUNNING
    if decision == "continue":
        return {"status": "extended", "agent": agent_id}
    else:
        subprocess.run("docker kill a01", shell=True)
        AGENT_RUNNING = False
        return {"status": "terminated", "agent": agent_id}

@app.post("/wallet/transaction")
def request_transaction(agent_id: str, amount_eth: float, to_address: str, from_address: str = None):
    """Request a transaction from the Android app"""
    # This endpoint would trigger a notification to the Android app
    # to request a transaction via WalletConnect
    return {
        "status": "transaction_requested",
        "agent_id": agent_id,
        "amount_eth": amount_eth,
        "to_address": to_address,
        "from_address": from_address
    }

@app.post("/wallet/session/connect")
def connect_wallet(address: str, chain_id: str):
    """Connect a wallet session"""
    session_id = f"session_{int(time.time())}"
    WALLET_SESSIONS[session_id] = {
        "address": address,
        "chain_id": chain_id,
        "connected_at": time.ctime()
    }
    return {
        "status": "connected",
        "session_id": session_id,
        "address": address
    }

@app.post("/wallet/session/disconnect")
def disconnect_wallet(session_id: str):
    """Disconnect a wallet session"""
    if session_id in WALLET_SESSIONS:
        del WALLET_SESSIONS[session_id]
        return {"status": "disconnected"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")

@app.get("/wallet/session/{session_id}")
def get_session(session_id: str):
    """Get wallet session information"""
    if session_id in WALLET_SESSIONS:
        return WALLET_SESSIONS[session_id]
    else:
        raise HTTPException(status_code=404, detail="Session not found")

@app.post("/convert-to-btc")
def convert_to_btc(amount_eth: float):
    """Convert ETH to BTC using exchange APIs"""
    # Implementation would use 1inch, Uniswap, or Thorchain
    # For simulation, we'll use a fixed rate
    btc_rate = 0.05  # Simulated ETH to BTC rate
    return {
        "status": "conversion_started",
        "amount_eth": amount_eth,
        "estimated_btc": amount_eth * btc_rate,
        "rate": btc_rate
    }

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