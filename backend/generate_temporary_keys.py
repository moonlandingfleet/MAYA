#!/usr/bin/env python3
"""
Script to generate temporary RSA keys for RS256 JWT validation
when the Supabase JWKS endpoint is not working.
"""

import jwt
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import base64
import hashlib

def generate_rsa_keypair():
    """Generate a new RSA key pair"""
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Get public key
    public_key = private_key.public_key()
    
    return private_key, public_key

def private_key_to_pem(private_key):
    """Convert private key to PEM format"""
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    return pem.decode('utf-8')

def public_key_to_pem(public_key):
    """Convert public key to PEM format"""
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem.decode('utf-8')

def public_key_to_jwk(public_key, key_id="temp-key-1"):
    """Convert public key to JWK format"""
    # Get the public numbers
    public_numbers = public_key.public_numbers()
    
    # Convert to JWK format
    jwk = {
        "kty": "RSA",
        "kid": key_id,
        "use": "sig",
        "alg": "RS256",
        "n": base64url_encode(public_numbers.n.to_bytes((public_numbers.n.bit_length() + 7) // 8, 'big')),
        "e": base64url_encode(public_numbers.e.to_bytes((public_numbers.e.bit_length() + 7) // 8, 'big'))
    }
    
    return jwk

def base64url_encode(data):
    """Base64 URL encode data"""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def create_temp_auth_config():
    """Create temporary auth configuration"""
    private_key, public_key = generate_rsa_keypair()
    
    # Convert keys to PEM format
    private_pem = private_key_to_pem(private_key)
    public_pem = public_key_to_pem(public_key)
    
    # Convert public key to JWK
    jwk = public_key_to_jwk(public_key)
    
    # Create JWKS
    jwks = {
        "keys": [jwk]
    }
    
    return {
        "private_key_pem": private_pem,
        "public_key_pem": public_pem,
        "jwk": jwk,
        "jwks": jwks
    }

def main():
    print("Generating temporary RSA key pair for RS256 JWT validation...")
    
    config = create_temp_auth_config()
    
    # Save private key
    with open("temp_private_key.pem", "w") as f:
        f.write(config["private_key_pem"])
    
    # Save public key
    with open("temp_public_key.pem", "w") as f:
        f.write(config["public_key_pem"])
    
    # Save JWK
    with open("temp_jwk.json", "w") as f:
        json.dump(config["jwk"], f, indent=2)
    
    # Save JWKS
    with open("temp_jwks.json", "w") as f:
        json.dump(config["jwks"], f, indent=2)
    
    print("\nFiles created:")
    print("- temp_private_key.pem: Private key in PEM format")
    print("- temp_public_key.pem: Public key in PEM format")
    print("- temp_jwk.json: Public key in JWK format")
    print("- temp_jwks.json: JWKS with the public key")
    
    print("\nTo use these keys for JWT validation, update your auth.py to:")
    print("1. Load the JWK from temp_jwk.json")
    print("2. Use it for RS256 validation instead of fetching from Supabase JWKS endpoint")
    
    # Example of how to use the keys for JWT operations
    print("\nExample usage:")
    print("```python")
    print("# To create a test JWT token")
    print("import jwt")
    print("with open('temp_private_key.pem', 'r') as f:")
    print("    private_key = f.read()")
    print("payload = {'sub': 'test-user', 'exp': 9999999999}")
    print("token = jwt.encode(payload, private_key, algorithm='RS256', headers={'kid': 'temp-key-1'})")
    print("print('Test token:', token)")
    print("```")

if __name__ == "__main__":
    main()