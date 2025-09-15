"""
Strategic Review API for the Digital Kingdom
This module provides enhanced endpoints for the King to review proposals with strategic context.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from maya_supabase.models import Proposal, Council
from maya_supabase.database import SupabaseService
from maya_supabase.kingdom_councils import get_council_strategy
import json

# Initialize the router
router = APIRouter(prefix="/strategic", tags=["strategic_review"])

# Initialize the database service
db_service = SupabaseService()

class StrategicProposalReview:
    """Enhanced proposal review with strategic context for the King"""
    
    def __init__(self, proposal: Proposal, council: Council):
        self.proposal = proposal
        self.council = council
        self.council_strategy = get_council_strategy(council)
    
    def get_strategic_summary(self) -> Dict[str, Any]:
        """Get a strategic summary of the proposal for the King's review"""
        return {
            "proposal_id": self.proposal.id,
            "council_name": self.council.council_name,
            "council_role": self.council.ethical_boundary,
            "proposal_purpose": self.proposal.purpose,
            "financial_summary": {
                "cost_eth": self.proposal.cost_eth,
                "expected_revenue_btc": self.proposal.expected_monthly_revenue_btc,
                "roi_percentage": self._calculate_roi_percentage()
            },
            "strategic_impact": self.proposal.strategic_impact or "Not specified",
            "collaborations": self.proposal.inter_council_collaborations or [],
            "resource_dependencies": self.proposal.resource_dependencies or [],
            "timeline_days": self.proposal.implementation_timeline_days,
            "risk_assessment": self.proposal.risk_assessment or "Not specified",
            "success_metrics": self.proposal.success_metrics or [],
            "strategic_priority": self._calculate_strategic_priority(),
            "recommendation": self._generate_recommendation()
        }
    
    def _calculate_roi_percentage(self) -> float:
        """Calculate ROI percentage"""
        if self.proposal.cost_eth <= 0:
            return 0.0
        # Simplified BTC to ETH conversion
        btc_to_eth_rate = 15.0
        expected_revenue_eth = self.proposal.expected_monthly_revenue_btc * btc_to_eth_rate
        roi = (expected_revenue_eth - self.proposal.cost_eth) / self.proposal.cost_eth
        return round(roi * 100, 2)
    
    def _calculate_strategic_priority(self) -> str:
        """Calculate strategic priority level"""
        # Simple heuristic based on various factors
        score = 0
        
        # Financial impact
        if self.proposal.expected_monthly_revenue_btc > 1.0:
            score += 3
        elif self.proposal.expected_monthly_revenue_btc > 0.5:
            score += 2
        elif self.proposal.expected_monthly_revenue_btc > 0.1:
            score += 1
            
        # Collaboration value
        collab_count = len(self.proposal.inter_council_collaborations or [])
        if collab_count >= 3:
            score += 2
        elif collab_count >= 1:
            score += 1
            
        # Strategic impact
        if self.proposal.strategic_impact and len(self.proposal.strategic_impact) > 50:
            score += 2
            
        # Timeline efficiency
        if self.proposal.implementation_timeline_days and self.proposal.implementation_timeline_days <= 30:
            score += 1
            
        if score >= 7:
            return "HIGH"
        elif score >= 4:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _generate_recommendation(self) -> str:
        """Generate a recommendation for the King"""
        priority = self._calculate_strategic_priority()
        roi = self._calculate_roi_percentage()
        
        if priority == "HIGH" and roi > 50:
            return "STRONGLY_RECOMMEND_APPROVAL"
        elif priority == "HIGH":
            return "RECOMMEND_APPROVAL_WITH_CONDITIONS"
        elif priority == "MEDIUM" and roi > 25:
            return "RECOMMEND_APPROVAL"
        elif priority == "MEDIUM":
            return "CONSIDER_FOR_APPROVAL"
        else:
            return "RECOMMEND_REJECTION_OR_DEFERRAL"

@router.get("/proposals/king_review", response_model=List[Dict[str, Any]])
def get_strategic_proposals_for_king_review():
    """Get all proposals with strategic context for the King's review"""
    if not db_service.client:
        raise HTTPException(status_code=503, detail="Database service not available")
    
    try:
        # Get all proposals awaiting review
        all_proposals = db_service.get_all_proposals()
        review_proposals = [
            p for p in all_proposals 
            if p.status in ["AWAITING_SOVEREIGN_APPROVAL", "PENDING_REVIEW"]
        ]
        
        # Get all councils
        councils = db_service.get_all_councils()
        council_map = {c.id: c for c in councils}
        
        # Create strategic reviews
        strategic_reviews = []
        for proposal in review_proposals:
            council = council_map.get(proposal.council_id)
            if council:
                review = StrategicProposalReview(proposal, council)
                strategic_reviews.append(review.get_strategic_summary())
        
        # Sort by strategic priority
        strategic_reviews.sort(key=lambda x: x["strategic_priority"], reverse=True)
        return strategic_reviews
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching strategic proposals: {str(e)}")

@router.get("/councils/strategic_overview", response_model=List[Dict[str, Any]])
def get_councils_strategic_overview():
    """Get strategic overview of all councils"""
    if not db_service.client:
        raise HTTPException(status_code=503, detail="Database service not available")
    
    try:
        councils = db_service.get_all_councils()
        overview = []
        
        for council in councils:
            # Get proposals for this council
            council_proposals = db_service.get_proposals_by_council(council.id)
            
            # Calculate council metrics
            active_proposals = [p for p in council_proposals if p.status in ["PENDING_REVIEW", "AWAITING_SOVEREIGN_APPROVAL"]]
            approved_proposals = [p for p in council_proposals if p.status in ["APPROVED_PENDING_FUNDING", "FUNDED_ACTIVE"]]
            total_revenue = sum(p.expected_monthly_revenue_btc for p in approved_proposals)
            
            council_overview = {
                "council_id": council.id,
                "council_name": council.council_name,
                "role": council.ethical_boundary,
                "domain": council.domain_description,
                "status": council.status,
                "active_proposals_count": len(active_proposals),
                "approved_proposals_count": len(approved_proposals),
                "total_expected_monthly_revenue_btc": total_revenue,
                "resource_needs": [],  # Would be populated from council strategy
                "collaborations": []   # Would be populated from council strategy
            }
            overview.append(council_overview)
            
        return overview
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching council overview: {str(e)}")