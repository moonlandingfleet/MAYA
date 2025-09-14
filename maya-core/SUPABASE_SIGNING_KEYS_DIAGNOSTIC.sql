-- SUPABASE SIGNING KEYS DIAGNOSTIC SCRIPT
-- Run these queries in your Supabase SQL editor to diagnose the JWKS issue

-- 1. Check if the signing_keys table exists (this may fail if you don't have access)
SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'auth';

-- 2. List all tables in the auth schema
SELECT table_name FROM information_schema.tables WHERE table_schema = 'auth';

-- 3. Try to access the signing_keys table (if it exists)
-- This query may fail if you don't have access to this table
SELECT * FROM auth.signing_keys ORDER BY created_at DESC LIMIT 50;

-- 4. Check if there are any rows in the signing_keys table (alternative approach)
-- This query may fail if you don't have access to this table
SELECT COUNT(*) as total_keys FROM auth.signing_keys;

-- 5. Check for any auth-related tables that might contain key information
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'auth' 
AND (table_name LIKE '%key%' OR table_name LIKE '%sign%' OR table_name LIKE '%jwt%' OR table_name LIKE '%jwk%');

-- 6. Check the users table to confirm database access
SELECT COUNT(*) as user_count FROM auth.users;

-- 7. Check for any extensions related to JWT
SELECT name, installed_version 
FROM pg_available_extensions 
WHERE name LIKE '%jwt%' OR name LIKE '%jwk%' OR name LIKE '%crypto%';

-- If you can't access the signing_keys table directly, try this alternative approach:
-- 8. Check if there are any settings or configuration tables that might contain key information
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'auth' 
AND table_name LIKE '%setting%' OR table_name LIKE '%config%';