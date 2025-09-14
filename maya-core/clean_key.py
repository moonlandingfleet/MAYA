import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Supabase credentials
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

print("Key Cleaning Test")
print("================")
print(f"Original key: {repr(supabase_key)}")

# Clean the key by removing any non-alphanumeric characters except underscore
cleaned_key = re.sub(r'[^a-zA-Z0-9_]', '', supabase_key)

print(f"Cleaned key: {repr(cleaned_key)}")
print(f"Original key length: {len(supabase_key)}")
print(f"Cleaned key length: {len(cleaned_key)}")

# Write the cleaned key to a new .env file
with open('.env.cleaned', 'w') as f:
    f.write(f"SUPABASE_URL={supabase_url}\n")
    f.write(f"SUPABASE_KEY={cleaned_key}\n")

print("Created .env.cleaned file with cleaned key")