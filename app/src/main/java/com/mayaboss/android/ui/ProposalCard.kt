package com.mayaboss.android.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.mayaboss.android.model.Proposal

@Composable
fun ProposalCard(
    proposal: Proposal,
    onApprove: () -> Unit,
    onReject: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            horizontalAlignment = Alignment.Start
        ) {
            Text(text = proposal.name, style = MaterialTheme.typography.headlineSmall)
            Spacer(modifier = Modifier.height(8.dp))
            Text(text = "ROI: ${proposal.roi_hrs}$/hr", style = MaterialTheme.typography.bodyMedium)
            Text(text = "Risk: ${proposal.risk}", style = MaterialTheme.typography.bodyMedium)
            Text(text = "Cost: ${proposal.cost} ETH", style = MaterialTheme.typography.bodyMedium)
            Spacer(modifier = Modifier.height(16.dp))
            Row {
                Button(onClick = onApprove, modifier = Modifier.weight(1f)) {
                    Text("✅ Approve")
                }
                Spacer(modifier = Modifier.width(8.dp))
                Button(onClick = onReject, modifier = Modifier.weight(1f)) {
                    Text("❌ Reject")
                }
            }
        }
    }
}