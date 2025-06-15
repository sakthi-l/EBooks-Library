
import streamlit as st
import sqlite3
import pandas as pd
import os
from create_db import create_database

# Create database if it doesn't exist
if not os.path.exists("ebooks.db"):
    create_database()

def search_books(title, author, language):
    conn = sqlite3.connect("ebooks.db")
    query = """
        SELECT title, author, language, description, file_path
        FROM books
        WHERE title LIKE ? AND author LIKE ? AND language LIKE ?
    """
    rows = conn.execute(query, (f"%{title}%", f"%{author}%", f"%{language}%")).fetchall()
    conn.close()
    return rows

st.title("📚 Multilingual E‑Book Finder")
st.write("Search by entering any title, author, or language:")

title = st.text_input("Book Title")
author = st.text_input("Author")
language = st.text_input("Language")

if st.button("🔍 Search"):
    results = search_books(title, author, language)
    if results:
        df = pd.DataFrame(results, columns=["Title","Author","Language","Description","File Path"])
        st.success(f"Found {len(df)} book(s)")
        st.dataframe(df)
    else:
        st.warning("No matching books found.")
