# API Usage Examples

This document provides code examples for interacting with the WhatsApp Web Client API in various programming languages.

## API Endpoints

The API provides the following endpoints:

1. **GET /api/status** - Check connection status
2. **POST /send** - Send a WhatsApp message
3. **POST /api/simulate_connect** - (Demo) Simulate WhatsApp connection
4. **POST /api/simulate_disconnect** - (Demo) Simulate WhatsApp disconnection

## JavaScript Examples

### Checking Connection Status

```javascript
// Checking WhatsApp connection status
fetch('http://localhost:5000/api/status')
  .then(response => response.json())
  .then(data => {
    if (data.connected) {
      console.log('Connected to WhatsApp as', data.phone_number);
    } else {
      console.log('Not connected to WhatsApp');
      // If QR code is available
      if (data.qr_code_image) {
        // Display QR code for scanning
        const qrImage = document.createElement('img');
        qrImage.src = `data:image/png;base64,${data.qr_code_image}`;
        document.body.appendChild(qrImage);
      }
    }
  })
  .catch(error => console.error('Error:', error));
```

### Sending a Message

```javascript
// Sending a WhatsApp message
const messageData = {
  phone: '911234567890',  // Replace with actual phone number (with country code)
  message: 'Hello from JavaScript!'
};

fetch('http://localhost:5000/send', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(messageData),
})
.then(response => response.json())
.then(data => {
  if (data.status === 'success') {
    console.log('Message sent successfully');
  } else {
    console.error('Error:', data.message);
  }
})
.catch(error => console.error('Error:', error));
```

### Simulating Connection (Demo)

```javascript
// Simulating WhatsApp connection
fetch('http://localhost:5000/api/simulate_connect', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ phone: '911234567890' }),
})
.then(response => response.json())
.then(data => {
  if (data.success) {
    console.log('Successfully connected to WhatsApp');
  } else {
    console.error('Connection failed:', data.error);
  }
})
.catch(error => console.error('Error:', error));
```

## Python Examples

### Checking Connection Status

```python
import requests

# Check WhatsApp connection status
response = requests.get('http://localhost:5000/api/status')
data = response.json()

if data['connected']:
    print(f"Connected to WhatsApp as {data['phone_number']}")
else:
    print("Not connected to WhatsApp")
    # If QR code is available, you could save it to a file
    if 'qr_code_image' in data:
        import base64
        qr_image = data['qr_code_image']
        with open('whatsapp_qr.png', 'wb') as f:
            f.write(base64.b64decode(qr_image))
        print("QR code saved to whatsapp_qr.png")
```

### Sending a Message

```python
import requests

# Send a WhatsApp message
message_data = {
    'phone': '911234567890',  # Replace with actual phone number
    'message': 'Hello from Python!'
}

response = requests.post('http://localhost:5000/send', json=message_data)
data = response.json()

if data['status'] == 'success':
    print('Message sent successfully')
else:
    print(f"Error: {data['message']}")
```

### Simulating Connection (Demo)

```python
import requests

# Simulate WhatsApp connection
response = requests.post(
    'http://localhost:5000/api/simulate_connect',
    json={'phone': '911234567890'}
)
data = response.json()

if data['success']:
    print('Successfully connected to WhatsApp')
else:
    print(f"Connection failed: {data.get('error', 'Unknown error')}")
```

## cURL Examples

### Checking Connection Status

```bash
curl -X GET http://localhost:5000/api/status
```

### Sending a Message

```bash
curl -X POST http://localhost:5000/send \
  -H "Content-Type: application/json" \
  -d '{"phone":"911234567890","message":"Hello from cURL!"}'
```

### Simulating Connection (Demo)

```bash
curl -X POST http://localhost:5000/api/simulate_connect \
  -H "Content-Type: application/json" \
  -d '{"phone":"911234567890"}'
```

## Node.js Examples

### Checking Connection Status

```javascript
const axios = require('axios');

// Check WhatsApp connection status
axios.get('http://localhost:5000/api/status')
  .then(response => {
    const data = response.data;
    if (data.connected) {
      console.log(`Connected to WhatsApp as ${data.phone_number}`);
    } else {
      console.log('Not connected to WhatsApp');
      // Handle QR code if needed
    }
  })
  .catch(error => console.error('Error:', error));
```

### Sending a Message

```javascript
const axios = require('axios');

// Send a WhatsApp message
const messageData = {
  phone: '911234567890',  // Replace with actual phone number
  message: 'Hello from Node.js!'
};

axios.post('http://localhost:5000/send', messageData)
  .then(response => {
    const data = response.data;
    if (data.status === 'success') {
      console.log('Message sent successfully');
    } else {
      console.error('Error:', data.message);
    }
  })
  .catch(error => console.error('Error:', error));
```

## Integration Tips

1. **Error Handling**: Always implement robust error handling when using the API.

2. **Connection Check**: Before sending messages, check the connection status to ensure WhatsApp is connected.

3. **Rate Limiting**: Implement rate limiting in your application to avoid overwhelming the WhatsApp service.

4. **Webhooks**: In a production environment, you would want to implement webhooks for delivery receipts.

5. **Security**: In a real-world scenario, add proper authentication to these API endpoints.