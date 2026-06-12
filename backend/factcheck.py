def generate_fact_check_prompt(question, sources):

    prompt = f"""
You are InfoPulse AI in Fact Check Mode.

Claim:
{question}

Sources:
{sources}

Determine whether the claim is:

TRUE
FALSE
PARTLY TRUE
UNCERTAIN

Provide explanation and evidence.
"""

    return prompt