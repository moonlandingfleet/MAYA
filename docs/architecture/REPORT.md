# MAYA Codebase Analysis Report

## A. REPO & PROJECT STRUCTURE

### 1. Config files that control build, lint, test or deploy
- `android/build.gradle` - Top-level build configuration
- `android/app/build.gradle` - Android app module build configuration
- `android/settings.gradle` - Project settings and repository configuration
- `android/gradle.properties` - Gradle-wide settings
- `android/gradlew`/`android/gradlew.bat` - Gradle wrapper scripts
- `backend/requirements.txt` - Python dependencies

### 2. Source-code files per language
| Language | Count |
|----------|-------|
| Kotlin | ~50 files |
| Python | ~50 files |
| Java | 0 files |
| XML | ~10 files |
| SQL | 3 files |
| Markdown | ~20 files |
| Shell/Batch | 3 files |

### 3. Folders with their own package management
- `backend/` - Python project with `requirements.txt`
- `backend/agents/faucet_harvester/` - Python agent with its own `requirements.txt`
- `android/app/` - Android project with Gradle dependencies

### 4. Monorepo shared library
No explicit shared library folder found. The Android app and Python backend are separate components that communicate via REST API.

### 5. Orphaned files or folders
No clearly orphaned files identified. All components appear to be part of the MAYA ecosystem.

### 6. Directory nesting depth
Maximum directory depth is 6 levels:
```
backend/agents/faucet_harvester/Dockerfile
```
This is acceptable and not excessive.

## B. ENVIRONMENT & SECRETS

### 7. Environment variables
From `.env.template`:
- `SUPABASE_URL`
- `SUPABASE_KEY`

From code analysis:
- `INFURA_URL`
- `TREASURY_ADDRESS`
- `SUPABASE_JWKS_URI`
- `SUPABASE_AUTH_JWT_SECRET`
- `JWT_ALGORITHMS`
- `JWT_AUDIENCE`
- `JWT_ISSUER`

### 8. Hard-coded secrets
Several test credentials and example values found:
- WalletConnect Project ID in `android/gradle.properties`: `d3e4065175d57a7bbde46a5cfc71913a`
- Test Ethereum addresses (0x123...7890) throughout the codebase
- Infura URL with embedded API key in `backend/main.py`
- Test username/password in UI tests

### 9. Docker configuration
Dockerfile exists at `backend/agents/faucet_harvester/Dockerfile` but no docker-compose file found.

### 10. Exposed ports
- Port 8000 - Main FastAPI server
- Port 8080 - Faucet harvester agent
- Port 80 - Faucet harvester Dockerfile EXPOSE directive

## C. DATABASE & MIGRATIONS

### 11. Schema definition files
- `backend/api/maya_supabase/schema.sql` - Main Supabase schema
- `backend/SIGNING_KEY_INSERT_TEMPLATE.sql` - Auth signing keys template
- `backend/SUPABASE_SIGNING_KEYS_DIAGNOSTIC.sql` - Diagnostic queries

### 12. Tables with created_at/updated_at columns
- `councils` - has `created_at`
- `proposals` - has `submitted_at`, `last_status_update_at`, `sovereign_approved_at`
- `treasury_transactions` - has `timestamp`
- `council_opportunities` - has `reported_at`

### 13. Migration files
No explicit migration files found. Schema is defined in `schema.sql` but no versioned migrations exist.

### 14. Foreign-key constraints
Foreign key constraints are declared in the schema:
- `proposals.council_id` references `councils.id`
- `treasury_transactions.council_id` references `councils.id`
- `treasury_transactions.proposal_id` references `proposals.id`
- `council_opportunities.council_id` references `councils.id`

### 15. Missing indexes
Indexes are defined in the schema for:
- `proposals.council_id`
- `proposals.status`
- `treasury_transactions.council_id`
- `treasury_transactions.proposal_id`
- `treasury_transactions.transaction_type`
- `council_opportunities.council_id`
- `council_opportunities.status`

## D. API LAYER

### 16. Route definitions
Routes are defined in:
- `backend/main.py` - Main FastAPI routes
- `backend/api/maya_supabase/api.py` - Supabase integration routes
- `android/app/src/main/java/com/mayaboss/android/network/MAYAApiService.kt` - Android client

HTTP verb distribution:
- GET: ~10 routes
- POST: ~15 routes
- PUT: ~3 routes
- DELETE: ~2 routes

### 17. Unprotected endpoints
Several endpoints lack authentication middleware:
- `/agents/logs`
- `/agents/run`
- `/wallet/balance`
- `/wallet/session/connect`
- `/wallet/session/disconnect`
- `/wallet/session/{session_id}`

### 18. Wildcard/catch-all patterns
No wildcard or catch-all route patterns found.

