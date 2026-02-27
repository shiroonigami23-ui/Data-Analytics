# Data Analytics Android App

Data Analytics Android is a Jetpack Compose app for learning data analytics topics with resources, quizzes, progress tracking, and feedback submission.

## Repository Focus

This repository now ships a production-ready Android project in:

- `dataanalytics-android/`

Legacy web assets remain in the root for reference, while Android is the primary deliverable.

## Key Features

- Adaptive navigation for phone, tablet, and laptop layouts
- Persistent collapsible side navigation on large screens
- Dashboard with collapsible sections and learning stats
- Resource search with per-resource read/unread tracking
- Quiz flow with validation, score breakdown, answer review, and reset
- Progress and badges with DataStore persistence and reset action
- Contact/feedback form integration (Apps Script endpoint)
- Local analytics snapshot screen from JSON assets

## Build APK

From `dataanalytics-android/`:

```powershell
.\gradlew.bat assembleDebug
```

Generated APK:

- `dataanalytics-android/app/build/outputs/apk/debug/app-debug.apk`

## Ready Package

A packaged artifact is included in:

- `release-package/DataAnalyticsAndroid-debug.apk`
- `release-package/APK-SHA256.txt`
- `release-package/DataAnalyticsAndroid-package.zip`

## Required Tooling

- JDK 17
- Android SDK (configured by `local.properties` on each machine)
- Gradle wrapper (`gradlew`, `gradlew.bat`) is included

## Developer Docs

- Setup and run guide: `INSTRUCTION.md`
- Android module details: `dataanalytics-android/README.md`

## License

This project is licensed under the MIT License. See `LICENSE`.
