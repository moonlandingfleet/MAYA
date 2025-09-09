# Huawei Deployment Guide for MAYA Android App

This document provides detailed instructions for deploying the MAYA Android application on Huawei devices, including verification steps to ensure proper installation and functionality.

## Prerequisites

1. Huawei Android device with USB debugging enabled
2. USB cable for connection
3. Android Studio or ADB tools installed on development machine
4. Built APK file of the MAYA application

## Enable Developer Options on Huawei Device

1. Go to Settings > About phone
2. Tap "Build number" 7 times
3. Return to Settings > System & updates > Developer options
4. Enable "USB debugging"
5. (Optional) In Developer Options, find "Verify apps over USB" and disable it to prevent installation issues

## Connection and Verification

### 1. Connect Device to Computer

1. Connect your Huawei device to your computer using the USB cable
2. If prompted on your device, select "File transfer" or "MTP" mode
3. If prompted to allow USB debugging, tap "Allow" and check "Always allow from this computer"

### 2. Verify Device Connection

Open a terminal or command prompt and run:

```bash
adb devices
```

You should see your device listed. If not:
- Check your USB cable connection
- Ensure USB debugging is enabled
- Try a different USB port
- Install Huawei USB drivers if needed

## Build and Install APK

### 1. Build APK

You can build the APK in two ways:

**Option A: Using Android Studio**
1. Open the project in Android Studio
2. Select "Build" > "Build Bundle(s) / APK(s)" > "Build APK"
3. Wait for the build to complete
4. Click "locate" in the notification to find the APK file

**Option B: Using Command Line**
1. Navigate to the project root directory
2. Run the build script:
   ```bash
   build_apk.bat
   ```
3. The APK will be generated in `app/build/outputs/apk/debug/`

### 2. Install APK on Device

1. Uninstall any existing version of the app:
   ```bash
   adb uninstall com.mayaboss.android
   ```

2. Install the new APK:
   ```bash
   adb install path/to/your/app-debug.apk
   ```

   Replace `path/to/your/app-debug.apk` with the actual path to your APK file.

## Launch the Application

### Option 1: Using ADB
```bash
adb shell am start -n com.mayaboss.android/.MainActivity
```

### Option 2: Manual Launch
1. Find "MayaBoss" in your app drawer
2. Tap the icon to launch the application

## Verification Steps

### 1. Basic Functionality Verification

1. Launch the app and verify the main screen loads correctly
2. Check that the UI elements are properly displayed
3. Verify that the offer list is populated (either from API or mock data)

### 2. WalletConnect Integration Verification

1. Tap the "Connect Wallet" button
2. Verify that a QR code is generated
3. Scan the QR code with a WalletConnect-compatible wallet (MetaMask, Trust Wallet, etc.)
4. Approve the connection in your wallet
5. Verify that the wallet address and balance are displayed in the app

### 3. Transaction Request Verification

1. With a wallet connected, try to request a transaction
2. Verify that the transaction request is sent to your wallet
3. Approve or reject the transaction in your wallet
4. Verify that the app handles both responses correctly

### 4. Backend Connectivity Verification

1. Ensure the backend server is running
2. Verify that the app can fetch proposals from the backend
3. Check that agent logs are displayed correctly
4. Verify that treasury information is updated

## Troubleshooting

### Common Issues and Solutions

1. **Device not recognized by ADB**
   - Ensure USB debugging is enabled
   - Try a different USB cable
   - Install Huawei USB drivers
   - Try a different USB port

2. **Installation failures**
   - Ensure you've uninstalled any existing version
   - Check available storage space on the device
   - Verify the APK is not corrupted

3. **App crashes on launch**
   - Check logcat for error messages
   - Verify all dependencies are correctly included
   - Ensure the backend URL is correctly configured

4. **WalletConnect connection issues**
   - Verify your WalletConnect Project ID is correct
   - Check network connectivity
   - Ensure the wallet app is properly configured

### Checking Logs

To debug issues, you can check the Android logs:

```bash
adb logcat
```

To filter logs for your app only:

```bash
adb logcat -s "MAYA"
```

## Huawei-Specific Considerations

### 1. App Gallery Submission

If you plan to distribute the app through Huawei App Gallery:

1. Register as a developer on Huawei Developer website
2. Prepare app screenshots and descriptions
3. Ensure your app complies with Huawei App Gallery guidelines
4. Submit your app for review

### 2. Huawei Mobile Services (HMS)

For enhanced functionality on Huawei devices:

1. Integrate HMS Core if needed for push notifications or other services
2. Test the app on Huawei devices with HMS instead of Google Play Services
3. Ensure all features work correctly without Google Play Services

## Performance Optimization

### 1. Battery Usage

1. Test the app's battery consumption over time
2. Optimize background processes
3. Use appropriate wake locks if needed

### 2. Memory Usage

1. Monitor memory usage during extended operation
2. Optimize image loading and caching
3. Clean up resources properly

## Security Considerations

1. Ensure all network communications are secure
2. Protect sensitive data stored on the device
3. Validate all inputs to prevent injection attacks
4. Follow Android security best practices

## Version Management

1. Update version codes and names in `app/build.gradle`
2. Maintain a changelog of features and fixes
3. Test upgrades from previous versions

This guide should help you successfully deploy and verify the MAYA application on Huawei devices. If you encounter any issues not covered in this document, please refer to the main README.md and other documentation files in the project.