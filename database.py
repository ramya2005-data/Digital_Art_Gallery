import sqlite3

connection = sqlite3.connect("gallery.db")
cursor = connection.cursor()

# ---------------- USERS TABLE ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'user'
)
""")

# ---------------- ARTISTS TABLE ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS artists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    movement TEXT,
    nationality TEXT,
    bio TEXT
)
""")

# ---------------- ARTWORKS TABLE ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS artworks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    year TEXT,
    style TEXT,
    medium TEXT,
    description TEXT,
    price REAL,
    availability TEXT DEFAULT 'Available',
    image TEXT
)
""")

# Add image column if it does not already exist
try:
    cursor.execute("ALTER TABLE artworks ADD COLUMN image TEXT")
except sqlite3.OperationalError:
    pass

# ---------------- ADMIN ACCOUNT ----------------

cursor.execute("""
INSERT OR IGNORE INTO users
(name, email, password, role)
VALUES (?, ?, ?, ?)
""", (
    "Admin",
    "admin@gmail.com",
    "admin123",
    "admin"
))

# ---------------- PURCHASE REQUESTS TABLE ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS purchase_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT NOT NULL,
    artwork_id INTEGER NOT NULL,
    request_date TEXT NOT NULL,
    status TEXT DEFAULT 'Pending'
)
""")

# ---------------- AVAILABILITY REQUESTS TABLE ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS availability_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT NOT NULL,
    artwork_id INTEGER NOT NULL,
    request_date TEXT NOT NULL,
    status TEXT DEFAULT 'Waiting'
)
""")

# ---------------- NOTIFICATIONS TABLE ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TEXT NOT NULL,
    is_read INTEGER DEFAULT 0
)
""")

connection.commit()
connection.close()

print("Database updated successfully!")