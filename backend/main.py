'''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv() 

app = FastAPI(
    title="LinkedIn Post Generator AI Agent",
    description="Generate professional LinkedIn posts using LangChain",
    version="1.0.0"
)

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

# LLM setup
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=1,
    api_key=os.getenv("OPENAI_API_KEY")
)

# Prompt Template
template = """
You are a professional LinkedIn content writer.

Write a LinkedIn post about the topic: "{topic}"

Requirements:
- Language: {language}
- Length: 2–4 short paragraphs
- Professional and engaging tone
- Start with a strong hook
- End with a thoughtful insight or question
- Suitable for LinkedIn audience

Post:
"""

prompt = PromptTemplate(
    input_variables=["topic", "language"],
    template=template
)

# LangChain pipeline
chain = prompt | llm | StrOutputParser()

# API Route
@app.post("/generate-post")
def generate_post(request: PostRequest):
    result = chain.invoke({
        "topic": request.topic,
        "language": request.language
    })
    return {
        "topic": request.topic,
        "language": request.language,
        "post": result
    }

# Root route 
@app.get("/")
def root():
    return {"message": "LinkedIn Post Generator API is running 🚀"}
'''
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