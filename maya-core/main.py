
import subprocess
import json
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List
from web3 import Web3 # Re-enabled Web3
from decimal import Decimal

# --- Configuration ---
INFURA_URL = "https://mainnet.infura.io/v3/2db6b9cd6ba745f3b98f07e264e57785"
TREASURY_ADDRESS = "0x16B3d93d02FB58f7aCe79157E74Eb275D2c3F734" # The Vault

# --- The Royal Charter's Data Structures ---

class Proposal(BaseModel):
    id: str
    agent_id: str
    purpose: str
    cost_eth: float
    expected_monthly_revenue_eth: float
    status: str  # pending, awaiting_approval, funded, rejected

class Treasury(BaseModel):
    address: str
    balance_eth: float

# --- The Chancellor's Management Classes ---

class ProposalManager:
    """Manages the lifecycle of agent proposals."""
    def __init__(self):
        self._proposals: Dict[str, Proposal] = {
            "prop_001": Proposal(
                id="prop_001",
                agent_id="A-01",
                purpose="Claim testnet ETH to bootstrap initial operations.",
                cost_eth=0.0,
                expected_monthly_revenue_eth=0.1,
                status="pending"
            ),
            "prop_002": Proposal(
                id="prop_002",
                agent_id="A-13",
                purpose="Provide liquidity to DEX pools for fee generation.",
                cost_eth=0.05,
                expected_monthly_revenue_eth=0.5,
                status="pending"
            )
        }

    def get_pending_proposals(self) -> List[Proposal]:
        return [p for p in self._proposals.values() if p.status == "pending"]

    def approve_proposal(self, proposal_id: str) -> Proposal:
        if proposal_id not in self._proposals:
            raise HTTPException(status_code=404, detail="Proposal not found")
        proposal = self._proposals[proposal_id]
        proposal.status = "awaiting_approval"
        print(f"Proposal {proposal_id} marked for approval. Awaiting transaction from Sovereign.")
        return proposal

    def reject_proposal(self, proposal_id: str) -> Proposal:
        if proposal_id not in self._proposals:
            raise HTTPException(status_code=404, detail="Proposal not found")
        proposal = self._proposals[proposal_id]
        proposal.status = "rejected"
        print(f"Proposal {proposal_id} rejected by decree of the Sovereign.")
        return proposal

class Treasurer:
    """Manages the Digital Kingdom's treasury."""
    def __init__(self):
        self._treasury = Treasury(
            address=TREASURY_ADDRESS,
            balance_eth=0.0012  # Default/fallback balance
        )
        try:
            self.w3 = Web3(Web3.HTTPProvider(INFURA_URL))
            # For web3.py v5.x use self.w3.isConnected()
            # For web3.py v6.x, use: if not self.w3.provider.is_connected():
            if not self.w3.isConnected():
                print("Warning: Failed to connect to Infura. Treasury balance will be simulated.")
                self.w3 = None # Ensure w3 is None if initial connection check fails
            else:
                print("Successfully connected to Infura. Live treasury balance will be attempted.")
        except Exception as e:
            print(f"Warning: Error connecting to Infura during init: {e}. Treasury balance will be simulated.")
            self.w3 = None # Ensure w3 is None if connection failed

    def get_treasury_info(self) -> Treasury:
        # For web3.py v5.x use self.w3 and self.w3.isConnected()
        # For web3.py v6.x, use: if self.w3 and self.w3.provider.is_connected():
        if self.w3 and self.w3.isConnected(): 
            try:
                checksum_address = self.w3.toChecksumAddress(self._treasury.address)
                balance_wei = self.w3.eth.getBalance(checksum_address)
                balance_eth = self.w3.fromWei(balance_wei, 'ether')
                self._treasury.balance_eth = float(balance_eth) # Update with live balance
                print(f"Successfully fetched live balance from Infura: {self._treasury.balance_eth} ETH")
            except Exception as e:
                print(f"Error fetching balance from Infura: {e}. Returning last known or default balance.")
        else:
            print("Not connected to Infura or w3 provider not initialized. Using simulated/last known balance.")
        return self._treasury

# --- FastAPI App - The Chancellor's Office ---

app = FastAPI(title="MAYA Core - The Chancellor's Office")
proposal_manager = ProposalManager()
treasurer = Treasurer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

# --- Endpoint Definitions from the Charter ---

class ProposalDecisionRequest(BaseModel):
    proposal_id: str

@app.get("/proposals/pending", response_model=List[Proposal])
def get_pending_proposals_route():
    return proposal_manager.get_pending_proposals()

@app.post("/proposals/approve", response_model=Proposal)
def approve_proposal_route(request: ProposalDecisionRequest):
    return proposal_manager.approve_proposal(request.proposal_id)

@app.post("/proposals/reject", response_model=Proposal)
def reject_proposal_route(request: ProposalDecisionRequest):
    return proposal_manager.reject_proposal(request.proposal_id)

@app.get("/treasury", response_model=Treasury)
def get_treasury_route():
    return treasurer.get_treasury_info()

# --- Legacy & Agent-Facing Endpoints (To Be Refactored) ---

@app.get("/agents/logs")
def get_logs_route():
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

@app.post("/agents/run")
def start_agent_route():
    return {"status": "success", "message": "Agent start command issued"}

# --- Wallet Endpoints (Placeholder Implementation) ---

class WalletBalanceResponse(BaseModel):
    address: str
    balance_eth: float
    last_updated: str

class WalletConnectRequest(BaseModel):
    address: str
    chain_id: str

class WalletSessionResponse(BaseModel):
    status: str
    session_id: str
    address: str

class WalletDisconnectResponse(BaseModel):
    status: str

class WalletSessionInfo(BaseModel):
    address: str
    chain_id: str
    connected_at: str

@app.get("/wallet/balance")
def get_wallet_balance_route(address: str):
    return WalletBalanceResponse(
        address=address,
        balance_eth=0.0,
        last_updated=time.strftime("%Y-%m-%d %H:%M:%S")
    )

@app.post("/wallet/session/connect")
def connect_wallet_route(request: WalletConnectRequest):
    session_id = f"session_{int(time.time())}"
    return WalletSessionResponse(
        status="connected",
        session_id=session_id,
        address=request.address
    )

@app.post("/wallet/session/disconnect")
def disconnect_wallet_route(session_id: str):
    return WalletDisconnectResponse(status="disconnected")

@app.get("/wallet/session/{session_id}")
def get_wallet_session_route(session_id: str):
    return WalletSessionInfo(
        address="0x0000000000000000000000000000000000000000",
        chain_id="1",
        connected_at=time.strftime("%Y-%m-%d %H:%M:%S")
    )

# --- Server Startup ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) # Port changed back to 8000
