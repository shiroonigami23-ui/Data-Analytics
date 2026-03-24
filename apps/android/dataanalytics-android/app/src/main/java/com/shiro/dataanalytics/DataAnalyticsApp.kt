package com.shiro.dataanalytics

import androidx.compose.animation.animateContentSize
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.ChevronLeft
import androidx.compose.material.icons.outlined.ChevronRight
import androidx.compose.material.icons.outlined.Menu
import androidx.compose.material3.CenterAlignedTopAppBar
import androidx.compose.material3.DrawerValue
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalDrawerSheet
import androidx.compose.material3.ModalNavigationDrawer
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationDrawerItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.material3.rememberDrawerState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.navigation.NavDestination.Companion.hierarchy
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.shiro.dataanalytics.data.AppContainer
import com.shiro.dataanalytics.navigation.AppDestination
import com.shiro.dataanalytics.navigation.bottomDestinations
import com.shiro.dataanalytics.ui.screens.AnalyticsScreen
import com.shiro.dataanalytics.ui.screens.ContactScreen
import com.shiro.dataanalytics.ui.screens.HomeScreen
import com.shiro.dataanalytics.ui.screens.ProgressScreen
import com.shiro.dataanalytics.ui.screens.QuizScreen
import com.shiro.dataanalytics.ui.screens.ResourcesScreen
import com.shiro.dataanalytics.ui.theme.DataAnalyticsTheme
import kotlinx.coroutines.launch

private val compactBottomDestinations = listOf(
    AppDestination.Home,
    AppDestination.Resources,
    AppDestination.Quiz,
    AppDestination.Progress,
)

