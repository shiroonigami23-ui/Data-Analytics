package com.shiro.dataanalytics.navigation

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.MenuBook
import androidx.compose.material.icons.outlined.Analytics
import androidx.compose.material.icons.outlined.Email
import androidx.compose.material.icons.outlined.Home
import androidx.compose.material.icons.outlined.Psychology
import androidx.compose.material.icons.outlined.Stars
import androidx.compose.ui.graphics.vector.ImageVector

sealed class AppDestination(
    val route: String,
    val title: String,
    val icon: ImageVector,
) {
    data object Home : AppDestination("home", "Dashboard", Icons.Outlined.Home)
    data object Resources : AppDestination("resources", "Resources", Icons.AutoMirrored.Outlined.MenuBook)
    data object Quiz : AppDestination("quiz", "Quiz", Icons.Outlined.Psychology)
    data object Progress : AppDestination("progress", "Progress", Icons.Outlined.Stars)
    data object Contact : AppDestination("contact", "Contact", Icons.Outlined.Email)
    data object Analytics : AppDestination("analytics", "Analytics", Icons.Outlined.Analytics)
}

val bottomDestinations = listOf(
    AppDestination.Home,
    AppDestination.Resources,
    AppDestination.Quiz,
    AppDestination.Progress,
    AppDestination.Contact,
    AppDestination.Analytics,
)
