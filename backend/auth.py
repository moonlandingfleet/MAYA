import os
import requests
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, ExpiredSignatureError, JWTError
from typing import Dict, Any, Optional

# --- Configuration from Environment Variables ---
SUPABASE_JWKS_URI = os.getenv("SUPABASE_JWKS_URI")  # For RS256
SUPABASE_AUTH_JWT_SECRET = os.getenv("SUPABASE_AUTH_JWT_SECRET")  # For HS256
JWT_ALGORITHMS = os.getenv("JWT_ALGORITHMS", "RS256").split(',')
JWT_AUDIENCE = os.getenv("JWT_AUDIENCE")
JWT_ISSUER = os.getenv("JWT_ISSUER")
TESTING_ENVIRONMENT = os.getenv("TESTING_ENVIRONMENT", "false").lower() == "true"

# --- JWKS Caching ---
jwks_cache = None
jwks_cache_timestamp = 0
JWKS_CACHE_DURATION = 300  # 5 minutes

def get_jwks():
    """
    Fetches and caches the JSON Web Key Set (JWKS) from Supabase.
    """
    global jwks_cache, jwks_cache_timestamp
    import time
    
    current_time = time.time()
    if jwks_cache and (current_time - jwks_cache_timestamp) < JWKS_CACHE_DURATION:
        return jwks_cache

    if not SUPABASE_JWKS_URI:
        print("SUPABASE_JWKS_URI not configured. JWKS fetch skipped.")
        return None
        
    try:
        print("Fetching JWKS from Supabase...")
        response = requests.get(SUPABASE_JWKS_URI)
        response.raise_for_status()
        jwks_cache = response.json()
        jwks_cache_timestamp = current_time
        print("Successfully fetched and cached JWKS.")
        return jwks_cache
    except requests.RequestException as e:
        print(f"Error fetching JWKS: {e}")
        jwks_cache = None
        return None

# --- Token Validation Scheme ---
token_auth_scheme = HTTPBearer()

async def verify_token_and_get_payload(token: HTTPAuthorizationCredentials = Depends(token_auth_scheme)) -> Dict[str, Any]:
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated", headers={"WWW-Authenticate": "Bearer"})
    
    jwt_token = token.credentials
    
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials - token may be invalid, expired, or lack correct permissions.",
        headers={"WWW-Authenticate": "Bearer"}
    )
    last_error = None

    # Attempt RS256 validation first if configured (Supabase default)
    if "RS256" in JWT_ALGORITHMS:
        jwks = get_jwks()
        if jwks:
            try:
                print("Attempting RS256 validation...")
                unverified_header = jwt.get_unverified_header(jwt_token)
                rsa_key = {}
                for key_spec in jwks.get("keys", []):
                    if key_spec.get("kid") == unverified_header.get("kid"):
                        rsa_key = {
                            "kty": key_spec.get("kty"),
                            "kid": key_spec.get("kid"),
                            "use": key_spec.get("use"),
                            "n": key_spec.get("n"),
                            "e": key_spec.get("e")
                        }
                if not rsa_key:
                    print("RS256: Signing key not found in JWKS for the given kid.")
                    last_error = JWTError("RS256: Signing key not found in JWKS.")
                else:
                    payload = jwt.decode(
                        jwt_token, rsa_key, algorithms=["RS256"],
                        audience=JWT_AUDIENCE, issuer=JWT_ISSUER
                    )
                    print("RS256 validation successful.")
                    if payload.get("sub") is None:
                        print("Error: User ID (sub) not found in RS256 token payload.")
                        raise credentials_exception
                    return payload
            except ExpiredSignatureError:
                print("RS256: Token has expired.")
                last_error = ExpiredSignatureError("RS256: Token has expired.")
            except JWTError as e:
                print(f"RS256 validation failed: {e}")
                last_error = e
        else:
            print("Skipping RS256 validation as JWKS could not be fetched.")
            last_error = JWTError("RS256: JWKS not available.")

    # Attempt HS256 validation if configured and RS256 failed or wasn't configured
    if "HS256" in JWT_ALGORITHMS:
        if not SUPABASE_AUTH_JWT_SECRET:
            print("Warning: HS256 is in JWT_ALGORITHMS but SUPABASE_AUTH_JWT_SECRET is not set. HS256 validation skipped.")
            if not last_error: last_error = JWTError("HS256: Secret not configured.")
        else:
            try:
                print(f"Attempting HS256 validation with SUPABASE_AUTH_JWT_SECRET...")
                payload = jwt.decode(
                    jwt_token, SUPABASE_AUTH_JWT_SECRET, algorithms=["HS256"],
                    audience=JWT_AUDIENCE, issuer=JWT_ISSUER
                )
                print("HS256 validation successful.")
                if payload.get("sub") is None:
                    print("Error: User ID (sub) not found in HS256 token payload.")
                    raise credentials_exception
                return payload
            except ExpiredSignatureError:
                print("HS256: Token has expired.")
                last_error = ExpiredSignatureError("HS256: Token has expired.")
            except JWTError as e:
                print(f"HS256 validation failed: {e}")
                last_error = e

    # TESTING_ENVIRONMENT: If all real validations failed, and we are in testing mode
    if TESTING_ENVIRONMENT and last_error:
        print("--- TESTING MODE ACTIVE ---")
        print(f"All standard token validations failed. Last error: {last_error}")
        print("Attempting to decode token without signature verification (FOR TESTING ONLY!)...")
        try:
            # Use a dummy key for decoding without signature verification
            payload = jwt.decode(
                jwt_token, 
                "dummy-key", 
                options={
                    "verify_signature": False, 
                    "verify_aud": False, 
                    "verify_iss": False, 
                    "verify_exp": True
                },
                algorithms=["RS256", "HS256"]
            )
            print("TESTING MODE: Token decoded without signature. SUB: ", payload.get("sub"))
            if payload.get("sub") is None:
                 print("Error: User ID (sub) not found in TESTING MODE token payload.")
                 raise credentials_exception # Should still have a sub
            return payload
        except ExpiredSignatureError:
            print("TESTING MODE: Token has expired (even without signature check).")
            # Fall through to raise credentials_exception with last_error from real validation attempts
        except JWTError as e:
            print(f"TESTING MODE: Error decoding token even without signature: {e}")
            # Fall through

    # If we are here, all attempts (including testing mode if applicable) failed or weren't applicable.
    if isinstance(last_error, ExpiredSignatureError):
         raise HTTPException(status_code=401, detail=str(last_error), headers={"WWW-Authenticate": "Bearer"})
    
    print(f"Final credentials validation failed. Last error: {last_error if last_error else 'Unknown validation error'}")
    raise credentials_exception

async def get_current_user_id(payload: Dict[str, Any] = Depends(verify_token_and_get_payload)) -> str:
    user_id = payload.get("sub")
    # This check should be redundant if verify_token_and_get_payload ensures 'sub' exists
    if not user_id:
        raise HTTPException(status_code=500, detail="User ID (sub) could not be retrieved after token verification.")
    return user_id