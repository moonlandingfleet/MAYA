package com.mayaboss.android.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.mayaboss.android.model.Council
import com.mayaboss.android.model.CouncilOpportunity
import com.mayaboss.android.viewmodel.MAYAViewModel

@Composable
fun CouncilScreen(
    council: Council,
    viewModel: MAYAViewModel = viewModel(),
    onBack: () -> Unit
) {
    val opportunities by viewModel.opportunities.collectAsState(initial = emptyList())
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        // Header with back button
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(onClick = onBack) {
                Icon(
                    imageVector = androidx.compose.material.icons.Icons.Default.ArrowBack,
                    contentDescription = "Back"
                )
            }
            
            Text(
                text = council.council_name,
                style = MaterialTheme.typography.headlineMedium,
                modifier = Modifier.weight(1f)
            )
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // Council details
        Card(
            modifier = Modifier.fillMaxWidth(),
            elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text(
                    text = "Role: ${council.ethical_boundary}",
                    style = MaterialTheme.typography.titleMedium
                )
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "Domain: ${council.domain_description}",
                    style = MaterialTheme.typography.bodyLarge
                )
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "Revenue Model: ${council.revenue_model_description}",
                    style = MaterialTheme.typography.bodyMedium
                )
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "Status: ${council.status}",
                    style = MaterialTheme.typography.bodyMedium
                )
            }
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // Opportunities section
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = "Opportunities",
                style = MaterialTheme.typography.titleMedium
            )
            
            Button(
                onClick = { viewModel.loadCouncilOpportunities(council.id) }
            ) {
                Text("Refresh")
            }
        }
        
        Spacer(modifier = Modifier.height(8.dp))
        
        if (opportunities.isEmpty()) {
            Text(
                text = "No opportunities available for this council.",
                modifier = Modifier.fillMaxWidth(),
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        } else {
            LazyColumn {
                items(opportunities) { opportunity ->
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 4.dp),
                        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            Text(
                                text = opportunity.opportunity_description,
                                style = MaterialTheme.typography.bodyLarge
                            )
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(
                                text = "Status: ${opportunity.status}",
                                style = MaterialTheme.typography.bodySmall
                            )
                            if (opportunity.potential_cost_eth != null) {
                                Text(
                                    text = "Potential Cost: ${opportunity.potential_cost_eth} ETH",
                                    style = MaterialTheme.typography.bodySmall
                                )
                            }
                            if (opportunity.potential_revenue_btc != null) {
                                Text(
                                    text = "Potential Revenue: ${opportunity.potential_revenue_btc} BTC",
                                    style = MaterialTheme.typography.bodySmall
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}