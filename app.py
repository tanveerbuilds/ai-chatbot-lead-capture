"""
ai-chatbot-lead-capture -- sample build
A minimal lead-capture chatbot loop demonstrating:
  1. LLM integration (OpenAI-compatible chat API)
  2. Simple RAG over a local FAQ file (faq.md)
  3. Lead capture + CSV "CRM sync"

Sample/demo code for learning -- not production ready.
"""

import csv
import os
import re
from datetime import datetime, timezone

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None

SYSTEM_PROMPT = """You are a friendly assistant for a small business website.
Answer the visitor's questions using the FAQ context provided.
Your secondary goal is to capture leads: if the visitor shows interest,
politely ask for their name and a contact (email or phone), one at a time.
Keep replies short and conversational."""

FAQ_PATH = "faq.md"
LEADS_CSV = "leads.csv"


def load_faq(path=FAQ_PATH):
    """Load the tiny local knowledge base used for RAG."""
    if not os.path.exists(path):
        return ""
    with open(path, encoding="utf-8") as f:
        return f.read()


def retrieve(query, faq_text, max_chars=1200):
    """Naive keyword retrieval: return FAQ lines sharing words with the query."""
    words = set(re.findall(r"\w+", query.lower()))
    scored = []
    for line in faq_text.splitlines():
        line_words = set(re.findall(r"\w+", line.lower()))
        overlap = len(words & line_words)
        if overlap:
            scored.append((overlap, line))
    scored.sort(reverse=True)
    return "\n".join(line for _, line in scored)[:max_chars]


def chat_reply(client, messages):
    """Call the LLM. Swap model/prompt to suit your use case."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.4,
        max_tokens=300,
    )
    return response.choices[0].message.content.strip()


def save_lead(name, contact, topic):
    """Append a captured lead to CSV (swap for Google Sheets/CRM API)."""
    is_new = not os.path.exists(LEADS_CSV)
    with open(LEADS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["captured_at", "name", "contact", "topic"])
        writer.writerow([datetime.now(timezone.utc).isoformat(), name, contact, topic])
    print(f"[saved lead] {name} | {contact} | {topic}")


def main():
    if OpenAI is None:
        raise SystemExit("pip install openai, then set OPENAI_API_KEY and rerun.")
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("Set the OPENAI_API_KEY environment variable first.")
    client = OpenAI(api_key=api_key)
    faq_text = load_faq()

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("Chatbot ready. Ask me anything (type 'quit' to exit).")
    while True:
        user = input("you: ").strip()
        if user.lower() in {"quit", "exit"}:
            break
        context = retrieve(user, faq_text)
        messages.append({
            "role": "user",
            "content": f"FAQ context:\n{context}\n\nVisitor: {user}",
        })
        reply = chat_reply(client, messages)
        messages.append({"role": "assistant", "content": reply})
        print(f"bot: {reply}")

        # Toy lead detection for the demo: "my name is ... / reach me at ..."
        name = re.search(r"my name is ([a-zA-Z ]+)", user, re.I)
        contact = re.search(r"(?:reach me at|my email is|my phone is) ([\w@.+\- ]+)", user, re.I)
        if name and contact:
            save_lead(name.group(1).strip(), contact.group(1).strip(), user[:80])


if __name__ == "__main__":
    main()
