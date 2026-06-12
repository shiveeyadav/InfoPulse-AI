def build_prompt(question, search_results):
    sources = ""

    for i, item in enumerate(search_results, start=1):
        title = item.get("title", "No title")
        url = item.get("url", "No URL")
        content = item.get("content", "No content")

        sources += f"""
Source {i}
Title: {title}
URL: {url}
Content: {content}
"""

    prompt = f"""
You are InfoPulse AI, a real-time AI search assistant.

Answer the user's question using the web search results below.
Write the answer in simple English.
Make the answer clear, useful, and well-structured.
At the end, include source links.

User question:
{question}

Web search results:
{sources}
"""

    return prompt