import requests

# Create a session object to persist cookies
session = requests.Session()

# Base URL for the server
base_url = 'http://localhost:5000'

# Login credentials
login_payload = {
    'name': 'user1',
    'password': 'password123'
}

# Login request
login_response = session.post(f'{base_url}/api/login', json=login_payload)
print('Login Response:', login_response.json())

# Request photos
photos_response = session.get(f'{base_url}/api/photos')
print('Photos Response:', photos_response.json())

# Upload a photo (optional)
photo_path = 'client\\users\\user1\\WhatsApp Image 2024-10-27 at 23.32.36.jpeg'  # Replace with the local path to the photo
with open(photo_path, 'rb') as photo_file:
    files = {'photo': photo_file}
    upload_response = session.post(f'{base_url}/api/photos/upload', files=files)
    print('Upload Response:', upload_response.json())

# Logout request
logout_response = session.post(f'{base_url}/api/logout')
print('Logout Response:', logout_response.json())
