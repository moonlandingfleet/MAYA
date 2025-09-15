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

# Define the 12 councils with their specific roles
councils_data = [
    {
        "id": "council_digital_identity",
        "council_name": "Council of Digital Identity",
        "domain_description": "Controls access to the digital realm",
        "revenue_model_description": "DID verification, zero-knowledge proofs, wallet-based login",
        "ethical_boundary": "The Gatekeeper",
        "status": "ACTIVE"
    },
    {
        "id": "council_digital_commerce",
        "council_name": "Council of Digital Commerce",
        "domain_description": "Facilitates all economic exchange",
        "revenue_model_description": "NFT marketplace, escrow services, dynamic pricing",
        "ethical_boundary": "The Merchant",
        "status": "ACTIVE"
    },
    {
        "id": "council_digital_resources",
        "council_name": "Council of Digital Resources",
        "domain_description": "Supplies computational power",
        "revenue_model_description": "GPU/CPU allocation, bandwidth sharing",
        "ethical_boundary": "The Provider",
        "status": "ACTIVE"
    },
    {
        "id": "council_digital_communication",
        "council_name": "Council of Digital Communication",
        "domain_description": "Enables all connection",
        "revenue_model_description": "Encrypted messaging, WebRTC video calls",
        "ethical_boundary": "The Messenger",
        "status": "ACTIVE"
    },
    {
        "id": "council_digital_learning",
        "council_name": "Council of Digital Learning",
        "domain_description": "Imparts knowledge and wisdom",
        "revenue_model_description": "Course platforms, certificate NFTs",
        "ethical_boundary": "The Sage",
        "status": "ACTIVE"
    },
    {
        "id": "council_digital_storage",
        "council_name": "Council of Digital Storage",
        "domain_description": "Preserves all digital memory",
        "revenue_model_description": "IPFS pinning, Filecoin integration",
        "ethical_boundary": "The Archivist",
        "status": "ACTIVE"
    },
    {
        "id": "council_digital_health",
        "council_name": "Council of Digital Health",
        "domain_description": "Promotes wellness and vitality",
        "revenue_model_description": "AI coaching, biofeedback processing",
        "ethical_boundary": "The Healer",
        "status": "ACTIVE"
    },
    {
        "id": "council_digital_energy",
        "council_name": "Council of Digital Energy",
        "domain_description": "Orchestrates energy flow",
        "revenue_model_description": "EV charging networks, smart scheduling",
        "ethical_boundary": "The Conductor",
        "status": "ACTIVE"
    },
    {
        "id": "council_digital_agriculture",
        "council_name": "Council of Digital Agriculture",
        "domain_description": "Nourishes the digital realm",
        "revenue_model_description": "Crop yield prediction, supply chain tracking",
        "ethical_boundary": "The Cultivator",
        "status": "ACTIVE"
    },
    {
        "id": "council_digital_rentals",
        "council_name": "Council of Digital Rentals",
        "domain_description": "Manages dwelling and space",
        "revenue_model_description": "Rental listings, price analytics",
        "ethical_boundary": "The Steward",
        "status": "ACTIVE"
    },
    {
        "id": "council_digital_news",
        "council_name": "Council of Digital News",
        "domain_description": "Dispels misinformation",
        "revenue_model_description": "Fact-checking engines, credibility scoring",
        "ethical_boundary": "The Truth-Sayer",
        "status": "ACTIVE"
    },
    {
        "id": "council_digital_events",
        "council_name": "Council of Digital Events",
        "domain_description": "Brings people together",
        "revenue_model_description": "NFT ticketing, virtual events",
        "ethical_boundary": "The Convener",
        "status": "ACTIVE"
    }
]

# Insert the councils into the database
created_councils = []
for council_data in councils_data:
    council = Council(
        id=council_data["id"],
        council_name=council_data["council_name"],
        domain_description=council_data["domain_description"],
        revenue_model_description=council_data["revenue_model_description"],
        ethical_boundary=council_data["ethical_boundary"],
        status=council_data["status"],
        created_at=datetime.utcnow()
    )
    
    try:
        created_council = db_service.create_council(council)
        if created_council:
            created_councils.append(created_council)
            print(f"Successfully created council: {created_council.council_name}")
        else:
            print(f"Failed to create council: {council_data['council_name']}")
    except Exception as e:
        print(f"Error creating council {council_data['council_name']}: {e}")

print(f"\nSuccessfully created {len(created_councils)} councils out of {len(councils_data)}")