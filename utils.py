from flask import jsonify, request


def json_required(*keys):
    data = request.get_json(silent=True) or {}
    missing_keys = [key for key in keys if key not in data]
    if missing_keys:
        return None, jsonify({"error": "Missing required fields"})
    return data, None, None

def ok(payload, status=200):
    return jsonify(payload), status

def not_found(message="Resource not found"):
    return jsonify({"error": message}), 400

def bad_request(message="Bad Request"):
    return jsonify({"error": message}), 400