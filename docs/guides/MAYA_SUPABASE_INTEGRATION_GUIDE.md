# MAYA Supabase Integration Guide

This document provides a comprehensive guide on how to use the Supabase integration for the MAYA project's Digital Ministries ecosystem.

## Overview

The Supabase integration provides a complete backend solution for managing the Digital Ministries councils, proposals, treasury transactions, and opportunities. It includes:

1. Database schema definitions
2. Pydantic models for data validation
3. Database service for CRUD operations
4. FastAPI endpoints for RESTful API access

## Database Schema

The integration includes the following tables:

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

## Project Structure

```
backend/
├── api/
│   └── maya_supabase/
│       ├── models.py          # Pydantic models for data validation
│       ├── database.py        # Database service with CRUD operations
│       ├── api.py             # FastAPI endpoints
│       ├── schema.sql         # Database schema definition
│       ├── sample_data.py     # Sample data and usage examples
│       ├── example_usage.py   # Example usage of the integration
│       ├── test_supabase.py   # Test script
│       ├── README.md          # Supabase integration documentation
│       ├── USAGE.md           # Detailed usage guide
│       └── SUMMARY.md         # Summary of the integration
├── .env                   # Environment variables (not committed to git)
├── requirements.txt       # Python dependencies including python-dotenv
├── create_supabase_tables.py      # Script to create tables (placeholder)
└── create_supabase_tables_mcp.py  # Script for Supabase MCP environment
```

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

2. Install the Supabase package:
   ```bash
   pip install supabase==2.4.5
   ```

3. Install the python-dotenv package:
   ```bash
   pip install python-dotenv
   ```

## Configuration

To use the Supabase integration, you need to create a `.env` file in the [backend](file:///c%3A/Users/bryan/Desktop/MAYA/backend) directory with the following environment variables:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-key
```

Example:
```
SUPABASE_URL=https://ksrvtvqqikwjbqzpgacs.supabase.co
SUPABASE_KEY=your_actual_supabase_service_role_key
```

**Important:** Never commit the `.env` file to git if your project is public. The `.env` file has already been added to `.gitignore` to prevent accidental commits.

## Creating the Database Tables

### Method 1: Using the SQL Schema File

The easiest way to create the tables is to execute the SQL schema file directly in your Supabase project:

1. Go to your Supabase project dashboard
2. Navigate to the SQL editor
3. Copy the contents of `backend/api/maya_supabase/schema.sql`
4. Execute the SQL statements

### Method 2: Using the Python Script

If you have access to the Supabase MCP server, you can use the provided Python scripts:

1. Set the required environment variables in your `.env` file
2. Run the table creation script:
   ```bash
   python backend/create_supabase_tables_mcp.py
   ```

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

## Usage Examples

### Creating a Council
```python
from datetime import datetime
from maya_supabase.models import Council
from maya_supabase.database import SupabaseService

# Create the database service
db = SupabaseService()

# Create a council instance
council = Council(
    id="council_digital_identity",
    council_name="Council of Digital Identity",
    domain_description="Responsible for managing digital identities",
    revenue_model_description="Earns revenue through licensing fees",
    ethical_boundary="Must ensure user privacy",
    status="ACTIVE",
    created_at=datetime.now()
)

# Save to database
created_council = db.create_council(council)
```

### Creating a Proposal
```python
from datetime import datetime
from maya_supabase.models import Proposal
from maya_supabase.database import SupabaseService

# Create the database service
db = SupabaseService()

# Create a proposal instance
proposal = Proposal(
    id=None,  # This will be auto-generated by Supabase
    council_id="council_digital_identity",
    purpose="Launch 'Sign-In with Bitcoin' service",
    cost_eth=10.5,
    expected_monthly_revenue_btc=0.25,
    status="PENDING_REVIEW",
    submitted_at=datetime.now(),
    last_status_update_at=datetime.now(),
    roi_score=8.5
)

# Save to database
created_proposal = db.create_proposal(proposal)
```

### Using the API
The API endpoints are automatically available when you include the router in your FastAPI application:

```python
from fastapi import FastAPI
from maya_supabase.api import router as supabase_router

app = FastAPI()
app.include_router(supabase_router)
```

## Testing

To run the tests:
```bash
cd backend
python api/maya_supabase/test_supabase.py
```

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure the Supabase package is installed and the maya_supabase directory is in your Python path.

2. **Authentication errors**: Verify that your SUPABASE_URL and SUPABASE_KEY environment variables are set correctly in your `.env` file.

3. **Connection errors**: Check that your Supabase project is accessible and the URL is correct.

### Getting Help

If you encounter issues, check:
1. The Supabase documentation: https://supabase.com/docs
2. The Python Supabase client documentation: https://github.com/supabase/supabase-py
3. The MAYA project documentation in the main README.md

## Next Steps

1. Implement proper error handling in the database service
2. Add pagination support for list endpoints
3. Implement data validation and sanitization
4. Add authentication and authorization for API endpoints
5. Implement database migrations for schema updates