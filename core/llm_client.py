from dotenv import load_dotenv
load_dotenv()
import os
from openai import OpenAI

from config import DEFAULT_MODEL

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_llm(prompt: str, model: str = DEFAULT_MODEL) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a financial assistant."},
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message.content