### 19. Request validation
Request validation is implemented with Pydantic models in the Python backend and data classes in Kotlin.

### 20. Idempotency keys
No explicit idempotency key handling found for financial endpoints.

### 21. Health-check endpoint
No explicit health-check endpoint returning 200 OK found.

### 22. OpenAPI/Swagger documentation
FastAPI automatically generates OpenAPI documentation at `/docs` and `/redoc`, but no separate OpenAPI file exists.

## E. AUTH & SECURITY

### 23. Auth strategy
JWT-based authentication with support for both RS256 and HS256 algorithms.

### 24. JWT secret rotation
Supports multiple secrets and kid headers for key rotation.

### 25. Password hashing
No explicit password hashing found - authentication appears to be handled by Supabase.

### 26. CORS origins
CORS configured with `allow_origins=["*"]` in `backend/main.py` - this is a security risk.

### 27. Security headers
No explicit security headers (helmet, secure-headers) configured in the server setup.

### 28. SQL injection protection
SQL queries use parameterized statements through the Supabase client library.

## F. WALLET / PAYMENT LOGIC

### 29. Payment SDK functions
No direct payment SDK calls found. WalletConnect integration is for Ethereum transactions.

### 30. Wallet balance ledger
Treasury table tracks financial movements but no explicit double-entry bookkeeping.

### 31. Webhooks
No webhook listeners found.

### 32. Currency storage
Currency amounts stored as NUMERIC in database, which is appropriate for financial values.

### 33. Transaction reversals
No explicit refund/reversal code found.

## G. EXTERNAL INTEGRATIONS

### 34. Third-party API URLs
- Infura Ethereum API: `https://mainnet.infura.io/v3/...`
- Supabase: `https://ksrvtvqqikwjbqzpgacs.supabase.co`

### 35. Circuit-breaker/retry policy
No explicit circuit-breaker or retry policy found.

### 36. Timeout values
No explicit timeout values configured for HTTP calls.

### 37. File upload validation
No file upload functionality found.

## H. FRONTEND (Android App)

### 38. UI components
Jetpack Compose components found throughout `android/app/src/main/java/com/mayaboss/android/ui/`:
- MainScreen.kt
- ProposalCard.kt
- WalletConnectScreen.kt
- TransactionRequestScreen.kt
- CouncilOpportunitiesScreen.kt

### 39. Centralized API client
Yes, `MAYAApiService.kt` serves as a centralized API client.

### 40. Server-side vs client-side rendering
Android app is entirely client-side rendered.

### 41. ENV var validation
No explicit runtime validation of environment variables found.

### 42. Error boundary
Basic error handling exists but no global error boundary pattern.

### 43. Build output size
Not analyzed - would require building the app.

## I. TESTING

### 44. Test files by layer
- Unit tests: ~15 files in `android/app/src/test/`
- Integration tests: ~5 files in `android/app/src/androidTest/`
- Python tests: ~20 files in `backend/`

### 45. Folders with zero test files
- `backend/agents/` (except faucet_harvester)
- Several utility and model folders in Android app

### 46. Coverage report
No coverage report found.

### 47. Flaky tests
No tests explicitly marked as flaky found.

### 48. CI coverage requirements
No CI configuration found to determine coverage requirements.

## J. DEPLOY & INFRA

### 49. Dockerfiles
One Dockerfile exists at `backend/agents/faucet_harvester/Dockerfile`:
- Uses multi-stage build pattern
- Does not explicitly use non-root user

### 50. Base image versions
- `python:3.11-alpine` - Alpine is generally secure

### 51. Production docker-compose
No docker-compose.prod.yml or equivalent found.

### 52. Migration execution
No automatic migration execution on container start.

### 53. Exposed ports
Documented ports match actual exposure:
- 8000 for main server
- 8080 for agents

### 54. Infrastructure as code
No Helm charts, Terraform, or CloudFormation templates found.

### 55. Hard-coded paths
Some hard-coded localhost URLs found in the codebase.

## K. DOCS & HANDOFF

### 56. README with setup instructions
Yes, comprehensive README.md exists with setup, test, and deploy commands.

### 57. Architecture Decision Records
No ADRs found in a dedicated `/docs/adr` folder.

### 58. API schema documentation
OpenAPI documentation is automatically generated but no committed schema file.

### 59. Undocumented environment variables
Several environment variables are used in code but not documented:
- `INFURA_URL_ACTUAL`
- `TESTING_ENVIRONMENT`
- Various JWT-related variables

### 60. Old TODO/FIXME comments
Several TODO comments found:
- Web3.py version verification needed
- Authentication logic for proposal requests
- Sovereign approval permission checks
- Transaction request screen refactoring