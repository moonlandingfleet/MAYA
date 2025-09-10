# MAYA Inc. - Autonomous Agent Corporation

## Overview

MAYA Inc. transforms your Android phone into a **boardroom for autonomous agents**. You are the CEO. MAYA is the COO. Agents are subsidiaries. Crypto is profit.

MAYA v0.2 — One mind, many hands.

## Project Structure

This project implements an autonomous agent corporation with the following components:
- **MAYA Core**: Python FastAPI backend server running on `localhost:8000`
- **Dockerized Agents**: Autonomous bots that perform tasks and generate revenue
- **Android App**: Jetpack Compose UI for managing agents and connecting to wallets
- **WalletConnect Integration**: Secure connection to MetaMask/Trust Wallet for transaction approvals

## Features Implemented

1. **Agent Management**: View, approve, and monitor autonomous agents
2. **WalletConnect Integration**: Connect to Ethereum wallets via QR code
3. **Real-time Balance Updates**: Fetch ETH balances from the Ethereum network via Infura
4. **Decision Engine**: Approve/Reject agent actions every 10 minutes
5. **Profit Tracking**: Monitor agent logs and treasury balance
6. **Transaction Requests**: Send profits to your wallet via WalletConnect

## Technology Stack

- **Mobile Platform**: Android (Kotlin, Jetpack Compose)
- **Backend**: Python FastAPI with Web3.py
- **Containerization**: Docker for agent deployment
- **Blockchain**: Ethereum integration via Infura
- **Wallet Integration**: WalletConnect v2 protocol
- **Networking**: Retrofit for REST API communication
- **UI**: Material Design 3 (Jetpack Compose)

## Building the Project

### Prerequisites

- Android Studio
- Android SDK
- Python 3.7+
- Docker (for running agents)
- Kotlin plugin

### Backend Setup

1. Navigate to the maya-core directory:
   ```
   cd maya-core
   ```

2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Start the backend server:
   ```
   python main.py
   ```

4. Verify the server is running at `http://localhost:8000`

### Android App Setup

1. Open the project in Android Studio
2. Update the BASE_URL in `MAYAApiService.kt` with your PC's local IP address:
   ```kotlin
   private const val BASE_URL = "http://YOUR_LOCAL_IP:8000/"
   ```
3. Sync the project with Gradle files
4. Build the project using `Build > Make Project`

### Dependencies

All dependencies are specified in the respective files:
- `app/build.gradle`: Android app dependencies
- `maya-core/requirements.txt`: Python backend dependencies

## Deployment to Android Device

### Quick Steps
1. Enable Developer Options on your Android device:
   - Go to Settings > About phone
   - Tap "Build number" 7 times
   - Return to Settings > System > Developer options
   - Enable "USB debugging"

2. Connect device to computer via USB

3. Verify device connection:
   ```
   adb devices
   ```
   - If your device shows up, you're ready to proceed
   - If not, check USB cable and driver installation

4. Build APK:
   - In Android Studio: Build > Build Bundle(s) / APK(s) > Build APK
   - Or use the build script: `build_apk.bat`

5. Install APK on device:
   ```
   adb install app/build/outputs/apk/debug/app-debug.apk
   ```
   - For first-time installation, you may need to uninstall any existing version:
     ```
     adb uninstall com.mayaboss.android
     ```

6. Launch the application:
   - Find "MAYA" in your app drawer
   - Or launch via ADB:
     ```
     adb shell am start -n com.mayaboss.android/.MainActivity
     ```

## Running the Complete System

### Step 1: Start the Backend Server
```
cd maya-core
python main.py
```

### Step 2: Connect Phone to Same WiFi as PC
Find your PC's local IP address:
```
ipconfig
```
Look for the IPv4 Address (e.g., 192.168.1.5) and update `MAYAApiService.kt` accordingly.

### Step 3: Build and Install the Android App
Use Android Studio or the build script to create and install the APK.

### Step 4: Connect Your Wallet
1. Launch the MAYA app
2. Tap "Connect Wallet"
3. Scan the QR code with MetaMask or Trust Wallet
4. Approve the connection in your wallet

### Step 5: Approve and Run Agents
1. Tap "Approve" on the Faucet-Harvester agent
2. Watch logs appear every 10 seconds
3. After ~20 seconds, a dialog will appear asking you to continue execution
4. Tap "Continue"
5. Approve the transaction in MetaMask when requested
6. Check that the treasury balance updates

## Current Agents

1. **A-01 Faucet-Harvester**: Claims ETH from testnet faucets every 10 minutes
2. **A-13 Liquidity-Miner**: Provides liquidity to DEX pools for fees (locked until treasury ≥ 0.01 ETH)

## Risk Mitigation

| Risk | Probability | Mitigation |
|------|-------------|------------|
| Agent failure | Low | Docker containers with restart policies |
| Network issues | Medium | Local backend with retry mechanisms |
| Wallet connection loss | Low | Session persistence and reconnection |
| Transaction failure | Low | Error handling and user notifications |

## Success Metrics

| Milestone | Metric | Tool |
|-----------|--------|------|
| Agent running | Agent logs appearing | App log viewer |
| Profit generated | "📈 PROFIT:" lines in logs | App log viewer |
| Transaction sent | ETH balance increase | Wallet balance |
| Decision approval | User interaction with dialog | App UI |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.