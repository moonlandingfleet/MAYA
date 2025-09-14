from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

class Council(BaseModel):
    """Model for the councils table"""
    id: str  # Primary Key, e.g., "council_digital_identity"
    council_name: str  # e.g., "Council of Digital Identity"
    domain_description: str
    revenue_model_description: str
    ethical_boundary: str
    status: str  # e.g., "ACTIVE", "UNDER_DEVELOPMENT", "PAUSED"
    created_at: datetime  # default: now()

class Proposal(BaseModel):
    """Model for the proposals table (Funding requests from Councils, curated by MAYA)"""
    id: Optional[str]  # uuid (Primary Key, default: gen_random_uuid())
    council_id: str  # Foreign Key referencing councils.id
    purpose: str  # e.g., "Launch 'Sign-In with Bitcoin' service."
    cost_eth: float  # Use numeric for precise currency values
    expected_monthly_revenue_btc: float
    status: str  # e.g., "PENDING_REVIEW", "AWAITING_SOVEREIGN_APPROVAL", "APPROVED_PENDING_FUNDING", "FUNDED_ACTIVE", "REJECTED", "COMPLETED", "FAILED"
    details_json: Optional[Dict[str, Any]]  # Optional: for any council-specific data related to the proposal
    submitted_at: datetime  # default: now()
    last_status_update_at: datetime  # default: now()
    sovereign_approved_at: Optional[datetime]  # nullable
    funding_transaction_hash: Optional[str]  # nullable
    roi_score: float  # calculated by MAYA, for ranking

class TreasuryTransaction(BaseModel):
    """Model for the treasury_transactions table (Log of all financial movements)"""
    id: Optional[str]  # uuid (Primary Key, default: gen_random_uuid())
    timestamp: datetime  # default: now()
    transaction_type: str  # e.g., "COUNCIL_REVENUE_IN", "PROPOSAL_FUNDING_OUT", "ETH_TO_BTC_SWAP", "GAS_FEE"
    council_id: Optional[str]  # Nullable, Foreign Key referencing councils.id
    proposal_id: Optional[str]  # Nullable, Foreign Key referencing proposals.id
    asset: str  # e.g., "ETH", "USDC", "BTC", "DAI"
    amount: float  # positive for inflow, negative for outflow to treasury
    related_onchain_transaction_hash: Optional[str]  # nullable
    description: str
    status: str  # e.g., "PENDING", "COMPLETED", "FAILED"

class CouncilOpportunity(BaseModel):
    """Model for the council_opportunities table (Optional, if probes report opportunities before they become formal proposals)"""
    id: Optional[str]  # uuid (Primary Key, default: gen_random_uuid())
    council_id: str  # Foreign Key referencing councils.id
    opportunity_description: str
    reported_at: datetime  # default: now()
    potential_cost_eth: Optional[float]  # nullable
    potential_revenue_btc: Optional[float]  # nullable
    status: str  # e.g., "NEW", "UNDER_REVIEW_BY_MAYA", "CONVERTED_TO_PROPOSAL", "DISMISSED"