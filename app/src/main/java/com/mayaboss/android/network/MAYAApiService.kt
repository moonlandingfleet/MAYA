package com.mayaboss.android.network

import com.mayaboss.android.model.LogResponse
import com.mayaboss.android.model.Proposal
import com.mayaboss.android.model.Treasury
import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Query

interface MAYAApiService {
    @GET("proposals")
    fun getProposals(): Call<List<Proposal>>
    
    @POST("agents/run")
    fun startAgent(): Call<ResponseBody>
    
    @GET("agents/logs")
    fun getLogs(): Call<LogResponse>
    
    @GET("treasury")
    suspend fun getTreasury(): Treasury
    
    @POST("agents/decide")
    suspend fun agentDecide(@Query("agent_id") agentId: String, @Query("decision") decision: String): ResponseBody
    
    @GET("wallet/balance")
    fun getWalletBalance(@Query("address") address: String): Call<WalletBalanceResponse>
    
    @POST("wallet/session/connect")
    fun connectWallet(@Query("address") address: String, @Query("chain_id") chainId: String): Call<WalletSessionResponse>
    
    @POST("wallet/session/disconnect")
    fun disconnectWallet(@Query("session_id") sessionId: String): Call<WalletDisconnectResponse>
    
    @GET("wallet/session/{session_id}")
    fun getWalletSession(@Query("session_id") sessionId: String): Call<WalletSessionInfo>
    
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