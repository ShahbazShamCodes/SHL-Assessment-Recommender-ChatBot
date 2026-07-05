import json
import requests
import streamlit as st

FASTAPI_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(
    page_title="SHL Assessment Recommender",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 SHL Assessment Recommendation Chatbot")

st.write(
    "Ask questions about SHL assessments or choose an assessment from the catalog."
)

# -------------------------
# Load Catalog
# -------------------------

with open("data/catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

assessment_names = sorted(
    [item["name"] for item in catalog]
)

selected_assessment = st.selectbox(
    "Select an Assessment",
    ["None"] + assessment_names
)

question = st.text_area(
    "Ask your question",
    placeholder="Example: Recommend assessments for a Java Developer."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# Send Button
# -------------------------

if st.button("Send"):

    if selected_assessment != "None":

        question = f"{question}\n\nSelected Assessment: {selected_assessment}"

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    payload = {
        "messages": st.session_state.messages
    }

    response = requests.post(
        FASTAPI_URL,
        json=payload
    )

    if response.status_code == 200:

        data = response.json()

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": data["answer"]
            }
        )

        st.success("Assistant")

        st.write(data["answer"])

        if len(data["recommendations"]) > 0:

            st.subheader("Recommended Assessments")

            for rec in data["recommendations"]:

                with st.container():

                    st.markdown(
                        f"### {rec['name']}"
                    )

                    st.write(
                        f"**Duration:** {rec['duration']}"
                    )

                    st.write(
                        f"**Assessment Type:** {rec['assessment_type']}"
                    )

                    st.write(
                        f"**Job Levels:** {rec['job_levels']}"
                    )

                    st.write(
                        f"**Languages:** {rec['languages']}"
                    )

                    st.markdown(
                        f"[Open SHL Catalog]({rec['url']})"
                    )

    else:

        st.error(response.text)

# -------------------------
# Conversation History
# -------------------------

st.divider()

st.header("Conversation")

for msg in st.session_state.messages:

    if msg["role"] == "user":

        st.chat_message("user").write(msg["content"])

    else:

        st.chat_message("assistant").write(msg["content"])



#for run the code - streamlit run streamlit_app.py