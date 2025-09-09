package com.mayaboss.android.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.mayaboss.android.model.LogResponse
import com.mayaboss.android.model.Proposal
import com.mayaboss.android.network.MAYAApiService
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class MAYAViewModel(private val api: MAYAApiService) : ViewModel() {

    private val _proposals = MutableStateFlow<List<Proposal>>(emptyList())
    val proposals: StateFlow<List<Proposal>> = _proposals.asStateFlow()

    private val _logs = MutableStateFlow<List<String>>(emptyList())
    val logs: StateFlow<List<String>> = _logs.asStateFlow()

    init {
        loadProposals()
        startLogPolling()
    }

    private fun loadProposals() {
        viewModelScope.launch {
            try {
                val response = api.getProposals().execute()
                if (response.isSuccessful) {
                    _proposals.value = response.body() ?: emptyList()
                }
            } catch (e: Exception) {
                // Handle error
            }
        }
    }

    fun startAgent(agentId: String) {
        viewModelScope.launch {
            try {
                val response = api.startAgent().execute()
                if (response.isSuccessful) {
                    // Handle success
                }
            } catch (e: Exception) {
                // Handle error
            }
        }
    

    private fun startLogPolling() {
        viewModelScope.launch {
            while (true) {
                try {
                    val response = api.getLogs().execute()
                    if (response.isSuccessful) {
                        val logResponse = response.body()
                        _logs.value = logResponse?.logs ?: emptyList()
                    }
                } catch (e: Exception) {
                    // Silent fail
                }
                delay(10000) // 10s
            }
        }
    }
}