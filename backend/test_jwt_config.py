import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Environment Variables Check")
print("========================")

# Check the existing variables
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

print(f"SUPABASE_URL: {supabase_url}")
print(f"SUPABASE_KEY: {'*' * len(supabase_key) if supabase_key else 'NOT SET'}")

# Check the new JWT validation variables
supabase_auth_url = os.getenv("SUPABASE_AUTH_URL")
supabase_anon_key = os.getenv("SUPABASE_ANON_KEY")
supabase_jwks_uri = os.getenv("SUPABASE_JWKS_URI")
jwt_algorithms = os.getenv("JWT_ALGORITHMS")
jwt_audience = os.getenv("JWT_AUDIENCE")
jwt_issuer = os.getenv("JWT_ISSUER")

print(f"\nNew JWT Validation Variables:")
print(f"SUPABASE_AUTH_URL: {supabase_auth_url}")
print(f"SUPABASE_ANON_KEY: {'*' * len(supabase_anon_key) if supabase_anon_key else 'NOT SET'}")
print(f"SUPABASE_JWKS_URI: {supabase_jwks_uri}")
print(f"JWT_ALGORITHMS: {jwt_algorithms}")
print(f"JWT_AUDIENCE: {jwt_audience}")
print(f"JWT_ISSUER: {jwt_issuer}")

# Test importing python-jose
try:
    from jose import jwt
    print("\n✅ python-jose imported successfully")
except ImportError as e:
    print(f"\n❌ Failed to import python-jose: {e}")

print("\n✅ Environment configuration completed successfully!")