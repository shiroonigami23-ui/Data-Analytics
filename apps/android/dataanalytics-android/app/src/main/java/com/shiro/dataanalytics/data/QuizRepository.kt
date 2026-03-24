package com.shiro.dataanalytics.data

import com.shiro.dataanalytics.model.QuizQuestion
import kotlinx.serialization.builtins.ListSerializer

class QuizRepository(private val loader: AssetJsonLoader) {
    suspend fun getQuizQuestions(): List<QuizQuestion> {
        val raw = loader.loadRawAsset("quiz.json")
        return loader.json.decodeFromString(ListSerializer(QuizQuestion.serializer()), raw)
    }
}
