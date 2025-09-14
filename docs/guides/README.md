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
7. **Digital Ministries Management**: Store and manage information about the 12 Digital Ministries
8. **Proposal Tracking**: Manage funding requests from Councils
9. **Treasury Management**: Log all financial movements
10. **Opportunity Tracking**: Record potential opportunities before they become formal proposals

## Technology Stack

- **Mobile Platform**: Android (Kotlin, Jetpack Compose)
- **Backend**: Python FastAPI with Web3.py
- **Containerization**: Docker for agent deployment
- **Blockchain**: Ethereum integration via Infura
- **Wallet Integration**: WalletConnect v2 protocol
- **Database**: Supabase (PostgreSQL) for persistent data storage
- **Networking**: Retrofit for REST API communication
- **UI**: Material Design 3 (Jetpack Compose)

## Building the Project

### Prerequisites

- Android Studio
- Android SDK
- Python 3.7+
- Docker (for running agents)
- Kotlin plugin
- Supabase account (for database integration)

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install Supabase dependencies:
   ```
   pip install supabase==2.4.5
   ```

4. Set up your Supabase project:
   - Create a new project at https://supabase.com
   - Get your project URL and API key
   - Set environment variables:
     ```
     export SUPABASE_URL=your_project_url
     export SUPABASE_KEY=your_api_key
     ```

5. Deploy the database schema:
   - Execute the SQL in `backend/api/maya_supabase/schema.sql` in your Supabase SQL editor

6. Start the backend server:
   ```
   python main.py
   ```

7. Verify the server is running at `http://localhost:8000`

### Android App Setup

1. Navigate to the android directory:
   ```
   cd android
   ```

2. Open the project in Android Studio
3. Update the BASE_URL in `app/src/main/java/com/mayaboss/android/network/MAYAApiService.kt` with your PC's local IP address:
   ```kotlin
   private const val BASE_URL = "http://YOUR_LOCAL_IP:8000/"
   ```
4. Sync the project with Gradle files
5. Build the project using `Build > Make Project`

### Dependencies

All dependencies are specified in the respective files:
- `android/app/build.gradle`: Android app dependencies
- `backend/requirements.txt`: Python backend dependencies

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
   - Or use the build script: `scripts/build_apk.bat`

5. Install APK on device:
   ```
   adb install android/app/build/outputs/apk/debug/app-debug.apk
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
cd backend
python main.py
```

### Supabase Integration

The MAYA backend includes a complete Supabase integration for managing the Digital Ministries ecosystem:

1. **Councils API**: Manage the 12 Digital Ministries
2. **Proposals API**: Handle funding requests from Councils
3. **Treasury API**: Track all financial movements
4. **Opportunities API**: Record potential opportunities

All endpoints are available under the `/supabase` prefix. See `backend/api/maya_supabase/USAGE.md` for detailed API documentation.

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

## Documentation

For detailed information about specific components, see:

- `backend/api/maya_supabase/README.md` - Supabase integration documentation
- `backend/api/maya_supabase/USAGE.md` - Usage guide for the Supabase integration
- `backend/api/maya_supabase/SUMMARY.md` - Implementation summary
- `docs/guides/WALLETCONNECT_INTEGRATION.md` - WalletConnect implementation details
- `docs/setup/RUNNING_THE_APP.md` - Detailed running instructions
- `docs/testing/TESTING_GUIDE.md` - Testing procedures

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.