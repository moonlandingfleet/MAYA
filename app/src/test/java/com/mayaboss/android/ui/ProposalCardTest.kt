package com.mayaboss.android.ui

import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createComposeRule
import com.mayaboss.android.model.Proposal
import org.junit.Rule
import org.junit.Test

class ProposalCardTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun testProposalCardDisplaysCorrectly() {
        val proposal = Proposal(
            id = "A-01",
            name = "Faucet-Harvester",
            roi_hrs = 0.3,
            risk = "low",
            cost = 0,
            locked = false
        )
        
        var approveCalled = false
        var rejectCalled = false
        
        composeTestRule.setContent {
            ProposalCard(
                proposal = proposal,
                onApprove = { approveCalled = true },
                onReject = { rejectCalled = true }
            )
        }
        
        // Verify that the proposal card content is displayed
        composeTestRule.onNodeWithText("Faucet-Harvester").assertIsDisplayed()
        composeTestRule.onNodeWithText("ROI: 0.3$/hr").assertIsDisplayed()
        composeTestRule.onNodeWithText("Risk: low").assertIsDisplayed()
        composeTestRule.onNodeWithText("Cost: 0 ETH").assertIsDisplayed()
        
        // Verify that the buttons are displayed
        composeTestRule.onNodeWithText("✅ Approve").assertIsDisplayed()
        composeTestRule.onNodeWithText("❌ Reject").assertIsDisplayed()
    }

    @Test
    fun testProposalCardApproveButton() {
        val proposal = Proposal(
            id = "A-01",
            name = "Faucet-Harvester",
            roi_hrs = 0.3,
            risk = "low",
            cost = 0,
            locked = false
        )
        
        var approveCalled = false
        var rejectCalled = false
        
        composeTestRule.setContent {
            ProposalCard(
                proposal = proposal,
                onApprove = { approveCalled = true },
                onReject = { rejectCalled = true }
            )
        }
        
        // Click the approve button
        composeTestRule.onNodeWithText("✅ Approve").performClick()
        
        // Verify that the approve callback was invoked
        assert(approveCalled)
        assert(!rejectCalled)
    }

    @Test
    fun testProposalCardRejectButton() {
        val proposal = Proposal(
            id = "A-01",
            name = "Faucet-Harvester",
            roi_hrs = 0.3,
            risk = "low",
            cost = 0,
            locked = false
        )
        
        var approveCalled = false
        var rejectCalled = false
        
        composeTestRule.setContent {
            ProposalCard(
                proposal = proposal,
                onApprove = { approveCalled = true },
                onReject = { rejectCalled = true }
            )
        }
        
        // Click the reject button
        composeTestRule.onNodeWithText("❌ Reject").performClick()
        
        // Verify that the reject callback was invoked
        assert(rejectCalled)
        assert(!approveCalled)
    }

    @Test
    fun testLockedProposalCard() {
        val proposal = Proposal(
            id = "A-13",
            name = "Liquidity-Miner",
            roi_hrs = 5.0,
            risk = "medium",
            cost = 50,
            locked = true
        )
        
        var approveCalled = false
        var rejectCalled = false
        
        composeTestRule.setContent {
            ProposalCard(
                proposal = proposal,
                onApprove = { approveCalled = true },
                onReject = { rejectCalled = true }
            )
        }
        
        // Verify that the lock icon is displayed
        // Note: We can't directly test for the icon, but we can test for the locked state effects
        
        // Verify that the approve button is disabled for locked proposals
        composeTestRule.onNodeWithText("✅ Approve").assertIsNotEnabled()
        
        // Verify that the reject button is still enabled
        composeTestRule.onNodeWithText("❌ Reject").assertIsEnabled()
    }
}