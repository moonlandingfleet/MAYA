package com.mayaboss.android.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Info
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.mayaboss.android.viewmodel.MAYAViewModel

@Composable
fun MainScreen(viewModel: MAYAViewModel) {
    val proposals by viewModel.proposals.collectAsState()
    val logs by viewModel.logs.collectAsState()
    val treasury by viewModel.treasury.collectAsState()
    val totalProfit by viewModel.totalProfit.collectAsState()
    val showDecisionDialog by viewModel.showDecisionDialog.collectAsState()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text("MAYA v0.2 — One mind, many hands.", style = MaterialTheme.typography.headlineMedium)
        Spacer(modifier = Modifier.height(16.dp))
        
        // Treasury Information
        treasury?.let { t ->
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(8.dp)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Row(verticalAlignment = androidx.compose.ui.Alignment.CenterVertically) {
                        Icon(Icons.Default.Info, contentDescription = "Treasury Info")
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Treasury Information", style = MaterialTheme.typography.titleMedium)
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    Text("🏦 Treasury: ${t.balance_eth} ETH", style = MaterialTheme.typography.bodyLarge)
                    Text("Address: ${t.address.take(10)}...", style = MaterialTheme.typography.bodyMedium)
                    Text("💰 Revenue Today: ${String.format("%.6f", totalProfit)} ETH", style = MaterialTheme.typography.bodyLarge)
                }
            }
            Spacer(modifier = Modifier.height(16.dp))
        }

        // Proposals
        Text("Active Proposals", style = MaterialTheme.typography.titleLarge)
        LazyColumn {
            items(proposals) { proposal ->
                ProposalCard(
                    proposal = proposal,
                    onApprove = { viewModel.startAgent(proposal.id) },
                    onReject = { /* later */ }
                )
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        // Logs
        Text("Agent Logs (Last 10)", style = MaterialTheme.typography.titleLarge)
        logs.takeLast(10).forEach { log ->
            Text(text = log, style = MaterialTheme.typography.bodySmall)
        }
    }
    
    // Decision Dialog
    if (showDecisionDialog) {
        AlertDialog(
            onDismissRequest = { },
            title = { Text("Agent Decision Required") },
            text = { Text("A-01 earned 0.0003 ETH. Continue execution?") },
            confirmButton = {
                Button(onClick = { viewModel.onDecision(true) }) {
                    Text("✅ Continue")
                }
            },
            dismissButton = {
                Button(onClick = { viewModel.onDecision(false) }) {
                    Text("⏹️ Terminate")
                }
            }
        )
    }
}