
import sys
import os

# Add the api directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

import subprocess
import json
import time
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel # Keeping BaseModel for other models not yet replaced
from typing import Dict, Any, List, Optional
from web3 import Web3
from decimal import Decimal
from datetime import datetime # Added for timestamping

# Load environment variables from .env file
from dotenv import load_dotenv
import os # Already here, good.

load_dotenv()

# --- Custom Supabase Service and Models ---
# Initialize variables to None
db_service = None
SupabaseProposal = None
SupabaseCouncil = None
SupabaseTreasuryTransaction = None

try:
    from maya_supabase.database import SupabaseService
    from maya_supabase.models import Proposal as SupabaseProposal # Alias for clarity
    from maya_supabase.models import Council as SupabaseCouncil # If we need it soon
    from maya_supabase.models import TreasuryTransaction as SupabaseTreasuryTransaction # For later
    # Instantiate our custom Supabase service only if import succeeded
    db_service = SupabaseService()
except ImportError as e:
    print(f"Warning: Failed to import maya_supabase modules: {e}")
    print("Supabase functionality will be disabled.")

# --- Authentication --- NEWLY ADDED ---
from auth import verify_token_and_get_payload # verify_token_and_get_payload returns the whole payload

# --- Configuration ---
INFURA_URL = os.getenv("INFURA_URL", "https://mainnet.infura.io/v3/2db6b9cd6ba745f3b98f07e264e57785") 
TREASURY_ADDRESS = os.getenv("TREASURY_ADDRESS", "0x16B3d93d02FB58f7aCe79157E74Eb275D2c3F734")

class Treasury(BaseModel): # This is fine as it's for Infura response
    address: str
    balance_eth: float

# --- The Chancellor's Management Classes ---
class Treasurer: # Unchanged for now
    def __init__(self):
        self._treasury = Treasury(
            address=TREASURY_ADDRESS,
            balance_eth=0.0012  # Default/fallback balance
        )
        infura_url_to_use = os.getenv("INFURA_URL_ACTUAL", INFURA_URL) 
        try:
            self.w3 = Web3(Web3.HTTPProvider(infura_url_to_use))
            # Check connection using the correct method for web3.py v6
            if not self.w3.is_connected(): 
                print("Warning: Failed to connect to Infura. Treasury balance will be simulated.")
                self.w3 = None
            else:
                print("Successfully connected to Infura. Live treasury balance will be attempted.")
        except Exception as e:
            print(f"Warning: Error connecting to Infura during init: {e}. Treasury balance will be simulated.")
            self.w3 = None

    def get_treasury_info(self) -> Treasury:
        # Check connection using the correct method for web3.py v6
        if self.w3 and self.w3.is_connected(): 
            try:
                checksum_address = self.w3.to_checksum_address(self._treasury.address)
                balance_wei = self.w3.eth.get_balance(checksum_address)
                balance_eth = self.w3.from_wei(balance_wei, 'ether')
                self._treasury.balance_eth = float(balance_eth)
                print(f"Successfully fetched live balance from Infura: {self._treasury.balance_eth} ETH")
            except Exception as e:
                print(f"Error fetching balance from Infura: {e}. Returning last known or default balance.")
        else:
            print("Not connected to Infura or w3 provider not initialized. Using simulated/last known balance.")
        return self._treasury


# --- FastAPI App - The Chancellor's Office ---
app = FastAPI(title="MAYA Core - The Chancellor's Office")

# Include the Supabase API router
try:
    from maya_supabase.api import router as supabase_router
    app.include_router(supabase_router)
    print("Successfully included Supabase API router")
except ImportError as e:
    print(f"Warning: Failed to import Supabase API router: {e}")

# Add the new strategic review router
try:
    from maya_supabase.strategic_review import router as strategic_router
    app.include_router(strategic_router)
    print("Successfully included strategic review router")
except ImportError as e:
    print(f"Warning: Failed to import strategic review router: {e}")

