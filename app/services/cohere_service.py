from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
from app.utils.helper_function import generate_pengamalan_prompt
import os

COHERE_API_KEY = os.getenv('COHERE_KEY')
llm = ChatCohere(cohere_api_key=COHERE_API_KEY, max_tokens=128, temperature=0.2)

def generate_pengamalan(translation: str = "Hello world", tafsir: str = "Hello world"):
    prompt = generate_pengamalan_prompt(translation, tafsir)
    llm_chain = prompt | llm

    return llm_chain.invoke({
        "translation": translation,
        "tafsir": tafsir
    })