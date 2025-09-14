
import os
import requests # To fetch the JWKS
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, ExpiredSignatureError, JWTError, jwk
from jose.utils import base64url_decode
from typing import Dict, Any, Optional

# Load JWT configuration from environment variables
SUPABASE_JWKS_URI = os.getenv("SUPABASE_JWKS_URI")
JWT_ALGORITHMS = os.getenv("JWT_ALGORITHMS", "RS256").split(',') # Expects a comma-separated list if multiple
JWT_AUDIENCE = os.getenv("JWT_AUDIENCE")
JWT_ISSUER = os.getenv("JWT_ISSUER")

# A simple cache for JWKS to avoid fetching it on every request
# In a production scenario, consider a more robust caching mechanism with TTL
jwks_cache = None

def get_jwks():
    """
    Fetches and caches the JSON Web Key Set (JWKS) from Supabase.
    """
    global jwks_cache
    if jwks_cache:
        return jwks_cache
    
    if not SUPABASE_JWKS_URI:
        print("Error: SUPABASE_JWKS_URI is not set in environment variables.")
        raise JWTError("JWKS URI not configured.")
    try:
        response = requests.get(SUPABASE_JWKS_URI)
        response.raise_for_status() # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        jwks_cache = response.json()
        return jwks_cache
    except requests.exceptions.RequestException as e:
        print(f"Error fetching JWKS: {e}")
        jwks_cache = None # Clear cache on error
        raise JWTError(f"Failed to fetch JWKS: {e}")

# Scheme for extracting the bearer token
token_auth_scheme = HTTPBearer()

async def verify_token_and_get_payload(token: HTTPAuthorizationCredentials = Depends(token_auth_scheme)) -> Dict[str, Any]:
    """
    FastAPI dependency that verifies a Supabase JWT and returns its payload.
    """
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    jwt_token = token.credentials
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        jwks = get_jwks()
        unverified_header = jwt.get_unverified_header(jwt_token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if not rsa_key:
            print("Error: Unable to find appropriate key in JWKS")
            raise credentials_exception

        payload = jwt.decode(
            jwt_token,
            rsa_key,
            algorithms=JWT_ALGORITHMS,
            audience=JWT_AUDIENCE,
            issuer=JWT_ISSUER
        )
        
        user_id: Optional[str] = payload.get("sub")
        if user_id is None:
            print("Error: User ID (sub) not found in token payload.")
            raise credentials_exception
        
        return payload

    except ExpiredSignatureError:
        print("Token has expired.")
        raise HTTPException(
            status_code=401,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as e:
        print(f"JWT validation error: {e}")
        raise credentials_exception
    except Exception as e:
        print(f"An unexpected error occurred during token validation: {e}")
        raise credentials_exception

async def get_current_user_id(payload: Dict[str, Any] = Depends(verify_token_and_get_payload)) -> str:
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=500, detail="User ID not found in token after verification.")
    return user_id

