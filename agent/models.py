from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_google_genai import ChatGoogleGenerativeAI
import os



load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0,
)

# model = init_chat_model(llm)


# response=model.invoke("what is LLM in 10 words")
# print(response.content)