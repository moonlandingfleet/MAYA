package com.mayaboss.android.model

import java.util.Date

data class Council(
    val id: String,  // Primary Key
    val council_name: String,
    val domain_description: String,
    val revenue_model_description: String,
    val ethical_boundary: String,
    val status: String,
    val created_at: Date
)