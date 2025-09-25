import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv



load_dotenv() 
api_key = os.getenv("GOOGLE_API_KEY")

model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",  
        google_api_key=api_key,
    )

def chat_service(message):
    response = model.invoke(message)

    return response.content.strip()