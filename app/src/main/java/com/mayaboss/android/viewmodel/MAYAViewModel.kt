package com.mayaboss.android.viewmodel

import android.app.Application
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.mayaboss.android.model.LogResponse
import com.mayaboss.android.model.Proposal
import com.mayaboss.android.model.Treasury
import com.mayaboss.android.model.WalletSession
import com.mayaboss.android.network.MAYAApiService
import com.mayaboss.android.network.WalletBalanceResponse
import com.mayaboss.android.network.WalletConnectManager
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class MAYAViewModel(private val api: MAYAApiService, private val application: Application) : ViewModel() {

    private val _proposals = MutableStateFlow<List<Proposal>>(emptyList())
    val proposals: StateFlow<List<Proposal>> = _proposals

    private val _logs = MutableStateFlow<List<String>>(emptyList())
    val logs: StateFlow<List<String>> = _logs

    init {
        loadProposals()
        startLogPolling()
    }

    private fun loadProposals() {
        viewModelScope.launch {
            try {
                val response = api.getProposals()
                if (response.isSuccessful) {
                    _proposals.value = response.body() ?: emptyList()
                } else {
                    Log.e("MAYAViewModel", "Failed to load proposals: ${response.errorBody()?.string()}")
                }
            } catch (e: Exception) {
                Log.e("MAYAViewModel", "Error loading proposals: ${e.message}")
            }
        }
    }

    private fun startLogPolling() {
        viewModelScope.launch {
            while (true) {
                try {
                    val response = api.getLogs()
                    if (response.isSuccessful) {
                        val logResponse = response.body()
                        _logs.value = logResponse?.logs ?: emptyList()
                    } else {
                        Log.e("MAYAViewModel", "Failed to get logs: ${response.errorBody()?.string()}")
                    }
                } catch (e: Exception) {
                    Log.e("MAYAViewModel", "Error getting logs: ${e.message}")
                }
                delay(10000) // Poll every 10 seconds
            }
        }
    }
}