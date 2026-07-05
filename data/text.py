from langchain_community.document_loaders import JSONLoader


loader = JSONLoader(
    file_path="data/catalog.json",
    jq_schema=".[]",
    text_content=False
)

docs = loader.load()



for doc in docs:
   print(doc.page_content)


