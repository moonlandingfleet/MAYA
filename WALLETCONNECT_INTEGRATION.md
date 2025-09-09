# WalletConnect Integration for MAYA Android App

This document provides instructions on how to set up and use the WalletConnect integration in the MAYA Android application.

## Setup Instructions

### 1. WalletConnect Project ID

To use WalletConnect, you need to obtain a Project ID from [WalletConnect Cloud](https://cloud.walletconnect.com/):

1. Sign up for a free account at WalletConnect Cloud
2. Create a new project and obtain your Project ID
3. Update the `WC_PROJECT_ID` in `gradle.properties` with your actual Project ID:

```
WC_PROJECT_ID=your_actual_project_id_here
```

### 2. Infura Project ID (for backend)

To fetch real wallet balances, you need an Infura Project ID:

1. Sign up for a free account at [Infura](https://infura.io/)
2. Create a new project and obtain your Project ID
3. Update the Infura URL in `maya-core/main.py`:

```python
w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"))
```

### 3. Backend Dependencies

Install the required Python dependencies for the backend:

```bash
cd maya-core
pip install -r requirements.txt
```

## Features Implemented

### 1. Wallet Connection

- QR code generation for WalletConnect pairing
- Session management for wallet connections
- Display of connected wallet address and balance

### 2. Real-time Balance Updates

- Fetch real ETH balances from the Ethereum network
- Display wallet balance in the app UI

### 3. Transaction Requests

- Request transactions from connected wallets
- Handle transaction approval/rejection responses

## Code Structure

```
app/src/main/java/com/mayaboss/android/
├── network/
│   └── WalletConnectManager.kt      # WalletConnect integration
├── model/
│   ├── Treasury.kt                  # Extended with wallet connection status
│   └── WalletSession.kt             # Wallet session data class
├── viewmodel/
│   └── MAYAViewModel.kt             # Updated with wallet state management
├── ui/
│   ├── MainScreen.kt                # Updated to show wallet info
│   └── WalletConnectScreen.kt       # New screen for wallet connection
└── MainActivity.kt                  # Updated with navigation

maya-core/
├── main.py                          # Updated with wallet balance endpoints
└── requirements.txt                 # Web3.py dependencies
```

## Testing

### Test Wallets

For testing purposes, you can use:

- Testnet wallets (Goerli, Sepolia)
- WalletConnect test suite
- Mock wallet applications

### Manual Testing

1. Build and run the Android app
2. Tap "Connect Wallet" button
3. Scan the QR code with a WalletConnect-compatible wallet (MetaMask, Trust Wallet, etc.)
4. Approve the connection in your wallet
5. Verify that the wallet address and balance are displayed in the app

## Security

The integration follows these security principles:

- **Non-custodial**: MAYA never holds private keys
- **User-controlled**: All transactions require explicit user approval
- **Transparent**: Transaction details are always shown to the user
- **Session-limited**: Wallet sessions have appropriate timeouts
- **Encrypted communication**: All WalletConnect communication is encrypted

## Future Enhancements

1. **Multi-chain support** - Extend beyond Ethereum to support Bitcoin and other chains
2. **Transaction history** - Display past transactions in the app
3. **Gas fee optimization** - Implement gas fee suggestions
4. **Wallet switching** - Allow users to switch between multiple connected wallets
5. **Advanced session management** - Persistent sessions across app restarts