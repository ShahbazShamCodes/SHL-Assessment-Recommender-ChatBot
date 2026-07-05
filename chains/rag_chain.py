#for comment type command + / and for uncomment type command + /

import sys
from pathlib import Path

# Add the project root to Python's module search path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_mistralai import (
    ChatMistralAI,
    MistralAIEmbeddings
)

from prompts.prompt import prompt

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

# ----------------------------
# Create Retriever
# ----------------------------
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)

# ----------------------------
# Load LLM
# ----------------------------
llm = ChatMistralAI(
    model="mistral-small-2506"
)

# ----------------------------
# Chat Function
# ----------------------------
def chat(question: str):

    # Step 1: Retrieve relevant SHL assessments
    docs = retriever.invoke(question)

    # Step 2: Build context from retrieved documents
    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    # Step 3: Create Prompt
    final_prompt = prompt.invoke(
        {
            "context": context,
            "question": question
        }
    )

    # Step 4: Generate Answer
    response = llm.invoke(final_prompt)

    # Step 5: Build Structured Recommendations
    recommendations = []

    for doc in docs:

        recommendations.append(
            {
                "entity_id": doc.metadata.get("entity_id", ""),

                "name": doc.metadata.get("name", ""),

                "url": doc.metadata.get("url", ""),

                "duration": doc.metadata.get(
                    "duration",
                    "Not Specified"
                ),

                "assessment_type": doc.metadata.get(
                    "assessment_type",
                    "Not Specified"
                ),

                "job_levels": doc.metadata.get(
                    "job_levels",
                    "Not Specified"
                ),

                "languages": doc.metadata.get(
                    "languages",
                    "Not Specified"
                ),

                "remote": doc.metadata.get(
                    "remote",
                    "Unknown"
                ),

                "adaptive": doc.metadata.get(
                    "adaptive",
                    "Unknown"
                )
            }
        )

    # Step 6: Return Response
    return {

        "answer": response.content,

        "recommendations": recommendations

    }

if __name__ == "__main__":

    result = chat(".NET Framework 4.5")

    print("=" * 80)
    print("AI Answer")
    print("=" * 80)

    print(result["answer"])


