package com.shiro.dataanalytics.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.produceState
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.shiro.dataanalytics.data.ProgressRepository
import com.shiro.dataanalytics.model.ProgressState
import kotlinx.coroutines.launch

@Composable
fun ProgressScreen(progressRepository: ProgressRepository) {
    val progress by produceState(initialValue = ProgressState()) {
        progressRepository.progress.collect { value = it }
    }
    val scope = rememberCoroutineScope()
    var resetMessage by remember { mutableStateOf<String?>(null) }

    Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        Text(text = "Progress & Badges", style = MaterialTheme.typography.headlineMedium)

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            SmallMetricCard("Topics", progress.topicsRead.toString(), Modifier.weight(1f))
            SmallMetricCard("Quizzes", progress.quizzesCompleted.toString(), Modifier.weight(1f))
        }
        val bestScoreLabel = if (progress.bestQuizTotal > 0) {
            "${progress.bestQuizScore}/${progress.bestQuizTotal}"
        } else {
            "-"
        }
        SmallMetricCard("Best Quiz Score", bestScoreLabel, Modifier.fillMaxWidth())

        Button(
            onClick = {
                scope.launch {
                    progressRepository.resetProgress()
                    resetMessage = "Progress reset completed."
                }
            },
            modifier = Modifier.fillMaxWidth(),
        ) {
            Text("Reset Progress")
        }

        resetMessage?.let {
            Text(text = it, style = MaterialTheme.typography.bodyMedium)
        }

        Text("Unlocked Badges", style = MaterialTheme.typography.titleMedium)
        if (progress.badges.isEmpty()) {
            Text("No badges unlocked yet.", style = MaterialTheme.typography.bodyMedium)
        } else {
            LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                items(progress.badges) { badge ->
                    Card {
                        Column(modifier = Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                            Text("Badge: ${badge.name}", style = MaterialTheme.typography.titleSmall)
                            Text(badge.description, style = MaterialTheme.typography.bodySmall)
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun SmallMetricCard(title: String, value: String, modifier: Modifier) {
    Card(modifier = modifier) {
        Column(modifier = Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
            Text(title, style = MaterialTheme.typography.labelMedium)
            Text(value, style = MaterialTheme.typography.headlineSmall)
        }
    }
}
