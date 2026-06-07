from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

OLLAMA_HOST = "http://localhost:11434"
OLLAMA_GENERATE = f"{OLLAMA_HOST}/api/generate"
OLLAMA_TAGS = f"{OLLAMA_HOST}/api/tags"

MODEL = "gemma4:31b-cloud"

def get_ollama_status():
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=5)

        models = r.json().get("models", [])

        installed = any(
            m.get("name") == MODEL
            for m in models
        )

        return {
            "running": True,
            "installed": installed,
            "models": [m.get("name") for m in models]
        }

    except Exception as e:
        return {
            "running": False,
            "installed": False,
            "error": str(e)
        }

# --------------------------------------------------
# WEB UI
# --------------------------------------------------
@app.route("/")
def index():
    return render_template("chat.html")


# --------------------------------------------------
# STATUS
# --------------------------------------------------
@app.route("/status")
def status():
    return jsonify(get_ollama_status())


# --------------------------------------------------
# GENERATE
# --------------------------------------------------
@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.get_json()
    message = data.get("message", "")

    status_info = get_ollama_status()

    if not status_info["running"]:
        return jsonify({
            "reply": "❌ Ollama server is not running."
        })

    if not status_info["installed"]:
        return jsonify({
            "reply": f"❌ Model '{MODEL}' is not installed."
        })

    try:

        response = requests.post(
            OLLAMA_GENERATE,
            json={
                "model": MODEL,
                "prompt": message,
                "stream": False
            },
            timeout=300
        )

        result = response.json()

        print("\n========== OLLAMA RESPONSE ==========")
        print(result)
        print("=====================================\n")

        reply = result.get("response")

        if not reply:
            reply = f"Unexpected response:\n{result}"

        return jsonify({
            "reply": reply
        })

    except Exception as e:
        return jsonify({
            "reply": f"Error: {str(e)}"
        })


# --------------------------------------------------
# TEST MODEL
# --------------------------------------------------
@app.route("/test")
def test_model():

    try:

        response = requests.post(
            OLLAMA_GENERATE,
            json={
                "model": MODEL,
                "prompt": "Say Hello",
                "stream": False
            },
            timeout=60
        )

        return response.json()

    except Exception as e:
        return jsonify({
            "error": str(e)
        })


# --------------------------------------------------
# MAIN
# --------------------------------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
