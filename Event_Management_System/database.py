import sqlite3


# Database connection function
def get_connection():
    """Create a new database connection"""
    conn = sqlite3.connect('events.db')
    return conn


# Initialize database with tables
def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS events
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       name
                       TEXT
                       NOT
                       NULL,
                       date
                       TEXT
                       NOT
                       NULL,
                       location
                       TEXT
                       NOT
                       NULL,
                       description
                       TEXT
                   )
                   ''')

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS attendees
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       event_id
                       INTEGER,
                       name
                       TEXT
                       NOT
                       NULL,
                       email
                       TEXT,
                       FOREIGN
                       KEY
                   (
                       event_id
                   ) REFERENCES events
                   (
                       id
                   )
                       )
                   ''')

    conn.commit()
    conn.close()


# Initialize on import
init_database()


# Function to add an event
def add_event(name, date, location, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO events (name, date, location, description) VALUES (?, ?, ?, ?)',
                   (name, date, location, description))
    conn.commit()
    event_id = cursor.lastrowid
    conn.close()
    return event_id


# Function to get all events
def get_all_events():
    """Retrieve all events from database"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events')
    events = cursor.fetchall()
    conn.close()
    return events


# Function to get specific event details by ID
def get_event_details(event_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, date, location, description FROM events WHERE id = ?', (event_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return {
            'id': result[0],
            'name': result[1],
            'date': result[2],
            'location': result[3],
            'description': result[4]
        }
    return None


# Function to add an attendee to an event
def add_attendee(event_id, name, email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO attendees (event_id, name, email) VALUES (?, ?, ?)',
                   (event_id, name, email))
    conn.commit()
    # Force write to disk
    cursor.execute('PRAGMA wal_checkpoint(FULL)')
    conn.commit()
    conn.close()


# Function to get attendees for an event
def get_attendees(event_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name, email FROM attendees WHERE event_id = ?', (event_id,))
    attendees = cursor.fetchall()
    conn.close()
    return attendees


# ✅ Function to delete an event with auto ID reset
def delete_event(event_id):
    """Delete an event from the database by ID"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Delete the event
        cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))

        # ✅ Also delete associated attendees
        cursor.execute("DELETE FROM attendees WHERE event_id = ?", (event_id,))

        # ✅ Check if events table is empty
        cursor.execute("SELECT COUNT(*) FROM events")
        count = cursor.fetchone()[0]

        # ✅ If no events left, reset the ID counter to start from 1
        if count == 0:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='events'")

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(f"Error deleting event: {e}")
        return False


# ✅ Optional: Function to manually reset ID counter for events
def reset_event_id_counter():
    """Reset the event ID counter to 1 (use when table is empty)"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check if table is empty first
        cursor.execute("SELECT COUNT(*) FROM events")
        count = cursor.fetchone()[0]

        if count == 0:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='events'")
            conn.commit()
            conn.close()
            return True
        else:
            print("Cannot reset: Events table is not empty")
            conn.close()
            return False

    except Exception as e:
        print(f"Error resetting counter: {e}")
        return False


# Function to close the database connection (optional - connections auto-close now)
def close_db():
    pass  # Not needed anymore as each function opens/closes its own connection