package com.shiro.dataanalytics.data

import android.content.Context
import kotlinx.serialization.json.Json

class AssetJsonLoader(private val context: Context) {
    val json = Json {
        ignoreUnknownKeys = true
        isLenient = true
        coerceInputValues = true
    }

    fun loadRawAsset(fileName: String): String {
        return context.assets.open(fileName).bufferedReader().use { it.readText() }
    }
}
