package com.mayaboss.android.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.mayaboss.android.model.CouncilOpportunity
import com.mayaboss.android.viewmodel.MAYAViewModel
import timber.log.Timber

@Composable
fun CouncilOpportunitiesScreen(
    viewModel: MAYAViewModel,
    councilId: String,
    councilName: String,
    onBack: () -> Unit
) {
    var opportunities by remember { mutableStateOf<List<CouncilOpportunity>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }

    LaunchedEffect(councilId) {
        // In a real implementation, this would fetch opportunities from the viewModel
        // For now, we'll simulate with mock data
        isLoading = true
        // Simulate API call delay
        kotlinx.coroutines.delay(1000)
        
        // Mock opportunities
        opportunities = listOf(
            CouncilOpportunity(
                id = "1",
                council_id = councilId,
                opportunity_description = "New market opportunity in DeFi sector",
                reported_at = java.util.Date(),
                potential_cost_eth = 5.0,
                potential_revenue_btc = 0.2,
                status = "pending"
            ),
            CouncilOpportunity(
                id = "2",
                council_id = councilId,
                opportunity_description = "Partnership opportunity with major exchange",
                reported_at = java.util.Date(),
                potential_cost_eth = 10.0,
                potential_revenue_btc = 0.5,
                status = "pending"
            )
        )
        
        isLoading = false
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        // Header with back button
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Button(onClick = onBack) {
                Text("← Back")
            }
            Text(
                text = "$councilName Opportunities",
                style = MaterialTheme.typography.headlineSmall,
                modifier = Modifier.weight(1f)
            )
        }

        Spacer(modifier = Modifier.height(16.dp))

        if (isLoading) {
            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                CircularProgressIndicator()
            }
        } else {
            if (opportunities.isEmpty()) {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Text("No opportunities available for this council.")
                }
            } else {
                LazyColumn {
                    items(opportunities) { opportunity ->
                        CouncilOpportunityCard(
                            opportunity = opportunity,
                            onSubmitProposal = { proposalData ->
                                viewModel.submitCouncilProposal(councilId, proposalData)
                            }
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                    }
                }
            }
        }
    }
}

@Composable
fun CouncilOpportunityCard(
    opportunity: CouncilOpportunity,
    onSubmitProposal: (Map<String, Any>) -> Unit
) {
    var isExpanded by remember { mutableStateOf(false) }
    var proposalText by remember { mutableStateOf("") }

    Card(
        modifier = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    text = "Opportunity #${opportunity.id}",
                    style = MaterialTheme.typography.titleMedium
                )
                Text(
                    text = opportunity.status,
                    style = MaterialTheme.typography.bodySmall,
                    color = when (opportunity.status) {
                        "pending" -> MaterialTheme.colorScheme.primary
                        "approved" -> MaterialTheme.colorScheme.secondary
                        else -> MaterialTheme.colorScheme.error
                    }
                )
            }

            Spacer(modifier = Modifier.height(8.dp))

            Text(
                text = opportunity.opportunity_description,
                style = MaterialTheme.typography.bodyMedium
            )

            Spacer(modifier = Modifier.height(8.dp))

            Text(
                text = "Reported: ${opportunity.reported_at}",
                style = MaterialTheme.typography.bodySmall
            )

            if (opportunity.potential_cost_eth != null || opportunity.potential_revenue_btc != null) {
                Spacer(modifier = Modifier.height(8.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    opportunity.potential_cost_eth?.let {
                        Text(
                            text = "Cost: $it ETH",
                            style = MaterialTheme.typography.bodySmall
                        )
                    }
                    opportunity.potential_revenue_btc?.let {
                        Text(
                            text = "Revenue: $it BTC",
                            style = MaterialTheme.typography.bodySmall
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(12.dp))

            Button(
                onClick = { isExpanded = !isExpanded },
                modifier = Modifier.align(Alignment.End)
            ) {
                Text(if (isExpanded) "Hide Proposal" else "Submit Proposal")
            }

            if (isExpanded) {
                Spacer(modifier = Modifier.height(8.dp))
                OutlinedTextField(
                    value = proposalText,
                    onValueChange = { proposalText = it },
                    label = { Text("Proposal Details") },
                    modifier = Modifier.fillMaxWidth(),
                    maxLines = 3
                )
                Spacer(modifier = Modifier.height(8.dp))
                Button(
                    onClick = {
                        val proposalData = mapOf(
                            "opportunity_id" to opportunity.id,
                            "description" to proposalText,
                            "cost_eth" to (opportunity.potential_cost_eth ?: 0.0),
                            "expected_revenue_btc" to (opportunity.potential_revenue_btc ?: 0.0)
                        )
                        onSubmitProposal(proposalData)
                        proposalText = ""
                        isExpanded = false
                    },
                    modifier = Modifier.align(Alignment.End)
                ) {
                    Text("Submit")
                }
            }
        }
    }
}