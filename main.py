from dotenv import load_dotenv
import os

from langchain_mistralai import ChatMistralAI
from langchain_community.document_loaders import JSONLoader
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

loader = JSONLoader(
    file_path="data/catalog.json",
    jq_schema=".[]",
    text_content=False
)
docs = loader.load()

template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{data}")
])

#model = init_chat_model("gpt-oss-120b")
model = ChatMistralAI(model="mistral-small-2603")

prompt = template.format_messages(data = docs[0].page_content)

response = model.invoke(prompt)

print(response.content)


