# Supabase JWKS Issue Resolution Guide

## Problem Summary
The Supabase JWKS endpoint at `https://ksrvtvqqikwjbqzpgacs.supabase.co/auth/v1/.well-known/jwks.json` returns `{"keys": []}`, preventing RS256 token validation in the MAYA Core authentication system.

## Root Cause
The JWKS endpoint returns an empty keys array because the Auth service (GoTrue v2.179.0) is not publishing any public signing keys. This can happen due to:

1. No signing keys present in the database
2. Signing keys exist but have missing/empty public_jwk field
3. Auth service cannot read or expose the keys
4. Configuration or permission issues

## Files Created for Resolution

### 1. Diagnostic Script
- **File**: [SUPABASE_SIGNING_KEYS_DIAGNOSTIC.sql](file:///c%3A/Users/bryan/Desktop/MAYA/maya-core/SUPABASE_SIGNING_KEYS_DIAGNOSTIC.sql)
- **Purpose**: Run in Supabase SQL editor to check for signing keys
- **Location**: `c:\Users\bryan\Desktop\MAYA\maya-core\SUPABASE_SIGNING_KEYS_DIAGNOSTIC.sql`

### 2. Remediation Plan
- **File**: [SUPABASE_JWKS_REMEDIATION_PLAN.md](file:///c%3A/Users/bryan/Desktop/MAYA/maya-core/SUPABASE_JWKS_REMEDIATION_PLAN.md)
- **Purpose**: Comprehensive guide to resolve the issue
- **Location**: `c:\Users\bryan\Desktop\MAYA\maya-core\SUPABASE_JWKS_REMEDIATION_PLAN.md`

### 3. PEM to JWK Converter
- **File**: [pem_to_jwk_converter.py](file:///c%3A/Users/bryan/Desktop/MAYA/maya-core/pem_to_jwk_converter.py)
- **Purpose**: Convert RSA public keys from PEM to JWK format
- **Location**: `c:\Users\bryan\Desktop\MAYA\maya-core\pem_to_jwk_converter.py`

### 4. Signing Key Insert Template
- **File**: [SIGNING_KEY_INSERT_TEMPLATE.sql](file:///c%3A/Users/bryan/Desktop/MAYA/maya-core/SIGNING_KEY_INSERT_TEMPLATE.sql)
- **Purpose**: Template for inserting new signing keys (use with caution)
- **Location**: `c:\Users\bryan\Desktop\MAYA\maya-core\SIGNING_KEY_INSERT_TEMPLATE.sql`

## Recommended Next Steps

### Immediate Actions
1. **Run Diagnostic Queries**: Execute [SUPABASE_SIGNING_KEYS_DIAGNOSTIC.sql](file:///c%3A/Users/bryan/Desktop/MAYA/maya-core/SUPABASE_SIGNING_KEYS_DIAGNOSTIC.sql) in your Supabase SQL editor
2. **Check Auth Logs**: Look for errors in Supabase Dashboard → Project → Logs → Auth
3. **Verify Configuration**: Check Authentication Settings in the Supabase Dashboard

### Safe Remediation Options
1. **Restart Auth Service**: Contact Supabase Support for a managed restart
2. **Check Existing Keys**: If keys exist but have empty public_jwk, use the converter script
3. **Generate New Keys**: Only as a last resort with explicit permission

### Validation
After any remediation:
```bash
curl https://ksrvtvqqikwjbqzpgacs.supabase.co/auth/v1/.well-known/jwks.json
```
Should return a proper keys array with RSA public keys.

## Security Considerations
- Never share private keys in unencrypted form
- Store private keys securely (environment variables, secrets manager)
- Only insert public_jwk into the database, never private key material
- Rotate keys regularly for security

## Expected Outcome
Once resolved:
1. JWKS endpoint returns proper RSA public keys
2. RS256 validation works in production mode (`TESTING_ENVIRONMENT=false`)
3. No code changes needed in MAYA Core authentication system
4. System ready for production deployment

## Contact Supabase Support
If you're unable to resolve the issue:

**Provide to Support**:
- Project ID: `ksrvtvqqikwjbqzpgacs`
- Issue: JWKS endpoint returns `{"keys": []}`
- Impact: Blocking RS256 validation and production deployment
- Already tried: Diagnostic queries, log checks
- Request: Assistance in repopulating JWKS or managed restart of Auth service

## Files Summary
All created files are located in `c:\Users\bryan\Desktop\MAYA\maya-core\`:
1. `SUPABASE_SIGNING_KEYS_DIAGNOSTIC.sql` - Diagnostic queries
2. `SUPABASE_JWKS_REMEDIATION_PLAN.md` - Comprehensive remediation guide
3. `pem_to_jwk_converter.py` - PEM to JWK conversion script
4. `SIGNING_KEY_INSERT_TEMPLATE.sql` - Template for inserting new signing keys