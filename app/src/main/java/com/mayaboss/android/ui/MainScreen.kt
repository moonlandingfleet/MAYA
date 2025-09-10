package com.mayaboss.android.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import com.mayaboss.android.viewmodel.MAYAViewModel

@Composable
fun MainScreen(viewModel: MAYAViewModel) {
    // Fetch proposals and logs
    val proposals by viewModel.proposals.collectAsState(initial = emptyList())
    val logs by viewModel.logs.collectAsState(initial = emptyList())

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text(text = "MAYA v0.2 — One mind, many hands.", style = MaterialTheme.typography.h4)
        
        // Wallet connection status
        if (viewModel.walletSession.value?.connected == true) {
            Text(text = "Wallet Connected", color = Color.Green)
            Text(text = "Address: ${viewModel.walletSession.value?.address}")
            Text(text = "Balance: ${viewModel.walletSession.value?.balance_eth} ETH")
        } else {
            Button(onClick = { /* Connect wallet logic */ }) {
                Text("Connect Wallet")
            }
        }

        // Active Proposals
        Text(text = "Active Proposals", style = MaterialTheme.typography.h6)
        LazyColumn {
            items(proposals) { proposal ->
                ProposalCard(proposal = proposal)
            }
        }

        // Agent Logs
        Text(text = "Agent Logs (Last 10)", style = MaterialTheme.typography.h6)
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
        Text(text = proposal.title, style = MaterialTheme.typography.h5)
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

data class Proposal(
    val id: Int,
    val title: String,
    val description: String
)