@Composable
fun DataAnalyticsApp(appContainer: AppContainer) {
    DataAnalyticsTheme {
        val navController = rememberNavController()
        val navBackStackEntry by navController.currentBackStackEntryAsState()
        val currentDestination = navBackStackEntry?.destination
        val currentRoute = currentDestination?.route
        val currentTopDestination = bottomDestinations.firstOrNull { it.route == currentRoute } ?: AppDestination.Home
        val showDashboardAction = currentRoute != null && currentRoute != AppDestination.Home.route

        BoxWithConstraints(modifier = Modifier.fillMaxSize()) {
            val isCompact = maxWidth < 840.dp

            if (isCompact) {
                CompactAdaptiveScaffold(
                    navController = navController,
                    currentDestination = currentDestination,
                    currentTopDestination = currentTopDestination,
                    showDashboardAction = showDashboardAction,
                    appContainer = appContainer,
                )
            } else {
                ExpandedAdaptiveScaffold(
                    navController = navController,
                    currentDestination = currentDestination,
                    currentTopDestination = currentTopDestination,
                    showDashboardAction = showDashboardAction,
                    appContainer = appContainer,
                )
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun CompactAdaptiveScaffold(
    navController: NavHostController,
    currentDestination: androidx.navigation.NavDestination?,
    currentTopDestination: AppDestination,
    showDashboardAction: Boolean,
    appContainer: AppContainer,
) {
    val drawerState = rememberDrawerState(initialValue = DrawerValue.Closed)
    val scope = rememberCoroutineScope()

    ModalNavigationDrawer(
        drawerState = drawerState,
        drawerContent = {
            ModalDrawerSheet {
                Spacer(modifier = Modifier.height(10.dp))
                Text(
                    text = "Data Analytics Hub",
                    style = MaterialTheme.typography.titleMedium,
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp),
                )
                bottomDestinations.forEach { destination ->
                    val selected = currentDestination?.hierarchy?.any { it.route == destination.route } == true
                    NavigationDrawerItem(
                        icon = { Icon(destination.icon, contentDescription = destination.title) },
                        label = { Text(destination.title) },
                        selected = selected,
                        onClick = {
                            navigateToDestination(navController, destination)
                            scope.launch { drawerState.close() }
                        },
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 4.dp),
                    )
                }
            }
        },
    ) {
        Scaffold(
            topBar = {
                CenterAlignedTopAppBar(
                    title = { Text(currentTopDestination.title) },
                    navigationIcon = {
                        IconButton(onClick = { scope.launch { drawerState.open() } }) {
                            Icon(Icons.Outlined.Menu, contentDescription = "Open navigation")
                        }
                    },
                    actions = {
                        if (showDashboardAction) {
                            TextButton(onClick = { navigateToDestination(navController, AppDestination.Home) }) {
                                Text("Dashboard")
                            }
                        }
                    },
                    colors = TopAppBarDefaults.centerAlignedTopAppBarColors(
                        containerColor = MaterialTheme.colorScheme.surface,
                    ),
                )
            },
            bottomBar = {
                NavigationBar {
                    compactBottomDestinations.forEach { destination ->
                        val selected = currentDestination?.hierarchy?.any { it.route == destination.route } == true
                        NavigationBarItem(
                            selected = selected,
                            onClick = { navigateToDestination(navController, destination) },
                            icon = { Icon(destination.icon, contentDescription = destination.title) },
                            label = { Text(destination.title) },
                            alwaysShowLabel = false,
                        )
                    }
                }
            },
        ) { innerPadding ->
            AppNavHost(
                navController = navController,
                appContainer = appContainer,
                modifier = Modifier.padding(innerPadding),
            )
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun ExpandedAdaptiveScaffold(
    navController: NavHostController,
    currentDestination: androidx.navigation.NavDestination?,
    currentTopDestination: AppDestination,
    showDashboardAction: Boolean,
    appContainer: AppContainer,
) {
    val scope = rememberCoroutineScope()
    val navCollapsed by appContainer.uiPreferencesRepository.navCollapsed.collectAsState(initial = false)
    val navWidth by animateDpAsState(
        targetValue = if (navCollapsed) 88.dp else 260.dp,
        label = "nav_width",
    )

    Scaffold(
        topBar = {
            CenterAlignedTopAppBar(
                title = { Text(currentTopDestination.title) },
                actions = {
                    if (showDashboardAction) {
                        TextButton(onClick = { navigateToDestination(navController, AppDestination.Home) }) {
                            Text("Dashboard")
                        }
                    }
                },
            )
        },
    ) { innerPadding ->
        Row(
            modifier = Modifier
                .padding(innerPadding)
                .fillMaxSize(),
        ) {
            Surface(
                tonalElevation = 2.dp,
                modifier = Modifier
                    .fillMaxHeight()
                    .width(navWidth)
                    .animateContentSize(),
            ) {
                Column(modifier = Modifier.fillMaxSize()) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 10.dp, vertical = 10.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically,
                    ) {
                        if (!navCollapsed) {
                            Text(
                                text = "Navigation",
                                style = MaterialTheme.typography.titleSmall,
                            )
                        }
                        IconButton(
                            onClick = {
                                scope.launch {
                                    appContainer.uiPreferencesRepository.setNavCollapsed(!navCollapsed)
                                }
                            },
                        ) {
                            Icon(
                                imageVector = if (navCollapsed) Icons.Outlined.ChevronRight else Icons.Outlined.ChevronLeft,
                                contentDescription = "Toggle navigation collapse",
                            )
                        }
                    }

                    bottomDestinations.forEach { destination ->
                        val selected = currentDestination?.hierarchy?.any { it.route == destination.route } == true
                        SideNavItem(
                            destination = destination,
                            selected = selected,
                            collapsed = navCollapsed,
                            onClick = { navigateToDestination(navController, destination) },
                        )
                    }
                }
            }

            AppNavHost(
                navController = navController,
                appContainer = appContainer,
                modifier = Modifier
                    .weight(1f)
                    .fillMaxHeight(),
            )
        }
    }
}

@Composable
private fun SideNavItem(
    destination: AppDestination,
    selected: Boolean,
    collapsed: Boolean,
    onClick: () -> Unit,
) {
    val background =
        if (selected) MaterialTheme.colorScheme.primary.copy(alpha = 0.12f)
        else MaterialTheme.colorScheme.surface

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 8.dp, vertical = 4.dp)
            .background(background, RoundedCornerShape(12.dp))
            .clickable(onClick = onClick)
            .padding(horizontal = 12.dp, vertical = 14.dp),
        horizontalArrangement = if (collapsed) Arrangement.Center else Arrangement.Start,
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Icon(destination.icon, contentDescription = destination.title)
        if (!collapsed) {
            Spacer(modifier = Modifier.width(12.dp))
            Text(destination.title)
        }
    }
}

private fun navigateToDestination(
    navController: NavHostController,
    destination: AppDestination,
) {
    navController.navigate(destination.route) {
        popUpTo(navController.graph.startDestinationId) {
            saveState = true
        }
        launchSingleTop = true
        restoreState = true
    }
}

@Composable
private fun AppNavHost(
    navController: NavHostController,
    appContainer: AppContainer,
    modifier: Modifier = Modifier,
) {
    NavHost(
        navController = navController,
        startDestination = AppDestination.Home.route,
        modifier = modifier,
    ) {
        composable(AppDestination.Home.route) {
            HomeScreen(
                resourcesRepository = appContainer.resourcesRepository,
                quizRepository = appContainer.quizRepository,
                progressRepository = appContainer.progressRepository,
            )
        }
        composable(AppDestination.Resources.route) {
            ResourcesScreen(
                resourcesRepository = appContainer.resourcesRepository,
                progressRepository = appContainer.progressRepository,
            )
        }
        composable(AppDestination.Quiz.route) {
            QuizScreen(
                quizRepository = appContainer.quizRepository,
                progressRepository = appContainer.progressRepository,
            )
        }
        composable(AppDestination.Progress.route) {
            ProgressScreen(progressRepository = appContainer.progressRepository)
        }
        composable(AppDestination.Contact.route) {
            ContactScreen(feedbackService = appContainer.feedbackService)
        }
        composable(AppDestination.Analytics.route) {
            AnalyticsScreen(analyticsRepository = appContainer.analyticsRepository)
        }
    }
}
