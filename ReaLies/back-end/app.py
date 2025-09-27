from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import tempfile

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from predict_deepfake import predict_video
    PREDICTION_AVAILABLE = True
    print("✅ Successfully imported predict_deepfake.py")
except ImportError as e:
    PREDICTION_AVAILABLE = False
    print(f"❌ Failed to import predict_deepfake: {e}")
    print("⚠️  Using simulation mode instead")

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze_video():
    print("🎬 Received analysis request")
    
    if 'video' not in request.files:
        return jsonify({'status': 'error', 'message': 'No video file provided'}), 400
    
    video_file = request.files['video']
    print(f"📁 Processing file: {video_file.filename}")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
        video_file.save(temp_file.name)
        temp_path = temp_file.name
    
    try:
        if PREDICTION_AVAILABLE:
            print("🔍 Using real deepfake detection...")
            result = predict_video(temp_path)
            
            if result['status'] == 'ok':
                response = {
                    'status': 'ok',
                    'probability': result['probability_fake'],
                    'label': result['label'],
                    'confidence': result['confidence'],
                    'message': 'Analysis completed successfully'
                }
            else:
                response = {
                    'status': 'error',
                    'message': result.get('message', 'Analysis failed')
                }
        else:
            print("⚠️  Using simulation mode (predict_deepfake not available)")
            import random
            import time
            
            time.sleep(2)  
            probability = random.uniform(0, 1)
            
            response = {
                'status': 'ok',
                'probability': probability,
                'label': 'YES (FAKE)' if probability > 0.5 else 'NO (REAL)',
                'confidence': 'HIGH' if abs(probability - 0.5) > 0.3 else 'MEDIUM',
                'message': 'Simulation mode - using random results'
            }
        
        print(f"✅ Analysis result: {response}")
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return jsonify({
            'status': 'error', 
            'message': f'Analysis failed: {str(e)}'
        }), 500
        
    finally:
        try:
            os.unlink(temp_path)
        except:
            pass

@app.route('/health', methods=['GET'])
def health_check():
    status = {
        'status': 'ok', 
        'message': 'Server is running',
        'prediction_available': PREDICTION_AVAILABLE
    }
    return jsonify(status)

@app.route('/test-prediction', methods=['GET'])
def test_prediction():
    """Test endpoint to verify prediction function works"""
    if not PREDICTION_AVAILABLE:
        return jsonify({'status': 'error', 'message': 'Prediction module not available'})
    
    try:
        test_video = '1.mp4'  
        if os.path.exists(test_video):
            result = predict_video(test_video)
            return jsonify({
                'status': 'ok', 
                'message': 'Prediction function works!',
                'test_result': result
            })
        else:
            return jsonify({
                'status': 'ok',
                'message': 'Prediction module imported successfully',
                'test_video': 'Not found, but module works'
            })
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Prediction test failed: {str(e)}'})

if __name__ == '__main__':
    print("🚀 Starting Deepfake Detection Backend...")
    print(f"📍 Prediction module available: {PREDICTION_AVAILABLE}")
    print("🔗 Endpoints:")
    print("   - POST /analyze : Analyze video")
    print("   - GET  /health  : Health check") 
    print("   - GET  /test-prediction : Test prediction function")
    print("🌐 Server running on: http://localhost:5000")
    
    app.run(debug=True, port=5000, host='0.0.0.0')