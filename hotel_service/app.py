from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize database
def init_db():
    conn = sqlite3.connect('destinations.db')
    cursor = conn.cursor()
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
    conn.commit()
    conn.close()

# Create sample hotels in Indonesia if DB is empty
def create_sample_destinations():
    conn = sqlite3.connect('destinations.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM destinations")
    count = cursor.fetchone()[0]
    
    if count == 0:
        sample_destinations = [
            (
                'Hotel Borobudur Jakarta',
                'A luxurious 5-star hotel in the heart of Jakarta, offering elegant rooms and world-class amenities.',
                1250000,
                '1 night',
                'https://i.imgur.com/1irutwz.jpeg'
            ),
            (
                'The Pavilions Bali',
                'An adults-only boutique resort featuring private pool villas surrounded by lush rice terraces.',
                2250000,
                '1 night',
                'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=1950&q=80'
            ),
            (
                'Sheraton Mustika Yogyakarta',
                'Riverside resort near Prambanan temples, with spacious rooms and spa services.',
                950000,
                '1 night',
                'https://www.agoda.com/images/hotel/sheraton-mustika-yogyakarta.jpg'
            ),
            (
                'Grand Mercure Bandung Setiabudi',
                'Modern hotel in Bandung with mountain views, fine dining, and meeting facilities.',
                800000,
                '1 night',
                'https://www.accorhotels.com/images/hotel/grand-mercure-bandung.jpg'
            ),
            (
                'Plataran Komodo Beach Resort',
                'Beachfront resort on Flores Island offering traditional architecture and diving packages.',
                3100000,
                '1 night',
                'https://www.myboutiquehotel.com/images/hotel/plataran-komodo.jpg'
            )
        ]
        cursor.executemany(
            "INSERT INTO destinations (name, description, price, duration, image_url) VALUES (?, ?, ?, ?, ?)",
            sample_destinations
        )
        conn.commit()
    conn.close()

@app.route('/api/destinations', methods=['GET'])
def get_destinations():
    conn = sqlite3.connect('destinations.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM destinations")
    destinations = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({"destinations": destinations})

@app.route('/api/destinations/<int:destination_id>', methods=['GET'])
def get_destination(destination_id):
    conn = sqlite3.connect('destinations.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM destinations WHERE id=?", (destination_id,))
    destination = cursor.fetchone()
    conn.close()
    
    if destination:
        return jsonify(dict(destination))
    return jsonify({"error": "Destination not found"}), 404

@app.route('/api/destinations', methods=['POST'])
def add_destination():
    data = request.json or {}
    required = ['name', 'description', 'price', 'duration', 'image_url']
    if not all(key in data for key in required):
        return jsonify({"error": "Missing required fields"}), 400
    
    conn = sqlite3.connect('destinations.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO destinations (name, description, price, duration, image_url) VALUES (?, ?, ?, ?, ?)",
        (data['name'], data['description'], data['price'], data['duration'], data['image_url'])
    )
    conn.commit()
    destination_id = cursor.lastrowid
    conn.close()
    
    return jsonify({"id": destination_id, "message": "Hotel added successfully"}), 201

if __name__ == '__main__':
    init_db()
    create_sample_destinations()
    app.run(debug=True, port=5002)