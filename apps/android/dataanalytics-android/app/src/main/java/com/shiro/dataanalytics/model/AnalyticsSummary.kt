package com.shiro.dataanalytics.model

import kotlinx.serialization.Serializable

@Serializable
data class AnalyticsSummary(
    val topics: List<String> = emptyList(),
)
