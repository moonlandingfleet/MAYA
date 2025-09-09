package com.mayaboss.android.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.mayaboss.android.model.LogResponse
import com.mayaboss.android.model.Proposal
import com.mayaboss.android.model.Treasury
import com.mayaboss.android.model.WalletSession
import com.mayaboss.android.network.MAYAApiService
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class MAYAViewModel(private val api: MAYAApiService) : ViewModel() {

    private val _proposals = MutableStateFlow<List<Proposal>>(emptyList())
    val proposals: StateFlow<List<Proposal>> = _proposals.asStateFlow()

    private val _logs = MutableStateFlow<List<String>>(emptyList())
    val logs: StateFlow<List<String>> = _logs.asStateFlow()
    
    private val _treasury = MutableStateFlow<Treasury?>(null)
    val treasury: StateFlow<Treasury?> = _treasury.asStateFlow()
    
    private val _totalProfit = MutableStateFlow(0.0)
    val totalProfit: StateFlow<Double> = _totalProfit.asStateFlow()
    
    private val _showDecisionDialog = MutableStateFlow(false)
    val showDecisionDialog: StateFlow<Boolean> = _showDecisionDialog.asStateFlow()
    
    private val _walletSession = MutableStateFlow<WalletSession>(WalletSession(false, null, null, null))
    val walletSession: StateFlow<WalletSession> = _walletSession.asStateFlow()
    
    private val _walletBalance = MutableStateFlow(0.0)
    val walletBalance: StateFlow<Double> = _walletBalance.asStateFlow()

    init {
        loadProposals()
        loadTreasury()
        startLogPolling()
    }

    private fun loadProposals() {
        viewModelScope.launch {
            try {
                val response = api.getProposals().execute()
                if (response.isSuccessful) {
                    _proposals.value = response.body() ?: emptyList()
                }
            } catch (e: Exception) {
                // Handle error
            }
        }
    }

    fun startAgent(agentId: String) {
        viewModelScope.launch {
            try {
                val response = api.startAgent().execute()
                if (response.isSuccessful) {
                    // Handle success
                }
            } catch (e: Exception) {
                // Handle error
            }
        }
    }
    
    fun connectWallet(onUri: (String) -> Unit, onError: (Throwable) -> Unit) {
        // WalletConnectManager.getInstance().connect { uri ->
        //     onUri(uri)
        // }
        // Placeholder implementation for now
        onUri("wc:placeholder_uri")
    }

    private fun loadTreasury() {
        viewModelScope.launch {
            try {
                val treasury = api.getTreasury()
                _treasury.value = treasury
            } catch (e: Exception) {
                // Handle
            }
        }
    }
    
    fun fetchWalletBalance() {
        viewModelScope.launch {
            try {
                // Fetch real balance from backend
                // val response = api.getWalletBalance()
                // _walletBalance.value = response.balance
                // Placeholder implementation
                _walletBalance.value = 0.0015
            } catch (e: Exception) {
                // Handle error
            }
        }
    }
    
    fun requestTransaction(to: String, amount: String) {
        // WalletConnectManager.getInstance().sendTransaction(to, amount) { result ->
        //     // Handle transaction result
        // }
        // Placeholder implementation
    }
    
    fun onDecision(choice: Boolean) {
        viewModelScope.launch {
            try {
                api.agentDecide("A-01", if (choice) "continue" else "terminate")
            } catch (e: Exception) {
                // Handle
            }
            _showDecisionDialog.value = false
        }
    }
    
    private fun startLogPolling() {
        viewModelScope.launch {
            while (true) {
                try {
                    val response = api.getLogs().execute()
                    if (response.isSuccessful) {
                        val logResponse = response.body()
                        _logs.value = logResponse?.logs ?: emptyList()
                        
                        // Calculate profit from logs
                        val profitLines = logResponse?.logs?.filter { it.contains("📈 PROFIT:") } ?: emptyList()
                        val total = profitLines.sumOf { line ->
                            line.substringAfter("📈 PROFIT: ").substringBefore(" ETH").toDoubleOrNull() ?: 0.0
                        }
                        _totalProfit.value = total
                        
                        // Show decision dialog after 10 minutes (simplified for demo)
                        if (logResponse?.logs?.size ?: 0 > 5 && logResponse?.logs?.any { it.contains("HEARTBEAT") } == true) {
                            _showDecisionDialog.value = true
                        }
                    }
                } catch (e: Exception) {
                    // Silent fail
                }
                delay(10000) // 10s
            }
        }
    }
}