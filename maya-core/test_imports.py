#!/usr/bin/env python3

print("Testing imports...")

try:
    import subprocess
    print("✓ subprocess")
except Exception as e:
    print(f"✗ subprocess: {e}")

try:
    import json
    print("✓ json")
except Exception as e:
    print(f"✗ json: {e}")

try:
    import time
    print("✓ time")
except Exception as e:
    print(f"✗ time: {e}")

try:
    from fastapi import FastAPI
    print("✓ fastapi")
except Exception as e:
    print(f"✗ fastapi: {e}")

try:
    from fastapi.middleware.cors import CORSMiddleware
    print("✓ CORS middleware")
except Exception as e:
    print(f"✗ CORS middleware: {e}")

try:
    from pydantic import BaseModel
    print("✓ pydantic")
except Exception as e:
    print(f"✗ pydantic: {e}")

try:
    from typing import Dict, Any, List
    print("✓ typing")
except Exception as e:
    print(f"✗ typing: {e}")

try:
    from decimal import Decimal
    print("✓ decimal")
except Exception as e:
    print(f"✗ decimal: {e}")

print("All imports completed!")
