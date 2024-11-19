import sqlite3

def initialize_database():
    conn = sqlite3.connect('database/internship_management.db')
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # Internship Details table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS InternshipDetails (
            detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            company_name TEXT NOT NULL,
            company_address TEXT NOT NULL,
            external_mentor_name TEXT NOT NULL,
            external_mentor_contact TEXT NOT NULL,
            external_mentor_email TEXT NOT NULL,
            company_registration_number TEXT NOT NULL,
            city TEXT NOT NULL,
            stipend_amount REAL NOT NULL,
            offer_letter BLOB NOT NULL,
            FOREIGN KEY(student_id) REFERENCES Users(user_id)
        )
    """)

    # Reports table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Reports (
            report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            report_type TEXT NOT NULL,
            submission_date TEXT NOT NULL,
            file_path TEXT NOT NULL,
            mentor_marks REAL,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY(student_id) REFERENCES Users(user_id)
        )
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()
