package com.mayaboss.android.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.mayaboss.android.model.Proposal // Ensure this is the updated model
import com.mayaboss.android.viewmodel.MAYAViewModel
import timber.log.Timber // Import Timber

@Composable
fun MainScreen(viewModel: MAYAViewModel = viewModel()) {
    // Fetch proposals and logs
    // Make sure 'proposals' uses the new model structure after fetching
    val proposals by viewModel.proposals.collectAsState(initial = emptyList())
    val logs by viewModel.logs.collectAsState(initial = emptyList())
    val walletSession by viewModel.walletSession.collectAsState()


    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text(text = "MAYA v0.2 — One mind, many hands.", style = MaterialTheme.typography.headlineMedium)

        // Wallet connection status
        if (walletSession?.connected == true) {
            Text(text = "Wallet Connected", color = MaterialTheme.colorScheme.primary)
            Text(text = "Address: ${walletSession?.address}")
            Text(text = "Session ID: ${walletSession?.sessionId}") // Display sessionId
            Text(text = "Balance: ${walletSession?.balance_eth ?: "N/A"} ETH") // Display balance
        } else {
            Button(onClick = { viewModel.connectWallet(address = "0x1234567890123456789012345678901234567890", chainId = "1") }) {
                Text("Connect Wallet")
            }
        }

        Spacer(modifier = Modifier.height(8.dp))

        // Active Proposals
        Text(text = "Active Proposals", style = MaterialTheme.typography.titleMedium)
        if (proposals.isEmpty()) {
            Text("No pending proposals from Agents.")
        } else {
            LazyColumn(Modifier.weight(1f)) {
                items(proposals) { proposal ->
                    // Pass viewModel to ProposalCard
                    // This will now use the ProposalCard from ProposalCard.kt
                    ProposalCard(proposal = proposal, viewModel = viewModel)
                }
            }
        }

        Spacer(modifier = Modifier.height(8.dp))

        // Agent Logs
        Text(text = "Agent Logs (Last 10)", style = MaterialTheme.typography.titleMedium)
        if (logs.isEmpty()){
            Text("No agent logs to display.")
        } else {
            LazyColumn(Modifier.weight(1f)) {
                items(logs) { log ->
                    Text(text = log, modifier = Modifier.padding(vertical = 2.dp))
                }
            }
        }
    }
}

// The @Composable fun ProposalCard(...) definition that was here has been removed.
// It will now use the definition from com.mayaboss.android.ui.ProposalCard.kt