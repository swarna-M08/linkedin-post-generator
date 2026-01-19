import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",  
    temperature=0.7,
    google_api_key=GOOGLE_API_KEY
)

linkedin_prompt = PromptTemplate(
    input_variables=["topic", "language"],
    template="""
    You are an expert LinkedIn content writer.
    
    Topic: {topic}
    Language: {language}
    
    Write a professional LinkedIn post.
    - Write a paragraphs and use easy words so that everyone can easily understand.
    - Add a strong hook at the start.
    - Include relevant emojis.
    - Suitable for LinkedIn audience
    - Add hashtags at the end.
    """
)

chain = linkedin_prompt | llm | StrOutputParser()

def generate_post(topic: str, language: str) -> str:
    result = chain.invoke({
        "topic": topic,
        "language": language
    })
    return result