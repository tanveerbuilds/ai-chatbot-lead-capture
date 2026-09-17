# ai-chatbot-lead-capture

> **Sample / demo build** — a minimal example showing how an AI chatbot can capture leads from a website or WhatsApp. Built for learning and demonstration, not production use.

## What this sample demonstrates

- **LLM integration** — answers visitor questions using an OpenAI-compatible chat model with a system prompt tuned for lead capture
- **RAG knowledge base** — retrieves relevant snippets from a small FAQ document so answers stay grounded in business info
- **Lead capture flow** — collects name, contact details, and enquiry topic through natural conversation, then validates the inputs
- **CRM sync** — appends each captured lead as a row in Google Sheets (or posts it to a webhook) so nothing gets lost

## Project structure

```
.
├── app.py          # Minimal chatbot loop (sample code)
├── faq.md          # Tiny example knowledge base for RAG
└── README.md
```

## How to run the sample

```bash
pip install openai

export OPENAI_API_KEY="your-key-here"
python app.py
```

Type messages at the prompt. Type `quit` to exit. Leads are printed to the console and appended to `leads.csv`.

## Notes

- This is a **demonstration**, not a finished product: no auth, no rate limiting, no WhatsApp Business API wiring.
- Swap in the [WhatsApp Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api/) webhook handler to receive real WhatsApp messages.
- Replace the CSV writer with your CRM's API (HubSpot, Pipedrive, etc.) for production use.

## Tech

Python · OpenAI API · simple retrieval over a local FAQ file · CSV / Google Sheets for lead storage
