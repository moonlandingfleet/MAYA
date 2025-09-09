# Running the MAYA Application with WalletConnect Integration

This document provides instructions on how to build and run the MAYA Android application with WalletConnect integration.

## Prerequisites

1. Android Studio (latest version recommended)
2. Android SDK (API level 24 or higher)
3. Python 3.7 or higher for the backend
4. Node.js and npm (for frontend development tools)

## Setting up the Android App

### 1. Open the Project

1. Open Android Studio
2. Select "Open an existing Android Studio project"
3. Navigate to the MAYA project directory and open it

### 2. Configure WalletConnect

1. Obtain a Project ID from [WalletConnect Cloud](https://cloud.walletconnect.com/)
2. Update the `WC_PROJECT_ID` in `gradle.properties` with your actual Project ID

### 3. Build the Project

1. In Android Studio, select "Build" > "Make Project"
2. Wait for the build to complete successfully

### 4. Run the App

1. Connect an Android device or start an emulator
2. Select "Run" > "Run 'app'" from the menu
3. Select your target device when prompted

## Setting up the Backend

### 1. Install Dependencies

```bash
cd maya-core
pip install -r requirements.txt
```

### 2. Configure Infura

1. Obtain an Infura Project ID from [Infura](https://infura.io/)
2. Update the Infura URL in `maya-core/main.py`:

```python
w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"))
```

### 3. Run the Backend

```bash
cd maya-core
python main.py
```

The backend will start on `http://localhost:8000`

## Using WalletConnect

### 1. Connect Your Wallet

1. Launch the MAYA Android app
2. Tap the "Connect Wallet" button
3. Scan the QR code with a WalletConnect-compatible wallet (MetaMask, Trust Wallet, etc.)
4. Approve the connection in your wallet

### 2. View Wallet Information

Once connected, the app will display:
- Wallet address
- Real-time ETH balance
- Connection status

### 3. Transaction Requests

The app can request transactions from your wallet:
1. When an agent generates profit, you'll be prompted to approve a transaction
2. Review the transaction details in your wallet
3. Approve or reject the transaction

## Troubleshooting

### Common Issues

1. **Build Failures**: Ensure all dependencies are correctly installed
2. **Wallet Connection Failures**: Verify your WalletConnect Project ID is correct
3. **Balance Not Updating**: Check your Infura connection and network connectivity

### Debugging

1. Check the Android logcat for error messages
2. Verify the backend is running and accessible
3. Ensure your wallet app is properly configured

## Testing

### Unit Tests

Run the unit tests from Android Studio:
1. Right-click on the test package
2. Select "Run Tests"

### Manual Testing

1. Test wallet connection with various wallets
2. Verify balance updates are working
3. Test transaction approval flows
4. Check error handling scenarios

## Development

### Code Structure

The WalletConnect integration is organized as follows:

- `network/WalletConnectManager.kt`: Core WalletConnect functionality
- `model/WalletSession.kt`: Wallet session data model
- `viewmodel/MAYAViewModel.kt`: Wallet state management
- `ui/WalletConnectScreen.kt`: Wallet connection UI
- `ui/MainScreen.kt`: Main UI with wallet information
- `maya-core/main.py`: Backend with wallet balance endpoints

### Adding New Features

1. Extend the WalletConnectManager for new functionality
2. Update the ViewModel to manage new state
3. Create new UI components as needed
4. Add backend endpoints for coordination