package com.mayaboss.android.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.mayaboss.android.BuildConfig
import com.mayaboss.android.model.CouncilOpportunity
import com.mayaboss.android.model.Proposal
import com.mayaboss.android.viewmodel.MAYAViewModel
import timber.log.Timber

@Composable
fun MainScreen(viewModel: MAYAViewModel = viewModel()) {
    val isAuthenticated by viewModel.isAuthenticated.collectAsState()
    
    if (isAuthenticated) {
        AuthenticatedMainScreen(viewModel)
    } else {
        LoginScreen(viewModel)
    }
}

@Composable
fun LoginScreen(viewModel: MAYAViewModel) {
    var username by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "MAYA Login",
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.align(Alignment.CenterHorizontally)
        )
        
        Spacer(modifier = Modifier.height(32.dp))
        
        OutlinedTextField(
            value = username,
            onValueChange = { username = it },
            label = { Text("Username") },
            modifier = Modifier.fillMaxWidth()
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        OutlinedTextField(
            value = password,
            onValueChange = { password = it },
            label = { Text("Password") },
            modifier = Modifier.fillMaxWidth(),
            visualTransformation = androidx.compose.ui.text.input.PasswordVisualTransformation()
        )
        
        Spacer(modifier = Modifier.height(24.dp))
        
        Button(
            onClick = { viewModel.login(username, password) },
            modifier = Modifier.align(Alignment.CenterHorizontally)
        ) {
            Text("Login")
        }
        
        // Testing mode button for debug builds
        if (BuildConfig.DEBUG) {
            Spacer(modifier = Modifier.height(16.dp))
            Button(
                onClick = { viewModel.enableTestingMode() },
                modifier = Modifier.align(Alignment.CenterHorizontally),
                colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
            ) {
                Text("Enable Testing Mode")
            }
        }
    }
}

@Composable
fun AuthenticatedMainScreen(viewModel: MAYAViewModel) {
    // Fetch proposals and logs
    val proposals by viewModel.proposals.collectAsState(initial = emptyList())
    val councils by viewModel.councils.collectAsState(initial = emptyList())
    val treasury by viewModel.treasury.collectAsState()
    val logs by viewModel.logs.collectAsState(initial = emptyList())
    val walletSession by viewModel.walletSession.collectAsState()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(text = "MAYA v0.2 — One mind, many hands.", style = MaterialTheme.typography.headlineMedium)
            
            // Testing mode indicator and logout button
            Row(
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Testing mode indicator for debug builds
                if (BuildConfig.DEBUG && BuildConfig.FLAVOR == "testing") {
                    Text(
                        text = "TESTING MODE",
                        color = MaterialTheme.colorScheme.error,
                        style = MaterialTheme.typography.bodySmall,
                        modifier = Modifier.padding(end = 8.dp)
                    )
                }
                
                Button(onClick = { viewModel.logout() }) {
                    Text("Logout")
                }
            }
        }

        // Wallet connection status
        if (walletSession?.connected == true) {
            Text(text = "Wallet Connected", color = MaterialTheme.colorScheme.primary)
            Text(text = "Address: ${walletSession?.address}")
            Text(text = "Session ID: ${walletSession?.sessionId}")
            Text(text = "Balance: ${walletSession?.balance_eth ?: "N/A"} ETH")
        } else {
            Button(onClick = { viewModel.connectWallet(address = "0x1234567890123456789012345678901234567890", chainId = "1") }) {
                Text("Connect Wallet")
            }
        }

        Spacer(modifier = Modifier.height(8.dp))

        // Treasury Information
        treasury?.let {
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp),
                elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(text = "Treasury Information", style = MaterialTheme.typography.titleMedium)
                    Text(text = "ETH Balance: ${it.balance_eth}")
                    Text(text = "BTC Balance: ${it.balance_btc}")
                    Text(text = "Last Updated: ${it.last_updated}")
                }
            }
        }

        Spacer(modifier = Modifier.height(8.dp))

        // Active Proposals
        Text(text = "Active Proposals", style = MaterialTheme.typography.titleMedium)
        if (proposals.isEmpty()) {
            Text("No pending proposals from Councils.")
        } else {
            LazyColumn(Modifier.weight(1f)) {
                items(proposals) { proposal ->
                    ProposalCard(proposal = proposal, viewModel = viewModel)
                }
            }
        }

        Spacer(modifier = Modifier.height(8.dp))

        // Councils
        Text(text = "Councils", style = MaterialTheme.typography.titleMedium)
        if (councils.isEmpty()) {
            Text("No councils available.")
        } else {
            LazyColumn(Modifier.weight(1f)) {
                items(councils) { council ->
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 4.dp),
                        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            Text(text = council.council_name, style = MaterialTheme.typography.titleMedium)
                            Text(text = council.domain_description, style = MaterialTheme.typography.bodyMedium)
                            Text(text = "Status: ${council.status}", style = MaterialTheme.typography.bodySmall)
                            
                            Spacer(modifier = Modifier.height(8.dp))
                            
                            Button(
                                onClick = { 
                                    // Load opportunities for this council
                                    viewModel.loadCouncilOpportunities(council.id)
                                },
                                modifier = Modifier.align(Alignment.End)
                            ) {
                                Text("View Opportunities")
                            }
                        }
                    }
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