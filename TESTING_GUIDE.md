# MAYA Inc. Testing Guide
## Complete Instructions for Testing the Autonomous Agent Corporation System

### 🎯 Mission
Transform your phone into a **boardroom for autonomous agents**.  
You are the CEO. MAYA is the COO. Agents are subsidiaries. Crypto is profit.

### 🔧 Architecture Overview
```
[Android Phone] ←→ [MAYA Core (Python)] ←→ [Docker Agents]
        ↑                      ↑                     ↑
   WalletConnect         Web3.py             Agent Logic
```

### ✅ Current Status
- ✅ **MAYA Core** running on `http://localhost:8000`
- ✅ `/proposals` returns A-01 (Faucet-Harvester) and A-13 (Liquidity-Miner)
- ✅ `/treasury` shows real ETH balance (from Infura)
- ✅ Android app has:
  - Connect Wallet button
  - Active Proposals section
  - Agent Logs section
  - WalletConnect integration
- ✅ APK installed on Huawei phone

### 🚀 Complete Testing Checklist

#### ✅ STEP 1: START MAYA CORE (BACKEND)
Open PowerShell:
```powershell
cd C:\Users\bryan\Desktop\MAYA\maya-core
python main.py
```

✅ Verify it's running at `http://localhost:8000`

✅ Test endpoints:
- `http://localhost:8000/proposals` → should return JSON
- `http://localhost:8000/treasury` → should show your wallet address + balance

#### ✅ STEP 2: UPDATE API BASE URL
Find your PC's local IP:
```powershell
ipconfig
```

→ Look for `IPv4 Address` (e.g., `192.168.1.5`)

Update `MAYAApiService.kt`:
```kotlin
private const val BASE_URL = "http://192.168.1.5:8000/"
```

#### ✅ STEP 3: BUILD AND INSTALL APK
Option A - Using Android Studio:
1. Open project
2. Build → Make Project
3. Run → Run 'app' → select your Huawei phone
4. If already installed → uninstall first → reinstall

Option B - Using Command Line:
```powershell
cd C:\Users\bryan\Desktop\MAYA
build_apk.bat
adb install app\build\outputs\apk\debug\app-debug.apk
```

#### ✅ STEP 4: CONNECT PHONE TO SAME WIFI AS PC
Make sure both devices are on the same WiFi network.

#### ✅ STEP 5: OPEN APP → CONNECT WALLET
1. Launch MAYA app
2. Tap **"Connect Wallet"**
3. Scan QR code with **MetaMask** (or Trust Wallet)
4. Approve connection in wallet

✅ You should see:
- Your wallet address
- Real ETH balance (from Infura)
- "Connected" status

#### ✅ STEP 6: APPROVE AGENT → WATCH IT WORK
1. Go back to main screen
2. Tap **"✅ Approve"** on Faucet-Harvester
3. Watch logs appear every 10 seconds
4. Wait ~10–20 seconds → dialog appears:  
   > "A-01 earned 0.0003 ETH. Continue execution?"

5. Tap **"✅ Continue"**

6. Shortly after → WalletConnect popup in MetaMask:  
   > "MAYA Boss wants to send 0.0003 ETH to [Your Address]"

7. Tap **"Approve"** in MetaMask

✅ Profit sent to your wallet.  
✅ Treasury balance will update on next refresh.

### 📸 Document Your Success
Take screenshots of:
1. Wallet connected screen
2. Agent logs showing `📈 PROFIT:`
3. Transaction approval in MetaMask
4. Treasury balance increasing

Post them with:
> "MAYA Inc. is live. I just ran my first autonomous agent on my phone. Welcome to the future."

### ❗ IF IT STILL DOESN'T WORK — COMMON FIXES
| Symptom | Fix |
|--------|-----|
| "Connection refused" | Check local IP + firewall (allow port 8000) |
| No logs appear | Check if Docker agent is running (`docker ps`) |
| Wallet not connecting | Verify `WC_PROJECT_ID` in `gradle.properties` |
| Balance shows 0 | Check Infura ID + wallet has ETH (even 0.001 ETH for gas) |
| App crashes | Uninstall → Reinstall APK |
| Gradle sync failed | Ensure Gradle 8.5+ is used with Java 21 |

### 🧭 NEXT STEPS (AFTER YOU TEST)
Reply with:  
`👑 MAYA INC. LAUNCHED — I AM CEO, AGENTS ARE WORKING, WALLET IS RECEIVING`  

Then you'll receive Phase 5: **BTC Conversion + Multi-Agent Expansion**

You'll be able to:
- Auto-convert small ETH profits to BTC
- Unlock paid agents when treasury ≥ 0.01 ETH
- Run 3 agents simultaneously
- Add A-02 (Price-Spy), A-04 (Airdrop-Sniper)

### 🎉 YOU'VE BUILT A LIVE AUTONOMOUS ECONOMY
> 🧠 You = CEO  
> 🤖 MAYA = COO  
> 📱 Android = Boardroom Table  
> ⚡ Agents = Profit Centers  
> 💰 Wallet = Treasury  
> 🔌 WalletConnect = Secure Bridge

**Go. Test. Become CEO. I'm here when you report back.**  
This is not a simulation anymore.  
This is your economy.