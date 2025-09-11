package com.mayaboss.android.viewmodel

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.mayaboss.android.model.Proposal
import com.mayaboss.android.model.WalletSession // Assuming this model exists and is appropriate
import com.mayaboss.android.network.MAYAApiService
import com.mayaboss.android.network.ProposalDecisionRequest
import com.mayaboss.android.network.WalletConnectRequest
import com.mayaboss.android.network.WalletSessionResponse // From MAYAApiService.kt
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import timber.log.Timber
import retrofit2.Response

class MAYAViewModel(application: Application) : AndroidViewModel(application) {

    private val api: MAYAApiService = MAYAApiService.create("http://192.168.0.103:8000/")

    private val _proposals = MutableStateFlow<List<Proposal>>(emptyList())
    val proposals: StateFlow<List<Proposal>> = _proposals

    private val _logs = MutableStateFlow<List<String>>(emptyList())
    val logs: StateFlow<List<String>> = _logs

    private val _walletSession = MutableStateFlow<WalletSession?>(null)
    val walletSession: StateFlow<WalletSession?> = _walletSession

    init {
        loadPendingProposals()
        startLogPolling()
    }

    fun loadPendingProposals() {
        viewModelScope.launch {
            try {
                val response: Response<List<Proposal>> = api.getPendingProposals()
                if (response.isSuccessful) {
                    _proposals.value = response.body() ?: emptyList()
                    Timber.d("Pending proposals loaded: ${_proposals.value.size}")
                } else {
                    Timber.e("Failed to load pending proposals: ${response.errorBody()?.string()}")
                }
            } catch (e: Exception) {
                Timber.e(e, "Error loading pending proposals")
            }
        }
    }

    fun approveProposal(proposalId: String) {
        viewModelScope.launch {
            try {
                Timber.d("Approving proposal: $proposalId")
                val response = api.approveProposal(ProposalDecisionRequest(proposal_id = proposalId))
                if (response.isSuccessful) {
                    Timber.i("Proposal $proposalId approved successfully on backend: ${response.body()}")
                    loadPendingProposals()
                } else {
                    Timber.e("Failed to approve proposal $proposalId: ${response.errorBody()?.string()}")
                }
            } catch (e: Exception) {
                Timber.e(e, "Error approving proposal $proposalId")
            }
        }
    }

    fun rejectProposal(proposalId: String) {
        viewModelScope.launch {
            try {
                Timber.d("Rejecting proposal: $proposalId")
                val response = api.rejectProposal(ProposalDecisionRequest(proposal_id = proposalId))
                if (response.isSuccessful) {
                    Timber.i("Proposal $proposalId rejected successfully on backend: ${response.body()}")
                    loadPendingProposals()
                } else {
                    Timber.e("Failed to reject proposal $proposalId: ${response.errorBody()?.string()}")
                }
            } catch (e: Exception) {
                Timber.e(e, "Error rejecting proposal $proposalId")
            }
        }
    }

    private fun startLogPolling() {
        viewModelScope.launch {
            while (true) {
                try {
                    val response = api.getLogs()
                    if (response.isSuccessful) {
                        _logs.value = response.body()?.logs ?: emptyList()
                    } else {
                        Timber.e("Failed to get logs: ${response.errorBody()?.string()}")
                    }
                } catch (e: Exception) {
                    Timber.e(e, "Error getting logs")
                }
                delay(10000) // Poll every 10 seconds
            }
        }
    }

    fun connectWallet(address: String, chainId: String) {
        viewModelScope.launch {
            try {
                Timber.d("Connecting wallet: address=$address, chainId=$chainId")
                val response: Response<WalletSessionResponse> = api.connectWallet(WalletConnectRequest(address = address, chain_id = chainId))
                if (response.isSuccessful && response.body()?.status == "connected") {
                    val sessionResponse = response.body()!!
                    _walletSession.value = WalletSession(
                        connected = true,
                        address = sessionResponse.address,
                        chainId = chainId, // Passed the chainId parameter
                        sessionId = sessionResponse.session_id,
                        balance_eth = _walletSession.value?.balance_eth
                    )
                    Timber.i("Wallet connected: ${sessionResponse.address}, session: ${sessionResponse.session_id}")
                    // TODO: Fetch wallet balance after connection
                    // fetchWalletBalance(sessionResponse.address)
                } else {
                    Timber.e("Failed to connect wallet: ${response.errorBody()?.string() ?: response.message()}")
                    _walletSession.value = WalletSession(
                        connected = false,
                        address = "",
                        chainId = null, // Added null for chainId
                        sessionId = null,
                        balance_eth = null
                    )
                }
            } catch (e: Exception) {
                Timber.e(e, "Error connecting wallet")
                _walletSession.value = WalletSession(
                    connected = false,
                    address = "",
                    chainId = null, // Added null for chainId
                    sessionId = null,
                    balance_eth = null
                )
            }
        }
    }

    // fun fetchWalletBalance(address: String) { ... } // Keep placeholder

    fun isConnected(): Boolean {
        return _walletSession.value?.connected ?: false
    }

    fun startAgent(agentId: String) {
        viewModelScope.launch {
            try {
                val response = api.startAgent()
                if (response.isSuccessful) {
                    Timber.d("Agent $agentId (or generic agent) start command issued.")
                } else {
                    Timber.e("Failed to start agent $agentId: ${response.errorBody()?.string()}")
                }
            } catch (e: Exception) {
                Timber.e(e, "Error starting agent $agentId")
            }
        }
    }
}

// Ensure you have a WalletSession data class in your model package, for example:
// package com.mayaboss.android.model
// data class WalletSession(
//     val connected: Boolean,
//     val address: String,
//     val chainId: String?,
//     val sessionId: String?,
//     val balance_eth: Double? = null
// )
