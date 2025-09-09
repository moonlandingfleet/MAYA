package com.mayaboss.android.network

import com.mayaboss.android.model.LogResponse
import com.mayaboss.android.model.Proposal
import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import retrofit2.http.POST

interface MAYAApiService {
    @GET("proposals")
    fun getProposals(): Call<List<Proposal>>
    
    @POST("agents/run")
    fun startAgent(): Call<ResponseBody>
    
    @GET("agents/logs")
    fun getLogs(): Call<LogResponse>
    
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