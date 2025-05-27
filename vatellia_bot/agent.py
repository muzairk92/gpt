import os
from typing import List

import openai
import sqlite_utils

DB_PATH = os.getenv("VATELLIA_DB", "vatellia.db")
TABLE_NAME = "documents"

system_prompt = "You are Vatellia's virtual assistant. Ask the user for their name, email, phone number, and any wellness concerns such as sleep issues, fatigue, or stress. Recommend Vatellia products based on their concerns and politely offer to connect them with a human representative if needed. Do not provide medical advice."


def fetch_relevant_docs(question: str, limit: int = 2) -> List[str]:
    db = sqlite_utils.Database(DB_PATH)
    if TABLE_NAME not in db.table_names():
        return []
    table = db[TABLE_NAME]
    q_embed = openai.embeddings.create(input=question, model="text-embedding-ada-002").data[0].embedding
    docs = []
    for row in table.rows:
        doc_embed = row["embedding"]
        # simple dot product similarity
        score = sum(a*b for a, b in zip(q_embed, doc_embed))
        docs.append((score, row["text"]))
    docs.sort(key=lambda x: x[0], reverse=True)
    return [text for _, text in docs[:limit]]


def chat(messages: List[dict]) -> str:
    # add context from docs
    question = messages[-1]["content"]
    docs = fetch_relevant_docs(question)
    context = "\n\n".join(docs)
    content = f"Context:\n{context}\n\nUser question: {question}"
    prompt_messages = [
        {"role": "system", "content": system_prompt},
    ] + messages[:-1] + [{"role": "user", "content": content}]

    response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=prompt_messages)
    return response.choices[0].message.content.strip()
