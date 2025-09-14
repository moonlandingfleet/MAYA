import os
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our auth module
from auth import verify_token_and_get_payload, get_current_user_id

# Create FastAPI app
app = FastAPI(title="MAYA Auth Test Server")

# Simple model for testing
class TestResponse(BaseModel):
    message: str
    user_id: str

# Protected endpoint that requires authentication
@app.get("/protected", response_model=TestResponse)
async def protected_route(user_id: str = Depends(get_current_user_id)):
    return TestResponse(
        message="Successfully accessed protected route",
        user_id=user_id
    )

# Public endpoint that doesn't require authentication
@app.get("/public")
async def public_route():
    return {"message": "This is a public route"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)