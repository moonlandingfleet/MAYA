package com.mayaboss.android.network

import okhttp3.Interceptor
import okhttp3.Response
import timber.log.Timber

class AuthInterceptor : Interceptor {
    private var authToken: String? = null

    fun setAuthToken(token: String) {
        authToken = token
    }

    fun clearAuthToken() {
        authToken = null
    }

    override fun intercept(chain: Interceptor.Chain): Response {
        val originalRequest = chain.request()
        val builder = originalRequest.newBuilder()

        authToken?.let { token ->
            if (token.isNotEmpty()) {
                builder.addHeader("Authorization", "Bearer $token")
                Timber.d("Added auth token to request: ${originalRequest.url().toString()}")
            }
        }

        val newRequest = builder.build()
        return chain.proceed(newRequest)
    }
}