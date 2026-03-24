package com.shiro.dataanalytics.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class ResourceItem(
    val title: String,
    val file: String,
    val type: String,
    @SerialName("summary") val summary: String? = null,
    @SerialName("preview") val preview: String? = null,
)
