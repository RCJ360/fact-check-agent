# Fact Check Agent

## Overview

Fact Check Agent is an AI-powered application that verifies factual claims found in PDF documents.

The application extracts factual claims from uploaded PDFs, searches the web for supporting evidence, and classifies each claim as:

* Verified
* Inaccurate
* False

It also provides reasoning and corrected facts when applicable.

---

## Features

* Upload PDF documents
* Extract factual claims automatically
* Search live web evidence using Tavily
* Verify claims using Gemini AI
* Classify claims as Verified, Inaccurate, or False
* Display detailed analysis
* Generate summary table of results

---

## Technology Stack

* Streamlit
* Google Gemini API
* Tavily Search API
* PyMuPDF
* Python

---

## Project Structure

fact-check-agent/
├── app.py
├── requirements.txt
├── README.md
└── .env

---

## Installation

1. Clone the repository
git clone <repository-url>

2. Install dependencies
pip install -r requirements.txt

3. Add API Keys in .env file
GEMINI_API_KEY=your_key
TAVILY_API_KEY=your_key

4. Run the application
streamlit run app.py

---

## How It Works

1. User uploads a PDF document.
2. PDF text is extracted using PyMuPDF.
3. Gemini extracts factual claims from the text.
4. Tavily searches the web for evidence.
5. Gemini evaluates the evidence.
6. Claims are classified as:
   * Verified
   * Inaccurate
   * False
7. Results are displayed with explanations and corrected facts.

---

## Sample Output

Claim:
India's population is 1.2 billion

Status:
Inaccurate

Correct Fact:
India's population is currently over 1.4 billion.

---

## Author

Rupak C. Jogi

Product Management Trainee Assignment - 2026