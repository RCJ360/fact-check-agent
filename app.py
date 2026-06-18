# Import Required Libraries
import streamlit as st
import fitz
import os
import json
from dotenv import load_dotenv
from tavily import TavilyClient
import google.generativeai as genai

# Load API Keys
load_dotenv()

# Configure Gemini and Tavily (LLM Models)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Load Gemini Model
model = genai.GenerativeModel("gemini-2.5-flash")

# Configure Streamlit Page
st.set_page_config(page_title="Fact Check Agent")
st.title("🔍 Fact Check Agent")

# Upload PDF File
uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

# Extract Text from PDF
def extract_text(pdf_file):
    try:
        doc = fitz.open(
            stream=pdf_file.read(),
            filetype="pdf"
        )

        text = ""
        for page in doc:
            text += page.get_text()

        return text

    except Exception as e:
        st.error(f"Invalid PDF File: {e}")
        return ""

# Extract Factual Claims from Text
def extract_claims(text):
    prompt = f"""
Extract factual claims from the text.

Only extract:

* statistics
* percentages
* dates
* financial figures
* technical facts

Return ONLY a JSON array.

Example:
[
"India population is 1.4 billion",
"OpenAI founded in 2015"
]

Text:
{text[:15000]}
"""
    response = model.generate_content(prompt)

    raw_text = response.text.strip()

    #st.write("Gemini Response:")
    #st.code(raw_text)

    try:
        cleaned = raw_text.replace("```json", "")
        cleaned = cleaned.replace("```", "")
        cleaned = cleaned.strip()

        return json.loads(cleaned)

    except Exception as e:
        st.error(f"Claim Extraction Error: {e}")
        return []

# Verify Claim Using Web Search and Gemini
def verify_claim(claim):
    search_results = tavily.search(
        query=claim,
        max_results=5
    )

    evidence = ""
    for result in search_results["results"]:
        evidence += result["content"] + "\n"

    prompt = f"""
Claim:
{claim}

Evidence:
{evidence}

Classify as:

Verified
Inaccurate
False

Return in format:

Status:
Reason:
Correct Fact:
"""
    response = model.generate_content(prompt)
    return response.text

# Process Uploaded PDF
if uploaded_file:

    with st.spinner("Reading PDF..."):
        text = extract_text(uploaded_file)

    st.success("PDF Loaded")

    with st.spinner("Extracting Claims..."):
        claims = extract_claims(text)

    st.subheader("Claims Found")
    st.write(claims)

    results_summary = []

    st.subheader("Fact Check Results")
    
    # Verify Each Claim
    for claim in claims:

        st.markdown("---")

        with st.spinner(f"Verifying: {claim}"):
            result = verify_claim(claim)

        # Identify Claim Status
        if "Status: Verified" in result:
            status = "✅ Verified"
        elif "Status: Inaccurate" in result:
            status = "⚠️ Inaccurate"
        elif "Status: False" in result:
            status = "❌ False"
        else:
            status = "❓ Unknown"

        correct_fact = ""
        
        # Extract Corrected Fact
        if "Correct Fact:" in result:
            correct_fact = result.split("Correct Fact:")[-1].strip()

        # Store Results for Summary Table
        results_summary.append({
            "Claim": claim,
            "Status": status,
            "Correct Fact": correct_fact
        })

        st.markdown(f"### {status}")

        st.write("**Claim:**")
        st.write(claim)

        st.write("**Analysis:**")
        st.info(result)

    st.markdown("---")
    st.subheader("Summary Table")
    st.table(results_summary)