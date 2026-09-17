import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def build_business_prompt(user_question, analytics_result):
    return f"""
You are an AI Business Intelligence Copilot.

The user asked:
{user_question}

Below is the EXACT result produced by our analytics/business logic:

{analytics_result}

Your job is to explain this result clearly to a business user.

IMPORTANT RULES:

1. Use ONLY the information provided in the analytics result.
2. Do NOT invent numbers, facts, customers, products, categories, causes, or business explanations.
3. Do NOT change any numerical values.
4. NEVER say "more data is required" if the analytics result already contains the requested information.
5. If the analytics result contains specific names, lists, IDs, categories, products, or sellers relevant to the user's question, INCLUDE them in your answer.
6. Preserve the actual names from the analytics result exactly as provided.
7. If the user asks "which", "what are", "show me", or "list", provide the specific items from the analytics result.
8. Clearly distinguish facts from recommendations.
9. Recommendations must be based only on the available evidence.
10. Keep the answer concise and professional.
11. Focus on business meaning rather than technical details.
12. Do not mention that you are an AI unless necessary.

Use this format:

📊 Business Insight
Explain the main finding and provide the specific requested items when available.

💡 Why It Matters
Explain why the finding is important for the business.

🎯 Recommended Action
Give practical actions based only on the available evidence.
"""


def clean_llm_response(response):
    if response is None:
        return "No response generated."

    text = response.strip()

    if not text:
        return "No response generated."

    return text


def generate_llm_response(
    user_question,
    analytics_result,
    llm_client=None
):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return (
            "❌ OpenAI API key was not found.\n\n"
            "Please check your .env file."
        )

    try:
        if llm_client is None:
            llm_client = OpenAI(api_key=api_key)

        prompt = build_business_prompt(
            user_question,
            analytics_result
        )

        response = llm_client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        return clean_llm_response(
            response.output_text
        )

    except Exception as e:
        return (
            "❌ LLM request failed.\n\n"
            f"Error: {str(e)}"
        )