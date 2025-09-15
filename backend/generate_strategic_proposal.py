"""
Strategic Proposal Generator for the Digital Kingdom Councils
This utility helps councils generate well-structured strategic proposals for the King's review.
"""

from maya_supabase.models import Proposal
from datetime import datetime
from typing import List, Dict, Any

class StrategicProposalGenerator:
    """Helper class to generate strategic proposals for councils"""
    
    @staticmethod
    def create_identity_proposal(
        council_id: str,
        service_type: str,
        cost_eth: float = 5.0,
        expected_revenue_btc: float = 0.1
    ) -> Proposal:
        """Create a strategic proposal for the Council of Digital Identity"""
        return Proposal(
            id=None,
            council_id=council_id,
            purpose=f"Launch {service_type} identity service for the digital kingdom",
            cost_eth=cost_eth,
            expected_monthly_revenue_btc=expected_revenue_btc,
            status="PENDING_REVIEW",
            details_json={"service_type": service_type},
            submitted_at=datetime.utcnow(),
            last_status_update_at=datetime.utcnow(),
            sovereign_approved_at=None,
            funding_transaction_hash=None,
            roi_score=0.0,
            
            # Enhanced strategic fields
            strategic_impact="Establishes the foundation for all other digital services by providing secure identity management",
            resource_dependencies=["computing_power", "security_audits"],
            inter_council_collaborations=["council_digital_commerce", "council_digital_health"],
            implementation_timeline_days=60,
            risk_assessment="Security risks if implementation is flawed; requires thorough auditing",
            success_metrics=["User adoption rate", "Security incident count", "Service uptime"]
        )
    
    @staticmethod
    def create_commerce_proposal(
        council_id: str,
        platform_type: str,
        cost_eth: float = 10.0,
        expected_revenue_btc: float = 0.25
    ) -> Proposal:
        """Create a strategic proposal for the Council of Digital Commerce"""
        return Proposal(
            id=None,
            council_id=council_id,
            purpose=f"Create {platform_type} marketplace for peer-to-peer exchange in the digital kingdom",
            cost_eth=cost_eth,
            expected_monthly_revenue_btc=expected_revenue_btc,
            status="PENDING_REVIEW",
            details_json={"platform_type": platform_type},
            submitted_at=datetime.utcnow(),
            last_status_update_at=datetime.utcnow(),
            sovereign_approved_at=None,
            funding_transaction_hash=None,
            roi_score=0.0,
            
            # Enhanced strategic fields
            strategic_impact="Drives economic activity and value creation within the digital kingdom",
            resource_dependencies=["identity_verification", "payment_processing_infrastructure"],
            inter_council_collaborations=["council_digital_identity", "council_digital_storage"],
            implementation_timeline_days=90,
            risk_assessment="Market adoption risk; competition from existing platforms",
            success_metrics=["Transaction volume", "User count", "Revenue growth"]
        )
    
    @staticmethod
    def create_resource_proposal(
        council_id: str,
        resource_type: str,
        cost_eth: float = 3.0,
        expected_revenue_btc: float = 0.05
    ) -> Proposal:
        """Create a strategic proposal for the Council of Digital Resources"""
        return Proposal(
            id=None,
            council_id=council_id,
            purpose=f"Coordinate {resource_type} resources across the digital kingdom",
            cost_eth=cost_eth,
            expected_monthly_revenue_btc=expected_revenue_btc,
            status="PENDING_REVIEW",
            details_json={"resource_type": resource_type},
            submitted_at=datetime.utcnow(),
            last_status_update_at=datetime.utcnow(),
            sovereign_approved_at=None,
            funding_transaction_hash=None,
            roi_score=0.0,
            
            # Enhanced strategic fields
            strategic_impact="Ensures optimal allocation of computational and network resources for all kingdom services",
            resource_dependencies=["resource_monitoring_tools", "allocation_algorithms"],
            inter_council_collaborations=["council_digital_storage", "council_digital_energy"],
            implementation_timeline_days=45,
            risk_assessment="Resource contention risks; potential for inefficient allocation",
            success_metrics=["Resource utilization rate", "Service response time", "Resource availability"]
        )
    
    @staticmethod
    def create_generic_proposal(
        council_id: str,
        purpose: str,
        cost_eth: float,
        expected_revenue_btc: float,
        strategic_impact: str,
        resource_dependencies: List[str],
        collaborating_councils: List[str],
        implementation_days: int = 30,
        risk_assessment: str = "Standard implementation risks",
        success_metrics: List[str] = None
    ) -> Proposal:
        """Create a generic strategic proposal with all fields specified"""
        if success_metrics is None:
            success_metrics = ["Key performance indicators to be defined"]
            
        return Proposal(
            id=None,
            council_id=council_id,
            purpose=purpose,
            cost_eth=cost_eth,
            expected_monthly_revenue_btc=expected_revenue_btc,
            status="PENDING_REVIEW",
            details_json={"custom_proposal": True},
            submitted_at=datetime.utcnow(),
            last_status_update_at=datetime.utcnow(),
            sovereign_approved_at=None,
            funding_transaction_hash=None,
            roi_score=0.0,
            
            # Enhanced strategic fields
            strategic_impact=strategic_impact,
            resource_dependencies=resource_dependencies,
            inter_council_collaborations=collaborating_councils,
            implementation_timeline_days=implementation_days,
            risk_assessment=risk_assessment,
            success_metrics=success_metrics
        )

def main():
    """Example usage of the Strategic Proposal Generator"""
    print("Strategic Proposal Generator for Digital Kingdom")
    print("=" * 50)
    
    # Example: Generate an identity proposal
    identity_proposal = StrategicProposalGenerator.create_identity_proposal(
        council_id="council_digital_identity",
        service_type="Zero-Knowledge Proof"
    )
    
    print("Generated Identity Proposal:")
    print(f"Purpose: {identity_proposal.purpose}")
    print(f"Cost: {identity_proposal.cost_eth} ETH")
    print(f"Expected Revenue: {identity_proposal.expected_monthly_revenue_btc} BTC/month")
    print(f"Strategic Impact: {identity_proposal.strategic_impact}")
    print(f"Collaborations: {identity_proposal.inter_council_collaborations}")
    print()
    
    # Example: Generate a commerce proposal
    commerce_proposal = StrategicProposalGenerator.create_commerce_proposal(
        council_id="council_digital_commerce",
        platform_type="Decentralized NFT Marketplace"
    )
    
    print("Generated Commerce Proposal:")
    print(f"Purpose: {commerce_proposal.purpose}")
    print(f"Cost: {commerce_proposal.cost_eth} ETH")
    print(f"Expected Revenue: {commerce_proposal.expected_monthly_revenue_btc} BTC/month")
    print(f"Strategic Impact: {commerce_proposal.strategic_impact}")
    print(f"Collaborations: {commerce_proposal.inter_council_collaborations}")
    print()
    
    # Example: Generate a resource proposal
    resource_proposal = StrategicProposalGenerator.create_resource_proposal(
        council_id="council_digital_resources",
        resource_type="GPU Computing Pool"
    )
    
    print("Generated Resource Proposal:")
    print(f"Purpose: {resource_proposal.purpose}")
    print(f"Cost: {resource_proposal.cost_eth} ETH")
    print(f"Expected Revenue: {resource_proposal.expected_monthly_revenue_btc} BTC/month")
    print(f"Strategic Impact: {resource_proposal.strategic_impact}")
    print(f"Collaborations: {resource_proposal.inter_council_collaborations}")

if __name__ == "__main__":
    main()