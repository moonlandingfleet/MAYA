package com.mayaboss.android.viewmodel

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.mayaboss.android.BuildConfig
import com.mayaboss.android.model.Council
import com.mayaboss.android.model.CouncilOpportunity
import com.mayaboss.android.model.LogResponse
import com.mayaboss.android.model.Proposal
import com.mayaboss.android.model.Treasury
import com.mayaboss.android.model.TreasuryTransaction
import com.mayaboss.android.model.WalletSession
import com.mayaboss.android.network.AuthManager
import com.mayaboss.android.network.CouncilManager
import com.mayaboss.android.network.FundingRequest
import com.mayaboss.android.network.LoginRequest
import com.mayaboss.android.network.LoginResponse
import com.mayaboss.android.network.MAYAApiService
import com.mayaboss.android.network.ProposalDecisionRequest
import com.mayaboss.android.network.WalletConnectRequest
import com.mayaboss.android.network.WalletConnectV2Manager
import com.mayaboss.android.network.WalletSessionResponse
import com.mayaboss.android.util.ErrorHandlingUtil
import com.mayaboss.android.util.ProposalScoringUtil
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import timber.log.Timber
import retrofit2.Response

class MAYAViewModel(application: Application) : AndroidViewModel(application) {

    private val api: MAYAApiService = MAYAApiService.create("http://192.168.0.100:8000/")
    private val authManager: AuthManager = AuthManager.getInstance()
    private val walletConnectManager: WalletConnectV2Manager = WalletConnectV2Manager.getInstance()
    private val councilManager: CouncilManager = CouncilManager.getInstance()

    private val _proposals = MutableStateFlow<List<Proposal>>(emptyList())
    val proposals: StateFlow<List<Proposal>> = _proposals

    private val _rankedProposals = MutableStateFlow<List<Proposal>>(emptyList())
    val rankedProposals: StateFlow<List<Proposal>> = _rankedProposals

    private val _councils = MutableStateFlow<List<Council>>(emptyList())
    val councils: StateFlow<List<Council>> = _councils

    private val _opportunities = MutableStateFlow<List<CouncilOpportunity>>(emptyList())
    val opportunities: StateFlow<List<CouncilOpportunity>> = _opportunities

    private val _treasury = MutableStateFlow<Treasury?>(null)
    val treasury: StateFlow<Treasury?> = _treasury

    private val _transactions = MutableStateFlow<List<TreasuryTransaction>>(emptyList())
    val transactions: StateFlow<List<TreasuryTransaction>> = _transactions

    private val _logs = MutableStateFlow<List<String>>(emptyList())
    val logs: StateFlow<List<String>> = _logs

    private val _walletSession = MutableStateFlow<WalletSession?>(null)
    val walletSession: StateFlow<WalletSession?> = _walletSession

    private val _isAuthenticated = MutableStateFlow<Boolean>(false)
    val isAuthenticated: StateFlow<Boolean> = _isAuthenticated

    init {
        authManager.initialize(application)
        walletConnectManager.initialize(application)
        checkAuthentication()
        if (_isAuthenticated.value) {
            loadPendingProposals()
            loadCouncils()
            loadTreasury()
            startLogPolling()
        }
    }

    private fun checkAuthentication() {
        // In testing mode, bypass authentication
        if (BuildConfig.DEBUG && BuildConfig.FLAVOR == "testing") {
            authManager.setMockTokenForTesting()
            _isAuthenticated.value = true
            MAYAApiService.setAuthToken("mock-testing-token")
            return
        }
        
        val token = authManager.getAuthToken()
        if (!token.isNullOrEmpty()) {
            _isAuthenticated.value = true
            MAYAApiService.setAuthToken(token)
        }
    }

