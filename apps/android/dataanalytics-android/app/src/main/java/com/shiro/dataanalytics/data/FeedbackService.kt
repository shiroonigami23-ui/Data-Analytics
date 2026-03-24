package com.shiro.dataanalytics.data

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.FormBody
import okhttp3.OkHttpClient
import okhttp3.Request

class FeedbackService(
    private val client: OkHttpClient = OkHttpClient(),
    private val endpoint: String = DEFAULT_ENDPOINT,
) {
    suspend fun submitFeedback(
        name: String,
        email: String,
        message: String,
    ): Result<Unit> = withContext(Dispatchers.IO) {
        runCatching {
            val body = FormBody.Builder()
                .add("name", name)
                .add("email", email)
                .add("message", message)
                .build()

            val request = Request.Builder()
                .url(endpoint)
                .post(body)
                .build()

            client.newCall(request).execute().use { response ->
                if (!response.isSuccessful) {
                    error("Feedback request failed: ${response.code}")
                }
            }
        }
    }

    companion object {
        const val DEFAULT_ENDPOINT =
            "https://script.google.com/macros/s/AKfycbxuFHf4WlRXYq2I0QJdC5D3zolFzg70moOFoKJIwDklQRfugmD8LYsl4JZ3Z9hTIonhKw/exec"
    }
}
