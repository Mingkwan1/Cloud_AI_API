from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.llm import get_answer

# import uvicorn
import traceback

app = FastAPI()

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

load_dotenv()

# Serve index.html at root
@app.get("/")
async def serve_homepage():
    return FileResponse("frontend/index.html")

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
async def ask_question(request: QueryRequest):
    try:
        result = get_answer(request.query)
        return {"answer": result}
    except Exception as e:
        error_details = traceback.format_exc()  # Captures the full traceback
        print("Error details:", error_details)  # Prints full traceback to the log
        raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
