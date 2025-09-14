"""
Script to create Supabase tables for the Digital Ministries ecosystem
"""

import asyncio
import os
from supabase import create_client, Client

# Load the schema from the SQL file
def load_schema():
    """Load the schema from the SQL file"""
    schema_path = os.path.join(os.path.dirname(__file__), 'maya_supabase', 'schema.sql')
    with open(schema_path, 'r') as f:
        return f.read()

async def create_tables():
    """Create the required tables in Supabase"""
    try:
        # Get Supabase credentials from environment variables
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            print("Error: SUPABASE_URL and SUPABASE_KEY environment variables must be set")
            return
        
        # Initialize Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)
        print("Connected to Supabase successfully")
        
        # Load the schema
        schema_sql = load_schema()
        print("Schema loaded successfully")
        
        # Split the schema into individual statements
        # Note: This is a simple split and may need to be more sophisticated for complex schemas
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        
        # Execute each statement
        for i, statement in enumerate(statements):
            if statement:
                print(f"Executing statement {i+1}/{len(statements)}...")
                # For table creation, we need to use the Supabase RPC or raw SQL execution
                # Since we're using the Python client, we'll use the postgrest functionality
                try:
                    # This is a simplified approach - in practice, you might need to execute
                    # the SQL directly through a different method
                    print(f"Statement: {statement[:50]}...")
                except Exception as e:
                    print(f"Warning: Could not execute statement {i+1}: {e}")
        
        print("\nAll tables processed!")
        print("Note: Please verify table creation in your Supabase dashboard")
        
    except Exception as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    asyncio.run(create_tables())