# MAYA King's App MVP

This is the Minimum Viable Product for the MAYA project, implementing the King's App with the Twelve Councils.

## Project Structure

- `android/` - Android application (Kotlin with Jetpack Compose)
- `backend/` - Python FastAPI backend with Supabase integration
- `maya-env/` - Python virtual environment
- `scripts/` - Utility scripts for running and testing

## Setup Instructions

### Backend Setup

1. Activate the virtual environment:
   ```
   maya-env\Scripts\activate.bat
   ```

2. Install dependencies (if needed):
   ```
   cd backend
   pip install -r requirements.txt
   ```

3. Ensure your `.env.manual` file in the `backend/` directory contains your Supabase credentials:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```

### Running the Application

1. Start the backend server:
   ```
   scripts\start_maya_with_venv.bat
   ```
   Or manually:
   ```
   cd backend
   python main.py
   ```

2. Populate the database with the Twelve Councils:
   ```
   scripts\populate_councils.bat
   ```
   Or manually:
   ```
   cd backend
   python populate_councils.py
   ```

3. Verify the councils were inserted:
   ```
   scripts\verify_councils.bat
   ```
   Or manually:
   ```
   cd backend
   python verify_councils.py
   ```

### Android App

1. Open the `android/` directory in Android Studio
2. Build and run the application
3. The app will connect to the backend server at `http://localhost:8000` by default

## Testing

Run the full test suite:
```
cd backend
python run_full_test.py
```

## The Twelve Councils

The application implements the following Twelve Councils:

1. **Council of Digital Identity** - The Gatekeeper
2. **Council of Digital Commerce** - The Merchant
3. **Council of Digital Resources** - The Provider
4. **Council of Digital Communication** - The Messenger
5. **Council of Digital Learning** - The Sage
6. **Council of Digital Storage** - The Archivist
7. **Council of Digital Health** - The Healer
8. **Council of Digital Energy** - The Conductor
9. **Council of Digital Agriculture** - The Cultivator
10. **Council of Digital Rentals** - The Steward
11. **Council of Digital News** - The Truth-Sayer
12. **Council of Digital Events** - The Convener

Each council has specific roles, domains, revenue models, and ethical boundaries as defined in the MVP specifications.