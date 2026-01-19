from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agent import generate_post

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PostRequest(BaseModel):
    topic: str
    language: str

@app.get("/")
def read_root():
    return {"message": "LinkedIn Post Generator API is running!"}

@app.post("/generate-post")
def generate_linkedin_post(request: PostRequest):
    try:
        post_content = generate_post(request.topic, request.language)
        return {"post": post_content}
    
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))