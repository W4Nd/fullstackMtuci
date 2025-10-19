from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    print(f"Starting Medication Reminder API on {host}:{port}")
    print(f"Debug mode: {debug}")
    print("API available at: http://localhost:5000/api/v1/reminders")
    print("Health check: http://localhost:5000/health")
    
    app.run(host=host, port=port, debug=debug)