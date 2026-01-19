from flask import Flask, request, jsonify
import json
import hashlib
import logging
from redis_client import redis_client
from feature_engineering import compute_features

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.route("/compute-features", methods=["POST"])
def compute():
    data = request.get_json()

    if not data or "values" not in data:
        return jsonify({"error": "Invalid input"}), 400

    values = data["values"]
    if not isinstance(values, list):
        return jsonify({"error": "Values must be a list"}), 400

    key = hashlib.md5(json.dumps(values).encode()).hexdigest()

    cached = redis_client.get(key)
    if cached:
        return jsonify(json.loads(cached))

    result = compute_features(values)
    redis_client.set(key, json.dumps(result))

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
