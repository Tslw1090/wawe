# WhatsApp Web Client API

A Flask-based WhatsApp client API with status checking and message sending capabilities.

## Features

- **Status Monitoring**: Check WhatsApp connection status with QR code display
- **Message Sending**: Send WhatsApp messages via API calls
- **Modern UI**: Clean, responsive Bootstrap interface
- **Interactive Documentation**: Detailed API documentation with examples
- **Demo Controls**: Test the application with simulated connection features

## Screenshots

Here are some screenshots of the application (when deployed):

- Home Page: Displays main navigation and quick test form
- Status Page: Shows connection status and QR code when not connected
- Documentation: Provides detailed API usage examples

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Local Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/Tslw1090/wawe.git
   cd wawe
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python main.py
   ```

5. Open your browser and go to http://localhost:5000

### Required Python Packages

- Flask
- Flask-SQLAlchemy
- gunicorn (for production deployment)
- qrcode
- pillow (for QR code generation)

## Usage

### Connecting to WhatsApp

1. Navigate to the `/status` endpoint in your browser
2. If not connected, you'll see a QR code
3. In a real implementation, you would scan this QR code with WhatsApp on your phone
4. For demo purposes, use the "Simulate Connection" button at the bottom of the page

### Sending Messages

**Via Web Interface:**

1. Go to the homepage
2. Fill in the "Quick Test" form with a phone number and message
3. Click "Send Message"

**Via API:**

Make a POST request to `/send` with the following JSON payload:

```json
{
  "phone": "911234567890",
  "message": "Hello from WhatsApp Web Client API!"
}
```

Example using curl:

```bash
curl -X POST http://localhost:5000/send \
  -H "Content-Type: application/json" \
  -d '{"phone":"911234567890","message":"Hello from API"}'
```

## API Documentation

### Status Endpoint

**GET /api/status**

Returns the current WhatsApp connection status, with QR code data if not connected.

### Message Sending Endpoint

**POST /send**

Sends a WhatsApp message to the specified phone number.

Required JSON payload:
- `phone`: Phone number with country code (e.g., "911234567890")
- `message`: Message content to send

## Deploying to Other Platforms

### Deploying to Heroku

1. Make sure you have the Heroku CLI installed and are logged in.
2. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```
3. Create a `Procfile` in the root directory with:
   ```
   web: gunicorn main:app
   ```
4. Add a `requirements.txt` file with all dependencies.
5. Deploy to Heroku:
   ```bash
   git push heroku main
   ```

### Deploying to Docker

1. Create a `Dockerfile`:
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   EXPOSE 5000
   
   CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
   ```
2. Build and run the Docker image:
   ```bash
   docker build -t whatsapp-web-client .
   docker run -p 5000:5000 whatsapp-web-client
   ```

## Implementation Notes

This is a demonstration application that simulates WhatsApp connection functionality. In a real-world implementation, you would:

1. Use an official WhatsApp Business API or a compatible library
2. Implement proper authentication and security measures
3. Add a database to store message history and user profiles
4. Handle webhooks for message delivery status and notifications

## License

MIT License - Feel free to use, modify, and distribute this code.

## Disclaimer

This project is for educational purposes only. For production use, please use official WhatsApp Business APIs.