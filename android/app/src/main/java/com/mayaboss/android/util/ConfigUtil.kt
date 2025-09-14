package com.mayaboss.android.util

import com.mayaboss.android.BuildConfig

object ConfigUtil {
    /**
     * Check if the app is running in debug mode
     */
    fun isDebugMode(): Boolean {
        return BuildConfig.DEBUG
    }
    
    /**
     * Check if testing mode is enabled
     */
    fun isTestingMode(): Boolean {
        return BuildConfig.DEBUG && BuildConfig.BUILD_TYPE == "debug"
    }
    
    /**
     * Get the API base URL
     */
    fun getApiBaseUrl(): String {
        return if (isDebugMode()) {
            "http://192.168.0.100:8000/"
        } else {
            "https://api.mayaboss.com/"
        }
    }
    
    /**
     * Check if authentication should be bypassed in testing mode
     */
    fun shouldBypassAuthentication(): Boolean {
        return isTestingMode() && BuildConfig.FLAVOR == "testing"
    }
}