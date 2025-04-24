from fastapi import FastAPI, HTTPException, Request
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

load_dotenv()

# CORS middleware to allow cross-origin requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace this with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set the URL for your Runpod Serverless API endpoint
RUNPOD_URL = "https://api.runpod.ai/v2/obhiuyqj2cpkhy/run"  # Replace YOUR_RUNPOD_ID

@app.post("/api/ask")
async def ask(request: Request):
    """
    Endpoint that receives a user query, forwards it to Runpod model,
    and returns the model's response.
    
    Args:
        request (Request): The incoming HTTP request.
        
    Returns:
        dict: The response from the model (Runpod).
    """
    data = await request.json()
    prompt = data.get("prompt", "")
    
    # Send the request to Runpod serverless function (model API)
    async with httpx.AsyncClient() as client:
        response = await client.post(RUNPOD_URL, json={"input": {"prompt": prompt}})
        result = response.json()

    return result

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
