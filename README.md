# Vatellia AI Agent Example

This repository contains a minimal example of building a GPT-powered customer assistant for Vatellia supplements. The agent uses OpenAI's API to answer customer questions based on company data and collects basic lead information.

## Features

- Ingest text, PDF, and Word documents from the `data/` directory and store embeddings in SQLite.
- Query stored documents to provide context for GPT responses.
- Collects user name, email, phone, and wellness requirements during chat.
- Saves leads to a local SQLite database.
- Exposes a FastAPI server with a `/chat` endpoint.

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Set your OpenAI API key in the environment:

   ```bash
   export OPENAI_API_KEY=your-key
   ```

3. Ingest documents from the `data/` directory:

   ```bash
   python -m vatellia_bot.ingest
   ```

4. Start the server:

   ```bash
   python -m vatellia_bot.server
   ```

The server will run on `http://localhost:8000`. You can send POST requests to `/chat` with chat history to interact with the agent.

## Example Request

```json
{
  "messages": [{"role": "user", "content": "I have trouble sleeping"}],
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "123-456-7890",
  "requirements": "sleep issues"
}
```

The response will contain the assistant's answer and your lead information will be stored in `vatellia.db`.

## Disclaimer

This code is a simplified demonstration and not intended for production use without additional security, error handling, and compliance checks. Always consult appropriate legal and regulatory guidance when deploying AI systems in healthcare or wellness contexts.
