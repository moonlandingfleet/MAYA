package com.mayaboss.android.network

import android.app.Application
import android.content.Context
import android.content.SharedPreferences
import com.mayaboss.android.model.WalletSession // Ensure this is the updated model
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

class WalletConnectManager private constructor() {
    companion object {
        private var INSTANCE: WalletConnectManager? = null

        fun getInstance(): WalletConnectManager {
            return INSTANCE ?: synchronized(this) {
                INSTANCE ?: WalletConnectManager().also { INSTANCE = it }
            }
        }
    }

    private val _sessionState = MutableStateFlow<WalletSession?>(null)
    val sessionState: StateFlow<WalletSession?> = _sessionState

    private lateinit var sharedPreferences: SharedPreferences
    // private lateinit var apiService: MAYAApiService // This seems unused here, consider removing if not needed

    fun initialize(application: Application) {
        sharedPreferences = application.getSharedPreferences("wallet_connect_prefs", Context.MODE_PRIVATE)

        // Initialize API service - This instance seems separate from ViewModel's.
        // If this WalletConnectManager is to be deprecated, this might not be an issue.
        // apiService = MAYAApiService.create("http://192.168.0.101:8000/")

        restoreSession()
    }

    private fun restoreSession() {
        val connected = sharedPreferences.getBoolean("connected", false)
        if (connected) {
            val address = sharedPreferences.getString("address", null)
            val chainId = sharedPreferences.getString("chainId", null)
            val sessionId = sharedPreferences.getString("sessionId", null) // Changed from topic

            if (address != null && chainId != null && sessionId != null) { // Check sessionId
                val walletSession = WalletSession(
                    connected = true,
                    address = address,
                    chainId = chainId,
                    sessionId = sessionId // Changed from topic
                )
                _sessionState.value = walletSession
            }
        }
    }

    private fun saveSession(session: WalletSession) {
        sharedPreferences.edit()
            .putBoolean("connected", session.connected)
            .putString("address", session.address)
            .putString("chainId", session.chainId)
            .putString("sessionId", session.sessionId) // Changed from topic
            .apply()
    }

    private fun clearSavedSession() {
        sharedPreferences.edit()
            .clear()
            .apply()
    }

    fun connect(onUri: (String) -> Unit, onError: (Throwable) -> Unit) {
        // Mock WalletConnect implementation
        val mockUri = "wc:mock-connection-uri" // This URI is for a true WalletConnect SDK flow
        onUri(mockUri)

        android.os.Handler(android.os.Looper.getMainLooper()).postDelayed({
            val mockSession = WalletSession(
                connected = true,
                address = "0x1234567890123456789012345678901234567890",
                chainId = "1",
                sessionId = "mock-session-id-from-manager" // Changed from topic
            )
            _sessionState.value = mockSession
            saveSession(mockSession)
        }, 2000)
    }

    fun sendTransaction(to: String, from: String, value: String, data: String = "", onResult: (String?) -> Unit, onError: (Throwable) -> Unit) {
        if (_sessionState.value?.connected == true) {
            val mockTxHash = "0x${(1..64).map { (0..15).random().toString(16) }.joinToString("")}"
            onResult(mockTxHash)
        } else {
            onError(Throwable("Wallet not connected (WalletConnectManager)"))
        }
    }

    fun signTransaction(transaction: Map<String, Any>, onResult: (String?) -> Unit, onError: (Throwable) -> Unit) {
        if (_sessionState.value?.connected == true) {
            val mockSignature = "0x${(1..130).map { (0..15).random().toString(16) }.joinToString("")}"
            onResult(mockSignature)
        } else {
            onError(Throwable("Wallet not connected (WalletConnectManager)"))
        }
    }

    fun signTypedData(typedData: String, onResult: (String?) -> Unit, onError: (Throwable) -> Unit) {
        if (_sessionState.value?.connected == true) {
            val mockSignature = "0x${(1..130).map { (0..15).random().toString(16) }.joinToString("")}"
            onResult(mockSignature)
        } else {
            onError(Throwable("Wallet not connected (WalletConnectManager)"))
        }
    }

    fun disconnect() {
        _sessionState.value = null
        clearSavedSession()
    }

    fun getCurrentSession(): WalletSession? {
        return _sessionState.value
    }

    fun isConnected(): Boolean {
        return _sessionState.value?.connected ?: false
    }
}