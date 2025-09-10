package com.mayaboss.android.model

data class Proposal(
    val id: String,
    val name: String,
    val description: String,
    val roi_hrs: Double,
    val risk: String,
    val cost: Double,
    val locked: Boolean = false
)