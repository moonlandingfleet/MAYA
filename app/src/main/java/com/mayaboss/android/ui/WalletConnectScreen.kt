package com.mayaboss.android.ui

import android.graphics.Bitmap
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.unit.dp
import com.google.zxing.BarcodeFormat
import com.journeyapps.barcodescanner.BarcodeEncoder
import com.mayaboss.android.viewmodel.MAYAViewModel

@Composable
fun WalletConnectScreen(viewModel: MAYAViewModel, onBack: () -> Unit) {
    var uri by remember { mutableStateOf<String?>(null) }
    var isConnected by remember { mutableStateOf(false) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    
    LaunchedEffect(Unit) {
        viewModel.connectWallet(
            onUri = { generatedUri ->
                uri = generatedUri
            },
            onError = { error ->
                errorMessage = error.message
            }
        )
    }
    
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
        
        Text("🔌 Connect Your Wallet", style = MaterialTheme.typography.headlineMedium)
        Spacer(modifier = Modifier.height(16.dp))
        
        uri?.let { wcUri ->
            val bitmap = remember(wcUri) {
                try {
                    BarcodeEncoder().encodeBitmap(wcUri, BarcodeFormat.QR_CODE, 400, 400)
                } catch (e: Exception) {
                    null
                }
            }
            
            bitmap?.let {
                Image(
                    bitmap = it.asImageBitmap(),
                    contentDescription = "WalletConnect QR Code",
                    modifier = Modifier.size(300.dp)
                )
            } ?: Text("Error generating QR Code")
        } ?: if (errorMessage != null) {
            Text("Error: $errorMessage")
        } else {
            Text("Generating QR Code...")
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        Text("Scan with MetaMask or any WalletConnect-compatible wallet", 
             style = MaterialTheme.typography.bodyMedium)
    }
}