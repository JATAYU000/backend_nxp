from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)
uploads = []

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


@app.route('/', methods=['GET'])
def home():
    """
    Home route with API documentation
    """
    return jsonify({
        'message': 'Flask Upload API',
        'endpoints': {
            'POST /upload/': 'Upload data (requires x-api-key header and {"data": {...}} format)',
            'GET /uploads/': 'Get all saved uploads',
            'POST /reset/': 'Reset all uploads'
        },
        'example': {
            'curl': 'curl -X POST -H "x-api-key: mykey" -H "Content-Type: application/json" -d \'{"data":{"banana":1,"clock":2}}\' http://your-url/upload/'
        }
    }), 200


if __name__ == '__main__':
    app.run(debug=False)
