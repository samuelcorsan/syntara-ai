import os
from openai import OpenAI
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
