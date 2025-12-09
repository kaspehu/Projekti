import os
import mysql.connector
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

conn = mysql.connector.connect(
    host=os.environ.get('HOST'),
    port=3306,
    database=os.environ.get('DB_NAME'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASS'),
    autocommit=True,
    use_pure=True
)


@app.route("/api/airports")
def api_airports():
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT ident, name, latitude_deg, longitude_deg 
        FROM Airport 
        WHERE iso_country = 'BR' 
          AND type = 'medium_airport'
        ORDER BY RAND() 
        LIMIT 30
    """)

    rows = cur.fetchall()
    return jsonify(rows)


if __name__ == "__main__":
    app.run(debug=True)
