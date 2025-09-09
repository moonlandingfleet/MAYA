package com.mayaboss.android.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.mayaboss.android.viewmodel.MAYAViewModel

@Composable
fun MainScreen(viewModel: MAYAViewModel) {
    val proposals by viewModel.proposals.collectAsState()
    val logs by viewModel.logs.collectAsState()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text("MAYA v0.2 — One mind, many hands.", style = MaterialTheme.typography.headlineMedium)
        Spacer(modifier = Modifier.height(16.dp))

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
}