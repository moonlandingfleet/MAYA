package com.mayaboss.android.util

import timber.log.Timber

object ErrorHandlingUtil {
    
    /**
     * Log an error with context
     */
    fun logError(tag: String, message: String, throwable: Throwable? = null) {
        if (throwable != null) {
            Timber.tag(tag).e(throwable, message)
        } else {
            Timber.tag(tag).e(message)
        }
    }
    
    /**
     * Log a warning with context
     */
    fun logWarning(tag: String, message: String) {
        Timber.tag(tag).w(message)
    }
    
    /**
     * Log an info message with context
     */
    fun logInfo(tag: String, message: String) {
        Timber.tag(tag).i(message)
    }
    
    /**
     * Log a debug message with context
     */
    fun logDebug(tag: String, message: String) {
        Timber.tag(tag).d(message)
    }
    
    /**
     * Handle API errors consistently
     */
    fun handleApiError(tag: String, operation: String, errorBody: String?, throwable: Throwable? = null) {
        val errorMessage = when {
            errorBody != null -> "API error during $operation: $errorBody"
            throwable != null -> "Exception during $operation: ${throwable.message}"
            else -> "Unknown error during $operation"
        }
        
        logError(tag, errorMessage, throwable)
    }
    
    /**
     * Handle network errors
     */
    fun handleNetworkError(tag: String, operation: String, throwable: Throwable) {
        val errorMessage = "Network error during $operation: ${throwable.message}"
        logError(tag, errorMessage, throwable)
    }
    
    /**
     * Handle unexpected errors
     */
    fun handleUnexpectedError(tag: String, operation: String, throwable: Throwable) {
        val errorMessage = "Unexpected error during $operation: ${throwable.message}"
        logError(tag, errorMessage, throwable)
    }
    
    /**
     * Create a user-friendly error message
     */
    fun createUserFriendlyErrorMessage(operation: String): String {
        return "An error occurred while $operation. Please try again later."
    }
}