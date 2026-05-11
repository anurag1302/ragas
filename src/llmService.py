import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1"
)

CHAT_MODEL = "deepseek/deepseek-chat-v3-0324"


def ask_llm(question, context):
    prompt = f"""
You are a helpful AI assistant.
Answer the question ONLY using the provided context.
Context:{context}
Question:{question}
"""
    response = client.chat.completions.create(
        model=CHAT_MODEL, messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
