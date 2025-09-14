# MAYA Supabase Integration Usage Guide

This document explains how to use the Supabase integration for the MAYA project.

## Overview

The Supabase integration provides a complete backend solution for managing the Digital Ministries councils, proposals, treasury transactions, and opportunities. It includes:

1. Database schema definitions
2. Pydantic models for data validation
3. Database service for CRUD operations
4. FastAPI endpoints for RESTful API access

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```

2. Install the Supabase package:
   ```bash
   pip install supabase==2.4.5
   ```

## Configuration

To use the Supabase integration, you need to set the following environment variables:

- `SUPABASE_URL` - The URL of your Supabase project
- `SUPABASE_KEY` - The API key for your Supabase project

Example:
```bash
export SUPABASE_URL=https://your-project.supabase.co
export SUPABASE_KEY=your-supabase-key
```

## Database Schema

The integration includes the following tables:

### Councils
Stores information about the 12 Digital Ministries:
- `id`: text (Primary Key)
- `council_name`: text
- `domain_description`: text
- `revenue_model_description`: text
- `ethical_boundary`: text
- `status`: text (ACTIVE, UNDER_DEVELOPMENT, PAUSED)
- `created_at`: timestamp with time zone

### Proposals
Funding requests from Councils:
- `id`: uuid (Primary Key)
- `council_id`: text (Foreign Key)
- `purpose`: text
- `cost_eth`: numeric
- `expected_monthly_revenue_btc`: numeric
- `status`: text (PENDING_REVIEW, AWAITING_SOVEREIGN_APPROVAL, etc.)
- `details_json`: jsonb (optional)
- `submitted_at`: timestamp
- `last_status_update_at`: timestamp
- `sovereign_approved_at`: timestamp (nullable)
- `funding_transaction_hash`: text (nullable)
- `roi_score`: numeric

### Treasury Transactions
Log of all financial movements:
- `id`: uuid (Primary Key)
- `timestamp`: timestamp
- `transaction_type`: text (COUNCIL_REVENUE_IN, PROPOSAL_FUNDING_OUT, etc.)
- `council_id`: text (Foreign Key, nullable)
- `proposal_id`: uuid (Foreign Key, nullable)
- `asset`: text (ETH, USDC, BTC, DAI)
- `amount`: numeric
- `related_onchain_transaction_hash`: text (nullable)
- `description`: text
- `status`: text (PENDING, COMPLETED, FAILED)

### Council Opportunities
Opportunities reported by probes:
- `id`: uuid (Primary Key)
- `council_id`: text (Foreign Key)
- `opportunity_description`: text
- `reported_at`: timestamp
- `potential_cost_eth`: numeric (nullable)
- `potential_revenue_btc`: numeric (nullable)
- `status`: text (NEW, UNDER_REVIEW_BY_MAYA, CONVERTED_TO_PROPOSAL, DISMISSED)

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
    id="proposal-123",
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
cd ../..
python -m api.maya_supabase.test_supabase
```

## Schema Deployment

To deploy the database schema to your Supabase project, you can use the SQL file:

```sql
-- Execute the contents of schema.sql in your Supabase SQL editor
```

The schema file includes:
- Table creation statements
- Foreign key constraints
- Indexes for performance optimization
- Check constraints for data validation

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure the Supabase package is installed and the maya_supabase directory is in your Python path.

2. **Authentication errors**: Verify that your SUPABASE_URL and SUPABASE_KEY environment variables are set correctly.

3. **Connection errors**: Check that your Supabase project is accessible and the URL is correct.

### Getting Help

If you encounter issues, check:
1. The Supabase documentation: https://supabase.com/docs
2. The Python Supabase client documentation: https://github.com/supabase/supabase-py
3. The MAYA project documentation in the main README.md