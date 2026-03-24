package com.shiro.dataanalytics.data

import com.shiro.dataanalytics.model.ResourceItem
import kotlinx.serialization.builtins.ListSerializer

class ResourcesRepository(private val loader: AssetJsonLoader) {
    suspend fun getResources(): List<ResourceItem> {
        val raw = loader.loadRawAsset("resources.json")
        return loader.json.decodeFromString(ListSerializer(ResourceItem.serializer()), raw)
    }
}
