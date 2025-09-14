package com.mayaboss.android.model

import java.util.Date

data class TreasuryTransaction(
    val id: String,  // uuid (Primary Key)
    val timestamp: Date,
    val transaction_type: String,
    val council_id: String?,
    val proposal_id: String?,
    val asset: String,
    val amount: Double,
    val related_onchain_transaction_hash: String?,
    val description: String,
    val status: String
)