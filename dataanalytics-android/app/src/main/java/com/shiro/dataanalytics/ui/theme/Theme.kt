package com.shiro.dataanalytics.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable

private val LightColors = lightColorScheme(
    primary = BluePrimary,
    secondary = BlueSecondary,
    surface = SurfaceLight,
)

private val DarkColors = darkColorScheme(
    primary = BlueSecondary,
)

@Composable
fun DataAnalyticsTheme(
    darkTheme: Boolean = false,
    content: @Composable () -> Unit,
) {
    MaterialTheme(
        colorScheme = if (darkTheme) DarkColors else LightColors,
        content = content,
    )
}
