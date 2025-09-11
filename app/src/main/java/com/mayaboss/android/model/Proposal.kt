package com.mayaboss.android.model

data class Proposal(
    val id: String,
    val agent_id: String,
    val purpose: String,
    val cost_eth: Double,
    val expected_monthly_revenue_eth: Double,
    val status: String // pending, awaiting_approval, funded, rejected
)