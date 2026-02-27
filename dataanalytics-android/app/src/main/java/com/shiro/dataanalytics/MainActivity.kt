package com.shiro.dataanalytics

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.shiro.dataanalytics.data.AppContainer

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val appContainer = AppContainer(applicationContext)
        setContent {
            DataAnalyticsApp(appContainer = appContainer)
        }
    }
}
