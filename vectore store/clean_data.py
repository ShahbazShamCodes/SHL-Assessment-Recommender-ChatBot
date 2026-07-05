import json
from dotenv import load_dotenv

load_dotenv()

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

#with open("data/catalog.json", "r", encoding="utf-8") as file:
#    catalog = json.load(file)

#print(clean_metadata(catalog[2]))

with open("data/catalog.json", "r", encoding="utf-8") as file:
    catalog = json.load(file)

cleaned_catalog = []

for assessment in catalog:
    cleaned_catalog.append(clean_metadata(assessment))

print(f"Total records cleaned: {len(cleaned_catalog)}")

# Print first cleaned record
print(cleaned_catalog[0])


