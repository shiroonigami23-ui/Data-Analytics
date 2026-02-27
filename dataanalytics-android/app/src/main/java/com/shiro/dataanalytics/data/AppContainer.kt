package com.shiro.dataanalytics.data

import android.content.Context

class AppContainer(context: Context) {
    private val loader = AssetJsonLoader(context)

    val resourcesRepository = ResourcesRepository(loader)
    val quizRepository = QuizRepository(loader)
    val analyticsRepository = AnalyticsRepository(loader)
    val progressRepository = ProgressRepository(context)
    val uiPreferencesRepository = UiPreferencesRepository(context)
    val feedbackService = FeedbackService()
}
