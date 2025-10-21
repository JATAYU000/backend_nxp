from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
import json

app = Flask(__name__)
uploads = []
ANGLES_FILE = "angles.txt"

# Function to save angles to file
def save_angles_to_file(angles):
    with open(ANGLES_FILE, 'w') as f:
        json.dump(angles, f)

# Function to read angles from file
def read_angles_from_file():
    try:
        with open(ANGLES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Angle Input Form</title>
    <script>
        async function saveAngles() {
            const angles = {
                angle1: document.getElementById('angle1').value,
                angle2: document.getElementById('angle2').value,
                angle3: document.getElementById('angle3').value,
                angle4: document.getElementById('angle4').value,
                angle5: document.getElementById('angle5').value
            };
            
            // Send angles to backend
            const response = await fetch('/save_angles', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(angles)
            });
            
            if (response.ok) {
                alert('Angles saved successfully!');
            } else {
                alert('Error saving angles');
            }
        }

        // Load saved angles when page loads
        window.onload = async function() {
            const response = await fetch('/get_angles');
            const angles = await response.json();
            for (let i = 1; i <= 5; i++) {
                const angle = angles[`angle${i}`];
                if (angle) {
                    document.getElementById(`angle${i}`).value = angle;
                }
            }
        }
    </script>
</head>
<body>
    <h1>Enter Angles</h1>
    <form onsubmit="event.preventDefault(); saveAngles();">
        <div>
            <label for="angle1">Angle 1:</label>
            <input type="number" id="angle1" name="angle1"><br><br>
        </div>
        <div>
            <label for="angle2">Angle 2:</label>
            <input type="number" id="angle2" name="angle2"><br><br>
        </div>
        <div>
            <label for="angle3">Angle 3:</label>
            <input type="number" id="angle3" name="angle3"><br><br>
        </div>
        <div>
            <label for="angle4">Angle 4:</label>
            <input type="number" id="angle4" name="angle4"><br><br>
        </div>
        <div>
            <label for="angle5">Angle 5:</label>
            <input type="number" id="angle5" name="angle5"><br><br>
        </div>
        <button type="submit">Save Angles</button>
    </form>
</body>
</html>
"""

@app.route('/save_angles', methods=['POST'])
def save_angles():
    """Save angles to file"""
    angles = request.get_json()
    save_angles_to_file(angles)
    return jsonify({"message": "Angles saved successfully"}), 200

@app.route('/get_angles', methods=['GET'])
def get_angles():
    """Get angles from file"""
    angles = read_angles_from_file()
    return jsonify(angles)

@app.route('/', methods=['GET'])
def home():
    """Home route with angle input form"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/qr1', methods=['GET'])
def qr1():
    """Return QR1 string"""
    angles = read_angles_from_file()
    angle = angles.get('angle1', 0)
    return f"1_{angle}_MotorBrew"

@app.route('/qr2', methods=['GET'])
def qr2():
    """Return QR2 string"""
    angles = read_angles_from_file()
    angle = angles.get('angle2', 0)
    return f"2_{angle}_MotorBrew"

@app.route('/qr3', methods=['GET'])
def qr3():
    """Return QR3 string"""
    angles = read_angles_from_file()
    angle = angles.get('angle3', 0)
    return f"3_{angle}_MotorBrew"

@app.route('/qr4', methods=['GET'])
def qr4():
    """Return QR4 string"""
    angles = read_angles_from_file()
    angle = angles.get('angle4', 0)
    return f"4_{angle}_MotorBrew"

@app.route('/qr5', methods=['GET'])
def qr5():
    """Return QR5 string"""
    angles = read_angles_from_file()
    angle = angles.get('angle5', 0)
    return f"5_{angle}_MotorBrew"

# ...existing code for upload, uploads, and reset endpoints...

@app.route('/upload/', methods=['POST'])
def upload_file():
    """
    Upload data in the format: {"data": {"item1": count1, "item2": count2, ...}}
    Requires x-api-key header
    """
    try:
        api_key = request.headers.get('x-api-key')
        if not api_key:
            return jsonify({'error': 'Missing x-api-key header'}), 401
        
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        payload = request.get_json()
        
        if 'data' not in payload:
            return jsonify({'error': 'Missing "data" field in request'}), 400
        
        if not isinstance(payload['data'], dict):
            return jsonify({'error': '"data" field must be a dictionary/object'}), 400
        
        upload_record = {
            'id': len(uploads) + 1,
            'data': payload['data'],
            'timestamp': datetime.now().isoformat()
        }
        
        uploads.append(upload_record)
        
        return jsonify({
            'message': 'Upload successful',
            'upload': upload_record
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/uploads/', methods=['GET'])
def get_uploads():
    """
    Get all saved uploads
    """
    return jsonify({
        'count': len(uploads),
        'uploads': uploads
    }), 200


@app.route('/reset/', methods=['POST'])
def reset_uploads():
    """
    Reset all saved uploads
    """
    global uploads
    uploads = []
    
    return jsonify({
        'message': 'Uploads reset successfully'
    }), 200



if __name__ == '__main__':
    app.run(debug=False)
