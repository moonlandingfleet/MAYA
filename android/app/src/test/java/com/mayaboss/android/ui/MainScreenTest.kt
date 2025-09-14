package com.mayaboss.android.ui

import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createComposeRule
import com.mayaboss.android.model.Proposal
import com.mayaboss.android.model.Treasury
import com.mayaboss.android.model.WalletSession
import com.mayaboss.android.viewmodel.MAYAViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.mockito.Mockito.*
import org.mockito.junit.MockitoJUnitRunner

@RunWith(MockitoJUnitRunner::class)
class MainScreenTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun testMainScreenDisplays() {
        // Mock the ViewModel with disconnected wallet state
        val viewModel = mock(MAYAViewModel::class.java)
        
        // Mock the state flows
        val proposalsFlow = MutableStateFlow<List<Proposal>>(emptyList())
        val logsFlow = MutableStateFlow<List<String>>(emptyList())
        val treasuryFlow = MutableStateFlow<Treasury?>(null)
        val totalProfitFlow = MutableStateFlow(0.0)
        val showDecisionDialogFlow = MutableStateFlow(false)
        val walletSessionFlow = MutableStateFlow(WalletSession(false, null, null, null))
        val walletBalanceFlow = MutableStateFlow(0.0)
        
        `when`(viewModel.proposals).thenReturn(proposalsFlow)
        `when`(viewModel.logs).thenReturn(logsFlow)
        `when`(viewModel.treasury).thenReturn(treasuryFlow)
        `when`(viewModel.totalProfit).thenReturn(totalProfitFlow)
        `when`(viewModel.showDecisionDialog).thenReturn(showDecisionDialogFlow)
        `when`(viewModel.walletSession).thenReturn(walletSessionFlow)
        `when`(viewModel.walletBalance).thenReturn(walletBalanceFlow)
        
        composeTestRule.setContent {
            MainScreen(
                viewModel = viewModel,
                onNavigateToWalletConnect = {}
            )
        }
        
