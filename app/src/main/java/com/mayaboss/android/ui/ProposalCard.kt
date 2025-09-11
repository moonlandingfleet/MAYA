package com.mayaboss.android.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.mayaboss.android.model.Proposal // Ensure this is the updated model
import com.mayaboss.android.viewmodel.MAYAViewModel // Import ViewModel

@Composable
fun ProposalCard(
    proposal: Proposal,
    viewModel: MAYAViewModel // Changed parameters
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp), // Adjusted padding from version in MainScreen
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            horizontalAlignment = Alignment.Start
        ) {
            Text(text = "Proposal ID: ${proposal.id}", style = MaterialTheme.typography.titleSmall)
            Text(text = "Agent: ${proposal.agent_id}", style = MaterialTheme.typography.titleMedium)
            // Removed Icon for 'locked' as 'locked' field is gone. Status is handled by 'proposal.status'.

            Spacer(modifier = Modifier.height(8.dp))

            Text(text = "Purpose: ${proposal.purpose}", style = MaterialTheme.typography.bodyMedium)
            Text(text = "Cost: ${proposal.cost_eth} ETH", style = MaterialTheme.typography.bodySmall)
            Text(text = "Expected Revenue: ${proposal.expected_monthly_revenue_eth} ETH/month", style = MaterialTheme.typography.bodySmall)
            Text(text = "Status: ${proposal.status}", style = MaterialTheme.typography.bodySmall)

            Spacer(modifier = Modifier.height(16.dp))
            Row {
                Button(
                    onClick = { viewModel.approveProposal(proposal.id) },
                    modifier = Modifier.weight(1f)
                    // The 'enabled' logic based on 'proposal.locked' is removed.
                    // If you need to disable based on status, it would be: enabled = proposal.status == "pending"
                ) {
                    Text("✅ Approve")
                }
                Spacer(modifier = Modifier.width(8.dp))
                Button(
                    onClick = { viewModel.rejectProposal(proposal.id) },
                    modifier = Modifier.weight(1f)
                ) {
                    Text("❌ Reject")
                }
            }
        }
    }
}