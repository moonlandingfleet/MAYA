package com.mayaboss.android.model

data class WalletSession(
    val connected: Boolean,
    val address: String?,
    val chainId: String?,
    val topic: String?
)