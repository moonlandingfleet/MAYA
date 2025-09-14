from fastapi import APIRouter, HTTPException, Depends
from typing import List
from maya_supabase.models import Council, Proposal, TreasuryTransaction, CouncilOpportunity
from maya_supabase.database import SupabaseService

# Initialize the router
router = APIRouter(prefix="/supabase", tags=["supabase"])

# Initialize the database service
db_service = SupabaseService()

# Council endpoints
@router.post("/councils", response_model=Council)
def create_council(council: Council):
    """Create a new council"""
    created_council = db_service.create_council(council)
    if not created_council:
        raise HTTPException(status_code=500, detail="Failed to create council")
    return created_council

@router.get("/councils/{council_id}", response_model=Council)
def get_council(council_id: str):
    """Get a council by ID"""
    council = db_service.get_council(council_id)
    if not council:
        raise HTTPException(status_code=404, detail="Council not found")
    return council

@router.get("/councils", response_model=List[Council])
def get_all_councils():
    """Get all councils"""
    return db_service.get_all_councils()

@router.put("/councils/{council_id}", response_model=Council)
def update_council(council_id: str, council_data: dict):
    """Update a council"""
    updated_council = db_service.update_council(council_id, council_data)
    if not updated_council:
        raise HTTPException(status_code=404, detail="Council not found")
    return updated_council

@router.delete("/councils/{council_id}")
def delete_council(council_id: str):
    """Delete a council"""
    success = db_service.delete_council(council_id)
    if not success:
        raise HTTPException(status_code=404, detail="Council not found")
    return {"message": "Council deleted successfully"}

# Proposal endpoints
@router.post("/proposals", response_model=Proposal)
def create_proposal(proposal: Proposal):
    """Create a new proposal"""
    created_proposal = db_service.create_proposal(proposal)
    if not created_proposal:
        raise HTTPException(status_code=500, detail="Failed to create proposal")
    return created_proposal

@router.get("/proposals/{proposal_id}", response_model=Proposal)
def get_proposal(proposal_id: str):
    """Get a proposal by ID"""
    proposal = db_service.get_proposal(proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return proposal

@router.get("/proposals/council/{council_id}", response_model=List[Proposal])
def get_proposals_by_council(council_id: str):
    """Get all proposals for a council"""
    return db_service.get_proposals_by_council(council_id)

@router.get("/proposals", response_model=List[Proposal])
def get_all_proposals():
    """Get all proposals"""
    return db_service.get_all_proposals()

@router.put("/proposals/{proposal_id}", response_model=Proposal)
def update_proposal(proposal_id: str, proposal_data: dict):
    """Update a proposal"""
    updated_proposal = db_service.update_proposal(proposal_id, proposal_data)
    if not updated_proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return updated_proposal

@router.delete("/proposals/{proposal_id}")
def delete_proposal(proposal_id: str):
    """Delete a proposal"""
    success = db_service.delete_proposal(proposal_id)
    if not success:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return {"message": "Proposal deleted successfully"}

# Treasury transaction endpoints
@router.post("/treasury-transactions", response_model=TreasuryTransaction)
def create_treasury_transaction(transaction: TreasuryTransaction):
    """Create a new treasury transaction"""
    created_transaction = db_service.create_treasury_transaction(transaction)
    if not created_transaction:
        raise HTTPException(status_code=500, detail="Failed to create treasury transaction")
    return created_transaction

@router.get("/treasury-transactions/{transaction_id}", response_model=TreasuryTransaction)
def get_treasury_transaction(transaction_id: str):
    """Get a treasury transaction by ID"""
    transaction = db_service.get_treasury_transaction(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Treasury transaction not found")
    return transaction

@router.get("/treasury-transactions/council/{council_id}", response_model=List[TreasuryTransaction])
def get_treasury_transactions_by_council(council_id: str):
    """Get all treasury transactions for a council"""
    return db_service.get_treasury_transactions_by_council(council_id)

@router.get("/treasury-transactions", response_model=List[TreasuryTransaction])
def get_all_treasury_transactions():
    """Get all treasury transactions"""
    return db_service.get_all_treasury_transactions()

# Council opportunity endpoints
@router.post("/council-opportunities", response_model=CouncilOpportunity)
def create_council_opportunity(opportunity: CouncilOpportunity):
    """Create a new council opportunity"""
    created_opportunity = db_service.create_council_opportunity(opportunity)
    if not created_opportunity:
        raise HTTPException(status_code=500, detail="Failed to create council opportunity")
    return created_opportunity

@router.get("/council-opportunities/{opportunity_id}", response_model=CouncilOpportunity)
def get_council_opportunity(opportunity_id: str):
    """Get a council opportunity by ID"""
    opportunity = db_service.get_council_opportunity(opportunity_id)
    if not opportunity:
        raise HTTPException(status_code=404, detail="Council opportunity not found")
    return opportunity

@router.get("/council-opportunities/council/{council_id}", response_model=List[CouncilOpportunity])
def get_council_opportunities_by_council(council_id: str):
    """Get all council opportunities for a council"""
    return db_service.get_council_opportunities_by_council(council_id)

@router.get("/council-opportunities", response_model=List[CouncilOpportunity])
def get_all_council_opportunities():
    """Get all council opportunities"""
    return db_service.get_all_council_opportunities()

@router.put("/council-opportunities/{opportunity_id}", response_model=CouncilOpportunity)
def update_council_opportunity(opportunity_id: str, opportunity_data: dict):
    """Update a council opportunity"""
    updated_opportunity = db_service.update_council_opportunity(opportunity_id, opportunity_data)
    if not updated_opportunity:
        raise HTTPException(status_code=404, detail="Council opportunity not found")
    return updated_opportunity

@router.delete("/council-opportunities/{opportunity_id}")
def delete_council_opportunity(opportunity_id: str):
    """Delete a council opportunity"""
    success = db_service.delete_council_opportunity(opportunity_id)
    if not success:
        raise HTTPException(status_code=404, detail="Council opportunity not found")
    return {"message": "Council opportunity deleted successfully"}