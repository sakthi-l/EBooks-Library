import streamlit as st
import sqlite3

# ---------- DATABASE SETUP ----------
def create_database():
    conn = sqlite3.connect("ebooks.db")
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        language TEXT,
        description TEXT,
        file_path TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tags (
        tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        tag TEXT,
        FOREIGN KEY (book_id) REFERENCES books(book_id)
    )
    """)

    # Insert sample books (only if books table is empty)
    cursor.execute("SELECT COUNT(*) FROM books")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
        INSERT INTO books (title, author, language, description, file_path)
        VALUES (?, ?, ?, ?, ?)
        """, [
            (
                'Thirukkural', 'Thiruvalluvar', 'Tamil', 'Ancient Tamil couplets',
                'https://www.scribd.com/document/456942075/%E0%AE%A4%E0%AE%BF%E0%AE%B0%E0%AF%81%E0%AE%95-%E0%AE%95%E0%AF%81%E0%AE%B1%E0%AE%B3-%E0%AE%8E%E0%AE%B3%E0%AE%BF%E0%AE%AF-%E0%AE%89%E0%AE%B0%E0%AF%88-pdf'
            ),
            (
                'Gitanjali', 'Rabindranath Tagore', 'Bengali', 'Poems of devotion',
                'https://archive.org/details/gitanjali00unse/page/n21/mode/2up'
            ),
            (
                'Panchatantra', 'Vishnu Sharma', 'Sanskrit', 'Stories with morals',
                'https://archive.org/details/PanchatantraSanskritHindi-JpMishra1910'
            )
        ])
        conn.commit()

    conn.close()


# ---------- DISPLAY UI ----------
def display_books():
    conn = sqlite3.connect("ebooks.db")
    cursor = conn.cursor()

    # Fetch all books
    cursor.execute("SELECT book_id, title, author, language, description, file_path FROM books")
    books = cursor.fetchall()

    st.title("📚 Multilingual eBook Library")
    st.markdown("Click a book **twice** to open the link.")

    for book in books:
        book_id, title, author, language, description, file_path = book

        # Unique key for each book
        click_key = f"book_clicks_{book_id}"

        # Initialize session state
        if click_key not in st.session_state:
            st.session_state[click_key] = 0

        # Book button
        if st.button(f"📖 {title} by {author} ({language})", key=click_key):
            st.session_state[click_key] += 1

            if st.session_state[click_key] == 2:
                st.success(f"✅ Opening: {title}")
                st.markdown(f"🔗 [Click here to open **{title}**]({file_path})", unsafe_allow_html=True)
                st.session_state[click_key] = 0
            else:
                st.info("Click once more to open the book!")

    conn.close()


# ---------- MAIN ----------
if __name__ == "__main__":
    create_database()
    display_books()
