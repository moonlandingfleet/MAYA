import subprocess
import json
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime

# Load environment variables from .env file
from dotenv import load_dotenv
import os

load_dotenv()

# --- Custom Supabase Service and Models ---
from maya_supabase.database import SupabaseService
from maya_supabase.models import Proposal as SupabaseProposal

# --- FastAPI App - The Chancellor's Office ---
app = FastAPI(title="MAYA Core - The Chancellor's Office")

db_service = SupabaseService()

if not db_service.client:
    print("FATAL: Supabase client in db_service not initialized. Check .env file and Supabase credentials.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

# --- NEW AND REFACTORED ENDPOINT DEFINITIONS ---

class AgentFundingRequest(BaseModel):
    purpose: str
    cost_eth: float 
    expected_monthly_revenue_btc: float 
    details_json: Optional[Dict[str, Any]] = None

@app.post("/council/{council_id}/request_funding", response_model=SupabaseProposal)
async def council_request_funding_route(council_id: str, request: AgentFundingRequest):
    if not db_service.client:
        raise HTTPException(status_code=503, detail="Supabase service not available.")

    roi_score = 0.0
    if request.cost_eth > 0: 
        eth_to_btc_rate_placeholder = 0.05 
        cost_btc_equivalent = request.cost_eth * eth_to_btc_rate_placeholder
        if cost_btc_equivalent > 0:
             roi_score = request.expected_monthly_revenue_btc / cost_btc_equivalent
    else: 
        roi_score = 99999.0 

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
    
    print(f"New proposal {created_proposal.id} submitted by council {council_id} for PENDING_REVIEW.")
    return created_proposal

@app.get("/proposals/sovereign_review", response_model=List[SupabaseProposal])
async def get_proposals_for_sovereign_review_route():
    if not db_service.client:
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

# --- Server Startup ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)