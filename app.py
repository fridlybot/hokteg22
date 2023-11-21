
# from flask import Flask, request
# from flask_cors import CORS 
# import requests

# app = Flask(__name__)

# # Use Flask-CORS with default options
# CORS(app)

# # Replace with your Google Apps Script web app URL
# GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzRuc_TqUsLK7bmYj3QLvl8-MtpeGOCTV_dOoMLm2DzOK2wZAT7n0hRRA4-KMFv6wBWSw/exec"

# @app.route('/webhook', methods=['POST'])
# def webhook():
#     data = request.json  # Assuming the incoming data is in JSON format
    
#     # Send the data to Google Apps Script
#     response = requests.post(GOOGLE_SCRIPT_URL, json=data)
    
#     # Handle the response from the Google Apps Script if needed
#     if response.status_code == 200:
#         return "Data sent to Google Apps Script successfully"
#     else:
#         return "Failed to send data to Google Apps Script"

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, request
from flask_cors import CORS 
import requests
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Replace with your Google Apps Script web app URL
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzRuc_TqUsLK7bmYj3QLvl8-MtpeGOCTV_dOoMLm2DzOK2wZAT7n0hRRA4-KMFv6wBWSw/exec"

# SQLite database file
DB_FILE = "dataDB.db"
SQL_SCRIPT = "init.sql"

# Create tables from SQL script
def create_tables():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    
    with open(SQL_SCRIPT, 'r') as script_file:
        script = script_file.read()
        cursor.executescript(script)
    
    connection.commit()
    connection.close()

# Route to handle incoming data and store it in the database
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json  # Assuming the incoming data is in JSON format

    # Send the data to Google Apps Script
    response = requests.post(GOOGLE_SCRIPT_URL, json=data)
    
    # Store data in the local database
    create_tables()
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    # Insert order information
    cursor.execute('''
        INSERT INTO orders (chat_id) VALUES (?)
    ''', (data.get('chatId'),))
    order_id = cursor.lastrowid  # Get the ID of the inserted order

    # Insert order items
    for item_id, item_data in data.get('foods', {}).items():
        cursor.execute('''
            INSERT INTO order_items (order_id, title, quantity, price) VALUES (?, ?, ?, ?)
        ''', (order_id, item_data.get('title'), item_data.get('quantity'), item_data.get('price')))

    connection.commit()
    connection.close()

    # Handle the response from the Google Apps Script if needed
    if response.status_code == 200:
        return "Data sent to Google Apps Script and stored in the database successfully"
    else:
        return "Failed to send data to Google Apps Script, but data stored in the database"

if __name__ == '__main__':
    # Create tables when the script is run
    create_tables()
    app.run(debug=True)

