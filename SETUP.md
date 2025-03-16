# Installation and Setup Instructions

This document provides detailed instructions for setting up the WhatsApp Web Client API on your local machine or deploying it to various platforms.

## Local Development Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Tslw1090/wawe.git
cd wawe
```

### Step 2: Create a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

Install the following required packages:

```bash
pip install flask==2.3.3
pip install flask-sqlalchemy==3.1.1
pip install gunicorn==23.0.0
pip install qrcode==7.4.2
pip install pillow==10.0.0
```

Or simply create a requirements.txt file with the following content and install all dependencies at once:

```
flask==2.3.3
flask-sqlalchemy==3.1.1
gunicorn==23.0.0
qrcode==7.4.2
pillow==10.0.0
```

Then run:
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
# Run the Flask development server
python main.py
```

The application will be available at http://localhost:5000

## Production Deployment

### Deploying to a VPS or Dedicated Server

1. Clone the repository on your server
2. Install dependencies (preferably in a virtual environment)
3. Set up a proper WSGI server (Gunicorn, uWSGI, etc.)
4. Configure Nginx or Apache as a reverse proxy
5. Set proper environment variables for production

Example Gunicorn startup command:
```bash
gunicorn --bind 0.0.0.0:5000 --workers 3 main:app
```

### Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### Docker Deployment

Create a Dockerfile in your project root:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

Build and run the Docker container:

```bash
docker build -t whatsapp-web-client .
docker run -p 5000:5000 whatsapp-web-client
```

## Environment Variables

The application uses the following environment variables:

- `SESSION_SECRET`: Secret key for Flask sessions (defaults to "whatsapp_web_client_secret" if not set)
- `DATABASE_URL`: Database connection URL (if using a database)

## Troubleshooting Common Issues

### Application Won't Start

- Check if all dependencies are installed correctly
- Verify that the port 5000 is not in use by another application
- Make sure you have the correct Python version installed

### QR Code Not Displaying

- Ensure the Pillow library is installed correctly
- Check for any errors in the server logs

### Connection Simulation Not Working

- Verify that JavaScript is enabled in your browser
- Check for any console errors in the browser developer tools