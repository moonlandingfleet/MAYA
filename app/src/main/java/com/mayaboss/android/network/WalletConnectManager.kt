package com.mayaboss.android.network

import android.app.Application
import android.content.Context
import android.content.SharedPreferences
import com.mayaboss.android.model.WalletSession
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
    private lateinit var apiService: MAYAApiService
    
    fun initialize(application: Application) {
        sharedPreferences = application.getSharedPreferences("wallet_connect_prefs", Context.MODE_PRIVATE)
        
        // Initialize API service
        apiService = MAYAApiService.create("http://192.168.0.101:8000/")
        
        // WalletConnect initialization temporarily disabled due to build issues
        // For now, we'll use mock implementation
        restoreSession()
    }
    
    private fun restoreSession() {
        val connected = sharedPreferences.getBoolean("connected", false)
        if (connected) {
            val address = sharedPreferences.getString("address", null)
            val chainId = sharedPreferences.getString("chainId", null)
            val topic = sharedPreferences.getString("topic", null)
            
            if (address != null && chainId != null && topic != null) {
                val walletSession = WalletSession(
                    connected = true,
                    address = address,
                    chainId = chainId,
                    topic = topic
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
            .putString("topic", session.topic)
            .apply()
    }
    
    private fun clearSavedSession() {
        sharedPreferences.edit()
            .clear()
            .apply()
    }
    
    fun connect(onUri: (String) -> Unit, onError: (Throwable) -> Unit) {
        // Mock WalletConnect implementation
        // For demo purposes, simulate a connection
        val mockUri = "wc:mock-connection-uri"
        onUri(mockUri)
        
        // Simulate successful connection after a delay
        android.os.Handler(android.os.Looper.getMainLooper()).postDelayed({
            val mockSession = WalletSession(
                connected = true,
                address = "0x1234567890123456789012345678901234567890",
                chainId = "1",
                topic = "mock-topic"
            )
            _sessionState.value = mockSession
            saveSession(mockSession)
        }, 2000)
    }
    
    fun sendTransaction(to: String, from: String, value: String, data: String = "", onResult: (String?) -> Unit, onError: (Throwable) -> Unit) {
        // Mock transaction implementation
        if (_sessionState.value?.connected == true) {
            val mockTxHash = "0x${(1..64).map { (0..15).random().toString(16) }.joinToString("")}"
            onResult(mockTxHash)
        } else {
            onError(Throwable("Wallet not connected"))
        }
    }
    
    fun signTransaction(transaction: Map<String, Any>, onResult: (String?) -> Unit, onError: (Throwable) -> Unit) {
        // Mock sign transaction implementation
        if (_sessionState.value?.connected == true) {
            val mockSignature = "0x${(1..130).map { (0..15).random().toString(16) }.joinToString("")}"
            onResult(mockSignature)
        } else {
            onError(Throwable("Wallet not connected"))
        }
    }
    
    fun signTypedData(typedData: String, onResult: (String?) -> Unit, onError: (Throwable) -> Unit) {
        // Mock sign typed data implementation
        if (_sessionState.value?.connected == true) {
            val mockSignature = "0x${(1..130).map { (0..15).random().toString(16) }.joinToString("")}"
            onResult(mockSignature)
        } else {
            onError(Throwable("Wallet not connected"))
        }
    }
    
    fun disconnect() {
        // Mock disconnect implementation
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