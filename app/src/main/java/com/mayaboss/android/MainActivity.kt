package com.mayaboss.android

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.ComposeView
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.*
import androidx.lifecycle.ViewModelProvider
import com.mayaboss.android.network.MAYAApiService
import com.mayaboss.android.ui.MainScreen
import com.mayaboss.android.ui.WalletConnectScreen
import com.mayaboss.android.viewmodel.MAYAViewModel
import androidx.lifecycle.ViewModel

class MainActivity : AppCompatActivity() {
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Use only Compose UI instead of mixing with traditional View system
        setContent {
            MaterialTheme {
                Surface(modifier = Modifier.fillMaxSize()) {
                    val apiService = MAYAApiService.create("http://localhost:8080/") // Adjust base URL as needed
                    val viewModel = ViewModelProvider(this, MAYAViewModelFactory(this.application, apiService))[MAYAViewModel::class.java]
                    AppNavigation(viewModel)
                }
            }
        }
    }
    
    @Composable
    fun AppNavigation(viewModel: MAYAViewModel) {
        var currentScreen by remember { mutableStateOf("main") }
        
        when (currentScreen) {
            "main" -> MainScreen(
                viewModel = viewModel,
                onNavigateToWalletConnect = { currentScreen = "walletConnect" }
            )
            "walletConnect" -> WalletConnectScreen(
                viewModel = viewModel,
                onBack = { currentScreen = "main" }
            )
        }
    }
    
    private fun setContent(content: @Composable () -> Unit) {
        val composeView = ComposeView(this).apply {
            setContent(content)
        }
        setContentView(composeView)
    }
}

class MAYAViewModelFactory(private val application: android.app.Application, private val apiService: MAYAApiService) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(MAYAViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return MAYAViewModel(apiService, application) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}