package com.mayaboss.android.viewmodel

import android.app.Application
import androidx.arch.core.executor.testing.InstantTaskExecutorRule
import androidx.lifecycle.Observer
import com.mayaboss.android.model.Proposal
import com.mayaboss.android.util.ProposalScoringUtil
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.StandardTestDispatcher
import kotlinx.coroutines.test.resetMain
import kotlinx.coroutines.test.setMain
import org.junit.After
import org.junit.Before
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.mockito.Mock
import org.mockito.Mockito.*
import org.mockito.junit.MockitoJUnitRunner
import java.util.*

@ExperimentalCoroutinesApi
@RunWith(MockitoJUnitRunner::class)
class MAYAViewModelTest {

    @get:Rule
    val instantExecutorRule = InstantTaskExecutorRule()

    private lateinit var viewModel: MAYAViewModel

    @Mock
    private lateinit var application: Application

    private val testDispatcher = StandardTestDispatcher()

    @Before
    fun setUp() {
        Dispatchers.setMain(testDispatcher)
        viewModel = MAYAViewModel(application)
    }

    @After
    fun tearDown() {
        Dispatchers.resetMain()
    }

    @Test
    fun `test proposal scoring`() {
        // Create test proposals
        val proposal1 = Proposal(
            id = "1",
            council_id = "council1",
            purpose = "Test proposal 1",
            cost_eth = 1.0,
            expected_monthly_revenue_btc = 0.1,
            status = "PENDING_REVIEW",
            details_json = null,
            submitted_at = Date(),
            last_status_update_at = Date(),
            sovereign_approved_at = null,
            funding_transaction_hash = null,
            roi_score = 0.0
        )

        val proposal2 = Proposal(
            id = "2",
            council_id = "council2",
            purpose = "Test proposal 2",
            cost_eth = 2.0,
            expected_monthly_revenue_btc = 0.2,
            status = "PENDING_REVIEW",
            details_json = null,
            submitted_at = Date(),
            last_status_update_at = Date(),
            sovereign_approved_at = null,
            funding_transaction_hash = null,
            roi_score = 0.0
        )

        // Test ROI calculation
        val roi1 = ProposalScoringUtil.calculateROI(proposal1)
        val roi2 = ProposalScoringUtil.calculateROI(proposal2)

        // Test proposal scoring
        val score1 = ProposalScoringUtil.calculateProposalScore(proposal1)
        val score2 = ProposalScoringUtil.calculateProposalScore(proposal2)

        // Verify that scores are calculated
        assert(roi1 >= 0.0)
        assert(roi2 >= 0.0)
        assert(score1 >= 0.0)
        assert(score2 >= 0.0)
    }

    @Test
    fun `test proposal ranking`() {
        // Create test proposals with different scores
        val proposal1 = Proposal(
            id = "1",
            council_id = "council1",
            purpose = "Low value proposal",
            cost_eth = 10.0,
            expected_monthly_revenue_btc = 0.01,
            status = "PENDING_REVIEW",
            details_json = null,
            submitted_at = Date(),
            last_status_update_at = Date(),
            sovereign_approved_at = null,
            funding_transaction_hash = null,
            roi_score = 0.0
        )

        val proposal2 = Proposal(
            id = "2",
            council_id = "council2",
            purpose = "High value proposal",
            cost_eth = 1.0,
            expected_monthly_revenue_btc = 1.0,
            status = "PENDING_REVIEW",
            details_json = null,
            submitted_at = Date(),
            last_status_update_at = Date(),
            sovereign_approved_at = null,
            funding_transaction_hash = null,
            roi_score = 0.0
        )

        val proposals = listOf(proposal1, proposal2)
        val rankedProposals = ProposalScoringUtil.rankProposals(proposals)

        // Verify that the higher value proposal is ranked first
        assert(rankedProposals[0].id == "2")
        assert(rankedProposals[1].id == "1")
    }
}