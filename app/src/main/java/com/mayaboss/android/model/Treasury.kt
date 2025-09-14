package com.mayaboss.android.model

import java.util.Date

data class Treasury(
    val address: String,
    val balance_eth: Double,
    val balance_btc: Double,
    val last_updated: Date
)