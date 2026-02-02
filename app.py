from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect("tetris.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, score, level, played_at FROM high_scores ORDER BY score DESC LIMIT 10")
    scores = cursor.fetchall()
    conn.close()
    return render_template('index.html', scores=scores)

if __name__ == '__main__':
    app.run(debug=True, port=5000)