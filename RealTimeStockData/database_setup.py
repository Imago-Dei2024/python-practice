import sqlite3
import os

DATABASE_FILE = 'financial_data.db'
SCHEMA_FILE = 'schema.sql'

def setup_database():
    """
    Sets up the database by creating tables from the schema.sql file.
    This function will delete and recreate the database file if it already exists
    to ensure a clean setup.
    """
    # Delete the old database file if it exists
    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)
        print(f"Removed old database file: {DATABASE_FILE}")

    try:
        # Connect to the SQLite database (this will create the file)
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        print(f"Successfully connected to {DATABASE_FILE}")

        # Read the SQL schema file
        with open(SCHEMA_FILE, 'r') as f:
            sql_script = f.read()
        
        # Execute the entire SQL script
        cursor.executescript(sql_script)
        print("Successfully executed schema and created tables.")

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
        print("Database setup complete and connection closed.")

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except FileNotFoundError:
        print(f"❌ Error: The schema file '{SCHEMA_FILE}' was not found.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == '__main__':
    setup_database()
