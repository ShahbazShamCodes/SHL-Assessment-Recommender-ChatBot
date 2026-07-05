from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_mistralai import MistralAIEmbeddings

# ----------------------------
# Load Environment Variables
# ----------------------------
load_dotenv()

# ----------------------------
# Embedding Model
# ----------------------------
embedding_model = MistralAIEmbeddings()

# ----------------------------
# Load Existing ChromaDB
# ----------------------------
vectorstore = Chroma(
    persist_directory="chroma-db",
    embedding_function=embedding_model
)

print("✅ ChromaDB Loaded Successfully\n")

# ----------------------------
# Test Query
# ----------------------------
query = "Need a .NET assessment"

print(f"Query: {query}\n")

results = vectorstore.similarity_search(
    query=query,
    k=5
)

# ----------------------------
# Display Results
# ----------------------------
print(f"Retrieved {len(results)} documents\n")

for i, doc in enumerate(results, start=1):

    print("=" * 80)

    print(f"Result {i}")

    print("-" * 80)

    print("Assessment Name:")
    print(doc.metadata.get("name"))

    print("\nURL:")
    print(doc.metadata.get("url"))

    print("\nDuration:")
    print(doc.metadata.get("duration"))

    print("\nAssessment Type:")
    print(doc.metadata.get("assessment_type"))

    print("\nContent:")
    print(doc.page_content)

    print()

    