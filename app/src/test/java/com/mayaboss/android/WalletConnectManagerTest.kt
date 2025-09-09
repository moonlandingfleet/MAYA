package com.mayaboss.android

import com.mayaboss.android.network.WalletConnectManager
import org.junit.Test
import org.junit.Assert.*

class WalletConnectManagerTest {

    @Test
    fun testSingletonInstance() {
        val instance1 = WalletConnectManager.getInstance()
        val instance2 = WalletConnectManager.getInstance()
        
        // Verify that the same instance is returned
        assertSame(instance1, instance2)
    }
    
    @Test
    fun testWalletSessionDataClass() {
        val walletSession = com.mayaboss.android.model.WalletSession(
            connected = true,
            address = "0x1234567890123456789012345678901234567890",
            chainId = "eip155:1",
            topic = "topic123"
        )
        
        assertTrue(walletSession.connected)
        assertEquals("0x1234567890123456789012345678901234567890", walletSession.address)
        assertEquals("eip155:1", walletSession.chainId)
        assertEquals("topic123", walletSession.topic)
    }
    
    @Test
    fun testTreasuryModelExtension() {
        val treasury = com.mayaboss.android.model.Treasury(
            address = "0x1234567890123456789012345678901234567890",
            balance_eth = 1.5,
            agents_contributed = listOf("A-01", "A-02"),
            last_updated = "2023-01-01T00:00:00Z",
            wallet_connected = true
        )
        
        assertEquals("0x1234567890123456789012345678901234567890", treasury.address)
        assertEquals(1.5, treasury.balance_eth, 0.0)
        assertEquals(2, treasury.agents_contributed.size)
        assertTrue(treasury.wallet_connected)
    }
}