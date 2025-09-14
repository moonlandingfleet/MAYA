-- SIGNING KEY INSERT TEMPLATE
-- This is a template for inserting a new signing key into the auth.signing_keys table.
-- WARNING: This is a destructive operation that should only be performed with explicit permission.
-- WARNING: Never share private keys in unencrypted form.

/*
IMPORTANT SECURITY NOTES:

1. Generate the RSA key pair locally (NOT in the database):
   openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:4096 -out private.pem
   openssl rsa -in private.pem -pubout -out public.pem

2. Convert the public key to JWK format using the pem_to_jwk_converter.py script:
   python pem_to_jwk_converter.py public.pem

3. Store the private key securely (environment variable, secrets manager)

4. Only insert the public_jwk into the database, never the private key
*/

-- Template INSERT statement (replace placeholders with actual values):
INSERT INTO auth.signing_keys (
    id,
    kid,
    alg,
    public_jwk,
    private_key,  -- WARNING: Only include this if you're sure it's encrypted/secure
    created_at,
    updated_at,
    active,
    expires_at
) VALUES (
    'GENERATED_UUID',  -- Use a proper UUID generator
    'GENERATED_KID',   -- Should match the kid in the JWK
    'RS256',
    '{"kty":"RSA","use":"sig","alg":"RS256","n":"PUBLIC_KEY_MODULUS","e":"AQAB","kid":"GENERATED_KID"}',  -- Replace with actual JWK
    NULL,  -- Recommended to leave as NULL and store private key securely elsewhere
    NOW(),
    NOW(),
    true,
    NOW() + INTERVAL '365 days'  -- Adjust expiration as needed
);

-- After inserting the key:
-- 1. Restart the Auth service (contact Supabase Support for managed restart)
-- 2. Verify the JWKS endpoint returns the new key:
--    curl https://ksrvtvqqikwjbqzpgacs.supabase.co/auth/v1/.well-known/jwks.json

-- Example of what the JWKS should look like after successful insertion:
/*
{
  "keys": [
    {
      "alg": "RS256",
      "e": "AQAB",
      "kid": "GENERATED_KID",
      "kty": "RSA",
      "n": "PUBLIC_KEY_MODULUS",
      "use": "sig"
    }
  ]
}
*/