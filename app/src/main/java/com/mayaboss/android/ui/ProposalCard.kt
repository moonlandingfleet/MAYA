package com.mayaboss.android.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.mayaboss.android.model.Proposal
import com.mayaboss.android.util.ProposalScoringUtil
import com.mayaboss.android.viewmodel.MAYAViewModel
import java.text.SimpleDateFormat

@Composable
fun ProposalCard(
    proposal: Proposal,
    viewModel: MAYAViewModel
) {
    val roi = ProposalScoringUtil.calculateROI(proposal)
    val score = ProposalScoringUtil.calculateProposalScore(proposal)
    
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            horizontalAlignment = Alignment.Start
        ) {
            Text(text = "Proposal ID: ${proposal.id}", style = MaterialTheme.typography.titleSmall)
            Text(text = "Council: ${proposal.council_id}", style = MaterialTheme.typography.titleMedium)
            
            Spacer(modifier = Modifier.height(8.dp))

            Text(text = "Purpose: ${proposal.purpose}", style = MaterialTheme.typography.bodyMedium)
            Text(text = "Cost: ${proposal.cost_eth} ETH", style = MaterialTheme.typography.bodySmall)
            Text(text = "Expected Revenue: ${proposal.expected_monthly_revenue_btc} BTC/month", style = MaterialTheme.typography.bodySmall)
            
            Spacer(modifier = Modifier.height(8.dp))
            
            // ROI and Score information
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    text = "ROI: ${String.format("%.2f", roi * 100)}%",
                    style = MaterialTheme.typography.bodySmall,
                    color = if (roi > 0) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.error
                )
                Text(
                    text = "Score: ${String.format("%.2f", score)}",
                    style = MaterialTheme.typography.bodySmall
                )
            }
            
            Text(text = "Status: ${proposal.status}", style = MaterialTheme.typography.bodySmall)
            
            val dateFormat = SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
            Text(text = "Submitted: ${proposal.submitted_at}", style = MaterialTheme.typography.bodySmall)
            Text(text = "Last Update: ${proposal.last_status_update_at}", style = MaterialTheme.typography.bodySmall)
            
            if (proposal.sovereign_approved_at != null) {
                Text(text = "Approved: ${proposal.sovereign_approved_at}", style = MaterialTheme.typography.bodySmall)
            }
            
            if (proposal.funding_transaction_hash != null) {
                Text(text = "Tx Hash: ${proposal.funding_transaction_hash}", style = MaterialTheme.typography.bodySmall)
            }

            Spacer(modifier = Modifier.height(16.dp))
            Row {
                Button(
                    onClick = { viewModel.approveProposal(proposal.id) },
                    modifier = Modifier.weight(1f),
                    enabled = proposal.status == "PENDING_REVIEW" || proposal.status == "AWAITING_SOVEREIGN_APPROVAL"
                ) {
                    Text("✅ Approve")
                }
                Spacer(modifier = Modifier.width(8.dp))
                Button(
                    onClick = { viewModel.rejectProposal(proposal.id) },
                    modifier = Modifier.weight(1f),
                    enabled = proposal.status == "PENDING_REVIEW" || proposal.status == "AWAITING_SOVEREIGN_APPROVAL"
                ) {
                    Text("❌ Reject")
                }
            }
        }
    }
}