# MAYA Inc. - Autonomous Agent Corporation
## Project Summary and Testing Instructions

### Project Overview
MAYA Inc. transforms your Android phone into a **boardroom for autonomous agents**:
- **You**: CEO
- **MAYA**: COO (Core Operations)
- **Agents**: Subsidiaries that generate revenue
- **Crypto**: Profit distribution

### Key Components

1. **MAYA Core (Backend)**
   - Python FastAPI server
   - Web3.py for Ethereum integration
   - Docker container management
   - REST API endpoints for agent communication

2. **Android App (Frontend)**
   - Kotlin with Jetpack Compose
   - WalletConnect v2 integration
   - Agent management UI
   - Real-time log monitoring

3. **Dockerized Agents**
   - A-01 Faucet-Harvester: Claims ETH from testnet faucets
   - A-13 Liquidity-Miner: Provides liquidity to DEX pools (locked until treasury ≥ 0.01 ETH)

### Recent Updates Made

1. **README.md**: Updated to accurately describe the autonomous agent corporation system instead of the Bitcoin routing app
2. **strings.xml**: Updated string resources to reflect agent system terminology
3. **AndroidManifest.xml**: Updated to use string resources for app name
4. **LICENSE**: Added MIT License file
5. **gradle-wrapper.properties**: Confirmed using Gradle 8.5 for Java 21 compatibility

### Testing Instructions

#### Prerequisites
1. Android device with USB debugging enabled
2. Same WiFi network for PC and Android device
3. MetaMask or Trust Wallet installed on Android device
4. Docker installed (for running agents)

#### Step 1: Start the Backend Server
```powershell
cd C:\Users\bryan\Desktop\MAYA\maya-core
python main.py
```

Verify the server is running by accessing:
- http://localhost:8000/proposals
- http://localhost:8000/treasury

#### Step 2: Update API Base URL
1. Find your PC's local IP address:
   ```powershell
   ipconfig
   ```
2. Update the BASE_URL in `MAYAApiService.kt`:
   ```kotlin
   private const val BASE_URL = "http://YOUR_LOCAL_IP:8000/"
   ```
   Replace `YOUR_LOCAL_IP` with your actual IP (e.g., 192.168.1.5)

#### Step 3: Build and Install the Android App
Option 1 - Using Android Studio:
1. Open the project in Android Studio
2. Sync the project with Gradle files
3. Build the project using `Build > Make Project`
4. Run the app on your connected device

Option 2 - Using the build script:
1. Run the build script:
   ```powershell
   C:\Users\bryan\Desktop\MAYA\build_apk.bat
   ```
2. Install the APK manually:
   ```powershell
   adb install app\build\outputs\apk\debug\app-debug.apk
   ```

#### Step 4: Connect Your Wallet
1. Launch the MAYA app on your Android device
2. Tap "🔌 Connect Wallet"
3. Scan the QR code with MetaMask or Trust Wallet
4. Approve the connection in your wallet
5. Verify that your wallet address and balance are displayed

#### Step 5: Approve and Run Agents
1. Go back to the main screen
2. Tap "✅ Approve" on the Faucet-Harvester agent
3. Watch the logs appear every 10 seconds at the bottom of the screen
4. After ~20 seconds, a dialog will appear:
   > "A-01 earned 0.0003 ETH. Continue execution?"
5. Tap "✅ Continue"
6. Shortly after, you'll receive a transaction request in MetaMask:
   > "MAYA Boss wants to send 0.0003 ETH to [Your Address]"
7. Tap "Approve" in MetaMask
8. Check that the treasury balance updates on the next refresh

### Troubleshooting

#### Common Issues and Solutions

| Symptom | Fix |
|--------|-----|
| "Connection refused" | Check local IP + firewall (allow port 8000) |
| No logs appear | Check if Docker agent is running (`docker ps`) |
| Wallet not connecting | Verify `WC_PROJECT_ID` in `gradle.properties` |
| Balance shows 0 | Check Infura ID + wallet has ETH (even 0.001 ETH for gas) |
| App crashes | Uninstall → Reinstall APK |
| Gradle sync failed | Ensure Gradle 8.5+ is used with Java 21 |

#### ADB Commands for Manual Testing
```powershell
# Check connected devices
adb devices

# Install APK
adb install app\build\outputs\apk\debug\app-debug.apk

# Uninstall existing app
adb uninstall com.mayaboss.android

# Launch app
adb shell am start -n com.mayaboss.android/.MainActivity

# View app logs
adb logcat -s "MAYA"
```

### Next Steps for Development

1. **BTC Conversion**: Implement `/convert-to-btc` endpoint using Uniswap API
2. **Multi-Agent Support**: Allow 3 agents to run simultaneously
3. **Agent Expansion**: Add A-02 (Price-Spy), A-04 (Airdrop-Sniper)
4. **Queue System**: Add queue for overflow agents
5. **Push Notifications**: Notify when profit occurs

### Success Metrics

| Milestone | Metric | Verification |
|-----------|--------|--------------|
| Wallet Connected | Wallet address displayed | App main screen |
| Agent Running | Logs appearing | App log viewer |
| Profit Generated | "📈 PROFIT:" in logs | App log viewer |
| Transaction Sent | ETH balance increase | Wallet balance |
| Decision Approved | Dialog interaction | App UI |

This summary provides a comprehensive overview of your autonomous agent corporation system and instructions for testing its functionality.