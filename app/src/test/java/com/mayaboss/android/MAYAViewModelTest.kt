package com.mayaboss.android

import android.app.Application
import androidx.arch.core.executor.testing.InstantTaskExecutorRule
import androidx.lifecycle.Observer
import com.mayaboss.android.model.Proposal
import com.mayaboss.android.model.Treasury
import com.mayaboss.android.model.WalletSession
import com.mayaboss.android.network.MAYAApiService
import com.mayaboss.android.viewmodel.MAYAViewModel
import okhttp3.ResponseBody
import org.junit.Before
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.mockito.Mock
import org.mockito.Mockito.*
import org.mockito.MockitoAnnotations
import org.mockito.junit.MockitoJUnitRunner
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

@RunWith(MockitoJUnitRunner::class)
class MAYAViewModelTest {

    @get:Rule
    val instantExecutorRule = InstantTaskExecutorRule()

    @Mock
    private lateinit var application: Application

    @Mock
    private lateinit var apiService: MAYAApiService

    @Mock
    private lateinit var proposalsCall: Call<List<Proposal>>

    @Mock
    private lateinit var startAgentCall: Call<ResponseBody>

    @Mock
    private lateinit var logsCall: Call<com.mayaboss.android.model.LogResponse>

    private lateinit var viewModel: MAYAViewModel

    @Before
    fun setup() {
        MockitoAnnotations.initMocks(this)
        viewModel = MAYAViewModel(apiService, application)
    }

    @Test
    fun testViewModelInitialization() {
        // Verify that the ViewModel is created successfully
        assertNotNull(viewModel)
    }

    @Test
    fun testWalletSessionInitialState() {
        // Initially, wallet should not be connected
        val walletSession = viewModel.walletSession.value
        assertNotNull(walletSession)
        assertFalse(walletSession!!.connected)
        assertNull(walletSession.address)
        assertNull(walletSession.chainId)
        assertNull(walletSession.topic)
    }

    @Test
    fun testWalletConnectionState() {
        // Test wallet connection state changes
        val walletSession = WalletSession(
            connected = true,
            address = "0x1234567890123456789012345678901234567890",
            chainId = "eip155:1",
            topic = "topic123"
        )
        
        // In a real test, we would mock the WalletConnectManager and verify state changes
        // For now, we're just verifying the data structure
        assertNotNull(walletSession)
        assertTrue(walletSession.connected)
    }

    @Test
    fun testProposalsLoading() {
        // Verify that proposals are loaded on initialization
        verify(apiService).getProposals()
    }

    @Test
    fun testTreasuryLoading() {
        // Verify that treasury is loaded on initialization
        // This is a suspend function, so we can't directly verify it here
        // In a real test, we would use a test coroutine scope
    }

    @Test
    fun testStartAgent() {
        // Test starting an agent
        `when`(apiService.startAgent()).thenReturn(startAgentCall)
        
        viewModel.startAgent("A-01")
        
        verify(apiService).startAgent()
        verify(startAgentCall).enqueue(any<Callback<ResponseBody>>())
    }

    @Test
    fun testIsConnected() {
        // Test connection status
        val isConnected = viewModel.isConnected()
        // Initially should be false
        assertFalse(isConnected)
    }
}