    fun login(username: String, password: String) {
        // In testing mode, bypass authentication
        if (BuildConfig.DEBUG && BuildConfig.FLAVOR == "testing") {
            authManager.setMockTokenForTesting()
            _isAuthenticated.value = true
            MAYAApiService.setAuthToken("mock-testing-token")
            
            // Load data after successful login
            loadPendingProposals()
            loadCouncils()
            loadTreasury()
            startLogPolling()
            
            return
        }
        
        viewModelScope.launch {
            try {
                val request = LoginRequest(username, password)
                val response = api.login(request)
                if (response.isSuccessful) {
                    val loginResponse = response.body()
                    if (loginResponse != null) {
                        authManager.saveAuthToken(loginResponse.token)
                        MAYAApiService.setAuthToken(loginResponse.token)
                        _isAuthenticated.value = true
                        ErrorHandlingUtil.logInfo("MAYAViewModel", "Login successful for user: ${loginResponse.user_id}")
                        
                        // Load data after successful login
                        loadPendingProposals()
                        loadCouncils()
                        loadTreasury()
                        startLogPolling()
                    }
                } else {
                    val errorBody = response.errorBody()?.string()
                    ErrorHandlingUtil.handleApiError("MAYAViewModel", "login", errorBody)
                    _isAuthenticated.value = false
                }
            } catch (e: Exception) {
                ErrorHandlingUtil.handleUnexpectedError("MAYAViewModel", "login", e)
                _isAuthenticated.value = false
            }
        }
    }

    fun logout() {
        // In testing mode, just clear the authentication state
        if (BuildConfig.DEBUG && BuildConfig.FLAVOR == "testing") {
            authManager.clearAuthToken()
            MAYAApiService.clearAuthToken()
            _isAuthenticated.value = false
            return
        }
        
        viewModelScope.launch {
            try {
                val response = api.logout()
                if (response.isSuccessful) {
                    authManager.clearAuthToken()
                    MAYAApiService.clearAuthToken()
                    _isAuthenticated.value = false
                    ErrorHandlingUtil.logInfo("MAYAViewModel", "Logout successful")
                } else {
                    val errorBody = response.errorBody()?.string()
                    ErrorHandlingUtil.handleApiError("MAYAViewModel", "logout", errorBody)
                }
            } catch (e: Exception) {
                ErrorHandlingUtil.handleUnexpectedError("MAYAViewModel", "logout", e)
            }
        }
    }

    fun loadPendingProposals() {
        if (!_isAuthenticated.value) return
        
        viewModelScope.launch {
            try {
                val response: Response<List<Proposal>> = api.getPendingProposals()
                if (response.isSuccessful) {
                    val fetchedProposals = response.body() ?: emptyList()
                    _proposals.value = fetchedProposals
                    
                    // Calculate and rank proposals
                    val ranked = ProposalScoringUtil.rankProposals(fetchedProposals)
                    _rankedProposals.value = ranked
                    
                    ErrorHandlingUtil.logDebug("MAYAViewModel", "Pending proposals loaded: ${_proposals.value.size}")
                } else {
                    val errorBody = response.errorBody()?.string()
                    ErrorHandlingUtil.handleApiError("MAYAViewModel", "loading pending proposals", errorBody)
                }
            } catch (e: Exception) {
                ErrorHandlingUtil.handleUnexpectedError("MAYAViewModel", "loading pending proposals", e)
            }
        }
    }

    fun loadCouncils() {
        if (!_isAuthenticated.value) return
        
        viewModelScope.launch {
            try {
                val response: Response<List<Council>> = api.getCouncils()
                if (response.isSuccessful) {
                    _councils.value = response.body() ?: emptyList()
                    ErrorHandlingUtil.logDebug("MAYAViewModel", "Councils loaded: ${_councils.value.size}")
                } else {
                    val errorBody = response.errorBody()?.string()
                    ErrorHandlingUtil.handleApiError("MAYAViewModel", "loading councils", errorBody)
                }
            } catch (e: Exception) {
                ErrorHandlingUtil.handleUnexpectedError("MAYAViewModel", "loading councils", e)
            }
        }
    }

    fun loadTreasury() {
        if (!_isAuthenticated.value) return
        
        viewModelScope.launch {
            try {
                val response: Response<Treasury> = api.getTreasury()
                if (response.isSuccessful) {
                    _treasury.value = response.body()
                    ErrorHandlingUtil.logDebug("MAYAViewModel", "Treasury loaded: ${_treasury.value}")
                } else {
                    val errorBody = response.errorBody()?.string()
                    ErrorHandlingUtil.handleApiError("MAYAViewModel", "loading treasury", errorBody)
                }
            } catch (e: Exception) {
                ErrorHandlingUtil.handleUnexpectedError("MAYAViewModel", "loading treasury", e)
            }
        }
    }

