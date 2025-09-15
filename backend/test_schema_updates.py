"""
Test script to verify the enhanced database schema updates
"""

import os
from dotenv import load_dotenv
from maya_supabase.database import SupabaseService
from maya_supabase.models import Proposal, Council
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Supabase service
db_service = SupabaseService()

if not db_service.client:
    print("Failed to initialize Supabase service")
    exit(1)

def test_enhanced_proposal():
    """Test creating and retrieving an enhanced proposal"""
    print("Testing enhanced proposal creation...")
    
    # First, get a council to associate with the proposal
    councils = db_service.get_all_councils()
    if not councils:
        print("No councils found. Please populate councils first.")
        return False
    
    council = councils[0]  # Use the first council
    print(f"Using council: {council.council_name}")
    
    # Create an enhanced proposal
    enhanced_proposal = Proposal(
        id=None,  # Let Supabase auto-generate
        council_id=council.id,
        purpose="Test enhanced proposal for digital kingdom",
        cost_eth=2.5,
        expected_monthly_revenue_btc=0.1,
        status="PENDING_REVIEW",
        details_json={"test": "data"},
        submitted_at=datetime.utcnow(),
        last_status_update_at=datetime.utcnow(),
        sovereign_approved_at=None,
        funding_transaction_hash=None,
        roi_score=0.0,
        
        # Enhanced fields
        strategic_impact="This proposal will enhance the digital kingdom's infrastructure",
        resource_dependencies=["computing_power", "storage"],
        inter_council_collaborations=["council_digital_identity", "council_digital_storage"],
        implementation_timeline_days=45,
        risk_assessment="Low risk with proper implementation",
        success_metrics=["User adoption", "Revenue growth", "System stability"]
    )
    
    try:
        # Create the proposal
        created_proposal = db_service.create_proposal(enhanced_proposal)
        if created_proposal:
            print(f"Successfully created enhanced proposal: {created_proposal.id}")
            
            # Retrieve and verify the proposal
            retrieved_proposal = db_service.get_proposal(created_proposal.id)
            if retrieved_proposal:
                print("Proposal retrieved successfully")
                print(f"Strategic Impact: {retrieved_proposal.strategic_impact}")
                print(f"Resource Dependencies: {retrieved_proposal.resource_dependencies}")
                print(f"Collaborations: {retrieved_proposal.inter_council_collaborations}")
                print(f"Timeline: {retrieved_proposal.implementation_timeline_days} days")
                return True
            else:
                print("Failed to retrieve proposal")
                return False
        else:
            print("Failed to create proposal")
            return False
    except Exception as e:
        print(f"Error creating enhanced proposal: {e}")
        return False

def test_council_overview():
    """Test retrieving council overview"""
    print("\nTesting council overview...")
    
    try:
        councils = db_service.get_all_councils()
        print(f"Found {len(councils)} councils")
        
        for council in councils:
            proposals = db_service.get_proposals_by_council(council.id)
            active_proposals = [p for p in proposals if p.status in ["PENDING_REVIEW", "AWAITING_SOVEREIGN_APPROVAL"]]
            print(f"Council: {council.council_name} ({len(active_proposals)} active proposals)")
        
        return True
    except Exception as e:
        print(f"Error getting council overview: {e}")
        return False

if __name__ == "__main__":
    print("Testing Enhanced Database Schema Updates")
    print("=" * 40)
    
    success = True
    success &= test_enhanced_proposal()
    success &= test_council_overview()
    
    if success:
        print("\nAll tests passed! Schema updates are working correctly.")
    else:
        print("\nSome tests failed. Please check the implementation.")