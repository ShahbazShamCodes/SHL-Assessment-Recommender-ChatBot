import json
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_mistralai import MistralAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ----------------------------
# Load Environment Variables
# ----------------------------
load_dotenv()

# ----------------------------
# Load JSON File
# ----------------------------
with open("data/catalog.json", "r", encoding="utf-8") as file:
    catalog = json.load(file)


# ----------------------------
# Clean Metadata Function
# ----------------------------
def clean_metadata(assessment):

    return {

        "entity_id": assessment.get("entity_id", ""),

        "name": assessment.get("name", ""),

        "url": assessment.get("link", ""),

        "duration": assessment.get("duration") or "Not Specified",

        "job_levels": ", ".join(
            assessment.get("job_levels") or ["Not Specified"]
        ),

        "languages": ", ".join(
            assessment.get("languages") or ["Not Specified"]
        ),

        "assessment_type": ", ".join(
            assessment.get("keys") or ["Not Specified"]
        ),

        "remote": assessment.get("remote", ""),

        "adaptive": assessment.get("adaptive", "")
    }


# ----------------------------
# Convert JSON into Documents
# ----------------------------
documents = []

for assessment in catalog:

    # Clean metadata
    metadata = clean_metadata(assessment)

    # Create page content using cleaned metadata
    page_content = f"""
Assessment Name:
{metadata["name"]}

Description:
{assessment.get("description", "Not Specified")}

Job Levels:
{metadata["job_levels"]}

Languages:
{metadata["languages"]}

Duration:
{metadata["duration"]}

Assessment Type:
{metadata["assessment_type"]}

Remote Testing:
{metadata["remote"]}

Adaptive:
{metadata["adaptive"]}

SHL Catalog URL:
{metadata["url"]}
"""

    # Create LangChain Document
    document = Document(
        page_content=page_content,
        metadata=metadata
    )

    documents.append(document)


# ----------------------------
# Create Embeddings
# ----------------------------
embedding_model = MistralAIEmbeddings()

# ----------------------------
# Split Documents into Chunks   
# ----------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunked_documents = splitter.split_documents(documents)

print(f"Original Documents : {len(documents)}")
print(f"Chunked Documents  : {len(chunked_documents)}")


# ----------------------------
# Create Chroma Vector Database
# ----------------------------
vectorstore = Chroma.from_documents(
    documents=chunked_documents,
    #documents=documents,
    embedding=embedding_model,
    persist_directory="chroma-db"
)

print(f"✅ Successfully loaded {len(documents)} documents into ChromaDB.")


