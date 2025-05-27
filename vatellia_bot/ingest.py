import os
import glob
import pathlib
import sqlite_utils
from pdfminer.high_level import extract_text as pdf_extract
from docx import Document

import openai

DB_PATH = os.getenv("VATELLIA_DB", "vatellia.db")
DATA_DIR = pathlib.Path(os.getenv("VATELLIA_DATA", "data"))
TABLE_NAME = "documents"


def load_text(path: pathlib.Path) -> str:
    if path.suffix.lower() == ".pdf":
        return pdf_extract(str(path))
    elif path.suffix.lower() in {".doc", ".docx"}:
        doc = Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs)
    else:
        return path.read_text(encoding="utf-8")


def embed_file(path: pathlib.Path) -> dict:
    text = load_text(path)
    if not text.strip():
        return None
    resp = openai.embeddings.create(input=text, model="text-embedding-ada-002")
    embedding = resp.data[0].embedding
    return {"path": str(path), "text": text, "embedding": embedding}


def ingest_files():
    db = sqlite_utils.Database(DB_PATH)
    table = db[TABLE_NAME]
    table.create({"path": str, "text": str, "embedding": sqlite_utils.FloatList()}, pk="path", not_null=True, if_not_exists=True)

    for file_path in DATA_DIR.glob("**/*"):
        if file_path.is_dir():
            continue
        doc = embed_file(file_path)
        if doc:
            table.upsert(doc, pk="path")
            print(f"Ingested {file_path}")


if __name__ == "__main__":
    ingest_files()
