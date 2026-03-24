package com.shiro.dataanalytics.ui.screens

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.RadioButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateMapOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.produceState
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.shiro.dataanalytics.data.ProgressRepository
import com.shiro.dataanalytics.data.QuizRepository
import com.shiro.dataanalytics.model.QuizQuestion
import kotlinx.coroutines.launch

@Composable
fun QuizScreen(
    quizRepository: QuizRepository,
    progressRepository: ProgressRepository,
) {
    val questions by produceState(initialValue = emptyList<QuizQuestion>()) {
        value = runCatching { quizRepository.getQuizQuestions() }.getOrDefault(emptyList())
    }

    val selectedAnswers = remember { mutableStateMapOf<Int, String>() }
    var resultText by remember { mutableStateOf<String?>(null) }
    var submitted by remember { mutableStateOf(false) }
    val scope = rememberCoroutineScope()

    val unansweredCount = questions.indices.count { selectedAnswers[it].isNullOrBlank() }

    Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Text(text = "Quiz", style = MaterialTheme.typography.headlineMedium)
        Text(
            text = if (submitted) "Review your answers below." else "Answer all questions and submit.",
            style = MaterialTheme.typography.bodyMedium,
        )

        LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            itemsIndexed(questions) { index, question ->
                val selected = selectedAnswers[index]
                val isCorrect = selected == question.a

                Card {
                    Column(modifier = Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                        Text("Q${index + 1}. ${question.q}", style = MaterialTheme.typography.titleMedium)
                        question.options.forEach { option ->
                            OptionRow(
                                option = option,
                                selected = selected == option,
                                enabled = !submitted,
                                onClick = { selectedAnswers[index] = option },
                            )
                        }

                        if (submitted) {
                            val status = if (isCorrect) "Correct" else "Incorrect"
                            val tone = if (isCorrect) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.error
                            Text(
                                text = status,
                                style = MaterialTheme.typography.labelLarge,
                                color = tone,
                                fontWeight = FontWeight.SemiBold,
                            )
                            if (!isCorrect) {
                                Text("Correct answer: ${question.a}", style = MaterialTheme.typography.bodySmall)
                                Text(
                                    "Your answer: ${selected ?: "Not answered"}",
                                    style = MaterialTheme.typography.bodySmall,
                                )
                            }
                        }
                    }
                }
            }
        }

        if (!submitted && unansweredCount > 0) {
            Text(
                text = "Unanswered: $unansweredCount",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.error,
            )
        }

        Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
            Button(
                onClick = {
                    val score = questions.countIndexed { index, question ->
                        selectedAnswers[index] == question.a
                    }
                    val percentage = if (questions.isEmpty()) 0 else (score * 100) / questions.size
                    resultText = "You scored $score/${questions.size} ($percentage%)"
                    submitted = true
                    scope.launch {
                        progressRepository.markQuizCompleted(score, questions.size)
                    }
                },
                enabled = questions.isNotEmpty() && unansweredCount == 0 && !submitted,
                modifier = Modifier.weight(1f),
            ) {
                Text("Submit Quiz")
            }

            Button(
                onClick = {
                    selectedAnswers.clear()
                    resultText = null
                    submitted = false
                },
                modifier = Modifier.weight(1f),
            ) {
                Text("Reset Quiz")
            }
        }

        resultText?.let {
            Text(text = it, style = MaterialTheme.typography.titleMedium)
        }
    }
}

@Composable
private fun OptionRow(
    option: String,
    selected: Boolean,
    enabled: Boolean,
    onClick: () -> Unit,
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(enabled = enabled, onClick = onClick)
            .padding(vertical = 2.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        RadioButton(selected = selected, onClick = if (enabled) onClick else null)
        Text(option)
    }
}

private inline fun <T> List<T>.countIndexed(predicate: (index: Int, item: T) -> Boolean): Int {
    var count = 0
    forEachIndexed { index, item ->
        if (predicate(index, item)) count++
    }
    return count
}
