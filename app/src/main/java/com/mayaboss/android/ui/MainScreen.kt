package com.mayaboss.android.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.mayaboss.android.model.Proposal
import com.mayaboss.android.viewmodel.MAYAViewModel

@Composable
fun MainScreen(viewModel: MAYAViewModel = viewModel()) {
    // Fetch proposals and logs
    val proposals by viewModel.proposals.collectAsState(initial = emptyList())
    val logs by viewModel.logs.collectAsState(initial = emptyList())

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text(text = "MAYA v0.2 — One mind, many hands.", style = MaterialTheme.typography.headlineMedium)
        
        // Wallet connection status
        if (viewModel.walletSession.value?.connected == true) {
            Text(text = "Wallet Connected", color = MaterialTheme.colorScheme.primary)
            Text(text = "Address: ${viewModel.walletSession.value?.address}")
            Text(text = "Balance: ${viewModel.walletSession.value?.balance_eth} ETH")
        } else {
            Button(onClick = { /* Connect wallet logic */ }) {
                Text("Connect Wallet")
            }
        }

        // Active Proposals
        Text(text = "Active Proposals", style = MaterialTheme.typography.titleMedium)
        LazyColumn {
            items(proposals) { proposal ->
                Text(text = proposal.name)
            }
        }

        // Agent Logs
        Text(text = "Agent Logs (Last 10)", style = MaterialTheme.typography.titleMedium)
        LazyColumn {
            items(logs) { log ->
                Text(text = log)
            }
        }
    }
}

@Composable
fun ProposalCard(proposal: Proposal) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp)
    ) {
        Text(text = proposal.name, style = MaterialTheme.typography.titleMedium)
        Text(text = proposal.description)
        Row {
            Button(onClick = { /* Approve proposal logic */ }) {
                Text("Approve")
            }
            Button(onClick = { /* Reject proposal logic */ }) {
                Text("Reject")
            }
        }
    }
}

