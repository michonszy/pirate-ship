# app.py
from flask import Flask, request, jsonify
import os
import yaml
import json
import subprocess
import base64

app = Flask(__name__)

# Insecure configuration loading
admin_token = os.environ.get('ADMIN_TOKEN', 'ey9876adminbackendtoken1234')
db_user = os.environ.get('DB_USER', 'dbuser')
db_password = os.environ.get('DB_PASSWORD', 'dbpassword123')
debug_mode = os.environ.get('DEBUG', 'true').lower() == 'true'

# Simulated database
users_db = {
    'admin': 'super_admin_password',
    'user1': 'password123',
    'guest': 'guest'
}

# Flag stored in "database"
flags_db = {
    'flag1': 'FLAG{backend_database_access}'
}

@app.route('/')
def index():
    return jsonify({'message': 'Backend API is running'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in users_db and users_db[username] == password:
        return jsonify({
            'success': True,
            'message': f'Welcome {username}',
            'token': base64.b64encode(f"{username}:{password}".encode()).decode()
        })
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/api/users')
def get_users():
    # Insecure authorization check
    auth_header = request.headers.get('Authorization', '')
    if 'Bearer' in auth_header:
        token = auth_header.split(' ')[1]
        if token == admin_token:
            return jsonify(list(users_db.keys()))
    return jsonify({'error': 'Unauthorized'}), 401

@app.route('/api/config')
def get_config():
    # Intentionally returning sensitive info in debug mode
    if debug_mode:
        config = {
            'debug': debug_mode,
            'admin_token': admin_token,
            'db_connection': f'mongodb://{db_user}:{db_password}@mongodb:27017/vulnapp',
            'environment': dict(os.environ),
            'flag': 'FLAG{debug_mode_information_leak}'
        }
        return jsonify(config)
    return jsonify({'debug': False})

@app.route('/api/flags')
def get_flags():
    # This should be protected but isn't
    auth_header = request.headers.get('Authorization', '')
    if 'Bearer' in auth_header:
        return jsonify(flags_db)
    return jsonify({'error': 'Unauthorized'}), 401

@app.route('/api/exec', methods=['POST'])
def execute_command():
    # Command injection vulnerability
    data = request.get_json()
    command = data.get('command')
    
    auth_header = request.headers.get('Authorization', '')
    if 'Bearer' in auth_header and auth_header.split(' ')[1] == admin_token:
        try:
            output = subprocess.check_output(command, shell=True)
            return jsonify({'output': output.decode()})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'Unauthorized'}), 401

@app.route('/api/parse', methods=['POST'])
def parse_yaml():
    # YAML parsing vulnerability (allows deserialization attacks)
    data = request.get_data().decode()
    try:
        result = yaml.load(data, Loader=yaml.Loader)  # Unsafe loader
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/internal/admin')
def admin_panel():
    # This should be internal only, but network policies are missing
    return jsonify({
        'message': 'Internal admin API',
        'flag': 'FLAG{missing_network_policy}',
        'sensitive_data': 'This endpoint should not be accessible from outside'
    })

if __name__ == '__main__':
    # Running with debug=True in production is insecure
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
