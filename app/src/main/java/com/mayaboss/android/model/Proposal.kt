package com.mayaboss.android.model

data class Proposal(
    val id: String,
    val name: String,
    val roi_hrs: Double,
    val risk: String,
    val cost: Int,
    val locked: Boolean = false
)