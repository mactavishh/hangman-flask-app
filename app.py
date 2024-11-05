from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the SQLite database
def init_db():
    with sqlite3.connect('hangman.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                word TEXT PRIMARY KEY
            )
        ''')
        # Prepopulate the words table with some words
        words = ['SUNS'
  'SUNS', 'KAĶIS', 'MĀJA', 'SKOLA', 'GRĀMATA',
  'GALDA', 'DZIESMA', 'ZIVS', 'ŪDENS', 'ZVAIGZNE',
  'LAPA', 'KOKS', 'ZIEMA', 'VĀRDS', 'ROKA',
  'AUTO', 'VILCIENS', 'LIETUS', 'DRAUGS', 'DZIMŠANA',
  'PUĶE', 'DEBESIS', 'SMILTIS', 'VĒJŠ', 'SIRDS',
  'GULŠŅĀT', 'LAPA', 'GAISMA', 'KALNS', 'MEŽS',
  'CEĻOJUMS', 'TELEVIZORS', 'PIENA', 'KAFIJA', 'CEPUMS',
  'LAUKS', 'GRILĒT', 'TIKS', 'CIEMA', 'DZĒRVES',
  'VIENKĀRŠS', 'BIBLIOTEKA', 'STRĒLNIEKS', 'SVĒTKI', 'ĒDIENS',
  'LAIME', 'DĀVANA', 'LĀCIS', 'SAULE', 'ZEME'
]
        cursor.executemany('INSERT OR IGNORE INTO words (word) VALUES (?)', [(word,) for word in words])
        conn.commit()

@app.route('/words', methods=['GET'])
def get_words():
    with sqlite3.connect('hangman.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT word FROM words")
        words = cursor.fetchall()
        return jsonify([word[0] for word in words])

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    username = data['username']
    with sqlite3.connect('hangman.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
            conn.commit()
            return jsonify({'message': 'User registered successfully!'}), 200
        except sqlite3.IntegrityError:
            return jsonify({'message': 'User already exists!'}), 400

@app.route('/score', methods=['POST'])
def save_score():
    data = request.json
    username = data['username']
    win = data['win']

    with sqlite3.connect('hangman.db') as conn:
        cursor = conn.cursor()
        if win:
            cursor.execute("UPDATE users SET wins = wins + 1 WHERE username = ?", (username,))
        else:
            cursor.execute("UPDATE users SET losses = losses + 1 WHERE username = ?", (username,))
        conn.commit()
    return jsonify({'message': 'Score updated successfully!'}), 200

@app.route('/scoreboard', methods=['GET'])
def get_scoreboard():
    with sqlite3.connect('hangman.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username, wins, losses FROM users")
        scoreboard = cursor.fetchall()
        return jsonify([
            {'username': row[0], 'wins': row[1], 'losses': row[2]}
            for row in scoreboard
        ])

if __name__ == '__main__':
    init_db()  # Initialize the database and create tables if needed
    app.run(debug=True, host='0.0.0.0', port=5000)  # Allow connections from outside
