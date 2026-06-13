# InfoPulse AI

## Overview

InfoPulse AI is a real-time AI-powered search assistant featuring web search, research mode, fact checking, PDF chat, and voice interaction.

Unlike traditional chatbots with outdated knowledge, InfoPulse AI retrieves current information from the web and generates intelligent responses using Gemini AI.

---

## Features

* Real-Time Web Search
* AI Chat Mode
* Research Mode
* Fact Check Mode
* PDF Chat
* Source Citations
* Modern Professional UI
* Modular Backend Architecture
* Voice Assistant
* Speech-to-Text Input

---

## Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### APIs

* Gemini API
* Tavily Search API

### Libraries

* streamlit
* google-genai
* tavily-python
* python-dotenv
* pypdf

---

## Project Structure

```text
InfoPulse-AI/
│
├── app.py
│
├── backend/
│   ├── __init__.py
│   ├── search.py
│   ├── llm.py
│   ├── prompts.py
│   └── pdf_reader.py
│
├── .env
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

### Clone Repository

```bash
git clone <repository-link>
cd InfoPulse-AI
```

### Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Add Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### Run Application

```bash
streamlit run app.py
```

---

## Future Enhancements

* Voice Assistant Integration
* Multi-Language Support
* User Authentication
* Conversation Memory
* Vector Database Integration (RAG)
* AI Agent Workflows

---

## Author

Shivee Yadav

BCA (Artificial Intelligence & Machine Learning)
# InfoPulse-AI
