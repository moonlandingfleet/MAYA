# Supabase Integration for MAYA

This directory contains the Supabase integration for the MAYA project, implementing the database schema for the Digital Ministries councils, proposals, treasury transactions, and opportunities.

## Database Schema

### Councils
Stores information about the 12 Digital Ministries:

- `id`: text (Primary Key, e.g., "council_digital_identity")
- `council_name`: text (e.g., "Council of Digital Identity")
- `domain_description`: text
- `revenue_model_description`: text
- `ethical_boundary`: text
- `status`: text (e.g., "ACTIVE", "UNDER_DEVELOPMENT", "PAUSED")
- `created_at`: timestamp with time zone (default: now())

### Proposals
Funding requests from Councils, curated by MAYA:

- `id`: uuid (Primary Key, default: gen_random_uuid())
- `council_id`: text (Foreign Key referencing councils.id)
- `purpose`: text (e.g., "Launch 'Sign-In with Bitcoin' service.")
- `cost_eth`: numeric (Use numeric for precise currency values)
- `expected_monthly_revenue_btc`: numeric
- `status`: text (e.g., "PENDING_REVIEW", "AWAITING_SOVEREIGN_APPROVAL", "APPROVED_PENDING_FUNDING", "FUNDED_ACTIVE", "REJECTED", "COMPLETED", "FAILED")
- `details_json`: jsonb (Optional: for any council-specific data related to the proposal)
- `submitted_at`: timestamp with time zone (default: now())
- `last_status_update_at`: timestamp with time zone (default: now())
- `sovereign_approved_at`: timestamp with time zone (nullable)
- `funding_transaction_hash`: text (nullable)
- `roi_score`: numeric (calculated by MAYA, for ranking)

### Treasury Transactions
Log of all financial movements:

- `id`: uuid (Primary Key, default: gen_random_uuid())
- `timestamp`: timestamp with time zone (default: now())
- `transaction_type`: text (e.g., "COUNCIL_REVENUE_IN", "PROPOSAL_FUNDING_OUT", "ETH_TO_BTC_SWAP", "GAS_FEE")
- `council_id`: text (Nullable, Foreign Key referencing councils.id)
- `proposal_id`: uuid (Nullable, Foreign Key referencing proposals.id)
- `asset`: text (e.g., "ETH", "USDC", "BTC", "DAI")
- `amount`: numeric (positive for inflow, negative for outflow to treasury)
- `related_onchain_transaction_hash`: text (nullable)
- `description`: text
- `status`: text (e.g., "PENDING", "COMPLETED", "FAILED")

### Council Opportunities
Optional, if probes report opportunities before they become formal proposals:

- `id`: uuid (Primary Key, default: gen_random_uuid())
- `council_id`: text (Foreign Key referencing councils.id)
- `opportunity_description`: text
- `reported_at`: timestamp with time zone (default: now())
- `potential_cost_eth`: numeric (nullable)
- `potential_revenue_btc`: numeric (nullable)
- `status`: text (e.g., "NEW", "UNDER_REVIEW_BY_MAYA", "CONVERTED_TO_PROPOSAL", "DISMISSED")

## API Endpoints

All endpoints are prefixed with `/supabase`:

### Councils
- `POST /councils` - Create a new council
- `GET /councils/{council_id}` - Get a council by ID
- `GET /councils` - Get all councils
- `PUT /councils/{council_id}` - Update a council
- `DELETE /councils/{council_id}` - Delete a council

### Proposals
- `POST /proposals` - Create a new proposal
- `GET /proposals/{proposal_id}` - Get a proposal by ID
- `GET /proposals/council/{council_id}` - Get all proposals for a council
- `GET /proposals` - Get all proposals
- `PUT /proposals/{proposal_id}` - Update a proposal
- `DELETE /proposals/{proposal_id}` - Delete a proposal

### Treasury Transactions
- `POST /treasury-transactions` - Create a new treasury transaction
- `GET /treasury-transactions/{transaction_id}` - Get a treasury transaction by ID
- `GET /treasury-transactions/council/{council_id}` - Get all treasury transactions for a council
- `GET /treasury-transactions` - Get all treasury transactions

### Council Opportunities
- `POST /council-opportunities` - Create a new council opportunity
- `GET /council-opportunities/{opportunity_id}` - Get a council opportunity by ID
- `GET /council-opportunities/council/{council_id}` - Get all council opportunities for a council
- `GET /council-opportunities` - Get all council opportunities
- `PUT /council-opportunities/{opportunity_id}` - Update a council opportunity
- `DELETE /council-opportunities/{opportunity_id}` - Delete a council opportunity

## Configuration

To use the Supabase integration, you need to set the following environment variables:

- `SUPABASE_URL` - The URL of your Supabase project
- `SUPABASE_KEY` - The API key for your Supabase project

## Installation

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set the environment variables for Supabase:
   ```
   export SUPABASE_URL=your_supabase_url
   export SUPABASE_KEY=your_supabase_key
   ```

3. Run the MAYA Core server:
   ```
   python main.py
   ```