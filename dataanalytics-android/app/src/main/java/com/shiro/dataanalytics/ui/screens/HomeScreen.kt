package com.shiro.dataanalytics.ui.screens

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.animateContentSize
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.ExpandLess
import androidx.compose.material.icons.outlined.ExpandMore
import androidx.compose.material3.Card
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.produceState
import androidx.compose.runtime.setValue
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.shiro.dataanalytics.data.ProgressRepository
import com.shiro.dataanalytics.data.QuizRepository
import com.shiro.dataanalytics.data.ResourcesRepository
import com.shiro.dataanalytics.model.ProgressState

@Composable
fun HomeScreen(
    resourcesRepository: ResourcesRepository,
    quizRepository: QuizRepository,
    progressRepository: ProgressRepository,
) {
    val resourcesCount by produceState(initialValue = 0) {
        value = runCatching { resourcesRepository.getResources().size }.getOrDefault(0)
    }
    val quizCount by produceState(initialValue = 0) {
        value = runCatching { quizRepository.getQuizQuestions().size }.getOrDefault(0)
    }
    val progress by produceState(initialValue = ProgressState()) {
        progressRepository.progress.collect { value = it }
    }
    var tipsExpanded by rememberSaveable { mutableStateOf(true) }
    var shortcutsExpanded by rememberSaveable { mutableStateOf(true) }

    LazyColumn(
        modifier = Modifier.padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        item {
            Text(
                text = "Dashboard",
                style = MaterialTheme.typography.headlineMedium,
            )
        }
        item {
            Text(
                text = "Clean adaptive layout with persistent navigation and quick progress signals.",
                style = MaterialTheme.typography.bodyMedium,
            )
        }

        item {
            BoxWithConstraints {
                val isWide = maxWidth >= 700.dp
                if (isWide) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(12.dp),
                    ) {
                        StatCard("Resources", resourcesCount.toString(), Modifier.weight(1f))
                        StatCard("Quiz Qs", quizCount.toString(), Modifier.weight(1f))
                        StatCard("Badges", progress.badges.size.toString(), Modifier.weight(1f))
                    }
                } else {
                    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(12.dp),
                        ) {
                            StatCard("Resources", resourcesCount.toString(), Modifier.weight(1f))
                            StatCard("Quiz Qs", quizCount.toString(), Modifier.weight(1f))
                        }
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(12.dp),
                        ) {
                            StatCard("Topics Read", progress.topicsRead.toString(), Modifier.weight(1f))
                            StatCard("Quizzes Done", progress.quizzesCompleted.toString(), Modifier.weight(1f))
                        }
                    }
                }
            }
        }

        item {
            CollapsibleCard(
                title = "Quick Tips",
                expanded = tipsExpanded,
                onToggle = { tipsExpanded = !tipsExpanded },
            ) {
                Text("1. Open Resources and mark each one as read.", style = MaterialTheme.typography.bodyMedium)
                Text("2. Take Quiz after each resource cycle.", style = MaterialTheme.typography.bodyMedium)
                Text("3. Track unlocked badges in Progress tab.", style = MaterialTheme.typography.bodyMedium)
            }
        }

        item {
            CollapsibleCard(
                title = "Shortcuts",
                expanded = shortcutsExpanded,
                onToggle = { shortcutsExpanded = !shortcutsExpanded },
            ) {
                Text("- Dashboard button is available from all non-home pages.", style = MaterialTheme.typography.bodyMedium)
                Text("- On large screens, collapse or expand the left navigation panel.", style = MaterialTheme.typography.bodyMedium)
                Text("- On mobile, use bottom tabs and the menu drawer for full navigation.", style = MaterialTheme.typography.bodyMedium)
            }
        }
    }
}

@Composable
private fun CollapsibleCard(
    title: String,
    expanded: Boolean,
    onToggle: () -> Unit,
    content: @Composable ColumnScope.() -> Unit,
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .animateContentSize(),
        shape = RoundedCornerShape(14.dp),
    ) {
        Column(modifier = Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable(onClick = onToggle),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Text(title, style = MaterialTheme.typography.titleMedium)
                Icon(
                    imageVector = if (expanded) Icons.Outlined.ExpandLess else Icons.Outlined.ExpandMore,
                    contentDescription = "Toggle section",
                )
            }
            AnimatedVisibility(visible = expanded) {
                Column(verticalArrangement = Arrangement.spacedBy(6.dp), content = content)
            }
        }
    }
}

@Composable
private fun StatCard(title: String, value: String, modifier: Modifier = Modifier) {
    Card(modifier = modifier) {
        Column(modifier = Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
            Text(text = title, style = MaterialTheme.typography.labelMedium)
            Text(text = value, style = MaterialTheme.typography.headlineSmall)
        }
    }
}
