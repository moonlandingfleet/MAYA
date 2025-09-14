package com.mayaboss.android.network

import android.content.Context
import android.content.SharedPreferences
import com.mayaboss.android.BuildConfig
import com.mayaboss.android.util.ErrorHandlingUtil
import timber.log.Timber

class AuthManager private constructor() {
    private lateinit var sharedPreferences: SharedPreferences

    companion object {
        private var INSTANCE: AuthManager? = null

        fun getInstance(): AuthManager {
            return INSTANCE ?: synchronized(this) {
                INSTANCE ?: AuthManager().also { INSTANCE = it }
            }
        }
    }

    fun initialize(context: Context) {
        try {
            sharedPreferences = context.getSharedPreferences("maya_auth_prefs", Context.MODE_PRIVATE)
        } catch (e: Exception) {
            ErrorHandlingUtil.handleUnexpectedError("AuthManager", "initializing", e)
        }
    }

    fun saveAuthToken(token: String) {
        try {
            sharedPreferences.edit()
                .putString("auth_token", token)
                .apply()
            ErrorHandlingUtil.logDebug("AuthManager", "Auth token saved")
        } catch (e: Exception) {
            ErrorHandlingUtil.handleUnexpectedError("AuthManager", "saving auth token", e)
        }
    }

    fun getAuthToken(): String? {
        return try {
            sharedPreferences.getString("auth_token", null)
        } catch (e: Exception) {
            ErrorHandlingUtil.handleUnexpectedError("AuthManager", "getting auth token", e)
            null
        }
    }

    fun clearAuthToken() {
        try {
            sharedPreferences.edit()
                .remove("auth_token")
                .apply()
            ErrorHandlingUtil.logDebug("AuthManager", "Auth token cleared")
        } catch (e: Exception) {
            ErrorHandlingUtil.handleUnexpectedError("AuthManager", "clearing auth token", e)
        }
    }

    fun isAuthenticated(): Boolean {
        return try {
            // In testing mode, bypass authentication
            if (BuildConfig.DEBUG && BuildConfig.FLAVOR == "testing") {
                return true
            }
            !getAuthToken().isNullOrEmpty()
        } catch (e: Exception) {
            ErrorHandlingUtil.handleUnexpectedError("AuthManager", "checking authentication status", e)
            false
        }
    }
    
    /**
     * Set a mock token for testing mode
     */
    fun setMockTokenForTesting() {
        if (BuildConfig.DEBUG && BuildConfig.FLAVOR == "testing") {
            saveAuthToken("mock-testing-token")
        }
    }
}