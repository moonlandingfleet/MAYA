package com.mayaboss.android.model

data class WalletSession(
    val connected: Boolean,
    val address: String, // Made non-null, as it should always be present if connected
    val chainId: String?, // Retained, can be populated if needed
    val sessionId: String?, // Added to store the session ID from our backend
    val balance_eth: Double? = null
)