        // Verify that the main screen content is displayed
        composeTestRule.onNodeWithText("MAYA v0.2 — One mind, many hands.").assertIsDisplayed()
        composeTestRule.onNodeWithText("🔌 Connect Wallet").assertIsDisplayed()
    }

    @Test
    fun testConnectWalletButton() {
        // Mock the ViewModel with disconnected wallet state
        val viewModel = mock(MAYAViewModel::class.java)
        
        // Mock the state flows
        val proposalsFlow = MutableStateFlow<List<Proposal>>(emptyList())
        val logsFlow = MutableStateFlow<List<String>>(emptyList())
        val treasuryFlow = MutableStateFlow<Treasury?>(null)
        val totalProfitFlow = MutableStateFlow(0.0)
        val showDecisionDialogFlow = MutableStateFlow(false)
        val walletSessionFlow = MutableStateFlow(WalletSession(false, null, null, null))
        val walletBalanceFlow = MutableStateFlow(0.0)
        
        `when`(viewModel.proposals).thenReturn(proposalsFlow)
        `when`(viewModel.logs).thenReturn(logsFlow)
        `when`(viewModel.treasury).thenReturn(treasuryFlow)
        `when`(viewModel.totalProfit).thenReturn(totalProfitFlow)
        `when`(viewModel.showDecisionDialog).thenReturn(showDecisionDialogFlow)
        `when`(viewModel.walletSession).thenReturn(walletSessionFlow)
        `when`(viewModel.walletBalance).thenReturn(walletBalanceFlow)
        
        var navigateToWalletConnectCalled = false
        
        composeTestRule.setContent {
            MainScreen(
                viewModel = viewModel,
                onNavigateToWalletConnect = { navigateToWalletConnectCalled = true }
            )
        }
        
        // Click the connect wallet button
        composeTestRule.onNodeWithText("🔌 Connect Wallet").performClick()
        
        // Verify that the navigation callback was invoked
        assert(navigateToWalletConnectCalled)
    }

    @Test
    fun testWalletConnectedState() {
        // Mock the ViewModel with connected wallet state
        val viewModel = mock(MAYAViewModel::class.java)
        
        // Mock the state flows with connected wallet
        val proposalsFlow = MutableStateFlow<List<Proposal>>(emptyList())
        val logsFlow = MutableStateFlow<List<String>>(emptyList())
        val treasuryFlow = MutableStateFlow<Treasury?>(null)
        val totalProfitFlow = MutableStateFlow(0.0)
        val showDecisionDialogFlow = MutableStateFlow(false)
        val walletSessionFlow = MutableStateFlow(
            WalletSession(
                connected = true,
                address = "0x1234567890123456789012345678901234567890",
                chainId = "eip155:1",
                topic = "topic123"
            )
        )
        val walletBalanceFlow = MutableStateFlow(0.0015)
        
        `when`(viewModel.proposals).thenReturn(proposalsFlow)
        `when`(viewModel.logs).thenReturn(logsFlow)
        `when`(viewModel.treasury).thenReturn(treasuryFlow)
        `when`(viewModel.totalProfit).thenReturn(totalProfitFlow)
        `when`(viewModel.showDecisionDialog).thenReturn(showDecisionDialogFlow)
        `when`(viewModel.walletSession).thenReturn(walletSessionFlow)
        `when`(viewModel.walletBalance).thenReturn(walletBalanceFlow)
        
        composeTestRule.setContent {
            MainScreen(
                viewModel = viewModel,
                onNavigateToWalletConnect = {}
            )
        }
        
        // Verify that the wallet connected state is displayed
        composeTestRule.onNodeWithText("✅ Wallet Connected").assertIsDisplayed()
        composeTestRule.onNodeWithText("Address: 0x1234567890...").assertIsDisplayed()
        composeTestRule.onNodeWithText("Balance: 0.0015 ETH").assertIsDisplayed()
    }

    @Test
    fun testActiveProposalsSection() {
        // Mock the ViewModel
        val viewModel = mock(MAYAViewModel::class.java)
        
        // Mock the state flows
        val proposalsFlow = MutableStateFlow<List<Proposal>>(emptyList())
        val logsFlow = MutableStateFlow<List<String>>(emptyList())
        val treasuryFlow = MutableStateFlow<Treasury?>(null)
        val totalProfitFlow = MutableStateFlow(0.0)
        val showDecisionDialogFlow = MutableStateFlow(false)
        val walletSessionFlow = MutableStateFlow(WalletSession(false, null, null, null))
        val walletBalanceFlow = MutableStateFlow(0.0)
        
        `when`(viewModel.proposals).thenReturn(proposalsFlow)
        `when`(viewModel.logs).thenReturn(logsFlow)
        `when`(viewModel.treasury).thenReturn(treasuryFlow)
        `when`(viewModel.totalProfit).thenReturn(totalProfitFlow)
        `when`(viewModel.showDecisionDialog).thenReturn(showDecisionDialogFlow)
        `when`(viewModel.walletSession).thenReturn(walletSessionFlow)
        `when`(viewModel.walletBalance).thenReturn(walletBalanceFlow)
        
        composeTestRule.setContent {
            MainScreen(
                viewModel = viewModel,
                onNavigateToWalletConnect = {}
            )
        }
        
        // Verify that the active proposals section is displayed
        composeTestRule.onNodeWithText("Active Proposals").assertIsDisplayed()
    }

    @Test
    fun testAgentLogsSection() {
        // Mock the ViewModel
        val viewModel = mock(MAYAViewModel::class.java)
        
        // Mock the state flows
        val proposalsFlow = MutableStateFlow<List<Proposal>>(emptyList())
        val logsFlow = MutableStateFlow<List<String>>(emptyList())
        val treasuryFlow = MutableStateFlow<Treasury?>(null)
        val totalProfitFlow = MutableStateFlow(0.0)
        val showDecisionDialogFlow = MutableStateFlow(false)
        val walletSessionFlow = MutableStateFlow(WalletSession(false, null, null, null))
        val walletBalanceFlow = MutableStateFlow(0.0)
        
        `when`(viewModel.proposals).thenReturn(proposalsFlow)
        `when`(viewModel.logs).thenReturn(logsFlow)
        `when`(viewModel.treasury).thenReturn(treasuryFlow)
        `when`(viewModel.totalProfit).thenReturn(totalProfitFlow)
        `when`(viewModel.showDecisionDialog).thenReturn(showDecisionDialogFlow)
        `when`(viewModel.walletSession).thenReturn(walletSessionFlow)
        `when`(viewModel.walletBalance).thenReturn(walletBalanceFlow)
        
        composeTestRule.setContent {
            MainScreen(
                viewModel = viewModel,
                onNavigateToWalletConnect = {}
            )
        }
        
        // Verify that the agent logs section is displayed
        composeTestRule.onNodeWithText("Agent Logs (Last 10)").assertIsDisplayed()
    }
}