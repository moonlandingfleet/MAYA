package com.mayaboss.android.viewmodel

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.mayaboss.android.model.Proposal
import com.mayaboss.android.model.WalletSession
import com.mayaboss.android.network.MAYAApiService
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import timber.log.Timber
import retrofit2.Response

class MAYAViewModel(application: Application) : AndroidViewModel(application) {

    private val api: MAYAApiService = MAYAApiService.create("http://192.168.0.101:8000/")
    
    private val _proposals = MutableStateFlow<List<Proposal>>(emptyList())
    val proposals: StateFlow<List<Proposal>> = _proposals

    private val _logs = MutableStateFlow<List<String>>(emptyList())
    val logs: StateFlow<List<String>> = _logs

    private val _walletSession = MutableStateFlow<WalletSession?>(null)
    val walletSession: StateFlow<WalletSession?> = _walletSession

    init {
        loadProposals()
        startLogPolling()
    }

    private fun loadProposals() {
        viewModelScope.launch {
            try {
                val response: Response<List<Proposal>> = api.getProposals()
                if (response.isSuccessful) {
                    _proposals.value = response.body() ?: emptyList()
                } else {
                    Timber.e("Failed to load proposals: ${response.errorBody()?.string()}")
                }
            } catch (e: Exception) {
                Timber.e("Error loading proposals: ${e.message}")
            }
        }
    }

    private fun startLogPolling() {
        viewModelScope.launch {
            while (true) {
                try {
                    val response: Response<com.mayaboss.android.model.LogResponse> = api.getLogs()
                    if (response.isSuccessful) {
                        val logResponse = response.body()
                        _logs.value = logResponse?.logs ?: emptyList()
                    } else {
                        Timber.e("Failed to get logs: ${response.errorBody()?.string()}")
                    }
                } catch (e: Exception) {
                    Timber.e("Error getting logs: ${e.message}")
                }
                delay(10000) // Poll every 10 seconds
            }
        }
    }

    fun requestTransaction(toAddress: String, amount: String, data: String) {
        viewModelScope.launch {
            try {
                // TODO: Implement transaction request logic
                Timber.d("Transaction requested: to=$toAddress, amount=$amount, data=$data")
            } catch (e: Exception) {
                Timber.e("Error requesting transaction: ${e.message}")
            }
        }
    }

    fun connectWallet(
        onUri: (String) -> Unit,
        onError: (Exception) -> Unit
    ) {
        viewModelScope.launch {
            try {
                // TODO: Implement WalletConnect logic
                val uri = "wc:test-uri" // Placeholder
                onUri(uri)
            } catch (e: Exception) {
                onError(e)
            }
        }
    }
    
    fun startAgent(agentId: String) {
        viewModelScope.launch {
            try {
                val response = api.startAgent()
                if (response.isSuccessful) {
                    Timber.d("Agent $agentId started successfully")
                } else {
                    Timber.e("Failed to start agent $agentId: ${response.errorBody()?.string()}")
                }
            } catch (e: Exception) {
                Timber.e("Error starting agent $agentId: ${e.message}")
            }
        }
    }
    
    fun isConnected(): Boolean {
        return _walletSession.value?.connected ?: false
    }
}