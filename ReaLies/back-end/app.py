from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import time

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze_video():
    print("Received analysis request")
    
    if 'video' not in request.files:
        return jsonify({'status': 'error', 'message': 'No video file provided'}), 400
    
    video_file = request.files['video']
    print(f"Processing file: {video_file.filename}")
    
    # Simulate processing time
    time.sleep(2)
    
    # Simulate random result for testing
    probability = random.uniform(0, 1)
    is_fake = probability > 0.5
    
    result = {
        'status': 'ok',
        'probability': probability,
        'label': 'YES (FAKE)' if is_fake else 'NO (REAL)',
        'message': 'Analysis completed successfully'
    }
    
    print(f"Analysis result: {result}")
    return jsonify(result)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Server is running'})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')