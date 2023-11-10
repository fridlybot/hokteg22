from flask import Flask, request
from flask_cors import CORS 
import requests
import os

app = Flask(__name__)

# Use Flask-CORS with default options
CORS(app)

# Replace with your Google Apps Script web app URL
GOOGLE_SCRIPT_URL = os.environ.get('GOOGLE_SCRIPT_URL', 'https://script.google.com/macros/s/AKfycbzRuc_TqUsLK7bmYj3QLvl8-MtpeGOCTV_dOoMLm2DzOK2wZAT7n0hRRA4-KMFv6wBWSw/exec')

# Replace with your ngrok backend service URL
BACKEND_NGROK_SERVICE_URL = os.environ.get('BACKEND_NGROK_SERVICE_URL', 'https://d31c-41-100-195-1.ngrok-free.app/print')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json  # Assuming the incoming data is in JSON format
    
    # Send the data to Google Apps Script
    try:
        response_google_script = requests.post(GOOGLE_SCRIPT_URL, json=data)
        response_google_script.raise_for_status()
        app.logger.info("Data sent to Google Apps Script successfully")
    except requests.RequestException as e:
        app.logger.error(f"Failed to send data to Google Apps Script: {str(e)}")
        return "Failed to send data to Google Apps Script", 500  # Internal Server Error
    
    # Send the data to the ngrok backend service
    try:
        response_ngrok_service = requests.post(BACKEND_NGROK_SERVICE_URL, json=data)
        response_ngrok_service.raise_for_status()
        app.logger.info("Data sent to ngrok backend service successfully")
    except requests.RequestException as e:
        app.logger.error(f"Failed to send data to ngrok backend service: {str(e)}")
        return "Failed to send data to ngrok backend service", 500  # Internal Server Error
    
    return "Data sent successfully to both Google Apps Script and ngrok backend service"

if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc')






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
