from fastapi import FastAPI

from api.models import (
    ChatRequest,
    ChatResponse,
    Recommendation
)

from chains.rag_chain import chat


app = FastAPI(
    title="SHL Assessment Recommendation API",
    version="1.0.0"
)

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "message": "SHL Assessment Recommendation API is running."
    }

@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat_endpoint(request: ChatRequest):

    # Get the latest user message
    latest_question = ""

    for message in reversed(request.messages):

        if message.role.lower() == "user":

            latest_question = message.content

            break

    if latest_question == "":

        return ChatResponse(
            answer="No user question found.",
            recommendations=[]
        )

    # Call RAG Chain
    result = chat(latest_question)

    recommendations = []

    for item in result["recommendations"]:

        recommendations.append(
            Recommendation(
                entity_id=item["entity_id"],
                name=item["name"],
                url=item["url"],
                duration=item["duration"],
                assessment_type=item["assessment_type"],
                job_levels=item["job_levels"],
                languages=item["languages"],
                remote=item["remote"],
                adaptive=item["adaptive"]
            )
        )

    return ChatResponse(
        answer=result["answer"],
        recommendations=recommendations
    )

# for run the code :  uvicorn api.Fast_api:app --reload

# for example : checking 
# {
#   "messages": [
#     {
#       "role": "user",
#       "content": "Recommend SHL assessments for Java Developer"
#     }
#   ]
# }




