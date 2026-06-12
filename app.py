import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from tavily import TavilyClient

from backend.search import search_web
from backend.llm import generate_answer
from backend.pdf_reader import read_pdf

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

st.set_page_config(
    page_title="InfoPulse AI",
    page_icon="🔎",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at top left, rgba(56,189,248,0.12), transparent 30%),
        linear-gradient(135deg, #020617, #0f172a);
    color: white;
}

[data-testid="stHeader"] {
    background: transparent;
}

.hero {
    text-align: center;
    padding: 35px 20px 15px 20px;
}

.badge {
    display: inline-block;
    padding: 8px 18px;
    border-radius: 999px;
    background: rgba(56,189,248,0.10);
    border: 1px solid rgba(56,189,248,0.30);
    color: #7dd3fc;
    font-size: 14px;
    font-weight: 700;
}

.hero-title {
    font-size: 62px;
    font-weight: 900;
    margin-top: 14px;
    background: linear-gradient(90deg, #60a5fa, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 20px;
    color: #cbd5e1;
    margin-top: 8px;
}

.feature-card {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 22px;
    padding: 22px;
    text-align: center;
    backdrop-filter: blur(12px);
    box-shadow: 0 18px 45px rgba(0,0,0,0.25);
    min-height: 130px;
}

.card-icon {
    font-size: 30px;
    margin-bottom: 8px;
}

.card-title {
    font-size: 19px;
    font-weight: 800;
    color: #f8fafc;
}

.card-text {
    font-size: 14px;
    color: #cbd5e1;
}

.chat-panel {
    margin-top: 32px;
    padding: 26px;
    border-radius: 26px;
    background: rgba(15,23,42,0.82);
    border: 1px solid rgba(148,163,184,0.18);
    box-shadow: 0 25px 70px rgba(0,0,0,0.32);
    backdrop-filter: blur(14px);
}

.chat-heading {
    font-size: 27px;
    font-weight: 850;
    color: #f8fafc;
}

.chat-subheading {
    font-size: 15px;
    color: #94a3b8;
    margin-bottom: 20px;
}

.stChatMessage {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 14px;
    margin-bottom: 12px;
}

div[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid rgba(148,163,184,0.16);
}

.sidebar-title {
    font-size: 28px;
    font-weight: 900;
    color: #38bdf8;
}

.sidebar-text {
    color: #cbd5e1;
    font-size: 15px;
    line-height: 1.5;
}

.footer {
    text-align: center;
    color: #64748b;
    font-size: 13px;
    margin-top: 25px;
}
</style>
""", unsafe_allow_html=True)

if not gemini_api_key:
    st.error("GEMINI_API_KEY is missing. Please add it in your .env file.")
    st.stop()

if not tavily_api_key:
    st.error("TAVILY_API_KEY is missing. Please add it in your .env file.")
    st.stop()

client = genai.Client(api_key=gemini_api_key)
tavily = TavilyClient(api_key=tavily_api_key)

with st.sidebar:
    st.markdown('<div class="sidebar-title">🔎 InfoPulse AI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sidebar-text">A real-time AI search assistant with web search, fact-checking, research mode, and PDF support.</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    mode = st.radio(
        "Choose Mode",
        [
            "AI Chat",
            "Web Search",
            "Research Mode",
            "Fact Check",
            "PDF Chat"
        ]
    )

    uploaded_file = st.file_uploader(
        "Upload PDF for PDF Chat",
        type=["pdf"]
    )

    st.markdown("---")
    st.markdown("### Example Questions")
    st.markdown("- Latest AI news")
    st.markdown("- Fact check this claim")
    st.markdown("- Summarize this PDF")
    st.markdown("- Current technology updates")

st.markdown("""
<div class="hero">
    <div class="badge">Real-Time Search • AI Chat • Fact Check • PDF Assistant</div>
    <div class="hero-title">InfoPulse AI</div>
    <div class="hero-subtitle">
        A professional AI assistant that gives fresh, reliable, and source-backed answers.
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="card-icon">🌐</div>
        <div class="card-title">Live Web Search</div>
        <div class="card-text">Gets fresh information from the web for current topics.</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="card-icon">✅</div>
        <div class="card-title">Fact Check Mode</div>
        <div class="card-text">Checks claims using web sources and explains reliability.</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="card-icon">📄</div>
        <div class="card-title">PDF Chat</div>
        <div class="card-text">Upload a PDF and ask questions from its content.</div>
    </div>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

if uploaded_file is not None:
    st.session_state.pdf_text = read_pdf(uploaded_file)
    st.sidebar.success("PDF uploaded successfully")

def generate_fact_check_answer(question, search_results):
    sources = ""

    for i, item in enumerate(search_results, start=1):
        sources += f"""
Source {i}
Title: {item.get("title", "No title")}
URL: {item.get("url", "No URL")}
Content: {item.get("content", "No content")}
"""

    prompt = f"""
You are InfoPulse AI in Fact Check Mode.

Check the claim below using the web sources.

Claim:
{question}

Sources:
{sources}

Give the answer in this format:

Verdict: True / False / Partly True / Uncertain

Explanation:
Explain clearly in simple English.

Evidence:
Mention the important evidence from the sources.

Sources:
List the source links.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

def generate_pdf_answer(question, pdf_text):
    prompt = f"""
You are InfoPulse AI in PDF Chat Mode.

Answer the user's question only using the PDF content below.
If the answer is not present in the PDF, say that the PDF does not contain this information.

User question:
{question}

PDF content:
{pdf_text[:20000]}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

st.markdown('<div class="chat-panel">', unsafe_allow_html=True)
st.markdown('<div class="chat-heading">Ask InfoPulse AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="chat-subheading">Choose a mode from the sidebar and ask your question.</div>',
    unsafe_allow_html=True
)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_question = st.chat_input("Type your question here...")

if user_question:
    st.session_state.messages.append({"role": "user", "content": user_question})

    with st.chat_message("user"):
        st.write(user_question)

    with st.chat_message("assistant"):
        try:
            if mode == "AI Chat":
                with st.spinner("Generating answer..."):
                    search_results = search_web(user_question, tavily)
                    answer = generate_answer(client, user_question, search_results)
                    st.write(answer)

            elif mode == "Web Search":
                with st.spinner("Searching live web sources..."):
                    search_results = search_web(user_question, tavily)
                    answer = generate_answer(client, user_question, search_results)
                    st.write(answer)

                    st.markdown("### Sources")
                    for item in search_results:
                        st.markdown(f"- [{item.get('title', 'Source')}]({item.get('url', '#')})")

            elif mode == "Research Mode":
                with st.spinner("Researching deeply from multiple sources..."):
                    result = tavily.search(
                        query=user_question,
                        search_depth="advanced",
                        max_results=10
                    )

                    search_results = result["results"]
                    answer = generate_answer(client, user_question, search_results)
                    st.write(answer)

                    st.markdown("### Research Sources")
                    for item in search_results:
                        st.markdown(f"- [{item.get('title', 'Source')}]({item.get('url', '#')})")

            elif mode == "Fact Check":
                with st.spinner("Fact-checking the claim..."):
                    search_results = search_web(user_question, tavily)
                    answer = generate_fact_check_answer(user_question, search_results)
                    st.write(answer)

                    st.markdown("### Verification Sources")
                    for item in search_results:
                        st.markdown(f"- [{item.get('title', 'Source')}]({item.get('url', '#')})")

            elif mode == "PDF Chat":
                if not st.session_state.pdf_text:
                    answer = "Please upload a PDF from the sidebar first."
                    st.warning(answer)
                else:
                    with st.spinner("Reading PDF and generating answer..."):
                        answer = generate_pdf_answer(user_question, st.session_state.pdf_text)
                        st.write(answer)

        except Exception as e:
            answer = f"Error: {e}"
            st.error(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="footer">Built with Python • Streamlit • Gemini API • Tavily Search API</div>',
    unsafe_allow_html=True
)