# MayaBoss - Bitcoin Routing Android Application

## Project Status

**Important Note**: This project is currently conceptual and based on the specification document [inc.md](../inc.md). There is no existing Android project structure in the repository. To deploy this application to your Huawei device, you will first need to implement the application according to the design outlined in this document.

## Overview

MayaBoss is a conceptual Android application that gives phones three super-powers:
1. Hear spend-signals (coffee, airtime, Uber)
2. Offer discount if user pays via Lightning Network
3. Collect routing + rebate fees in BTC only, no fiat touch

This document outlines the design and implementation approach to create this application and deploy it to an Android device.

## Architecture

The application consists of two main components:

1. **Mobile Application (Android)**
   - Displays Lightning Network payment QR codes
   - Receives payment notifications
   - Communicates with cloud workers

2. **Cloud Workers (Docker Containers)**
   - RouteBot: Handles payment routing
   - RebateBot: Manages merchant rebates
   - SwapBot: Facilitates currency swaps

## Technology Stack

- **Mobile Platform**: Android (Java/Kotlin)
- **Lightning Network**: LND or similar implementation
- **QR Code Generation**: ZXing library
- **Backend**: Docker containers hosted on Fly.io
- **Communication**: REST APIs between mobile app and cloud workers
- **Payment Processing**: Lightning Network protocols

## Implementation Plan

### Phase 1: Basic Android Application
1. Create a basic Android project
2. Integrate ZXing library for QR code generation
3. Implement static Lightning invoice display
4. Add payment notification handling

### Phase 2: Cloud Worker Integration
1. Develop Docker containers for RouteBot, RebateBot, and SwapBot
2. Implement REST endpoints for each worker
3. Create polling mechanism in Android app
4. Display offers from cloud workers

### Phase 3: Mainnet Integration
1. Configure Bitcoin mainnet channels
2. Implement real merchant rebate functionality
3. Add security measures for production use

## Deployment to Huawei Device

### Prerequisites
- Huawei Android device with USB debugging enabled
- USB cable for connection
- Android Studio or ADB tools installed on development machine

### Steps
1. Enable Developer Options on Huawei device:
   - Go to Settings > About phone
   - Tap "Build number" 7 times
   - Return to Settings > System & updates > Developer options
   - Enable "USB debugging"

2. (Optional) Disable USB debugging security check on Huawei devices:
   - In Developer Options, find "Verify apps over USB" and disable it
   - This prevents potential installation issues

3. Connect device to computer via USB

4. Verify device connection:
   ```
   adb devices
   ```
   - If your device shows up, you're ready to proceed
   - If not, check USB cable and driver installation

5. Build APK:
   - In Android Studio: Build > Build Bundle(s) / APK(s) > Build APK
   - Or use command line build tools

6. Install APK on device:
   ```
   adb install path/to/your/app.apk
   ```
   - For first-time installation, you may need to uninstall any existing version:
     ```
     adb uninstall [package-name]
     ```

7. Launch the application:
   - Find "MayaBoss" in your app drawer
   - Or launch via ADB:
     ```
     adb shell am start -n [package-name]/[activity-name]
     ```

### Troubleshooting Huawei-specific Issues

1. **Installation blocked by phone**:
   - Check "Settings > Apps > Special access > Install unknown apps"
   - Allow installation from your computer/USB source

2. **USB debugging not working**:
   - Try different USB connection modes (File transfer, MTP, etc.)
   - Try a different USB cable
   - Ensure proper USB drivers are installed on your computer

3. **App crashes on launch**:
   - Check logcat output for error messages:
     ```
     adb logcat
     ```
   - Ensure all required permissions are granted

4. **Performance issues**:
   - Huawei devices may have aggressive battery optimization
   - Disable battery optimization for MayaBoss in Settings > Battery

## Lightning Network Integration

Based on research, there are several approaches to integrate Lightning Network functionality in mobile applications:

1. **LND (Lightning Network Daemon)**:
   - Can be cross-compiled to Android using gomobile
   - Provides full node functionality
   - Requires significant resources

2. **LDK (Lightning Development Kit)**:
   - SDK specifically designed for mobile applications
   - Focuses on non-custodial mobile nodes
   - More lightweight than full LND implementation

3. **Eclair Mobile**:
   - Existing Android wallet implementation
   - Can serve as reference implementation

For the MayaBoss application, a lightweight approach using LDK would be most appropriate since the primary function is routing rather than full node functionality.

## QR Code Generation with ZXing

The ZXing (Zebra Crossing) library is a popular choice for QR code generation in Android applications:

1. **Library Integration**:
   - Add ZXing Android Embedded library to project dependencies
   - No need to include full ZXing library if only generating QR codes

2. **Implementation Steps**:
   - Create BarcodeEncoder instance
   - Generate BitMatrix from string content
   - Convert BitMatrix to Bitmap for display
   - Display in ImageView or custom dialog

3. **Usage Considerations**:
   - Ensure proper error correction level for payment QR codes
   - Size QR code appropriately for scanning distance
   - Add appropriate padding around QR code

## Cloud Worker Deployment on Fly.io

The cloud workers (RouteBot, RebateBot, SwapBot) can be deployed as Docker containers on Fly.io:

1. **Container Preparation**:
   - Create Dockerfile for each worker service
   - Define REST endpoints for offer generation
   - Implement proper error handling

2. **Fly.io Deployment**:
   - Install Fly.io CLI tools
   - Run `fly launch` in each worker directory
   - Configure resource allocation for free tier usage
   - Set up health checks and monitoring

3. **API Contract**:
   - Standardized JSON response format
   - Consistent endpoint paths across workers
   - Proper HTTP status codes for error conditions

## Security Considerations

- Non-custodial approach means no fiat custody, reducing regulatory requirements
- Phone acts as key holder and decision maker
- Cloud workers are stateless and cannot move funds without phone-signed JWT
- Follow Lightning Network security best practices
- Implement proper encryption for communication between app and workers

## Testing Strategy

1. **Unit Testing**:
   - Test QR code generation
   - Verify Lightning invoice handling
   - Test REST API communication

2. **Integration Testing**:
   - End-to-end payment flow
   - Cloud worker communication
   - Device-specific functionality on Huawei

3. **User Acceptance Testing**:
   - Real payment scenarios
   - Merchant rebate functionality
   - Performance under various network conditions

## Risk Mitigation

| Risk | Probability | Mitigation |
|------|-------------|------------|
| App crash on crypto call | High | Use static invoice until library stable |
| Phone offline | Medium | Worker queues offers; retries when back |
| Regulatory | Low | No fiat custody → no MSB |
| BTC price drop | External | Income = sats, spend = sats, hedge optional |

## Success Metrics

| Milestone | Metric | Tool |
|-----------|--------|------|
| Basic QR functionality | 21 sats received | Bluewallet testnet payment |
| Cloud worker integration | 3 offers / hour | Worker /metrics endpoint |
| Mainnet functionality | > 50 payments / week | Channel forwarding events |
| Pilot program | 0.01 BTC / month creator slice | On-chain csv export |