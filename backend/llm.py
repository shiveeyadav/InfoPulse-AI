from backend.prompts import build_prompt

def generate_answer(client, question, search_results):
    prompt = build_prompt(question, search_results)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text