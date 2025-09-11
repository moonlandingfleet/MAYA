package com.mayaboss.android.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.mayaboss.android.viewmodel.MAYAViewModel
import timber.log.Timber

@Composable
fun TransactionRequestScreen(viewModel: MAYAViewModel, onBack: () -> Unit) {
    var toAddress by remember { mutableStateOf("") }
    var amount by remember { mutableStateOf("") }
    var data by remember { mutableStateOf("") }
    var resultMessage by remember { mutableStateOf<String?>(null) }
    var errorMessage by remember { mutableStateOf<String?>(null) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        // Back button
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.Start
        ) {
            Button(onClick = onBack) {
                Text("← Back")
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        Text("💸 Request Transaction", style = MaterialTheme.typography.headlineMedium)
        Spacer(modifier = Modifier.height(16.dp))

        TextField(
            value = toAddress,
            onValueChange = { toAddress = it },
            label = { Text("To Address") },
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(8.dp))

        TextField(
            value = amount,
            onValueChange = { amount = it },
            label = { Text("Amount (ETH)") },
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(8.dp))

        TextField(
            value = data,
            onValueChange = { data = it },
            label = { Text("Data (optional)") },
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(16.dp))

        Button(
            onClick = {
                if (toAddress.isNotEmpty() && amount.isNotEmpty()) {
                    // viewModel.requestTransaction(toAddress, amount, data) // TODO: Refactor this screen based on charter's transaction flow
                    Timber.d("Transaction Request UI: 'Send' clicked. To: $toAddress, Amount: $amount, Data: $data. Actual ViewModel call commented out.")
                    resultMessage = "Transaction request function is currently under review as per the Royal Charter. (Original call commented out)."
                    errorMessage = null
                } else {
                    errorMessage = "Please fill in all required fields."
                    resultMessage = null
                }
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Send Transaction Request")
        }

        resultMessage?.let {
            Spacer(modifier = Modifier.height(16.dp))
            Text(it, color = MaterialTheme.colorScheme.primary)
        }

        errorMessage?.let {
            Spacer(modifier = Modifier.height(16.dp))
            Text(it, color = MaterialTheme.colorScheme.error)
        }
    }
}