import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(query, context_docs):
    context = "\n\n---\n\n".join(context_docs)

    prompt = f"""
    Context information:
    ---------------------
    {context}
    ---------------------

    Answer the question: {query}
    """

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful teaching assistant."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.1-8b-instant",
        temperature=0.1
    )

    return response.choices[0].message.content