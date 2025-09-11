package com.mayaboss.android.network

import com.mayaboss.android.model.LogResponse
import com.mayaboss.android.model.Proposal
import com.mayaboss.android.model.Treasury
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

interface MAYAApiService {
    // Proposals
    @GET("proposals/pending")
    suspend fun getPendingProposals(): Response<List<Proposal>>

    @POST("proposals/approve")
    suspend fun approveProposal(@Body request: ProposalDecisionRequest): Response<Proposal>

    @POST("proposals/reject")
    suspend fun rejectProposal(@Body request: ProposalDecisionRequest): Response<Proposal>

    // Agents
    @POST("agents/run")
    suspend fun startAgent(): Response<ResponseBody>

    @GET("agents/logs")
    suspend fun getLogs(): Response<LogResponse>

    // Treasury
    @GET("treasury")
    suspend fun getTreasury(): Response<Treasury>

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
        fun create(baseUrl: String): MAYAApiService {
            val retrofit = Retrofit.Builder()
                .baseUrl(baseUrl)
                .addConverterFactory(GsonConverterFactory.create())
                .build()
            return retrofit.create(MAYAApiService::class.java)
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