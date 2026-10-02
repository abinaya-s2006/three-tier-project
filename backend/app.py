from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": "Typing Speed Test Backend is running"
    })


@app.route("/api/result", methods=["POST"])
def result():

    data = request.get_json()

    words = data.get("words", 0)
    time_taken = data.get("time", 0)
    wpm = data.get("wpm", 0)

    return jsonify({
        "message": "Typing test completed",
        "words": words,
        "time": round(time_taken, 2),
        "wpm": wpm
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
