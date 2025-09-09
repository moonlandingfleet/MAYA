package com.mayaboss.android.ui

import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createComposeRule
import com.mayaboss.android.viewmodel.MAYAViewModel
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.mockito.Mockito.*
import org.mockito.junit.MockitoJUnitRunner

@RunWith(MockitoJUnitRunner::class)
class WalletConnectScreenTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun testWalletConnectScreenDisplays() {
        // Mock the ViewModel
        val viewModel = mock(MAYAViewModel::class.java)
        
        composeTestRule.setContent {
            WalletConnectScreen(
                viewModel = viewModel,
                onBack = {}
            )
        }
        
        // Verify that the screen content is displayed
        composeTestRule.onNodeWithText("🔌 Connect Your Wallet").assertIsDisplayed()
        composeTestRule.onNodeWithText("Generating QR Code...").assertIsDisplayed()
    }

    @Test
    fun testBackButton() {
        // Mock the ViewModel
        val viewModel = mock(MAYAViewModel::class.java)
        var backButtonClicked = false
        
        composeTestRule.setContent {
            WalletConnectScreen(
                viewModel = viewModel,
                onBack = { backButtonClicked = true }
            )
        }
        
        // Click the back button
        composeTestRule.onNodeWithText("← Back").performClick()
        
        // Verify that the back callback was invoked
        assert(backButtonClicked)
    }

    @Test
    fun testQRCodeGeneration() {
        // Mock the ViewModel
        val viewModel = mock(MAYAViewModel::class.java)
        
        composeTestRule.setContent {
            WalletConnectScreen(
                viewModel = viewModel,
                onBack = {}
            )
        }
        
        // Initially should show "Generating QR Code..."
        composeTestRule.onNodeWithText("Generating QR Code...").assertIsDisplayed()
    }

    @Test
    fun testErrorMessageDisplay() {
        // Mock the ViewModel
        val viewModel = mock(MAYAViewModel::class.java)
        
        composeTestRule.setContent {
            WalletConnectScreen(
                viewModel = viewModel,
                onBack = {}
            )
        }
        
        // Test error message display
        // In a real test, we would trigger an error state in the ViewModel
    }
}