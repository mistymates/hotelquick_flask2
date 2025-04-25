import sqlite3
from flask import g

DATABASE = 'destinations.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

class Destination:
    @staticmethod
    def create_table():
        """Create the destinations table if it doesn't exist."""
        db = get_db()
        cursor = db.cursor()
        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS destinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            duration TEXT NOT NULL,
            image_url TEXT NOT NULL
        )
        ''')
        db.commit()
    
    @staticmethod
    def get_all():
        """Retrieve all destinations from the database."""
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM destinations")
        destinations = [dict(row) for row in cursor.fetchall()]
        return destinations

    @staticmethod
    def get_by_id(destination_id):
        """Retrieve a specific destination by its ID."""
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM destinations WHERE id=?", (destination_id,))
        destination = cursor.fetchone()
        return dict(destination) if destination else None

    @staticmethod
    def create(name, description, price, duration, image_url):
        """Create a new destination in the database."""
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO destinations (name, description, price, duration, image_url) VALUES (?, ?, ?, ?, ?)",
            (name, description, price, duration, image_url)
        )
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def create_sample_data():
        """Insert sample destination data if the table is empty."""
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM destinations")
        count = cursor.fetchone()[0]
        
        if count == 0:
            sample_destinations = [
                ('Hotel Borobudur Jakarta', 'A luxurious 5-star hotel in the heart of Jakarta, offering elegant rooms and world-class amenities.',
                 1250000, '1 night', 'https://i.imgur.com/1irutwz.jpeg'),
                ('The Pavilions Bali', 'An adults-only boutique resort featuring private pool villas surrounded by lush rice terraces.',
                 2250000, '1 night', 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=1950&q=80'),
                ('Sheraton Mustika Yogyakarta', 'Riverside resort near Prambanan temples, with spacious rooms and spa services.',
                 950000, '1 night', 'https://www.agoda.com/images/hotel/sheraton-mustika-yogyakarta.jpg'),
                ('Grand Mercure Bandung Setiabudi', 'Modern hotel in Bandung with mountain views, fine dining, and meeting facilities.',
                 800000, '1 night', 'https://www.accorhotels.com/images/hotel/grand-mercure-bandung.jpg'),
                ('Plataran Komodo Beach Resort', 'Beachfront resort on Flores Island offering traditional architecture and diving packages.',
                 3100000, '1 night', 'https://www.myboutiquehotel.com/images/hotel/plataran-komodo.jpg')
            ]
            cursor.executemany(
                "INSERT INTO destinations (name, description, price, duration, image_url) VALUES (?, ?, ?, ?, ?)",
                sample_destinations
            )
            db.commit()
            return True
        return False
