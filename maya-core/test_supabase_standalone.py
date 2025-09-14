import os
import sys
from dotenv import load_dotenv
from maya_supabase.database import SupabaseService

def test_supabase_standalone():
    """Test Supabase functionality without web3 dependencies"""
    
    print("Testing Supabase Integration Standalone")
    print("=====================================")
    
    # Load environment variables
    load_dotenv()
    
    # Test Supabase service initialization
    print("1. Initializing Supabase service...")
    try:
        db_service = SupabaseService()
        if db_service.client:
            print("   ✅ Supabase service initialized successfully")
        else:
            print("   ❌ Supabase service failed to initialize")
            return False
    except Exception as e:
        print(f"   ❌ Error initializing Supabase service: {e}")
        return False
    
    # Test basic connectivity
    print("2. Testing basic connectivity...")
    try:
        response = db_service.client.table("councils").select("*").limit(1).execute()
        print("   ✅ Basic connectivity test passed")
    except Exception as e:
        print(f"   ❌ Basic connectivity test failed: {e}")
        return False
    
    # Test data operations
    print("3. Testing data operations...")
    try:
        # Get all councils
        councils = db_service.get_all_councils()
        print(f"   ✅ Retrieved {len(councils)} councils from database")
        
        # Get all proposals
        proposals = db_service.get_all_proposals()
        print(f"   ✅ Retrieved {len(proposals)} proposals from database")
        
        print("   ✅ All data operations completed successfully")
    except Exception as e:
        print(f"   ❌ Data operations failed: {e}")
        return False
    
    print("\n🎉 All Supabase tests passed!")
    print("The Supabase integration is working correctly.")
    return True

if __name__ == "__main__":
    success = test_supabase_standalone()
    sys.exit(0 if success else 1)