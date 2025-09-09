package com.mayaboss.android.network

import android.app.Application
import com.walletconnect.android.Core
import com.walletconnect.android.CoreClient
import com.walletconnect.android.relay.ConnectionType
import com.walletconnect.sign.client.Sign
import com.walletconnect.sign.client.SignClient

class WalletConnectManager private constructor() {
    companion object {
        private var INSTANCE: WalletConnectManager? = null
        
        fun getInstance(): WalletConnectManager {
            return INSTANCE ?: synchronized(this) {
                INSTANCE ?: WalletConnectManager().also { INSTANCE = it }
            }
        }
    }
    
    fun initialize(application: Application) {
        val relayUrl = "relay.walletconnect.com"
        val projectId = BuildConfig.WC_PROJECT_ID // Get from gradle.properties
        val connectionType = ConnectionType.AUTOMATIC
        
        val appMetaData = Core.Model.AppMetaData(
            name = "MAYA",
            description = "MAYA Android App",
            url = "https://mayaboss.com",
            icons = listOf("https://mayaboss.com/icon.png"),
            redirect = "mayaboss://wc"
        )
        
        CoreClient.initialize(
            relayServerUrl = "wss://$relayUrl?projectId=$projectId",
            connectionType = connectionType,
            application = application,
            metaData = appMetaData
        ) { error ->
            // Handle error
            println("WalletConnect initialization error: ${error.throwable.message}")
        }
        
        val init = Sign.Params.Init(
            core = CoreClient
        )
        
        SignClient.initialize(init) { error ->
            // Handle error
            println("SignClient initialization error: ${error.throwable.message}")
        }
    }
    
    fun connect(onUri: (String) -> Unit, onError: (Throwable) -> Unit) {
        // Generate connection URI and QR code
        val namespaces = mapOf(
            "eip155" to Sign.Model.Namespace.Proposal(
                chains = listOf("eip155:1"), // Ethereum mainnet
                methods = listOf("eth_sendTransaction", "eth_signTransaction", "eth_signTypedData_v4"),
                events = listOf("accountsChanged", "chainChanged")
            )
        )
        
        val connectParams = Sign.Params.Connect(
            namespaces = namespaces,
            pairing = null
        )
        
        SignClient.connect(connectParams) { error ->
            onError(error.throwable)
        }
        
        // Get the URI from the pairing
        val pairings = CoreClient.Pairing.getPairings()
        if (pairings.isNotEmpty()) {
            val latestPairing = pairings.last()
            onUri(latestPairing.uri)
        }
    }
    
    fun sendTransaction(to: String, value: String, onResult: (String?) -> Unit) {
        // Send transaction request to wallet
        // Implementation would go here
        onResult("Transaction sent") // Placeholder
    }
    
    fun disconnect() {
        // Disconnect current session
        // Implementation would go here
    }
}