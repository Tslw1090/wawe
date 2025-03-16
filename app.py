import os
import logging
import json
import qrcode
import io
import base64
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from whatsapp_client import WhatsAppClient

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "whatsapp_web_client_secret")

# Initialize WhatsApp client
whatsapp_client = WhatsAppClient()

@app.route('/')
def index():
    """
    Render the home page with links to status and documentation
    """
    return render_template('index.html')

@app.route('/status')
def status():
    """
    Display the WhatsApp connection status and QR code if not connected
    """
    return render_template('status.html')

@app.route('/api/status', methods=['GET'])
def api_status():
    """
    API endpoint to check the WhatsApp connection status
    Returns: JSON with status and QR code if needed
    """
    status_info = whatsapp_client.get_status()
    
    if not status_info['connected']:
        # Generate QR code
        qr_data = status_info.get('qr_code', '')
        if qr_data:
            # Create a QR code with higher error correction for better scanning
            qr = qrcode.QRCode(
                version=4,  # Higher version for more data capacity
                error_correction=qrcode.constants.ERROR_CORRECT_H,  # Higher error correction
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # Create QR code image with clear contrast
            img = qr.make_image(fill_color="black", back_color="white")
            buffered = io.BytesIO()
            img.save(buffered, format="PNG", quality=100)  # Use high quality PNG
            qr_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            status_info['qr_code_image'] = qr_base64
    
    return jsonify(status_info)

@app.route('/api/simulate_connect', methods=['POST'])
def simulate_connect():
    """
    Demo endpoint to simulate a successful WhatsApp connection
    Expects JSON with 'phone' field
    Returns: JSON with success flag
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        phone = data.get('phone', '919876543210')  # Default phone if not provided
        
        # Simulate successful connection
        success = whatsapp_client.simulate_connection(phone)
        
        return jsonify({'success': success})
    except Exception as e:
        logger.exception("Error simulating connection")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/simulate_disconnect', methods=['POST'])
def simulate_disconnect():
    """
    Demo endpoint to simulate WhatsApp disconnection
    Returns: JSON with success flag
    """
    try:
        # Simulate disconnection
        success = whatsapp_client.disconnect()
        
        return jsonify({'success': success})
    except Exception as e:
        logger.exception("Error simulating disconnection")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/send', methods=['POST'])
def send_message():
    """
    Send a WhatsApp message to a specified number
    Expects JSON with 'phone' and 'message' fields
    Returns: JSON with status and error if any
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'status': 'error', 'message': 'No data provided'}), 400
        
        phone = data.get('phone')
        message = data.get('message')
        
        if not phone or not message:
            return jsonify({'status': 'error', 'message': 'Phone number and message are required'}), 400
        
        # Check if connected to WhatsApp
        status_info = whatsapp_client.get_status()
        if not status_info['connected']:
            return jsonify({
                'status': 'error', 
                'message': 'Not connected to WhatsApp. Please scan the QR code at /status'
            }), 403
        
        # Send the message
        result = whatsapp_client.send_message(phone, message)
        
        if result['success']:
            return jsonify({'status': 'success', 'message': 'Message sent successfully'})
        else:
            return jsonify({'status': 'error', 'message': result['error']}), 500
            
    except Exception as e:
        logger.exception("Error sending message")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/docs')
def docs():
    """
    Display API documentation
    """
    return render_template('docs.html')

# Error handling routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html', error="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('index.html', error="Server error occurred"), 500
