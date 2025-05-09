from fastapi import FastAPI, HTTPException, Request
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
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

# Serve index.html on root
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("frontend/index.html") as f:
        content = f.read()
    return content


# Define request and response model for sending a query to Runpod
class Prompt(BaseModel):
    prompt: str

@app.post("/ask")
async def ask(prompt: Prompt):
    """
    Endpoint that receives a user query, forwards it to Runpod model,
    and returns the model's response.
    
    Args:
        request (Request): The incoming HTTP request.
        
    Returns:
        dict: The response from the model (Runpod).
    """
    headers = {"Content-Type": "application/json"}
    payload = {"input": {"prompt": prompt.prompt}}
    # Send the request to Runpod serverless function (model API)
    async with httpx.AsyncClient() as client:
        res = await client.post(RUNPOD_URL, json=payload, headers=headers)
    if res.status_code != 200:
        return {
            "error": f"Runpod call failed",
            "status_code": res.status_code,
            "text": res.text  # return raw response for debugging
        }

    try:
        print(res)
        print(type(res))

        return {"answer": res.json()}
    except Exception as e:
        return {
            "error": "Could not decode Runpod response",
            "response_text": res.text,
            "exception": str(e)
        }

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
