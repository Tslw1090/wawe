import os
import logging
import time
import threading
import uuid
import random
import string
import base64
import io
import qrcode

logger = logging.getLogger(__name__)

class WhatsAppClient:
    """
    A simulated WhatsApp client for demonstration purposes.
    Uses the qrcode library to generate proper WhatsApp-like QR codes.
    
    In a real-world implementation, you would use an official WhatsApp API
    or a library that connects to the WhatsApp Web service.
    """
    def __init__(self):
        self.connected = False
        self.qr_code = None
        self.qr_code_image_base64 = None
        self.connection_time = None
        self.phone_number = None
        self.error = None
        self.messages = []  # Store sent messages for demo purposes
        
        # Initialize connection status
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Initialize connection status - generates a proper WhatsApp QR code"""
        self.connected = False
        
        # Generate a real WhatsApp web link
        session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        # This is the actual format WhatsApp Web uses
        self.qr_code = f"WAWC={session_id}:{int(time.time())}"
        
        # Generate QR code image directly here
        self._generate_qr_image()
        
        logger.info("WhatsApp connection initialized with new QR code. Ready for scan.")
        
    def _generate_qr_image(self):
        """Generate QR code image for the current qr_code value"""
        try:
            qr = qrcode.QRCode(
                version=4,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(self.qr_code)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            self.qr_code_image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        except Exception as e:
            logger.exception("Error generating QR code image")
            self.qr_code_image_base64 = None
    
    def get_status(self):
        """
        Get the current connection status
        Returns: dict with status information
        
        Note: This will generate a new QR code every time if not connected
        to ensure freshness of the code for better scanning
        """
        # If not connected, generate a new QR code to ensure freshness
        if not self.connected:
            self._initialize_connection()
            
        status_info = {
            'connected': self.connected,
            'qr_code': self.qr_code if not self.connected else None,
            'qr_code_image': self.qr_code_image_base64 if not self.connected else None,
            'connection_time': self.connection_time,
            'phone_number': self.phone_number,
        }
        
        if self.error:
            status_info['error'] = self.error
        
        return status_info
    
    def simulate_connection(self, phone_number):
        """
        Simulate a successful WhatsApp connection after QR scan
        """
        self.connected = True
        self.qr_code = None
        self.connection_time = time.time()
        self.phone_number = phone_number
        self.error = None
        logger.info(f"Connected to WhatsApp as {phone_number}")
        return True
    
    def disconnect(self):
        """
        Disconnect from WhatsApp
        """
        self.connected = False
        self.connection_time = None
        self.phone_number = None
        self._initialize_connection()
        logger.info("Disconnected from WhatsApp")
        return True
    
    def send_message(self, phone, message):
        """
        Simulate sending a WhatsApp message to the specified phone number
        Args:
            phone: Target phone number (with country code, no + needed)
            message: Message content
        Returns:
            dict: Result with success flag and error if any
        """
        if not self.connected:
            return {
                'success': False,
                'error': 'Not connected to WhatsApp'
            }
        
        try:
            # Format the phone number (remove any + at the beginning)
            if phone.startswith('+'):
                phone = phone[1:]
            
            # Simulate message sending process
            def send_in_thread():
                try:
                    # Simulate potential errors for demo purposes (10% chance of failure)
                    if random.random() < 0.1:
                        error_type = random.choice(['network', 'invalid_number', 'timeout'])
                        
                        if error_type == 'network':
                            self.error = "Network connection error"
                            logger.error("Network connection issue while sending message")
                        elif error_type == 'invalid_number':
                            self.error = "Invalid phone number format"
                            logger.error(f"Invalid phone number format: {phone}")
                        else:
                            self.error = "Operation timed out"
                            logger.error("Message sending timed out")
                    else:
                        # Successfully sent
                        msg_id = str(uuid.uuid4())
                        timestamp = time.time()
                        self.messages.append({
                            'id': msg_id,
                            'phone': phone,
                            'message': message,
                            'timestamp': timestamp,
                            'status': 'sent'
                        })
                        logger.info(f"Message sent to +{phone}: {message[:30]}...")
                except Exception as e:
                    self.error = str(e)
                    logger.exception(f"Error sending message to +{phone}")
            
            # Run in a separate thread to simulate async behavior
            threading.Thread(target=send_in_thread).start()
            
            return {
                'success': True,
                'message': 'Message sending initiated'
            }
            
        except Exception as e:
            logger.exception(f"Error sending message to {phone}")
            return {
                'success': False,
                'error': str(e)
            }