# Add the kingdom dashboard router
try:
    from maya_supabase.kingdom_dashboard import router as kingdom_router
    app.include_router(kingdom_router)
    print("Successfully included kingdom dashboard router")
except ImportError as e:
    print(f"Warning: Failed to import kingdom dashboard router: {e}")

treasurer = Treasurer() # Keep current treasurer

# Check if db_service was successfully initialized
if db_service is None or (hasattr(db_service, 'client') and not db_service.client):
    print("FATAL: Supabase client in db_service not initialized. Check .env file and Supabase credentials.")

app.add_middleware( 
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

# --- NEW AND REFACTORED ENDPOINT DEFINITIONS (NOW PROTECTED) ---

class AgentFundingRequest(BaseModel):
    purpose: str
    cost_eth: float 
    expected_monthly_revenue_btc: float 
    details_json: Optional[Dict[str, Any]] = None

class FundingConfirmationRequest(BaseModel):
    transaction_hash: str

@app.post("/council/{council_id}/request_funding", response_model=Dict[str, Any])
async def council_request_funding_route(
    council_id: str, 
    request: AgentFundingRequest,
    payload: Dict[str, Any] = Depends(verify_token_and_get_payload)
):
    requesting_agent_supa_id = payload.get("sub")
    print(f"Funding request received from authenticated agent Supabase ID: {requesting_agent_supa_id} for council: {council_id}")
    # TODO: Add logic to map requesting_agent_supa_id to council_id or verify permissions

    # Check if db_service is available
    if db_service is None or not hasattr(db_service, 'client') or not db_service.client:
        raise HTTPException(status_code=503, detail="Supabase service not available.")

    roi_score = 0.0
    if request.cost_eth > 0: 
        eth_to_btc_rate_placeholder = 0.05 
        cost_btc_equivalent = request.cost_eth * eth_to_btc_rate_placeholder
        if cost_btc_equivalent > 0:
             roi_score = request.expected_monthly_revenue_btc / cost_btc_equivalent
    else: 
        roi_score = 99999.0 

    # Only create proposal data if SupabaseProposal is available
    if SupabaseProposal is None:
        raise HTTPException(status_code=503, detail="Supabase models not available.")
        
    new_proposal_data = SupabaseProposal(
        council_id=council_id,
        purpose=request.purpose,
        cost_eth=request.cost_eth,
        expected_monthly_revenue_btc=request.expected_monthly_revenue_btc,
        status="PENDING_REVIEW", 
        details_json=request.details_json,
        submitted_at=datetime.utcnow(),
        last_status_update_at=datetime.utcnow(),
        roi_score=roi_score 
    )

    created_proposal = db_service.create_proposal(new_proposal_data)
    if not created_proposal:
        raise HTTPException(status_code=500, detail="Failed to create proposal in database.")
    
    print(f"New proposal {created_proposal.id} submitted by council {council_id} (Agent Supabase ID: {requesting_agent_supa_id}) for PENDING_REVIEW.")
    return created_proposal

@app.get("/proposals/sovereign_review", response_model=List[Dict[str, Any]])
async def get_proposals_for_sovereign_review_route(payload: Dict[str, Any] = Depends(verify_token_and_get_payload)):
    print(f"Sovereign review requested by user Supabase ID: {payload.get('sub')}")
    # Check if db_service is available
    if db_service is None or not hasattr(db_service, 'client') or not db_service.client:
        raise HTTPException(status_code=503, detail="Supabase service not available.")
    
    try:
        all_proposals = db_service.get_all_proposals()         
        review_proposals = [
            p for p in all_proposals 
            if p.status in ["AWAITING_SOVEREIGN_APPROVAL", "PENDING_REVIEW"] and p.roi_score is not None
        ]
        review_proposals.sort(key=lambda p: p.roi_score, reverse=True)
        return review_proposals
    except Exception as e:
        print(f"Error fetching proposals for sovereign review: {e}")
        raise HTTPException(status_code=500, detail="Error fetching proposals.")

@app.post("/proposals/{proposal_id}/sovereign_approve", response_model=Dict[str, Any])
async def sovereign_approve_proposal_route(proposal_id: str, payload: Dict[str, Any] = Depends(verify_token_and_get_payload)):
    print(f"Sovereign approval for {proposal_id} by user Supabase ID: {payload.get('sub')}")
    # Check if db_service is available
    if db_service is None or not hasattr(db_service, 'client') or not db_service.client:
        raise HTTPException(status_code=503, detail="Supabase service not available.")

    updated_proposal = db_service.update_proposal(
        proposal_id, 
        {
            "status": "APPROVED_PENDING_FUNDING", 
            "last_status_update_at": datetime.utcnow(),
            "sovereign_approved_at": datetime.utcnow()
        }
    )
    if not updated_proposal:
        raise HTTPException(status_code=404, detail=f"Proposal {proposal_id} not found or update failed.")
    
    print(f"Proposal {proposal_id} status changed to APPROVED_PENDING_FUNDING by user {payload.get('sub')}.")
    return updated_proposal

@app.post("/proposals/{proposal_id}/sovereign_reject", response_model=Dict[str, Any])
async def sovereign_reject_proposal_route(proposal_id: str, payload: Dict[str, Any] = Depends(verify_token_and_get_payload)):
    print(f"Sovereign rejection for {proposal_id} by user Supabase ID: {payload.get('sub')}")
    # Check if db_service is available
    if db_service is None or not hasattr(db_service, 'client') or not db_service.client:
        raise HTTPException(status_code=503, detail="Supabase service not available.")

    updated_proposal = db_service.update_proposal(
        proposal_id,
        {"status": "REJECTED", "last_status_update_at": datetime.utcnow()}
    )
    if not updated_proposal:
        raise HTTPException(status_code=404, detail=f"Proposal {proposal_id} not found or update failed.")
    
    print(f"Proposal {proposal_id} status changed to REJECTED by user {payload.get('sub')}.")
    return updated_proposal

@app.post("/proposals/{proposal_id}/funding_confirmed", response_model=Dict[str, Any])
async def funding_confirmed_route(proposal_id: str, request: FundingConfirmationRequest, payload: Dict[str, Any] = Depends(verify_token_and_get_payload)):
    print(f"Funding confirmation for {proposal_id} by user Supabase ID: {payload.get('sub')}")
    # Check if db_service is available
    if db_service is None or not hasattr(db_service, 'client') or not db_service.client:
        raise HTTPException(status_code=503, detail="Supabase service not available.")

    updated_proposal = db_service.update_proposal(
        proposal_id,
        {
            "status": "FUNDED_ACTIVE",
            "funding_transaction_hash": request.transaction_hash,
            "last_status_update_at": datetime.utcnow()
        }
    )
    if not updated_proposal:
        raise HTTPException(status_code=404, detail=f"Proposal {proposal_id} not found or update failed.")
    
    print(f"Proposal {proposal_id} status changed to FUNDED_ACTIVE by user {payload.get('sub')}. TxHash: {request.transaction_hash}")
    return updated_proposal

@app.get("/treasury", response_model=Treasury)
async def get_treasury_route(payload: Dict[str, Any] = Depends(verify_token_and_get_payload)):
    print(f"Treasury info requested by user Supabase ID: {payload.get('sub')}")
    return treasurer.get_treasury_info()

# --- Legacy & Agent-Facing Endpoints (Consider if these need auth or refactoring) ---

@app.get("/agents/logs") # Consider if this needs protection
def get_logs_route():
    # This currently calls a fixed localhost URL, may need rethinking for multiple agents
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

@app.post("/agents/run") # Consider if this needs protection
def start_agent_route():
    return {"status": "success", "message": "Agent start command issued"}

# --- Wallet Endpoints (Placeholder - Likely need auth if they become real) ---

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
    import sys
    # Use string reference to avoid type checking issues
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False) 

