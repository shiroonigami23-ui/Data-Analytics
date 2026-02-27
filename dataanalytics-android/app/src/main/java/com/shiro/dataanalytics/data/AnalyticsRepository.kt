package com.shiro.dataanalytics.data

import com.shiro.dataanalytics.model.AnalyticsSummary

class AnalyticsRepository(private val loader: AssetJsonLoader) {
    suspend fun getSummary(): AnalyticsSummary {
        val raw = loader.loadRawAsset("analytics.json")
        return loader.json.decodeFromString(AnalyticsSummary.serializer(), raw)
    }
}
