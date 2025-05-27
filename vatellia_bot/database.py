import os
import sqlite_utils

DB_PATH = os.getenv("VATELLIA_DB", "vatellia.db")


def get_db():
    return sqlite_utils.Database(DB_PATH)


def save_lead(name: str, email: str, phone: str, requirements: str):
    db = get_db()
    leads = db["leads"]
    leads.create({
        "name": str,
        "email": str,
        "phone": str,
        "requirements": str,
    }, pk="email", if_not_exists=True)
    leads.upsert({"name": name, "email": email, "phone": phone, "requirements": requirements}, pk="email")
