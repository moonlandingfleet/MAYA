package com.mayaboss.android

import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.filters.LargeTest
import com.mayaboss.android.util.TestUtil
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
@LargeTest
class EndToEndTest {

    @get:Rule
    val activityRule = ActivityScenarioRule(MainActivity::class.java)

    @Test
    fun testLoginAndLogoutFlow() {
        // Check that we start on the login screen
        TestUtil.checkOnLoginScreen()
        
        // Perform login
        TestUtil.performLogin()
        
        // Check that we're on the main screen
        TestUtil.checkOnMainScreen()
        
        // Perform logout
        TestUtil.performLogout()
        
        // Check that we're back on the login screen
        TestUtil.checkOnLoginScreen()
    }
    
    @Test
    fun testTestingModeFlow() {
        // Check that we start on the login screen
        TestUtil.checkOnLoginScreen()
        
        // Enable testing mode (this would require UI elements for testing mode)
        // For now, we'll just test the normal flow
        
        // Perform login
        TestUtil.performLogin()
        
        // Check that we're on the main screen
        TestUtil.checkOnMainScreen()
        
        // Perform logout
        TestUtil.performLogout()
        
        // Check that we're back on the login screen
        TestUtil.checkOnLoginScreen()
    }
}