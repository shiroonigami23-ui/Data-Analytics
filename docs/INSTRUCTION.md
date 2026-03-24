# INSTRUCTION

## 1. Prerequisites

- Windows PowerShell
- JDK 17 installed
- Android SDK installed
- Git installed

## 2. Clone and Open

```powershell
git clone https://github.com/shiroonigami23-ui/Data-Analytics.git
cd Data-Analytics
```

Android project location:

- `dataanalytics-android/`

## 3. Configure Android SDK (if needed)

Create `dataanalytics-android/local.properties` if it does not exist:

```properties
sdk.dir=C:\\Users\\<your-user>\\AppData\\Local\\Android\\Sdk
```

## 4. Build APK

```powershell
cd dataanalytics-android
.\gradlew.bat clean assembleDebug
```

APK output:

- `app/build/outputs/apk/debug/app-debug.apk`

## 5. Install APK on Device

```powershell
adb install -r app\build\outputs\apk\debug\app-debug.apk
```

Or manually copy/install:

- `release-package/DataAnalyticsAndroid-debug.apk`

## 6. Repo Package Contents

- Android source and Gradle wrapper
- `LICENSE`
- Updated `README.md`
- `release-package/` with APK + checksum + zip

## 7. Commit and Push

```powershell
git add .
git commit -m "Finalize Android app, docs, license, and APK package"
git push origin main
```

If your default branch is not `main`, replace it with your branch name.
