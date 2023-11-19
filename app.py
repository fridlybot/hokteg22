
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





# from flask import Flask, request, jsonify
# from flask_cors import CORS 
# import requests


# app = Flask(__name__)

# # Use Flask-CORS with default options
# CORS(app)

# # Replace with your Google Apps Script web app URL
# GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzRuc_TqUsLK7bmYj3QLvl8-MtpeGOCTV_dOoMLm2DzOK2wZAT7n0hRRA4-KMFv6wBWSw/exec"

# @app.route('/webhook', methods=['POST'])
# def webhook():
#     try:
#         data = request.json  # Assuming the incoming data is in JSON format
        
#         # Validate and sanitize the data if needed

#         # Send the data to Google Apps Script
#         response = requests.post(GOOGLE_SCRIPT_URL, json=data)

#         # Handle the response from the Google Apps Script if needed
#         if response.status_code == 200:
#             # return "Data sent to Google Apps Script successfully"
#              return jsonify(data)  # Returning the incoming data as JSON
#         else:
#             app.logger.error(f"Failed to send data to Google Apps Script. Status code: {response.status_code}")
#             return "Failed to send data to Google Apps Script"
#     except Exception as e:
#         app.logger.exception("An error occurred during webhook processing.")
#         return "Internal server error", 500

# @app.route('/dataFood', methods=['GET'])
# def get_data_food():
#     try:
#         data = request.json  # Assuming the incoming data is in JSON format

#         # Extract relevant information for the /dataFood endpoint
#         food_data = []
#         for food_id, food_info in data.get("foods", {}).items():
#             food_data.append({
#                 "id": food_id,
#                 "title": food_info.get("title", ""),
#                 "quantity": food_info.get("quantity", 0),
#                 "price": food_info.get("price", 0)
#             })

#         # Build the response JSON
#         response_data = {
#             "chatId": data.get("chatId", 0),
#             "foods": food_data
#         }

#         return jsonify(response_data)
#     except Exception as e:
#         app.logger.exception("An error occurred during processing the GET request.")
#         return "Internal server error", 500

# if __name__ == '__main__':
#     app.run(debug=True)





from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

GOOGLE_SCRIPT_URL = "https://telegramrequestbot.onrender.com/webhook"

last_received_data = None

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    global last_received_data

    if request.method == 'POST':
        # If it's a POST request, update the last received data
        data = request.json
        last_received_data = data

        # Send the data to Google Apps Script
        response = requests.post(GOOGLE_SCRIPT_URL, json=data)

        if response.status_code == 200:
            return jsonify(data)
        else:
            return "Failed to send data to Google Apps Script"
    elif request.method == 'GET':
        # If it's a GET request, return the last received data as JSON
        if last_received_data is not None:
            return jsonify(last_received_data)
        else:
            return "No data received yet"

if __name__ == '__main__':
    app.run(debug=True)