    fun loadTransactions() {
        if (!_isAuthenticated.value) return
        
        viewModelScope.launch {
            try {
                val response: Response<List<TreasuryTransaction>> = api.getTreasuryTransactions()
                if (response.isSuccessful) {
                    _transactions.value = response.body() ?: emptyList()
                    ErrorHandlingUtil.logDebug("MAYAViewModel", "Transactions loaded: ${_transactions.value.size}")
                } else {
                    val errorBody = response.errorBody()?.string()
                    ErrorHandlingUtil.handleApiError("MAYAViewModel", "loading transactions", errorBody)
                }
            } catch (e: Exception) {
                ErrorHandlingUtil.handleUnexpectedError("MAYAViewModel", "loading transactions", e)
            }
        }
    }

    fun approveProposal(proposalId: String) {
        if (!_isAuthenticated.value) return
        
        viewModelScope.launch {
            try {
                ErrorHandlingUtil.logDebug("MAYAViewModel", "Approving proposal: $proposalId")
                val response = api.sovereignApproveProposal(proposalId)
                if (response.isSuccessful) {
                    ErrorHandlingUtil.logInfo("MAYAViewModel", "Proposal $proposalId approved successfully on backend: ${response.body()}")
                    loadPendingProposals()
                } else {
                    val errorBody = response.errorBody()?.string()
                    ErrorHandlingUtil.handleApiError("MAYAViewModel", "approving proposal $proposalId", errorBody)
                }
            } catch (e: Exception) {
                ErrorHandlingUtil.handleUnexpectedError("MAYAViewModel", "approving proposal $proposalId", e)
            }
        }
    }

    fun rejectProposal(proposalId: String) {
        if (!_isAuthenticated.value) return
        
        viewModelScope.launch {
            try {
                ErrorHandlingUtil.logDebug("MAYAViewModel", "Rejecting proposal: $proposalId")
                val response = api.sovereignRejectProposal(proposalId)
                if (response.isSuccessful) {
                    ErrorHandlingUtil.logInfo("MAYAViewModel", "Proposal $proposalId rejected successfully on backend: ${response.body()}")
                    loadPendingProposals()
                } else {
                    val errorBody = response.errorBody()?.string()
                    ErrorHandlingUtil.handleApiError("MAYAViewModel", "rejecting proposal $proposalId", errorBody)
                }
            } catch (e: Exception) {
                ErrorHandlingUtil.handleUnexpectedError("MAYAViewModel", "rejecting proposal $proposalId", e)
            }
        }
    }

    fun requestFunding(councilId: String, purpose: String, costEth: Double, expectedRevenueBtc: Double) {
        if (!_isAuthenticated.value) return
        
        viewModelScope.launch {
            try {
                val request = FundingRequest(councilId, purpose, costEth, expectedRevenueBtc)
                val response = api.requestFunding(request)
                if (response.isSuccessful) {
                    ErrorHandlingUtil.logInfo("MAYAViewModel", "Funding request submitted successfully: ${response.body()}")
                    loadPendingProposals()
                } else {
                    val errorBody = response.errorBody()?.string()
                    ErrorHandlingUtil.handleApiError("MAYAViewModel", "submitting funding request", errorBody)
                }
            } catch (e: Exception) {
                ErrorHandlingUtil.handleUnexpectedError("MAYAViewModel", "submitting funding request", e)
            }
        }
    }

    private fun startLogPolling() {
        if (!_isAuthenticated.value) return
        
        viewModelScope.launch {
            while (_isAuthenticated.value) {
                try {
                    val response = api.getLogs()
                    if (response.isSuccessful) {
                        _logs.value = response.body()?.logs ?: emptyList()
                    } else {
                        val errorBody = response.errorBody()?.string()
                        ErrorHandlingUtil.handleApiError("MAYAViewModel", "getting logs", errorBody)
                    }
                } catch (e: Exception) {
                    ErrorHandlingUtil.handleUnexpectedError("MAYAViewModel", "getting logs", e)
                }
                delay(10000) // Poll every 10 seconds
            }
        }
    }

