# MayaBoss - Bitcoin Routing Android Application

## Overview

MayaBoss is an Android application that gives phones three super-powers:
1. Hear spend-signals (coffee, airtime, Uber)
2. Offer discount if user pays via Lightning Network
3. Collect routing + rebate fees in BTC only, no fiat touch

## Project Structure

This project implements the "Brick 2" functionality from the specification document:
- Safe Lightning invoice + QR (testnet)
- Uses pre-made testnet invoice string
- ZXing library to convert string to QR bitmap
- Shows QR in dialog with copy/share buttons

## Features Implemented

1. **QR Code Generation**: Using ZXing library to generate Lightning Network payment QR codes
2. **Static Invoice Display**: Shows a pre-defined testnet Lightning invoice
3. **Offer Display**: RecyclerView showing available merchant offers
4. **Payment Notifications**: Simulated payment notifications
5. **Cloud Worker Integration**: Retrofit client for fetching offers from cloud workers

## Technology Stack

- **Mobile Platform**: Android (Kotlin)
- **Lightning Network**: Testnet invoice (mainnet ready)
- **QR Code Generation**: ZXing library
- **Backend**: Retrofit for REST API communication
- **UI**: Material Design components

## Building the Project

### Prerequisites

- Android Studio
- Android SDK
- Kotlin plugin

### Steps

1. Open the project in Android Studio
2. Sync the project with Gradle files
3. Build the project using `Build > Make Project`

### Dependencies

All dependencies are specified in the `app/build.gradle` file:
- AndroidX libraries
- ZXing Android Embedded for QR code generation
- Retrofit for network requests
- Gson for JSON serialization

## Deployment to Huawei Device

For detailed instructions on deploying to Huawei devices, please refer to the [Huawei Deployment Guide](HUAWEI_DEPLOYMENT.md).

### Quick Steps
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

6. Install APK on device:
   ```
   adb install path/to/your/app.apk
   ```
   - For first-time installation, you may need to uninstall any existing version:
     ```
     adb uninstall com.mayaboss.android
     ```

7. Launch the application:
   - Find "MayaBoss" in your app drawer
   - Or launch via ADB:
     ```
     adb shell am start -n com.mayaboss.android/.MainActivity
     ```

## Next Steps

To implement the full functionality described in the specification:

1. **Brick 3 - Cloud worker fleet**:
   - Deploy RouteBot, RebateBot, and SwapBot Docker containers on Fly.io
   - Implement proper REST endpoints for each worker
   - Update the BASE_URL in OfferService.kt with actual worker URLs

2. **Brick 4 - Mainnet flip**:
   - Open Bitcoin mainnet channels
   - Update the Lightning invoice to use mainnet
   - Sign rebate deals with merchants

## Risk Mitigation

| Risk | Probability | Mitigation |
|------|-------------|------------|
| App crash on crypto call | Low | Uses static invoice until library stable |
| Phone offline | Medium | Worker queues offers; retries when back |
| Regulatory | Low | No fiat custody → no MSB |
| BTC price drop | External | Income = sats, spend = sats, hedge optional |

## Success Metrics

| Milestone | Metric | Tool |
|-----------|--------|------|
| Brick 2 done | 21 sats received | Bluewallet testnet payment |
| Brick 3 done | 3 offers / hour | Worker /metrics endpoint |
| Brick 4 done | > 50 payments / week | Channel forwarding events |
| Pilot done | 0.01 BTC / month creator slice | On-chain csv export |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.