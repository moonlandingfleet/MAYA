import os
from dotenv import load_dotenv
from maya_supabase.database import SupabaseService
from maya_supabase.models import Council
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Supabase service
db_service = SupabaseService()

if not db_service.client:
    print("Failed to initialize Supabase service")
    exit(1)

# Create a test council
test_council = Council(
    id="test_council",
    council_name="Test Council",
    domain_description="A test council for development purposes",
    revenue_model_description="Test revenue model",
    ethical_boundary="Test ethical boundary",
    status="ACTIVE",
    created_at=datetime.utcnow()
)

# Insert the council into the database
try:
    created_council = db_service.create_council(test_council)
    if created_council:
        print(f"Successfully created council: {created_council.council_name}")
    else:
        print("Failed to create council")
except Exception as e:
    print(f"Error creating council: {e}")