    fun connectWallet(address: String, chainId: String) {
        if (!_isAuthenticated.value) return
        
        viewModelScope.launch {
            try {
                ErrorHandlingUtil.logDebug("MAYAViewModel", "Connecting wallet: address=$address, chainId=$chainId")
                val response: Response<WalletSessionResponse> = api.connectWallet(WalletConnectRequest(address = address, chain_id = chainId))
                if (response.isSuccessful && response.body()?.status == "connected") {
                    val sessionResponse = response.body()!!
                    _walletSession.value = WalletSession(
                        connected = true,
                        address = sessionResponse.address,
                        chainId = chainId,
                        sessionId = sessionResponse.session_id,
                        balance_eth = _walletSession.value?.balance_eth
                    )
                    ErrorHandlingUtil.logInfo("MAYAViewModel", "Wallet connected: ${sessionResponse.address}, session: ${sessionResponse.session_id}")
                } else {
                    val errorBody = response.errorBody()?.string() ?: response.message()
                    ErrorHandlingUtil.handleApiError("MAYAViewModel", "connecting wallet", errorBody)
                    _walletSession.value = WalletSession(
                        connected = false,
                        address = "",
                        chainId = null,
                        sessionId = null,
                        balance_eth = null
                    )
                }
            } catch (e: Exception) {
                ErrorHandlingUtil.handleUnexpectedError("MAYAViewModel", "connecting wallet", e)
                _walletSession.value = WalletSession(
                    connected = false,
                    address = "",
                    chainId = null,
                    sessionId = null,
                    balance_eth = null
                )
            }
        }
    }

    fun connectWalletWithQR(onUri: (String) -> Unit, onError: (Throwable) -> Unit) {
        if (!_isAuthenticated.value) return
        
        try {
            walletConnectManager.connect(onUri, onError)
        } catch (e: Exception) {
            ErrorHandlingUtil.handleUnexpectedError("MAYAViewModel", "connecting wallet with QR", e)
            onError(e)
        }
    }

    fun isConnected(): Boolean {
        return _walletSession.value?.connected ?: false
    }

    fun startAgent(agentId: String) {
        if (!_isAuthenticated.value) return
        
        viewModelScope.launch {
            try {
                val response = api.startAgent()
                if (response.isSuccessful) {
                    ErrorHandlingUtil.logDebug("MAYAViewModel", "Agent $agentId (or generic agent) start command issued.")
                } else {
                    val errorBody = response.errorBody()?.string()
                    ErrorHandlingUtil.handleApiError("MAYAViewModel", "starting agent $agentId", errorBody)
                }
            } catch (e: Exception) {
                ErrorHandlingUtil.handleUnexpectedError("MAYAViewModel", "starting agent $agentId", e)
            }
        }
    }

    // Council integration methods
    fun reportCouncilData(councilId: String, metrics: Map<String, Any>) {
        if (!_isAuthenticated.value) return
        
        try {
            councilManager.reportCouncilData(councilId, metrics)
        } catch (e: Exception) {
            ErrorHandlingUtil.handleUnexpectedError("MAYAViewModel", "reporting council data for $councilId", e)
        }
    }

    fun submitCouncilProposal(councilId: String, proposalData: Map<String, Any>) {
        if (!_isAuthenticated.value) return
        
        try {
            councilManager.submitCouncilProposal(councilId, proposalData)
        } catch (e: Exception) {
            ErrorHandlingUtil.handleUnexpectedError("MAYAViewModel", "submitting council proposal for $councilId", e)
        }
    }

    fun loadCouncilOpportunities(councilId: String) {
        if (!_isAuthenticated.value) return
        
        viewModelScope.launch {
            try {
                val opportunities = councilManager.getCouncilOpportunities(councilId)
                // Update opportunities state if needed
            } catch (e: Exception) {
                ErrorHandlingUtil.handleUnexpectedError("MAYAViewModel", "loading council opportunities for $councilId", e)
            }
        }
    }
    
    // Proposal scoring methods
    fun getProposalROI(proposal: Proposal): Double {
        return ProposalScoringUtil.calculateROI(proposal)
    }
    
    fun getProposalScore(proposal: Proposal): Double {
        return ProposalScoringUtil.calculateProposalScore(proposal)
    }
    
    fun getRankedProposals(): List<Proposal> {
        return ProposalScoringUtil.rankProposals(_proposals.value)
    }
    
    // Testing mode methods
    fun enableTestingMode() {
        if (BuildConfig.DEBUG) {
            authManager.setMockTokenForTesting()
            _isAuthenticated.value = true
            MAYAApiService.setAuthToken("mock-testing-token")
        }
    }
    
    fun disableTestingMode() {
        if (BuildConfig.DEBUG) {
            authManager.clearAuthToken()
            MAYAApiService.clearAuthToken()
            _isAuthenticated.value = false
        }
    }
}