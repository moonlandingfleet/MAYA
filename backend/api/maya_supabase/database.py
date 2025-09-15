import os
from typing import List, Optional
from supabase import create_client, Client
from maya_supabase.models import Council, Proposal, TreasuryTransaction, CouncilOpportunity
from datetime import datetime
# Load environment variables from .env file
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

class SupabaseService:
    def __init__(self):
        # Initialize Supabase client
        self.url = os.getenv("SUPABASE_URL", "")
        self.key = os.getenv("SUPABASE_KEY", "")
        if self.url and self.key:
            try:
                self.client: Client = create_client(self.url, self.key)
            except Exception as e:
                print(f"Warning: Failed to initialize Supabase client: {e}")
                print("Supabase database operations will be disabled.")
                self.client = None
        else:
            self.client = None
            print("Warning: Supabase credentials not found. Database operations will be disabled.")

    def _serialize_datetime(self, obj):
        """Helper method to serialize datetime objects to ISO format strings"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {key: self._serialize_datetime(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._serialize_datetime(item) for item in obj]
        return obj

    # Council operations
    def create_council(self, council: Council) -> Optional[Council]:
        """Create a new council"""
        if not self.client:
            return None
            
        try:
            # Convert datetime objects to ISO format strings
            council_dict = self._serialize_datetime(council.dict())
            response = self.client.table("councils").insert(council_dict).execute()
            return Council(**response.data[0]) if response.data else None
        except Exception as e:
            print(f"Error creating council: {e}")
            return None

    def get_council(self, council_id: str) -> Optional[Council]:
        """Get a council by ID"""
        if not self.client:
            return None
            
        try:
            response = self.client.table("councils").select("*").eq("id", council_id).execute()
            return Council(**response.data[0]) if response.data else None
        except Exception as e:
            print(f"Error getting council: {e}")
            return None

    def get_all_councils(self) -> List[Council]:
        """Get all councils"""
        if not self.client:
            return []
            
        try:
            response = self.client.table("councils").select("*").execute()
            return [Council(**item) for item in response.data] if response.data else []
        except Exception as e:
            print(f"Error getting councils: {e}")
            return []

    def update_council(self, council_id: str, council_data: dict) -> Optional[Council]:
        """Update a council"""
        if not self.client:
            return None
            
        try:
            # Convert datetime objects to ISO format strings
            council_data = self._serialize_datetime(council_data)
            response = self.client.table("councils").update(council_data).eq("id", council_id).execute()
            return Council(**response.data[0]) if response.data else None
        except Exception as e:
            print(f"Error updating council: {e}")
            return None

    def delete_council(self, council_id: str) -> bool:
        """Delete a council"""
        if not self.client:
            return False
            
        try:
            self.client.table("councils").delete().eq("id", council_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting council: {e}")
            return False

    # Proposal operations
    def create_proposal(self, proposal: Proposal) -> Optional[Proposal]:
        """Create a new proposal"""
        if not self.client:
            return None
            
        try:
            # Convert datetime objects to ISO format strings
            proposal_dict = self._serialize_datetime(proposal.dict())
            # Remove the id field if it's None so Supabase can auto-generate it
            if proposal_dict.get('id') is None:
                del proposal_dict['id']
                
            response = self.client.table("proposals").insert(proposal_dict).execute()
            return Proposal(**response.data[0]) if response.data else None
        except Exception as e:
            print(f"Error creating proposal: {e}")
            return None

    def get_proposal(self, proposal_id: str) -> Optional[Proposal]:
        """Get a proposal by ID"""
        if not self.client:
            return None
            
        try:
            response = self.client.table("proposals").select("*").eq("id", proposal_id).execute()
            return Proposal(**response.data[0]) if response.data else None
        except Exception as e:
            print(f"Error getting proposal: {e}")
            return None

    def get_proposals_by_council(self, council_id: str) -> List[Proposal]:
        """Get all proposals for a council"""
        if not self.client:
            return []
            
        try:
            response = self.client.table("proposals").select("*").eq("council_id", council_id).execute()
            return [Proposal(**item) for item in response.data] if response.data else []
        except Exception as e:
            print(f"Error getting proposals: {e}")
            return []

    def get_all_proposals(self) -> List[Proposal]:
        """Get all proposals"""
        if not self.client:
            return []
            
        try:
            response = self.client.table("proposals").select("*").execute()
            return [Proposal(**item) for item in response.data] if response.data else []
        except Exception as e:
            print(f"Error getting proposals: {e}")
            return []

    def update_proposal(self, proposal_id: str, proposal_data: dict) -> Optional[Proposal]:
        """Update a proposal"""
        if not self.client:
            return None
            
        try:
            # Convert datetime objects to ISO format strings
            proposal_data = self._serialize_datetime(proposal_data)
            response = self.client.table("proposals").update(proposal_data).eq("id", proposal_id).execute()
            return Proposal(**response.data[0]) if response.data else None
        except Exception as e:
            print(f"Error updating proposal: {e}")
            return None

    def delete_proposal(self, proposal_id: str) -> bool:
        """Delete a proposal"""
        if not self.client:
            return False
            
        try:
            self.client.table("proposals").delete().eq("id", proposal_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting proposal: {e}")
            return False

    # Treasury transaction operations
    def create_treasury_transaction(self, transaction: TreasuryTransaction) -> Optional[TreasuryTransaction]:
        """Create a new treasury transaction"""
        if not self.client:
            return None
            
        try:
            # Convert datetime objects to ISO format strings
            transaction_dict = self._serialize_datetime(transaction.dict())
            # Remove the id field if it's None so Supabase can auto-generate it
            if transaction_dict.get('id') is None:
                del transaction_dict['id']
                
            response = self.client.table("treasury_transactions").insert(transaction_dict).execute()
            return TreasuryTransaction(**response.data[0]) if response.data else None
        except Exception as e:
            print(f"Error creating treasury transaction: {e}")
            return None

    def get_treasury_transaction(self, transaction_id: str) -> Optional[TreasuryTransaction]:
        """Get a treasury transaction by ID"""
        if not self.client:
            return None
            
        try:
            response = self.client.table("treasury_transactions").select("*").eq("id", transaction_id).execute()
            return TreasuryTransaction(**response.data[0]) if response.data else None
        except Exception as e:
            print(f"Error getting treasury transaction: {e}")
            return None

    def get_treasury_transactions_by_council(self, council_id: str) -> List[TreasuryTransaction]:
        """Get all treasury transactions for a council"""
        if not self.client:
            return []
            
        try:
            response = self.client.table("treasury_transactions").select("*").eq("council_id", council_id).execute()
            return [TreasuryTransaction(**item) for item in response.data] if response.data else []
        except Exception as e:
            print(f"Error getting treasury transactions: {e}")
            return []

    def get_all_treasury_transactions(self) -> List[TreasuryTransaction]:
        """Get all treasury transactions"""
        if not self.client:
            return []
            
        try:
            response = self.client.table("treasury_transactions").select("*").execute()
            return [TreasuryTransaction(**item) for item in response.data] if response.data else []
        except Exception as e:
            print(f"Error getting treasury transactions: {e}")
            return []

    # Council opportunity operations
    def create_council_opportunity(self, opportunity: CouncilOpportunity) -> Optional[CouncilOpportunity]:
        """Create a new council opportunity"""
        if not self.client:
            return None
            
        try:
            # Convert datetime objects to ISO format strings
            opportunity_dict = self._serialize_datetime(opportunity.dict())
            # Remove the id field if it's None so Supabase can auto-generate it
            if opportunity_dict.get('id') is None:
                del opportunity_dict['id']
                
            response = self.client.table("council_opportunities").insert(opportunity_dict).execute()
            return CouncilOpportunity(**response.data[0]) if response.data else None
        except Exception as e:
            print(f"Error creating council opportunity: {e}")
            return None

    def get_council_opportunity(self, opportunity_id: str) -> Optional[CouncilOpportunity]:
        """Get a council opportunity by ID"""
        if not self.client:
            return None
            
        try:
            response = self.client.table("council_opportunities").select("*").eq("id", opportunity_id).execute()
            return CouncilOpportunity(**response.data[0]) if response.data else None
        except Exception as e:
            print(f"Error getting council opportunity: {e}")
            return None

    def get_council_opportunities_by_council(self, council_id: str) -> List[CouncilOpportunity]:
        """Get all council opportunities for a council"""
        if not self.client:
            return []
            
        try:
            response = self.client.table("council_opportunities").select("*").eq("council_id", council_id).execute()
            return [CouncilOpportunity(**item) for item in response.data] if response.data else []
        except Exception as e:
            print(f"Error getting council opportunities: {e}")
            return []

    def get_all_council_opportunities(self) -> List[CouncilOpportunity]:
        """Get all council opportunities"""
        if not self.client:
            return []
            
        try:
            response = self.client.table("council_opportunities").select("*").execute()
            return [CouncilOpportunity(**item) for item in response.data] if response.data else []
        except Exception as e:
            print(f"Error getting council opportunities: {e}")
            return []

    def update_council_opportunity(self, opportunity_id: str, opportunity_data: dict) -> Optional[CouncilOpportunity]:
        """Update a council opportunity"""
        if not self.client:
            return None
            
        try:
            # Convert datetime objects to ISO format strings
            opportunity_data = self._serialize_datetime(opportunity_data)
            response = self.client.table("council_opportunities").update(opportunity_data).eq("id", opportunity_id).execute()
            return CouncilOpportunity(**response.data[0]) if response.data else None
        except Exception as e:
            print(f"Error updating council opportunity: {e}")
            return None

    def delete_council_opportunity(self, opportunity_id: str) -> bool:
        """Delete a council opportunity"""
        if not self.client:
            return False
            
        try:
            self.client.table("council_opportunities").delete().eq("id", opportunity_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting council opportunity: {e}")
            return False