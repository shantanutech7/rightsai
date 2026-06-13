from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))


def get_plain_summary(document_text, analysis_results):
    """Generate a plain language summary of the document using GPT."""

    red_clauses = [r["clause"] for r in analysis_results["red"]]
    yellow_clauses = [r["clause"] for r in analysis_results["yellow"]]

    prompt = f"""You are RightsAI — an AI that helps ordinary Indians understand legal documents.

Analyze this document and give a plain language summary. Write like you're explaining to a 25-year-old signing their first job offer or rent agreement.

Document text (first 3000 chars):
{document_text[:3000]}

High risk clauses found: {red_clauses}
Clauses needing review: {yellow_clauses}

Give your response in this exact format:

**What is this document?**
(1-2 lines about what type of document this is)

**What are you agreeing to? (Plain language)**
(3-5 bullet points of the most important things)

**Biggest risks for you:**
(Explain the red flag clauses in simple Hindi/English — what does it actually mean for the person)

**What you should do:**
(2-3 practical action items)

Keep it short, direct, and human. No legal jargon. Write as if talking to a friend."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.4
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ AI summary unavailable (API key needed): {str(e)}"


def chat_with_document(document_text, user_question, chat_history):
    """Allow user to ask questions about the document."""

    messages = [
        {
            "role": "system",
            "content": f"""You are RightsAI — a helpful legal assistant for Indians.
You have access to this document:

{document_text[:4000]}

Answer questions about this document in simple, plain language. 
- Be direct and clear
- Use Hindi/English mix if helpful  
- Always say what it means for the USER specifically
- If something is risky, say so clearly
- If you're unsure, say so — don't guess on legal matters"""
        }
    ]

    # Add chat history
    for msg in chat_history:
        messages.append(msg)

    # Add current question
    messages.append({"role": "user", "content": user_question})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=500,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Chat unavailable (API key needed): {str(e)}"
