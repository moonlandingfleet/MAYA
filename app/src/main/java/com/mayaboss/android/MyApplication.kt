package com.mayaboss.android

import android.app.Application
import com.mayaboss.android.BuildConfig
import timber.log.Timber

class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()

        if (BuildConfig.DEBUG) { // Only log in debug builds
            Timber.plant(Timber.DebugTree())
            Timber.d("Timber initialised") // Added a log to confirm initialization
        }
    }
}