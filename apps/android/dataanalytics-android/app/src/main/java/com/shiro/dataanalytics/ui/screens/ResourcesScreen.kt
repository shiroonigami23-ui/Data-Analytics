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
import androidx.compose.material3.OutlinedTextField
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
import com.shiro.dataanalytics.data.ResourcesRepository
import com.shiro.dataanalytics.model.ProgressState
import com.shiro.dataanalytics.model.ResourceItem
import kotlinx.coroutines.launch

@Composable
fun ResourcesScreen(
    resourcesRepository: ResourcesRepository,
    progressRepository: ProgressRepository,
) {
    var query by remember { mutableStateOf("") }
    val scope = rememberCoroutineScope()
    val resources by produceState(initialValue = emptyList<ResourceItem>()) {
        value = runCatching { resourcesRepository.getResources() }.getOrDefault(emptyList())
    }
    val progress by produceState(initialValue = ProgressState()) {
        progressRepository.progress.collect { value = it }
    }

    val filtered = remember(resources, query) {
        val normalized = query.trim().lowercase()
        if (normalized.isBlank()) {
            resources
        } else {
            resources.filter {
                it.title.lowercase().contains(normalized) ||
                    it.type.lowercase().contains(normalized) ||
                    (it.summary?.lowercase()?.contains(normalized) == true)
            }
        }
    }

    Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Text(text = "Resources", style = MaterialTheme.typography.headlineMedium)
        Text(
            text = "Read ${progress.readResourceIds.size}/${resources.size}",
            style = MaterialTheme.typography.bodyMedium,
        )

        OutlinedTextField(
            value = query,
            onValueChange = { query = it },
            label = { Text("Search resources") },
            modifier = Modifier.fillMaxWidth(),
        )

        LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            items(filtered, key = { it.resourceId() }) { item ->
                val isRead = progress.readResourceIds.contains(item.resourceId())
                ResourceCard(
                    item = item,
                    isRead = isRead,
                    onToggleRead = {
                        scope.launch {
                            if (isRead) {
                                progressRepository.unmarkResourceRead(item.resourceId())
                            } else {
                                progressRepository.markResourceRead(item.resourceId())
                            }
                        }
                    },
                )
            }
        }
    }
}

@Composable
private fun ResourceCard(item: ResourceItem, isRead: Boolean, onToggleRead: () -> Unit) {
    Card {
        Column(modifier = Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Text(text = item.title, style = MaterialTheme.typography.titleMedium)
            Text(text = "Type: ${item.type}", style = MaterialTheme.typography.bodySmall)
            Text(
                text = item.summary ?: item.preview ?: "No preview available.",
                style = MaterialTheme.typography.bodyMedium,
            )
            Text(
                text = if (isRead) "Status: Read" else "Status: Not read",
                style = MaterialTheme.typography.labelMedium,
            )
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Button(onClick = onToggleRead) {
                    Text(if (isRead) "Mark Unread" else "Mark as Read")
                }
            }
        }
    }
}

private fun ResourceItem.resourceId(): String = "$title|$file"
