// Status Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const statusHeader = document.getElementById('statusHeader');
    const statusContent = document.getElementById('statusContent');
    const refreshBtn = document.getElementById('refreshBtn');
    const simulateConnectBtn = document.getElementById('simulateConnectBtn');
    const simulateDisconnectBtn = document.getElementById('simulateDisconnectBtn');
    
    // Function to fetch and display status
    function fetchStatus() {
        statusHeader.innerHTML = '<i class="bi bi-hourglass-split"></i> Checking connection status...';
        statusContent.innerHTML = `
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p>Fetching connection status...</p>
        `;
        
        fetch('/api/status')
            .then(response => response.json())
            .then(data => {
                if (data.connected) {
                    // Connected state
                    statusHeader.innerHTML = '<i class="bi bi-wifi text-success"></i> Connected to WhatsApp';
                    statusContent.innerHTML = `
                        <div class="alert alert-success mb-4">
                            <h4><i class="bi bi-check-circle-fill"></i> WhatsApp is connected!</h4>
                            <p>Your WhatsApp client is ready to send messages.</p>
                        </div>
                        <div class="card bg-light text-dark mb-3">
                            <div class="card-body">
                                <h5 class="card-title">Connection Details</h5>
                                <p><strong>Phone Number:</strong> ${data.phone_number || 'Unknown'}</p>
                                <p><strong>Connected Since:</strong> ${data.connection_time ? new Date(data.connection_time * 1000).toLocaleString() : 'Unknown'}</p>
                            </div>
                        </div>
                    `;
                } else {
                    // Not connected state
                    statusHeader.innerHTML = '<i class="bi bi-wifi-off text-danger"></i> Not Connected to WhatsApp';
                    
                    let qrCodeHtml = '';
                    if (data.qr_code_image) {
                        qrCodeHtml = `
                            <div class="text-center mb-4">
                                <h4>Scan this QR code with WhatsApp</h4>
                                <img src="data:image/png;base64,${data.qr_code_image}" class="img-fluid border border-light p-2 bg-white" style="max-width: 300px;" alt="WhatsApp QR Code">
                            </div>
                        `;
                    } else {
                        qrCodeHtml = `
                            <div class="alert alert-warning">
                                <i class="bi bi-exclamation-triangle-fill"></i> QR code is not available. Please refresh to get a new QR code.
                            </div>
                        `;
                    }
                    
                    statusContent.innerHTML = `
                        <div class="alert alert-danger mb-4">
                            <h4><i class="bi bi-x-circle-fill"></i> WhatsApp is not connected</h4>
                            <p>Please scan the QR code below with your WhatsApp app to connect.</p>
                        </div>
                        ${qrCodeHtml}
                        <div class="alert alert-info">
                            <h5><i class="bi bi-lightbulb-fill"></i> How to scan:</h5>
                            <ol class="mb-0">
                                <li>Open WhatsApp on your phone</li>
                                <li>Go to Settings > WhatsApp Web/Desktop</li>
                                <li>Tap "Link a Device"</li>
                                <li>Point your phone camera at the QR code</li>
                            </ol>
                        </div>
                    `;
                }
            })
            .catch(error => {
                console.error('Error fetching status:', error);
                statusHeader.innerHTML = '<i class="bi bi-exclamation-triangle text-warning"></i> Error Checking Status';
                statusContent.innerHTML = `
                    <div class="alert alert-danger">
                        <h4><i class="bi bi-x-circle-fill"></i> Failed to fetch status</h4>
                        <p>There was an error retrieving the WhatsApp connection status: ${error.message}</p>
                        <button class="btn btn-primary" onclick="fetchStatus()">Try Again</button>
                    </div>
                `;
            });
    }
    
    // Initial status check
    fetchStatus();
    
    // Refresh button event
    refreshBtn.addEventListener('click', fetchStatus);
    
    // Simulate connect button (for demo purposes)
    simulateConnectBtn.addEventListener('click', function() {
        fetch('/api/simulate_connect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ phone: '919876543210' }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                fetchStatus(); // Refresh status
            } else {
                alert('Failed to simulate connection: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error simulating connection');
        });
    });
    
    // Simulate disconnect button (for demo purposes)
    simulateDisconnectBtn.addEventListener('click', function() {
        fetch('/api/simulate_disconnect', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                fetchStatus(); // Refresh status
            } else {
                alert('Failed to simulate disconnection: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error simulating disconnection');
        });
    });
    
    // Poll status every 30 seconds (for automatic updates)
    setInterval(fetchStatus, 30000);
});
