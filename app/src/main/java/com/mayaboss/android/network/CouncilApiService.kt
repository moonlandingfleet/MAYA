package com.mayaboss.android.network

import com.mayaboss.android.model.Council
import com.mayaboss.android.model.CouncilOpportunity
import okhttp3.ResponseBody
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Path
import retrofit2.http.Query

data class CouncilDataReport(
    val council_id: String,
    val metrics: Map<String, Any>,
    val timestamp: String
)

data class CouncilProposal(
    val council_id: String,
    val proposal_data: Map<String, Any>
)

interface CouncilApiService {
    // Council data reporting
    @POST("councils/{council_id}/report")
    suspend fun reportCouncilData(
        @Path("council_id") councilId: String,
        @Body report: CouncilDataReport
    ): Response<ResponseBody>

    // Council proposal submission
    @POST("councils/{council_id}/proposal")
    suspend fun submitCouncilProposal(
        @Path("council_id") councilId: String,
        @Body proposal: CouncilProposal
    ): Response<ResponseBody>

    // Get council information
    @GET("councils/{council_id}")
    suspend fun getCouncilInfo(
        @Path("council_id") councilId: String
    ): Response<Council>

    // Get council opportunities
    @GET("councils/{council_id}/opportunities")
    suspend fun getCouncilOpportunities(
        @Path("council_id") councilId: String
    ): Response<List<CouncilOpportunity>>

    companion object {
        fun create(baseUrl: String): CouncilApiService {
            return MAYAApiService.create(baseUrl) as CouncilApiService
        }
    }
}