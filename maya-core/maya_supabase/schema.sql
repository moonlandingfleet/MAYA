-- Create councils table
CREATE TABLE IF NOT EXISTS councils (
    id TEXT PRIMARY KEY,
    council_name TEXT NOT NULL,
    domain_description TEXT NOT NULL,
    revenue_model_description TEXT NOT NULL,
    ethical_boundary TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('ACTIVE', 'UNDER_DEVELOPMENT', 'PAUSED')),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create proposals table
CREATE TABLE IF NOT EXISTS proposals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    council_id TEXT REFERENCES councils(id) NOT NULL,
    purpose TEXT NOT NULL,
    cost_eth NUMERIC NOT NULL,
    expected_monthly_revenue_btc NUMERIC NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('PENDING_REVIEW', 'AWAITING_SOVEREIGN_APPROVAL', 'APPROVED_PENDING_FUNDING', 'FUNDED_ACTIVE', 'REJECTED', 'COMPLETED', 'FAILED')),
    details_json JSONB,
    submitted_at TIMESTAMPTZ DEFAULT NOW(),
    last_status_update_at TIMESTAMPTZ DEFAULT NOW(),
    sovereign_approved_at TIMESTAMPTZ,
    funding_transaction_hash TEXT,
    roi_score NUMERIC
);

-- Create treasury_transactions table
CREATE TABLE IF NOT EXISTS treasury_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    transaction_type TEXT NOT NULL CHECK (transaction_type IN ('COUNCIL_REVENUE_IN', 'PROPOSAL_FUNDING_OUT', 'ETH_TO_BTC_SWAP', 'GAS_FEE')),
    council_id TEXT REFERENCES councils(id),
    proposal_id UUID REFERENCES proposals(id),
    asset TEXT NOT NULL CHECK (asset IN ('ETH', 'USDC', 'BTC', 'DAI')),
    amount NUMERIC NOT NULL,
    related_onchain_transaction_hash TEXT,
    description TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('PENDING', 'COMPLETED', 'FAILED'))
);

-- Create council_opportunities table
CREATE TABLE IF NOT EXISTS council_opportunities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    council_id TEXT REFERENCES councils(id) NOT NULL,
    opportunity_description TEXT NOT NULL,
    reported_at TIMESTAMPTZ DEFAULT NOW(),
    potential_cost_eth NUMERIC,
    potential_revenue_btc NUMERIC,
    status TEXT NOT NULL CHECK (status IN ('NEW', 'UNDER_REVIEW_BY_MAYA', 'CONVERTED_TO_PROPOSAL', 'DISMISSED'))
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_proposals_council_id ON proposals(council_id);
CREATE INDEX IF NOT EXISTS idx_proposals_status ON proposals(status);
CREATE INDEX IF NOT EXISTS idx_treasury_transactions_council_id ON treasury_transactions(council_id);
CREATE INDEX IF NOT EXISTS idx_treasury_transactions_proposal_id ON treasury_transactions(proposal_id);
CREATE INDEX IF NOT EXISTS idx_treasury_transactions_transaction_type ON treasury_transactions(transaction_type);
CREATE INDEX IF NOT EXISTS idx_council_opportunities_council_id ON council_opportunities(council_id);
CREATE INDEX IF NOT EXISTS idx_council_opportunities_status ON council_opportunities(status);