import sqlite3

DB_NAME = "gallery.db"


def initialize_database():

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # USERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    )
    """)

    # ARTWORKS
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

    # PURCHASE REQUESTS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS purchase_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT NOT NULL,
        artwork_id INTEGER NOT NULL,
        request_date TEXT NOT NULL,
        status TEXT DEFAULT 'Pending'
    )
    """)

    # AVAILABILITY REQUESTS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS availability_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT NOT NULL,
        artwork_id INTEGER NOT NULL,
        request_date TEXT NOT NULL,
        status TEXT DEFAULT 'Waiting'
    )
    """)

    # NOTIFICATIONS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at TEXT NOT NULL,
        is_read INTEGER DEFAULT 0
    )
    """)

    # ADMIN ACCOUNT
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

    # SAMPLE ARTWORKS
    artworks = [

        ("Mona Lisa", "Leonardo da Vinci", "1503",
         "Renaissance", "Oil on poplar",
         "A famous Renaissance portrait known for its mysterious expression.",
         50000, "Sold", "mona_lisa.jpg"),

        ("The Starry Night", "Vincent van Gogh", "1889",
         "Post-Impressionism", "Oil on canvas",
         "A famous night landscape filled with expressive swirling stars.",
         25000, "Available", "starry_night.jpg"),

        ("Water Lilies", "Claude Monet", "1899",
         "Impressionism", "Oil on canvas",
         "A peaceful garden scene showing Monet's interest in light and colour.",
         30000, "Available", "water_lilies.jpg"),

        ("The Scream", "Edvard Munch", "1893",
         "Expressionism", "Oil and pastel",
         "An expressive artwork representing strong emotion and anxiety.",
         28000, "Sold", "the_scream.jpg"),

        ("The Persistence of Memory", "Salvador Dali", "1931",
         "Surrealism", "Oil on canvas",
         "A dream-like painting featuring melting clocks.",
         40000, "Available", "persistence_memory.jpg"),

        ("The Last Supper", "Leonardo da Vinci", "1498",
         "Renaissance", "Tempera",
         "A famous depiction of Jesus and his disciples.",
         45000, "Sold", "the_last_supper.jpg"),

        ("American Gothic", "Grant Wood", "1930",
         "Regionalism", "Oil on beaverboard",
         "A well-known American Regionalist painting.",
         22000, "Available", "american_gothic.jpg"),

        ("The Birth of Venus", "Sandro Botticelli", "1485",
         "Renaissance", "Tempera on canvas",
         "A celebrated Renaissance painting depicting Venus.",
         38000, "Sold", "birth_of_venus.jpg"),

        ("The Kiss", "Gustav Klimt", "1908",
         "Symbolism", "Oil and gold leaf",
         "A decorative artwork famous for its golden patterns.",
         42000, "Available", "the_kiss.jpg"),

        ("Impression, Sunrise", "Claude Monet", "1872",
         "Impressionism", "Oil on canvas",
         "The painting that gave Impressionism its name.",
         32000, "Available", "impression_sunrise.jpg"),

        ("Self-Portrait", "Vincent van Gogh", "1889",
         "Post-Impressionism", "Oil on canvas",
         "A self-portrait showing Van Gogh's distinctive brushwork.",
         27000, "Sold", "self_portrait.jpg"),

        ("The Night Watch", "Rembrandt", "1642",
         "Baroque", "Oil on canvas",
         "A dramatic group portrait known for its lighting.",
         36000, "Available", "the_night_watch.jpg"),

        ("The Creation of Adam", "Michelangelo", "1512",
         "Renaissance", "Fresco",
         "A famous scene from the Sistine Chapel ceiling.",
         48000, "Sold", "creation_of_adam.jpg"),

        ("Les Demoiselles d'Avignon", "Pablo Picasso", "1907",
         "Cubism", "Oil on canvas",
         "An influential modern artwork associated with Cubism.",
         39000, "Available", "les_demoiselles.jpg"),

        ("Girl with a Pearl Earring", "Johannes Vermeer", "1665",
         "Baroque", "Oil on canvas",
         "A famous portrait known for its delicate lighting.",
         35000, "Available", "girl_pearl_earring.jpg")
    ]

    cursor.execute("SELECT COUNT(*) FROM artworks")
    artwork_count = cursor.fetchone()[0]

    if artwork_count == 0:

        cursor.executemany("""
        INSERT INTO artworks
        (title, artist, year, style, medium,
         description, price, availability, image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, artworks)

    connection.commit()
    connection.close()


initialize_database()
