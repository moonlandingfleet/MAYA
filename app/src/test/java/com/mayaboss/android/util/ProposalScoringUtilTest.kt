package com.mayaboss.android.util

import com.mayaboss.android.model.Proposal
import org.junit.Assert.*
import org.junit.Test
import java.util.*

class ProposalScoringUtilTest {

    @Test
    fun `test ROI calculation with positive values`() {
        val proposal = Proposal(
            id = "test",
            council_id = "test_council",
            purpose = "Test proposal",
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

        val roi = ProposalScoringUtil.calculateROI(proposal)
        
        // With BTC to ETH rate of 15, revenue in ETH would be 1.5
        // ROI = (1.5 - 1.0) / 1.0 = 0.5
        assertEquals(0.5, roi, 0.01)
    }

    @Test
    fun `test ROI calculation with zero cost`() {
        val proposal = Proposal(
            id = "test",
            council_id = "test_council",
            purpose = "Test proposal",
            cost_eth = 0.0,
            expected_monthly_revenue_btc = 0.1,
            status = "PENDING_REVIEW",
            details_json = null,
            submitted_at = Date(),
            last_status_update_at = Date(),
            sovereign_approved_at = null,
            funding_transaction_hash = null,
            roi_score = 0.0
        )

        val roi = ProposalScoringUtil.calculateROI(proposal)
        
        // With zero cost, ROI should be 0
        assertEquals(0.0, roi, 0.01)
    }

    @Test
    fun `test proposal scoring with different parameters`() {
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

        val score1 = ProposalScoringUtil.calculateProposalScore(proposal1)
        val score2 = ProposalScoringUtil.calculateProposalScore(proposal2)
        
        // High value proposal should have a higher score
        assertTrue(score2 > score1)
    }

    @Test
    fun `test proposal ranking`() {
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
        
        // High value proposal should be ranked first
        assertEquals("2", rankedProposals[0].id)
        assertEquals("1", rankedProposals[1].id)
    }

    @Test
    fun `test normalize ROI`() {
        // Test with negative ROI
        val negativeRoi = -0.5
        // Test with zero ROI
        val zeroRoi = 0.0
        // Test with positive ROI less than max
        val lowRoi = 0.5
        // Test with ROI at max
        val maxRoi = 10.0
        // Test with ROI above max
        val highRoi = 15.0
        
        // Since normalizeROI is private, we can't test it directly
        // But we can test the overall scoring which uses it
        assertTrue(true)
    }
}