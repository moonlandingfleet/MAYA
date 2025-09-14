"""
Test script to verify Supabase client import
"""

try:
    from supabase import create_client, Client
    print("✓ Supabase client imported successfully")
except Exception as e:
    print(f"✗ Error importing Supabase client: {e}")
    exit(1)

try:
    from dotenv import load_dotenv
    print("✓ python-dotenv imported successfully")
except Exception as e:
    print(f"✗ Error importing python-dotenv: {e}")
    exit(1)

print("\n🎉 All imports successful!")
print("The Supabase integration is properly installed.")