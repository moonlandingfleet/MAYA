# Supabase JWKS Remediation Plan

## Overview

This document provides a step-by-step guide to resolve the Supabase JWKS issue where JWT tokens are failing validation due to missing signing keys in the Supabase database.

## Prerequisites

1. Access to your Supabase project dashboard
2. Service role key for your Supabase project
3. The diagnostic script: [SUPABASE_SIGNING_KEYS_DIAGNOSTIC.sql](file:///c%3A/Users/bryan/Desktop/MAYA/backend/SUPABASE_SIGNING_KEYS_DIAGNOSTIC.sql)
4. The key converter script: [pem_to_jwk_converter.py](file:///c%3A/Users/bryan/Desktop/MAYA/backend/pem_to_jwk_converter.py)
5. The SQL template: [SIGNING_KEY_INSERT_TEMPLATE.sql](file:///c%3A/Users/bryan/Desktop/MAYA/backend/SIGNING_KEY_INSERT_TEMPLATE.sql)

## Step-by-Step Remediation

### Step 1: Diagnose Current State

Execute the queries in [SUPABASE_SIGNING_KEYS_DIAGNOSTIC.sql](file:///c%3A/Users/bryan/Desktop/MAYA/backend/SUPABASE_SIGNING_KEYS_DIAGNOSTIC.sql) in your Supabase SQL editor. This will show:
- Current signing keys in the `auth.jwt_secrets` table
- Current JWKS configuration
- Any missing keys that are referenced in JWT tokens

### Step 2: Identify Missing Keys

From the diagnostic output, identify:
1. The `kid` values that are referenced in JWT tokens but missing from the database
2. The algorithm (`alg`) used for each missing key (typically RS256 for RSA keys)

### Step 3: Obtain the Signing Keys

You'll need to obtain the signing keys that match the missing `kid` values:
1. From your Supabase project settings, get the JWT secret (for HS256 keys)
2. From your Supabase project settings, get the RSA private key (for RS256 keys)
3. If you don't have these keys, you may need to generate new ones

### Step 4: Convert Keys to JWK Format

Use [pem_to_jwk_converter.py](file:///c%3A/Users/bryan/Desktop/MAYA/backend/pem_to_jwk_converter.py) to convert your PEM format keys to JWK format:
```bash
python pem_to_jwk_converter.py
```

Follow the prompts to:
1. Enter the path to your PEM key file
2. Specify the key type (RSA or HMAC)
3. Provide the `kid` value for the key
4. Get the JWK representation of the key

### Step 5: Insert Keys into Supabase

Using [SIGNING_KEY_INSERT_TEMPLATE.sql](file:///c%3A/Users/bryan/Desktop/MAYA/backend/SIGNING_KEY_INSERT_TEMPLATE.sql) as a template, create INSERT statements for each missing key:
1. Replace the placeholder values with your actual key data
2. Set the correct `key_id` (matching the `kid` in JWT tokens)
3. Set the correct `algorithm` (RS256 for RSA keys, HS256 for HMAC keys)
4. Set the correct `key` value (JWK representation of the key)

Execute the INSERT statements in your Supabase SQL editor.

### Step 6: Verify the Fix

Test the authentication system to verify that JWT tokens are now validating correctly:
1. Generate a new JWT token from Supabase
2. Try to validate it using the authentication system
3. Confirm that the token validates successfully
4. Check that the JWKS endpoint now returns the proper signing keys

## Important Notes

1. **Backup First**: Always backup your Supabase database before making changes
2. **Service Role Key**: Use a service role key for these operations as they require elevated privileges
3. **Key Security**: Keep your signing keys secure and never commit them to version control
4. **Testing Environment**: Test these changes in a development environment first
5. **No Code Changes**: No changes are needed to the [auth.py](file:///c%3A/Users/bryan/Desktop/MAYA/backend/auth.py) file

## Files Used

All files are located in `c:\Users\bryan\Desktop\MAYA\backend\`:
- [SUPABASE_SIGNING_KEYS_DIAGNOSTIC.sql](file:///c%3A/Users/bryan/Desktop/MAYA/backend/SUPABASE_SIGNING_KEYS_DIAGNOSTIC.sql)
- [pem_to_jwk_converter.py](file:///c%3A/Users/bryan/Desktop/MAYA/backend/pem_to_jwk_converter.py)
- [SIGNING_KEY_INSERT_TEMPLATE.sql](file:///c%3A/Users/bryan/Desktop/MAYA/backend/SIGNING_KEY_INSERT_TEMPLATE.sql)

## Troubleshooting

If you encounter issues:
1. Double-check that the `kid` values match exactly between JWT tokens and database records
2. Verify that the JWK format is correct
3. Ensure you're using a service role key for database operations
4. Check Supabase logs for any error messages
5. Confirm that the algorithm matches between the JWT header and database record

## Conclusion

Following this remediation plan should resolve the Supabase JWKS issue and allow JWT tokens to validate correctly while maintaining the existing multi-algorithm and key rotation functionality.