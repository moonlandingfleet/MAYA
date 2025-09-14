package com.mayaboss.android.model

import java.util.Date

data class CouncilOpportunity(
    val id: String,  // uuid (Primary Key)
    val council_id: String,
    val opportunity_description: String,
    val reported_at: Date,
    val potential_cost_eth: Double?,
    val potential_revenue_btc: Double?,
    val status: String
)