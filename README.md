# Data Analytics Platform

![Version](https://img.shields.io/badge/version-2.0.0-blue?style=for-the-badge)
![Android](https://img.shields.io/badge/Android-APK-3DDC84?style=for-the-badge&logo=android)
![Windows](https://img.shields.io/badge/Windows-EXE-0078D6?style=for-the-badge&logo=windows)
![Linux](https://img.shields.io/badge/Linux-Binary-FCC624?style=for-the-badge&logo=linux)
![iOS](https://img.shields.io/badge/iOS-IPA-black?style=for-the-badge&logo=apple)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

Cross-platform data analytics suite with:
- Android app
- iOS app (unsigned IPA build artifact)
- Desktop analyzer app (Windows EXE + Linux binary)
- Web learning resources and analytics dashboard assets

## Clean Repository Structure

```text
Data-Analytics/
├── .github/workflows/                 # CI/CD build and release
├── apps/
│   ├── android/dataanalytics-android/ # Android app
│   ├── desktop/                       # Desktop analyzer (Python + Tkinter)
│   └── ios/                           # iOS app source (SwiftUI + XcodeGen)
├── data/resources/                    # Learning resources
├── docs/                              # Setup and developer docs
├── scripts/                           # Utility and content generation scripts
├── web/                               # Web pages, web assets, JSON data
└── dist/release-package/              # Legacy packaged outputs
```

## Desktop Analyzer Features

- Analyze CSV/JSON datasets
- Dataset profile: rows, columns, missing values, duplicates
- Numeric summary statistics
- Top correlations
- Simple anomaly count using z-score threshold
- Export report to JSON

## Build and Run

### Desktop (local)
```bash
cd apps/desktop
pip install -r requirements.txt
python app.py
```

### Android (local)
```bash
cd apps/android/dataanalytics-android
./gradlew assembleDebug
```

### iOS (local, macOS)
```bash
cd apps/ios
xcodegen generate
xcodebuild -project DataAnalyticsIOS.xcodeproj -scheme DataAnalyticsIOS -configuration Release -sdk iphoneos CODE_SIGNING_ALLOWED=NO CODE_SIGNING_REQUIRED=NO
```

## Automated Releases

Push a tag like `v2.0.0` to trigger:
- `DataAnalytics-android.apk`
- `DataAnalytics-windows.exe`
- `DataAnalytics-linux`
- `DataAnalytics-ios-unsigned.ipa`

Published under GitHub Releases.

## License

MIT
