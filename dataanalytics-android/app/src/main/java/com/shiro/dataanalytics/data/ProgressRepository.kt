package com.shiro.dataanalytics.data

import android.content.Context
import androidx.datastore.preferences.core.intPreferencesKey
import androidx.datastore.preferences.core.stringSetPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.preferencesDataStore
import com.shiro.dataanalytics.model.Badge
import com.shiro.dataanalytics.model.ProgressState
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import kotlin.math.max

private val Context.dataStore by preferencesDataStore(name = "progress_store")

class ProgressRepository(private val context: Context) {
    private val topicsReadKey = intPreferencesKey("topics_read")
    private val quizzesCompletedKey = intPreferencesKey("quizzes_completed")
    private val bestQuizScoreKey = intPreferencesKey("best_quiz_score")
    private val bestQuizTotalKey = intPreferencesKey("best_quiz_total")
    private val readResourceIdsKey = stringSetPreferencesKey("read_resource_ids")

    val progress: Flow<ProgressState> = context.dataStore.data.map { prefs ->
        val readResourceIds = prefs[readResourceIdsKey] ?: emptySet()
        val legacyTopicsRead = prefs[topicsReadKey] ?: 0
        val topicsRead = max(legacyTopicsRead, readResourceIds.size)
        val quizzesCompleted = prefs[quizzesCompletedKey] ?: 0
        val bestQuizScore = prefs[bestQuizScoreKey] ?: 0
        val bestQuizTotal = prefs[bestQuizTotalKey] ?: 0
        ProgressState(
            topicsRead = topicsRead,
            quizzesCompleted = quizzesCompleted,
            bestQuizScore = bestQuizScore,
            bestQuizTotal = bestQuizTotal,
            readResourceIds = readResourceIds,
            badges = buildBadges(topicsRead, quizzesCompleted),
        )
    }

    suspend fun markResourceRead(resourceId: String) {
        if (resourceId.isBlank()) return

        context.dataStore.edit { prefs ->
            val currentIds = (prefs[readResourceIdsKey] ?: emptySet()).toMutableSet()
            currentIds += resourceId
            prefs[readResourceIdsKey] = currentIds
            prefs[topicsReadKey] = max(prefs[topicsReadKey] ?: 0, currentIds.size)
        }
    }

    suspend fun unmarkResourceRead(resourceId: String) {
        if (resourceId.isBlank()) return

        context.dataStore.edit { prefs ->
            val currentIds = (prefs[readResourceIdsKey] ?: emptySet()).toMutableSet()
            currentIds -= resourceId
            prefs[readResourceIdsKey] = currentIds
            prefs[topicsReadKey] = currentIds.size
        }
    }

    suspend fun markQuizCompleted(score: Int, total: Int) {
        context.dataStore.edit { prefs ->
            val current = prefs[quizzesCompletedKey] ?: 0
            val bestScore = prefs[bestQuizScoreKey] ?: 0
            val bestTotal = prefs[bestQuizTotalKey] ?: 0

            prefs[quizzesCompletedKey] = current + 1
            if (score > bestScore || (score == bestScore && total > bestTotal)) {
                prefs[bestQuizScoreKey] = score
                prefs[bestQuizTotalKey] = total
            }
        }
    }

    suspend fun resetProgress() {
        context.dataStore.edit { prefs ->
            prefs[topicsReadKey] = 0
            prefs[quizzesCompletedKey] = 0
            prefs[bestQuizScoreKey] = 0
            prefs[bestQuizTotalKey] = 0
            prefs[readResourceIdsKey] = emptySet()
        }
    }

    private fun buildBadges(topicsRead: Int, quizzesCompleted: Int): List<Badge> {
        val badges = mutableListOf<Badge>()

        if (topicsRead >= 1) {
            badges += Badge("First Reader", "Opened your first resource.")
        }
        if (quizzesCompleted >= 1) {
            badges += Badge("Quiz Starter", "Completed your first quiz.")
        }
        if (topicsRead >= 3) {
            badges += Badge("Data Enthusiast", "Completed 3 resource reads.")
        }
        if (quizzesCompleted >= 5) {
            badges += Badge("Quiz Master", "Completed 5 quizzes.")
        }
        if (topicsRead >= 10 && quizzesCompleted >= 10) {
            badges += Badge("Analytics Grinder", "Stayed consistent with learning.")
        }

        return badges
    }
}
