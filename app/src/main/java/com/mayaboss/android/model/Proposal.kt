package com.mayaboss.android.model

import java.util.Date

data class Proposal(
    val id: String,
    val council_id: String,
    val purpose: String,
    val cost_eth: Double,
    val expected_monthly_revenue_btc: Double,
    val status: String, // PENDING_REVIEW, AWAITING_SOVEREIGN_APPROVAL, APPROVED_PENDING_FUNDING, FUNDED_ACTIVE, REJECTED, COMPLETED, FAILED
    val details_json: Map<String, Any>?,
    val submitted_at: Date,
    val last_status_update_at: Date,
    val sovereign_approved_at: Date?,
    val funding_transaction_hash: String?,
    val roi_score: Double
)