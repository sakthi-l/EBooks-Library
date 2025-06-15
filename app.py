import streamlit as st
import sqlite3

# ---------- STEP 1: Create the database if it doesn't exist ----------
def create_database():
    conn = sqlite3.connect("ebooks.db")
    cursor = conn.cursor()

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

    conn.commit()
    conn.close()

# ---------- STEP 2: Insert a new book ----------
def insert_book(title, author, language, description, file_path):
    conn = sqlite3.connect("ebooks.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO books (title, author, language, description, file_path)
        VALUES (?, ?, ?, ?, ?)
    """, (title, author, language, description, file_path))

    conn.commit()
    conn.close()

# ---------- STEP 3: Display books based on search ----------
def display_books(search_term):
    conn = sqlite3.connect("ebooks.db")
    cursor = conn.cursor()

    query = """
        SELECT book_id, title, author, language, description, file_path
        FROM books
        WHERE title LIKE ? OR author LIKE ? OR language LIKE ?
    """
    like_term = f"%{search_term}%"
    cursor.execute(query, (like_term, like_term, like_term))
    books = cursor.fetchall()
    conn.close()

    st.subheader("📚 Matching Books")

    if not books:
        st.info("No books found matching your search.")
        return

    for book in books:
        book_id, title, author, language, description, file_path = book

        btn_key = f"btn_{book_id}"
        click_key = f"clicks_{book_id}"

        if click_key not in st.session_state:
            st.session_state[click_key] = 0

        clicked = st.button(f"📖 {title} by {author} ({language})", key=btn_key)

        if clicked:
            st.session_state[click_key] += 1

            if st.session_state[click_key] == 2:
                st.success(f"✅ Opening: {title}")
                st.markdown(f"🔗 [Click here to open **{title}**]({file_path})", unsafe_allow_html=True)
                st.session_state[click_key] = 0
            else:
                st.info("Click once more to open the book!")

# ---------- STEP 4: Form to insert book ----------
def book_entry_form():
    st.subheader("➕ Add New Book")
    with st.form("new_book_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        language = st.text_input("Language")
        description = st.text_area("Description")
        file_path = st.text_input("File URL (Link)")

        submitted = st.form_submit_button("Add Book")
        if submitted:
            if title and author and file_path:
                insert_book(title, author, language, description, file_path)
                st.success(f"✅ Book '{title}' added successfully!")
            else:
                st.error("❗ Title, Author, and File URL are required.")

# ---------- MAIN ----------
def main():
    st.title("📚 Multilingual eBook Library")
    st.markdown("Search and click a book **twice** to open the link.")

    create_database()

    # Book search box
    search_term = st.text_input("🔍 Search by title, author, or language", "")

    # Show filtered books
    display_books(search_term)

    st.markdown("---")
    # Add book form
    book_entry_form()

if __name__ == "__main__":
    main()
