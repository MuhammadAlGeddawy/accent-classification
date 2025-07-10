from flask import Flask, request, jsonify
from model import AccentClassifier
from audio_utils import get_video_path, extract_audio, clean_temp_files
import logging

# Initialize Flask app and model
app = Flask(__name__)
classifier = AccentClassifier()

logging.basicConfig(level=logging.INFO)

@app.route("/")
def health():
    return jsonify({"status": "Accent Classification API is running"}), 200

@app.route("/predict", methods=["POST"])
def predict_accent():
    try:
        data = request.get_json()
        if not data or "video_url" not in data:
            return jsonify({"error": "Missing 'video_url' in request body"}), 400

        video_url = data["video_url"]
        logging.info(f"📥 Received video input: {video_url}")

        # Step 1: Get video
        video_path = get_video_path(video_url)

        # Step 2: Extract audio
        audio_path = extract_audio(video_path)

        # Step 3: Predict
        result = classifier.predict(audio_path)

        # Step 4: Cleanup
        clean_temp_files(video_path, audio_path)

        # Step 5: Return result
        return jsonify(result), 200

    except Exception as e:
        logging.error(f"❌ Error during prediction: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
