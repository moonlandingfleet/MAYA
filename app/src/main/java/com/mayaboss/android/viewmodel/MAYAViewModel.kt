package com.mayaboss.android.viewmodel

import android.app.Application
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.mayaboss.android.model.LogResponse
import com.mayaboss.android.model.Proposal
import com.mayaboss.android.model.Treasury
import com.mayaboss.android.model.WalletSession
import com.mayaboss.android.network.MAYAApiService
import com.mayaboss.android.network.WalletBalanceResponse
import com.mayaboss.android.network.WalletConnectManager
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class MAYAViewModel(private val api: MAYAApiService, private val application: Application) : ViewModel() {

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
        // Initialize WalletConnect
        WalletConnectManager.getInstance().initialize(application)
        
        loadProposals()
        loadTreasury()
        startLogPolling()
        observeWalletSession()
    }

    private fun observeWalletSession() {
        viewModelScope.launch {
            WalletConnectManager.getInstance().sessionState.collect { session ->
                _walletSession.value = session ?: WalletSession(false, null, null, null)
                if (session?.address != null) {
                    fetchWalletBalance()
                }
            }
        }
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
        WalletConnectManager.getInstance().connect(
            onUri = onUri,
            onError = onError
        )
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
                val session = WalletConnectManager.getInstance().getCurrentSession()
                session?.address?.let { address ->
                    api.getWalletBalance(address).enqueue(object : Callback<WalletBalanceResponse> {
                        override fun onResponse(call: Call<WalletBalanceResponse>, response: Response<WalletBalanceResponse>) {
                            if (response.isSuccessful) {
                                response.body()?.let { walletBalanceResponse ->
                                    _walletBalance.value = walletBalanceResponse.balance_eth
                                }
                            }
                        }
                        
                        override fun onFailure(call: Call<WalletBalanceResponse>, t: Throwable) {
                            // Handle error
                        }
                    })
                }
            } catch (e: Exception) {
                // Handle error
            }
        }
    }
    
    fun requestTransaction(to: String, amount: String, data: String = "") {
        val session = WalletConnectManager.getInstance().getCurrentSession()
        if (session?.address != null) {
            WalletConnectManager.getInstance().sendTransaction(
                to = to,
                from = session.address ?: "",
                value = amount,
                data = data,
                onResult = { result ->
                    // Handle transaction result
                },
                onError = { error ->
                    // Handle transaction error
                }
            )
        }
    }
    
    fun signTransaction(transaction: Map<String, Any>) {
        WalletConnectManager.getInstance().signTransaction(
            transaction = transaction,
            onResult = { result ->
                // Handle sign result
            },
            onError = { error ->
                // Handle sign error
            }
        )
    }
    
    fun signTypedData(typedData: String) {
        WalletConnectManager.getInstance().signTypedData(
            typedData = typedData,
            onResult = { result ->
                // Handle sign result
            },
            onError = { error ->
                // Handle sign error
            }
        )
    }
    
    fun disconnectWallet() {
        WalletConnectManager.getInstance().disconnect()
    }
    
    fun isConnected(): Boolean {
        return WalletConnectManager.getInstance().isConnected()
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