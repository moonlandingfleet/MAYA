import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Supabase credentials
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

print("Key Cleaning and Verification")
print("=============================")
print(f"Original key: {repr(supabase_key)}")

# Thoroughly clean the key
# Remove all non-alphanumeric characters except underscore and 'p' after 'sb'
cleaned_key = re.sub(r'[^a-zA-Z0-9_]', '', supabase_key)
print(f"Regex cleaned key: {repr(cleaned_key)}")

# Manually reconstruct the key to ensure correct format
# Service role keys should start with 'sbp_'
if cleaned_key.startswith('sbp'):
    print("Key format looks correct")
else:
    # Try to fix the key format
    if cleaned_key.startswith('sb'):
        cleaned_key = 'sbp_' + cleaned_key[3:]
        print(f"Fixed key format: {repr(cleaned_key)}")
    else:
        print("Key format is unexpected")

print(f"Final cleaned key: {repr(cleaned_key)}")
print(f"Key length: {len(cleaned_key)}")

# Create a new .env file with the cleaned key
new_env_content = f"SUPABASE_URL={supabase_url}\nSUPABASE_KEY={cleaned_key}\n"

with open('.env.cleaned', 'w') as f:
    f.write(new_env_content)

print("Created .env.cleaned file with cleaned key")

# Also create a test script to verify the cleaned key
test_script = f'''
import os
from supabase import create_client, Client

supabase_url = "{supabase_url}"
supabase_key = "{cleaned_key}"

print("Testing with cleaned key:")
print(f"Key length: {{len(supabase_key)}}")

try:
    print("Initializing Supabase client...")
    supabase: Client = create_client(supabase_url, supabase_key)
    print("SUCCESS: Supabase client initialized successfully")
except Exception as e:
    print(f"ERROR: {{e}}")
'''

with open('test_with_cleaned_key.py', 'w') as f:
    f.write(test_script)

print("Created test_with_cleaned_key.py script")