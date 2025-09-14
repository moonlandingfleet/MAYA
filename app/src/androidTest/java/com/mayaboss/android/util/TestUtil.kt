package com.mayaboss.android.util

import androidx.test.espresso.Espresso
import androidx.test.espresso.action.ViewActions
import androidx.test.espresso.assertion.ViewAssertions
import androidx.test.espresso.matcher.ViewMatchers
import androidx.test.espresso.matcher.ViewMatchers.withText

object TestUtil {
    
    /**
     * Perform login with test credentials
     */
    fun performLogin(username: String = "testuser", password: String = "testpass") {
        // Enter username
        Espresso.onView(ViewMatchers.withId(com.mayaboss.android.R.id.username))
            .perform(ViewActions.typeText(username), ViewActions.closeSoftKeyboard())
        
        // Enter password
        Espresso.onView(ViewMatchers.withId(com.mayaboss.android.R.id.password))
            .perform(ViewActions.typeText(password), ViewActions.closeSoftKeyboard())
        
        // Click login button
        Espresso.onView(ViewMatchers.withId(com.mayaboss.android.R.id.login_button))
            .perform(ViewActions.click())
    }
    
    /**
     * Check if user is on the main screen
     */
    fun checkOnMainScreen() {
        Espresso.onView(withText("MAYA v0.2 — One mind, many hands."))
            .check(ViewAssertions.matches(ViewMatchers.isDisplayed()))
    }
    
    /**
     * Check if user is on the login screen
     */
    fun checkOnLoginScreen() {
        Espresso.onView(withText("MAYA Login"))
            .check(ViewAssertions.matches(ViewMatchers.isDisplayed()))
    }
    
    /**
     * Logout from the app
     */
    fun performLogout() {
        Espresso.onView(withText("Logout"))
            .perform(ViewActions.click())
    }
}