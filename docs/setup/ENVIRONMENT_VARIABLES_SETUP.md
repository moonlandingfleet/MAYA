# Environment Variables Setup for MAYA Supabase Integration

## Overview

This document summarizes the setup of environment variables for the MAYA project's Supabase integration. The setup includes creating a `.env` file, adding it to `.gitignore`, installing the `python-dotenv` library, and updating the code to use environment variables.

## Completed Tasks

### 1. Created `.env` File
- **Location**: `backend/.env`
- **Content**:
  ```
  SUPABASE_URL=https://ksrvtvqqikwjbqzpgacs.supabase.co
  SUPABASE_KEY=your_actual_supabase_service_role_key
  ```
- **Purpose**: Store sensitive configuration data separately from code

### 2. Updated `.gitignore` File
- **Location**: `.gitignore` (in root directory)
- **Added Line**: `.env`
- **Purpose**: Prevent accidental commits of sensitive data to the repository

### 3. Installed `python-dotenv` Library
- **Command**: `pip install python-dotenv`
- **Version Installed**: 1.1.1
- **Purpose**: Enable loading of environment variables from `.env` file

### 4. Updated `requirements.txt`
- **Added Line**: `python-dotenv==1.1.1`
- **Purpose**: Ensure the library is installed when others set up the project

### 5. Updated Code Files
- **Files Modified**:
  - `backend/api/maya_supabase/database.py`
  - `backend/main.py`
- **Changes**: Added `from dotenv import load_dotenv` and `load_dotenv()` to load environment variables

### 6. Created Test Script
- **File**: `backend/test_env_vars.py`
- **Purpose**: Verify that environment variables are loaded correctly

## Verification

The setup has been verified through:
1. Running the test script to confirm environment variables are loaded
2. Checking that the `.env` file is listed in `.gitignore`
3. Confirming that `python-dotenv` is installed and in `requirements.txt`
4. Verifying that code files have been updated to load environment variables

## Usage Instructions

To use the environment variables setup:

1. **Update the `.env` file** with your actual Supabase service role key:
   ```
   SUPABASE_URL=https://ksrvtvqqikwjbqzpgacs.supabase.co
   SUPABASE_KEY=your_actual_service_role_key_here
   ```

2. **Activate the virtual environment**:
   ```bash
   cd C:\Users\bryan\Desktop\MAYA\backend
   .venv-py310\Scripts\activate
   ```

3. **Install dependencies** (if not already done):
   ```bash
   pip install -r requirements.txt
   ```

4. **Run your application**:
   ```bash
   python main.py
   ```

## Security Notes

- The `.env` file contains sensitive information and should never be committed to version control
- The `.env` file has been added to `.gitignore` to prevent accidental commits
- When sharing the project with others, provide instructions to create their own `.env` file rather than sharing yours
- For production deployments, consider using more secure methods of managing secrets (e.g., cloud provider secret managers)

## Troubleshooting

If you encounter issues with environment variables:

1. **Check that the `.env` file exists** in the [backend](file:///c%3A/Users/bryan/Desktop/MAYA/backend) directory
2. **Verify the file contains the correct variables**:
   ```
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your_service_role_key
   ```
3. **Ensure `python-dotenv` is installed**:
   ```bash
   pip install python-dotenv
   ```
4. **Check that code files import and use `load_dotenv()`**:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

## Conclusion

The environment variables setup for the MAYA Supabase integration has been completed successfully. The project now properly loads configuration from the `.env` file, keeping sensitive data separate from the codebase while ensuring it's not accidentally committed to version control.