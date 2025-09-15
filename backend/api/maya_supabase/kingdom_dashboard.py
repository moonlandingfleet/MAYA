"""
Kingdom Dashboard API for the Digital Kingdom
This module provides a comprehensive overview of the digital kingdom's status for the King.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from maya_supabase.models import Proposal, Council, TreasuryTransaction
from maya_supabase.database import SupabaseService
from datetime import datetime, timedelta
import json

# Initialize the router
router = APIRouter(prefix="/kingdom", tags=["kingdom_dashboard"])

# Initialize the database service
db_service = SupabaseService()

@router.get("/dashboard", response_model=Dict[str, Any])
def get_kingdom_dashboard():
    """Get a comprehensive dashboard of the digital kingdom's status"""
    if not db_service.client:
        raise HTTPException(status_code=503, detail="Database service not available")
    
    try:
        # Get all councils
        councils = db_service.get_all_councils()
        
        # Get all proposals
        proposals = db_service.get_all_proposals()
        
        # Get recent treasury transactions
        transactions = db_service.get_all_treasury_transactions()
        
        # Calculate dashboard metrics
        dashboard = {
            "kingdom_status": _calculate_kingdom_status(councils, proposals, transactions),
            "council_overview": _get_council_overview(councils, proposals),
            "proposal_pipeline": _get_proposal_pipeline(proposals),
            "treasury_overview": _get_treasury_overview(transactions),
            "strategic_insights": _get_strategic_insights(councils, proposals),
            "last_updated": datetime.utcnow().isoformat()
        }
        
        return dashboard
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating kingdom dashboard: {str(e)}")

def _calculate_kingdom_status(councils: List[Council], proposals: List[Proposal], transactions: List[TreasuryTransaction]) -> Dict[str, Any]:
    """Calculate overall kingdom status"""
    # Count active councils
    active_councils = len([c for c in councils if c.status == "ACTIVE"])
    
    # Count active proposals
    active_proposals = len([p for p in proposals if p.status in ["PENDING_REVIEW", "AWAITING_SOVEREIGN_APPROVAL"]])
    
    # Calculate recent revenue (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_revenue = sum(
        t.amount for t in transactions 
        if t.timestamp >= thirty_days_ago and t.amount > 0 and t.status == "COMPLETED"
    )
    
    # Calculate recent expenses (last 30 days)
    recent_expenses = sum(
        abs(t.amount) for t in transactions 
        if t.timestamp >= thirty_days_ago and t.amount < 0 and t.status == "COMPLETED"
    )
    
    # Net financial position
    net_position = recent_revenue - recent_expenses
    
    return {
        "total_councils": len(councils),
        "active_councils": active_councils,
        "active_proposals": active_proposals,
        "recent_revenue_btc": round(recent_revenue, 4),
        "recent_expenses_eth": round(recent_expenses, 4),
        "net_position": round(net_position, 4),
        "overall_health": "HEALTHY" if net_position >= 0 else "AT_RISK"
    }

def _get_council_overview(councils: List[Council], proposals: List[Proposal]) -> List[Dict[str, Any]]:
    """Get overview of all councils"""
    proposal_map = {}
    for proposal in proposals:
        if proposal.council_id not in proposal_map:
            proposal_map[proposal.council_id] = []
        proposal_map[proposal.council_id].append(proposal)
    
    overview = []
    for council in councils:
        council_proposals = proposal_map.get(council.id, [])
        
        # Calculate council metrics
        active_proposals = [p for p in council_proposals if p.status in ["PENDING_REVIEW", "AWAITING_SOVEREIGN_APPROVAL"]]
        approved_proposals = [p for p in council_proposals if p.status in ["APPROVED_PENDING_FUNDING", "FUNDED_ACTIVE"]]
        total_revenue = sum(p.expected_monthly_revenue_btc for p in approved_proposals)
        
        council_data = {
            "council_id": council.id,
            "council_name": council.council_name,
            "role": council.ethical_boundary,
            "status": council.status,
            "active_proposals_count": len(active_proposals),
            "approved_proposals_count": len(approved_proposals),
            "total_expected_monthly_revenue_btc": round(total_revenue, 4),
            "collaboration_score": _calculate_collaboration_score(council_proposals)
        }
        overview.append(council_data)
    
    return overview

