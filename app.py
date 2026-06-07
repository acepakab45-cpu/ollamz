from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma4:31b-cloud"


# =========================
# 🌐 WEB CHAT INTERFACE
# =========================
@app.route("/")
def chat_ui():
    return render_template("chat.html")


# =========================
# 🤖 OLLAMA-STYLE GENERATE API (n8n friendly)
# =========================
@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json()

    prompt = data.get("prompt", "")

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# 💬 OLLAMA-STYLE CHAT API (BEST FOR n8n)
# =========================
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()

    message = data.get("message", "")

    payload = {
        "model": MODEL,
        "prompt": message,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        result = response.json()

        # CLEAN RESPONSE FOR n8n
        return jsonify({
            "reply": result.get("response"),
            "model": MODEL
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# 🏠 HOME
# =========================
@app.route("/status")
def status():
    return jsonify({
        "status": "running",
        "model": MODEL
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)