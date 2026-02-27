package com.shiro.dataanalytics.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.shiro.dataanalytics.data.FeedbackService
import kotlinx.coroutines.launch

@Composable
fun ContactScreen(feedbackService: FeedbackService) {
    var name by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var message by remember { mutableStateOf("") }
    var status by remember { mutableStateOf<String?>(null) }
    var sending by remember { mutableStateOf(false) }
    val scope = rememberCoroutineScope()

    Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Text("Contact & Feedback", style = MaterialTheme.typography.headlineMedium)
        OutlinedTextField(
            value = name,
            onValueChange = { name = it },
            label = { Text("Name (optional)") },
            modifier = Modifier.fillMaxWidth(),
        )
        OutlinedTextField(
            value = email,
            onValueChange = { email = it },
            label = { Text("Email (optional)") },
            modifier = Modifier.fillMaxWidth(),
        )
        OutlinedTextField(
            value = message,
            onValueChange = { message = it },
            label = { Text("Message") },
            modifier = Modifier.fillMaxWidth(),
            minLines = 4,
        )

        Button(
            onClick = {
                if (message.isBlank()) {
                    status = "Message is required."
                    return@Button
                }
                sending = true
                status = "Sending..."
                scope.launch {
                    val result = feedbackService.submitFeedback(name = name, email = email, message = message)
                    if (result.isSuccess) {
                        status = "Feedback submitted."
                        message = ""
                    } else {
                        status = "Failed: ${result.exceptionOrNull()?.message ?: "unknown error"}"
                    }
                    sending = false
                }
            },
            enabled = !sending,
            modifier = Modifier.fillMaxWidth(),
        ) {
            Text(if (sending) "Sending..." else "Send Feedback")
        }

        status?.let {
            Text(it, style = MaterialTheme.typography.bodyMedium)
        }
    }
}
