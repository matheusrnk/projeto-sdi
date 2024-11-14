import os
from flask import Flask, request, jsonify, session, redirect
from flask_session import Session
from datetime import timedelta

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True  # Set to True for session to be permanent
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)  # Adjust timeout as needed
app.config["SESSION_TYPE"] = "filesystem"  # Store session data on the filesystem
app.config["SESSION_FILE_DIR"] = './flask_session/'  # Custom session storage folder (ensure this exists)
app.secret_key = 'your_secret_key'
Session(app)

users = {
    "user1": "password123",
    "user2": "mypassword"
}

USER_PHOTO_DIR = 'server\\users'

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')

    if name in users and users[name] == password:
        session["user"] = name
        session.permanent = True
        return jsonify({"status": "success", "message": f"Welcome, {name}!"})
    else:
        return jsonify({"status": "failure", "message": "Invalid name or password"}), 401

@app.route('/api/photos', methods=['GET'])
def get_photos():
    if not session.get("user"):
        return jsonify({"status": "failure", "message": "User not logged in"}), 403

    user = session["user"]
    user_folder = os.path.join(USER_PHOTO_DIR, user)

    if not os.path.exists(user_folder):
        return jsonify({"status": "failure", "message": "No photos found"}), 404

    photos = [file for file in os.listdir(user_folder) if os.path.isfile(os.path.join(user_folder, file))]

    if not photos:
        return jsonify({"status": "success", "photos": [], "message": "No photos available"})

    return jsonify({"status": "success", "photos": photos})

@app.route('/api/photos/upload', methods=['POST'])
def upload_photo():
    if 'user' not in session:
        return jsonify({"status": "failure", "message": "User not logged in"}), 403

    if 'photo' not in request.files:
        return jsonify({"status": "failure", "message": "No file part in the request"}), 400

    photo = request.files['photo']
    user = session['user']

    user_folder = os.path.join(USER_PHOTO_DIR, user)
    os.makedirs(user_folder, exist_ok=True)

    photo_path = os.path.join(user_folder, photo.filename)
    photo.save(photo_path)

    return jsonify({"status": "success", "message": f"Photo '{photo.filename}' uploaded successfully"})

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"status": "success", "message": "Logged out successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
