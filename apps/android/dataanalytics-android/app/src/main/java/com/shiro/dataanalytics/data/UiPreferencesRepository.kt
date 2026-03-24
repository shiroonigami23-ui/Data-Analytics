package com.shiro.dataanalytics.data

import android.content.Context
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.emptyPreferences
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.map
import java.io.IOException

private val Context.uiPreferencesDataStore by preferencesDataStore(name = "ui_preferences")

class UiPreferencesRepository(private val context: Context) {
    private object Keys {
        val navCollapsed = booleanPreferencesKey("nav_collapsed")
    }

    val navCollapsed: Flow<Boolean> = context.uiPreferencesDataStore.data
        .catch { exception ->
            if (exception is IOException) {
                emit(emptyPreferences())
            } else {
                throw exception
            }
        }
        .map { preferences ->
            preferences[Keys.navCollapsed] ?: false
        }

    suspend fun setNavCollapsed(collapsed: Boolean) {
        context.uiPreferencesDataStore.edit { preferences ->
            preferences[Keys.navCollapsed] = collapsed
        }
    }
}
