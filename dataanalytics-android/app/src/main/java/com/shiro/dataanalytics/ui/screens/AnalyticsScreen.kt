package com.shiro.dataanalytics.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.produceState
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.shiro.dataanalytics.data.AnalyticsRepository
import com.shiro.dataanalytics.model.AnalyticsSummary

@Composable
fun AnalyticsScreen(analyticsRepository: AnalyticsRepository) {
    val summary by produceState(initialValue = AnalyticsSummary()) {
        value = runCatching { analyticsRepository.getSummary() }.getOrDefault(AnalyticsSummary())
    }

    Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Text("Analytics Snapshot", style = MaterialTheme.typography.headlineMedium)
        Text(
            "This is a lightweight local snapshot. You can wire Firebase Analytics or a custom backend next.",
            style = MaterialTheme.typography.bodyMedium,
        )

        if (summary.topics.isEmpty()) {
            Text("No topic analytics found.", style = MaterialTheme.typography.bodyMedium)
        } else {
            LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                items(summary.topics) { topic ->
                    Card {
                        Text(
                            text = "Hot topic: $topic",
                            modifier = Modifier.padding(12.dp),
                            style = MaterialTheme.typography.bodyLarge,
                        )
                    }
                }
            }
        }
    }
}
