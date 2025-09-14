package com.mayaboss.android.network

import com.mayaboss.android.model.Council
import com.mayaboss.android.model.CouncilOpportunity
import com.mayaboss.android.util.ErrorHandlingUtil
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import timber.log.Timber
import java.util.Date

class CouncilManager private constructor() {
    companion object {
        private var INSTANCE: CouncilManager? = null

        fun getInstance(): CouncilManager {
            return INSTANCE ?: synchronized(this) {
                INSTANCE ?: CouncilManager().also { INSTANCE = it }
            }
        }
    }

    private val api: CouncilApiService = CouncilApiService.create("http://192.168.0.100:8000/")

    private val _councils = MutableStateFlow<Map<String, Council>>(emptyMap())
    val councils: StateFlow<Map<String, Council>> = _councils

    private val _opportunities = MutableStateFlow<Map<String, List<CouncilOpportunity>>>(emptyMap())
    val opportunities: StateFlow<Map<String, List<CouncilOpportunity>>> = _opportunities

    fun reportCouncilData(councilId: String, metrics: Map<String, Any>) {
        try {
            ErrorHandlingUtil.logDebug("CouncilManager", "Reporting data for council: $councilId")
            
            // Simulate API call
            // api.reportCouncilData(councilId, CouncilDataReport(councilId, metrics, Date().toString()))
        } catch (e: Exception) {
            ErrorHandlingUtil.handleUnexpectedError("CouncilManager", "reporting council data for $councilId", e)
        }
    }

    fun submitCouncilProposal(councilId: String, proposalData: Map<String, Any>) {
        try {
            ErrorHandlingUtil.logDebug("CouncilManager", "Submitting proposal for council: $councilId")
            
            // Simulate API call
            // api.submitCouncilProposal(councilId, CouncilProposal(councilId, proposalData))
        } catch (e: Exception) {
            ErrorHandlingUtil.handleUnexpectedError("CouncilManager", "submitting council proposal for $councilId", e)
        }
    }

    suspend fun getCouncilInfo(councilId: String): Council? {
        return try {
            val response = api.getCouncilInfo(councilId)
            if (response.isSuccessful) {
                response.body()
            } else {
                val errorBody = response.errorBody()?.string()
                ErrorHandlingUtil.handleApiError("CouncilManager", "getting council info for $councilId", errorBody)
                null
            }
        } catch (e: Exception) {
            ErrorHandlingUtil.handleUnexpectedError("CouncilManager", "getting council info for $councilId", e)
            null
        }
    }

    suspend fun getCouncilOpportunities(councilId: String): List<CouncilOpportunity> {
        return try {
            val response = api.getCouncilOpportunities(councilId)
            if (response.isSuccessful) {
                response.body() ?: emptyList()
            } else {
                val errorBody = response.errorBody()?.string()
                ErrorHandlingUtil.handleApiError("CouncilManager", "getting council opportunities for $councilId", errorBody)
                emptyList()
            }
        } catch (e: Exception) {
            ErrorHandlingUtil.handleUnexpectedError("CouncilManager", "getting council opportunities for $councilId", e)
            emptyList()
        }
    }

    fun updateCouncil(council: Council) {
        try {
            val currentCouncils = _councils.value.toMutableMap()
            currentCouncils[council.id] = council
            _councils.value = currentCouncils
        } catch (e: Exception) {
            ErrorHandlingUtil.handleUnexpectedError("CouncilManager", "updating council ${council.id}", e)
        }
    }

    fun updateOpportunities(councilId: String, councilOpportunities: List<CouncilOpportunity>) {
        try {
            val currentOpportunities = _opportunities.value.toMutableMap()
            currentOpportunities[councilId] = councilOpportunities
            _opportunities.value = currentOpportunities
        } catch (e: Exception) {
            ErrorHandlingUtil.handleUnexpectedError("CouncilManager", "updating opportunities for council $councilId", e)
        }
    }
}