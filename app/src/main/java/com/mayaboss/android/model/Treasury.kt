package com.mayaboss.android.model

data class Treasury(
    val address: String,
    val balance_eth: Double,
    val agents_contributed: List<String>,
    val last_updated: String
)