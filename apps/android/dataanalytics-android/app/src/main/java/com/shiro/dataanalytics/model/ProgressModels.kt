package com.shiro.dataanalytics.model

data class Badge(
    val name: String,
    val description: String,
)

data class ProgressState(
    val topicsRead: Int = 0,
    val quizzesCompleted: Int = 0,
    val bestQuizScore: Int = 0,
    val bestQuizTotal: Int = 0,
    val readResourceIds: Set<String> = emptySet(),
    val badges: List<Badge> = emptyList(),
)
