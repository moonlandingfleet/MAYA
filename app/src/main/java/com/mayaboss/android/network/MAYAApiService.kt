package com.mayaboss.android.network

import com.mayaboss.android.model.*
import okhttp3.OkHttpClient
import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Query

// Data models for API requests
data class ProposalDecisionRequest(val proposal_id: String)
data class FundingRequest(val council_id: String, val purpose: String, val cost_eth: Double, val expected_monthly_revenue_btc: Double)
data class LoginRequest(val username: String, val password: String)
data class LoginResponse(val token: String, val user_id: String)

interface MAYAApiService {
    // Authentication
    @POST("auth/login")
    suspend fun login(@Body request: LoginRequest): Response<LoginResponse>

    @POST("auth/logout")
    suspend fun logout(): Response<ResponseBody>

    // Proposals
    @GET("proposals/pending")
    suspend fun getPendingProposals(): Response<List<Proposal>>

    @POST("proposals/approve")
    suspend fun approveProposal(@Body request: ProposalDecisionRequest): Response<Proposal>

    @POST("proposals/reject")
    suspend fun rejectProposal(@Body request: ProposalDecisionRequest): Response<Proposal>

    // Council funding requests
    @POST("council/{council_id}/request_funding")
    suspend fun requestFunding(@Body request: FundingRequest): Response<Proposal>

    // Sovereign review
    @GET("proposals/sovereign_review")
    suspend fun getSovereignReviewProposals(): Response<List<Proposal>>

    @POST("proposals/{proposal_id}/sovereign_approve")
    suspend fun sovereignApproveProposal(@Query("proposal_id") proposalId: String): Response<Proposal>

    @POST("proposals/{proposal_id}/sovereign_reject")
    suspend fun sovereignRejectProposal(@Query("proposal_id") proposalId: String): Response<Proposal>

    @POST("proposals/{proposal_id}/funding_confirmed")
    suspend fun confirmFunding(@Query("proposal_id") proposalId: String): Response<Proposal>

    // Agents
    @POST("agents/run")
    suspend fun startAgent(): Response<ResponseBody>

    @GET("agents/logs")
    suspend fun getLogs(): Response<LogResponse>

    // Treasury
    @GET("treasury")
    suspend fun getTreasury(): Response<Treasury>

    @GET("treasury/transactions")
    suspend fun getTreasuryTransactions(): Response<List<TreasuryTransaction>>

    // Councils
    @GET("councils")
    suspend fun getCouncils(): Response<List<Council>>

    @GET("councils/{council_id}/opportunities")
    suspend fun getCouncilOpportunities(@Query("council_id") councilId: String): Response<List<CouncilOpportunity>>

    // Wallet
    @GET("wallet/balance")
    suspend fun getWalletBalance(@Query("address") address: String): Response<WalletBalanceResponse>

    @POST("wallet/session/connect")
    suspend fun connectWallet(@Body request: WalletConnectRequest): Response<WalletSessionResponse>

    @POST("wallet/session/disconnect")
    suspend fun disconnectWallet(@Query("session_id") sessionId: String): Response<WalletDisconnectResponse>

    @GET("wallet/session/{session_id}")
    suspend fun getWalletSession(@Query("session_id") sessionId: String): Response<WalletSessionInfo>

    companion object {
        private lateinit var authInterceptor: AuthInterceptor

        fun create(baseUrl: String): MAYAApiService {
            authInterceptor = AuthInterceptor()
            
            val okHttpClient = OkHttpClient.Builder()
                .addInterceptor(authInterceptor)
                .build()

            val retrofit = Retrofit.Builder()
                .baseUrl(baseUrl)
                .client(okHttpClient)
                .addConverterFactory(GsonConverterFactory.create())
                .build()
            return retrofit.create(MAYAApiService::class.java)
        }

        fun setAuthToken(token: String) {
            if (::authInterceptor.isInitialized) {
                authInterceptor.setAuthToken(token)
            }
        }

        fun clearAuthToken() {
            if (::authInterceptor.isInitialized) {
                authInterceptor.clearAuthToken()
            }
        }
    }
}

// Data models for API requests and responses
data class LogResponse(val logs: List<String>?)

// Wallet related data models
data class WalletConnectRequest(val address: String, val chain_id: String)

data class WalletBalanceResponse(
    val address: String,
    val balance_eth: Double,
    val last_updated: String
)

data class WalletSessionResponse(
    val status: String,
    val session_id: String,
    val address: String
)

data class WalletDisconnectResponse(
    val status: String
)

data class WalletSessionInfo(
    val address: String,
    val chain_id: String,
    val connected_at: String
)