import json

from langchain_core.documents import Document

# Load JSON file
with open("data/catalog.json", "r", encoding="utf-8") as file:
    catalog = json.load(file)

documents = []

for assessment in catalog:

    content = f"""
Assessment Name: {assessment.get('name', 'N/A')}

Description:
{assessment.get('description', 'N/A')}

Job Levels:
{", ".join(assessment.get('job_levels', []))}

Languages:
{", ".join(assessment.get('languages', []))}

Duration:
{assessment.get('duration', 'N/A')}

Assessment Type:
{", ".join(assessment.get('keys', []))}

Remote Testing:
{assessment.get('remote', 'N/A')}

Adaptive:
{assessment.get('adaptive', 'N/A')}
"""

    doc = Document(
        page_content=content,
        metadata={
            "entity_id": assessment.get("entity_id"),
            "name": assessment.get("name"),
            "url": assessment.get("link"),   # <--  JSON uses "link"
            "duration": assessment.get("duration")
        }
    )

    documents.append(doc)

print(documents[0])


