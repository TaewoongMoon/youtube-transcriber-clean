from flask import Flask, jsonify
from main import run_batch_transcription  # 기존 main.py 함수 재활용

app = Flask(__name__)

@app.route("/run-transcription", methods=["POST"])
def run_transcription():
    try:
        run_batch_transcription()
        return jsonify({"status": "success", "message": "Transcription completed."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/", methods=["GET"])
def health_check():
    return "✅ Render 서버 정상 작동 중", 200

if __name__ == "__main__":
    app.run(debug=True)
