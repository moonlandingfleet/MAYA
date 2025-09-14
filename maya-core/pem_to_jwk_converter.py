#!/usr/bin/env python3
"""
PEM to JWK Converter Script

This script converts RSA public keys from PEM format to JWK format.
This is useful if you need to reconstruct the public_jwk field for signing keys.

Usage:
    python pem_to_jwk_converter.py public.pem

The script will output the JWK JSON that can be used to populate the public_jwk field.
"""

import sys
import json
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import hashlib
import base64url

def base64url_encode(data):
    """Encode data in Base64URL format"""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def pem_to_jwk(pem_file_path, kid=None):
    """
    Convert RSA public key from PEM format to JWK format
    
    Args:
        pem_file_path (str): Path to the PEM file containing the public key
        kid (str, optional): Key ID to use in the JWK. If None, will be generated from key content.
    
    Returns:
        dict: JWK representation of the public key
    """
    # Read the PEM file
    with open(pem_file_path, 'rb') as f:
        pem_data = f.read()
    
    # Load the public key
    public_key = serialization.load_pem_public_key(pem_data)
    
    # Ensure it's an RSA key
    if not isinstance(public_key, rsa.RSAPublicKey):
        raise ValueError("Only RSA keys are supported")
    
    # Get the public numbers
    public_numbers = public_key.public_numbers()
    
    # Convert to JWK format
    n = public_numbers.n
    e = public_numbers.e
    
    # Encode the values
    n_bytes = n.to_bytes((n.bit_length() + 7) // 8, 'big')
    e_bytes = e.to_bytes((e.bit_length() + 7) // 8, 'big')
    
    # Create the JWK
    jwk = {
        "kty": "RSA",
        "use": "sig",
        "alg": "RS256",
        "n": base64url_encode(n_bytes),
        "e": base64url_encode(e_bytes)
    }
    
    # Generate or use provided kid
    if kid is None:
        # Generate kid from key content
        key_content = f"{jwk['n']}.{jwk['e']}"
        kid = hashlib.sha256(key_content.encode()).hexdigest()[:16]
    
    jwk["kid"] = kid
    
    return jwk

def main():
    if len(sys.argv) < 2:
        print("Usage: python pem_to_jwk_converter.py public.pem [kid]")
        print("  public.pem: Path to the PEM file containing the RSA public key")
        print("  kid: Optional key ID to use in the JWK (if not provided, one will be generated)")
        sys.exit(1)
    
    pem_file_path = sys.argv[1]
    kid = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        jwk = pem_to_jwk(pem_file_path, kid)
        print("Generated JWK:")
        print(json.dumps(jwk, indent=2))
        print("\nTo use this in an UPDATE statement:")
        print(f"UPDATE auth.signing_keys SET public_jwk = '{json.dumps(jwk)}' WHERE id = 'YOUR_KEY_ID';")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()