def _calculate_collaboration_score(proposals: List[Proposal]) -> int:
    """Calculate collaboration score based on inter-council collaborations"""
    total_collaborations = sum(
        len(p.inter_council_collaborations) for p in proposals 
        if p.inter_council_collaborations
    )
    return min(100, total_collaborations * 10)  # Scale to 0-100

def _get_proposal_pipeline(proposals: List[Proposal]) -> Dict[str, Any]:
    """Get proposal pipeline information"""
    status_counts = {}
    for proposal in proposals:
        status = proposal.status
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Calculate total financial impact
    pending_review = [p for p in proposals if p.status in ["PENDING_REVIEW", "AWAITING_SOVEREIGN_APPROVAL"]]
    total_pending_cost = sum(p.cost_eth for p in pending_review)
    total_pending_revenue = sum(p.expected_monthly_revenue_btc for p in pending_review)
    
    return {
        "status_breakdown": status_counts,
        "total_pending_cost_eth": round(total_pending_cost, 4),
        "total_pending_revenue_btc": round(total_pending_revenue, 4),
        "pipeline_value": round(total_pending_revenue * 15 - total_pending_cost, 4)  # Simplified ETH/BTC conversion
    }

def _get_treasury_overview(transactions: List[TreasuryTransaction]) -> Dict[str, Any]:
    """Get treasury overview"""
    # Group transactions by type
    transaction_types = {}
    for transaction in transactions:
        tx_type = transaction.transaction_type
        if tx_type not in transaction_types:
            transaction_types[tx_type] = {"count": 0, "total_amount": 0.0}
        transaction_types[tx_type]["count"] += 1
        transaction_types[tx_type]["total_amount"] += transaction.amount
    
    # Calculate asset distribution
    asset_distribution = {}
    for transaction in transactions:
        asset = transaction.asset
        if asset not in asset_distribution:
            asset_distribution[asset] = 0.0
        asset_distribution[asset] += transaction.amount
    
    return {
        "transaction_types": transaction_types,
        "asset_distribution": asset_distribution,
        "total_transactions": len(transactions)
    }

def _get_strategic_insights(councils: List[Council], proposals: List[Proposal]) -> List[str]:
    """Generate strategic insights for the King"""
    insights = []
    
    # Insight 1: Most collaborative council
    collaboration_scores = []
    for council in councils:
        council_proposals = [p for p in proposals if p.council_id == council.id]
        score = _calculate_collaboration_score(council_proposals)
        collaboration_scores.append((council.council_name, score))
    
    if collaboration_scores:
        most_collaborative = max(collaboration_scores, key=lambda x: x[1])
        if most_collaborative[1] > 0:
            insights.append(f"The {most_collaborative[0]} is the most collaborative council with a score of {most_collaborative[1]}.")
    
    # Insight 2: Proposal pipeline health
    pending_proposals = [p for p in proposals if p.status in ["PENDING_REVIEW", "AWAITING_SOVEREIGN_APPROVAL"]]
    if len(pending_proposals) > 10:
        insights.append("The proposal pipeline is full with over 10 pending proposals. Consider prioritizing decisions.")
    elif len(pending_proposals) == 0:
        insights.append("The proposal pipeline is empty. Councils may need encouragement to submit new initiatives.")
    
    # Insight 3: High ROI opportunities
    high_roi_proposals = [p for p in pending_proposals if p.roi_score and p.roi_score > 2.0]
    if len(high_roi_proposals) > 3:
        insights.append(f"There are {len(high_roi_proposals)} high-ROI proposals awaiting approval.")
    
    return insights