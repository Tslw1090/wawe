import json
import unittest
from app import app
from whatsapp_client import WhatsAppClient


class TestApp(unittest.TestCase):
    """Tests for the Flask application."""

    def setUp(self):
        """Set up test client and other test variables."""
        self.app = app
        self.client = self.app.test_client()
        self.client.testing = True

    def test_index_route(self):
        """Test the index route."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'WhatsApp Web Client API', response.data)

    def test_status_route(self):
        """Test the status route."""
        response = self.client.get('/status')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Connection Status', response.data)

    def test_docs_route(self):
        """Test the docs route."""
        response = self.client.get('/docs')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'API Documentation', response.data)

    def test_api_status_route(self):
        """Test the API status endpoint."""
        response = self.client.get('/api/status')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('connected', data)

    def test_send_message_route(self):
        """Test the send message route."""
        test_message = {
            'phone': '1234567890',
            'message': 'Test message'
        }
        response = self.client.post(
            '/send',
            data=json.dumps(test_message),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('status', data)

    def test_simulate_connect_route(self):
        """Test the simulate connect endpoint."""
        test_data = {
            'phone': '1234567890'
        }
        response = self.client.post(
            '/api/simulate_connect',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('success', data)

    def test_simulate_disconnect_route(self):
        """Test the simulate disconnect endpoint."""
        response = self.client.post('/api/simulate_disconnect')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('success', data)


class TestWhatsAppClient(unittest.TestCase):
    """Tests for the WhatsApp client."""

    def setUp(self):
        """Set up WhatsApp client for testing."""
        self.client = WhatsAppClient()

    def test_get_status(self):
        """Test getting the WhatsApp client status."""
        status = self.client.get_status()
        self.assertIn('connected', status)
        
    def test_simulate_connection(self):
        """Test simulating a WhatsApp connection."""
        result = self.client.simulate_connection('1234567890')
        self.assertTrue(result['success'])
        self.assertEqual(result['phone'], '1234567890')
        
    def test_disconnect(self):
        """Test disconnecting from WhatsApp."""
        # Connect first to test disconnect
        self.client.simulate_connection('1234567890')
        result = self.client.disconnect()
        self.assertTrue(result['success'])
        self.assertFalse(self.client.get_status()['connected'])
        
    def test_send_message(self):
        """Test sending a WhatsApp message."""
        # Connect first to test sending
        self.client.simulate_connection('1234567890')
        result = self.client.send_message('1234567890', 'Test message')
        self.assertEqual(result['status'], 'success')


if __name__ == '__main__':
    unittest.main()