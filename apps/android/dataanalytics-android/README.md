# Data Analytics Android (Kotlin)

Android app module for the Data Analytics project using Jetpack Compose.

## Implemented

- Adaptive app shell:
  - Phone: top app bar + drawer + bottom navigation
  - Tablet/laptop: collapsible left navigation panel
  - Dashboard quick-jump from non-dashboard screens
- Persistent UI preference:
  - Left navigation collapsed state is saved in DataStore and restored
- Dashboard:
  - Quick stats and collapsible sections
- Resources:
  - Search resources
  - Mark read/unread per item
  - Read state persisted in DataStore
- Quiz:
  - Requires all questions answered before submit
  - Score percentage
  - Post-submit answer review with correct answer display
  - Reset quiz action
- Progress:
  - Topics read, quizzes completed, best score
  - Badge unlocking
  - Reset progress action
- Contact:
  - Feedback submission to configured Apps Script endpoint
- Analytics:
  - Local snapshot from `analytics.json`

## Project Structure

- `app/src/main/java/com/shiro/dataanalytics/` - app source
- `app/src/main/assets/` - `resources.json`, `quiz.json`, `analytics.json`
- `app/src/main/res/` - Android resources
- `gradle/wrapper/` - wrapper files for reproducible builds

## Build

```powershell
.\gradlew.bat assembleDebug
```

Debug APK output:

- `app/build/outputs/apk/debug/app-debug.apk`

## Run

1. Open `dataanalytics-android/` in Android Studio.
2. Let Gradle sync.
3. Run on emulator/device (API 24+).

## Requirements

- JDK 17
- Android SDK installed locally

If SDK path is not auto-detected, create `local.properties`:

```properties
sdk.dir=C:\\Users\\<your-user>\\AppData\\Local\\Android\\Sdk
```
