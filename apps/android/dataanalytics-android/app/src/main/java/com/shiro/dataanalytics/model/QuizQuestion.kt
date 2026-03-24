package com.shiro.dataanalytics.model

import kotlinx.serialization.Serializable

@Serializable
data class QuizQuestion(
    val q: String,
    val options: List<String>,
    val a: String,
)
