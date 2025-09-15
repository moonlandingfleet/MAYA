import os
from dotenv import load_dotenv
from maya_supabase.database import SupabaseService

# Load environment variables
load_dotenv()

# Initialize Supabase service
db_service = SupabaseService()

if not db_service.client:
    print("Failed to initialize Supabase service")
    exit(1)

# Get all councils from the database
try:
    councils = db_service.get_all_councils()
    print(f"Found {len(councils)} councils in the database:")
    
    for council in councils:
        print(f"- {council.council_name} ({council.id})")
        print(f"  Domain: {council.domain_description}")
        print(f"  Revenue Model: {council.revenue_model_description}")
        print(f"  Ethical Boundary: {council.ethical_boundary}")
        print(f"  Status: {council.status}")
        print()
        
except Exception as e:
    print(f"Error fetching councils: {e}")