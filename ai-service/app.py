from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
from datetime import datetime, timezone
import os
from services.groq_client import call_groq

load_dotenv()

app = Flask(__name__)

# Rate limiter — 30 requests per minute per IP
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["30 per minute"],
    storage_uri="memory://"
)


def get_current_time() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_input(data):
    """
    Validate and sanitise input.
    Returns (cleaned_text, error_message)
    """
    from services.sanitiser import sanitise_input

    if not data or "text" not in data:
        return None, "text field is required"

    cleaned, is_injection = sanitise_input(data["text"])

    if cleaned is None:
        return None, "Input cannot be empty"

    if is_injection:
        return None, "INJECTION_DETECTED"

    return cleaned, None


def get_sanitised_input(data):
    """
    Wrapper around validate_input that returns a 3-tuple:
      (cleaned_text, error_jsonify_response | None, http_status_code | None)
    Callers should check: if error_response is not None and status_code is not None
    """
    cleaned, error = validate_input(data)

    if error == "INJECTION_DETECTED":
        return None, jsonify({
            "error": "Potential prompt injection detected",
            "code": "INJECTION_DETECTED"
        }), 400

    if error:
        return None, jsonify({"error": error}), 400

    return cleaned, None, None


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "model": "llama-3.3-70b-versatile",
        "generated_at": get_current_time()
    }), 200


@app.route("/describe", methods=["POST"])
@limiter.limit("30 per minute")
def describe():
    data = request.get_json()
    cleaned, error_response, status_code = get_sanitised_input(data)
    if error_response is not None and status_code is not None:
        return error_response, status_code

    messages = [
        {
            "role": "system",
            "content": "You are a workplace safety analyst. Describe the near miss incident clearly in 2-3 sentences."
        },
        {
            "role": "user",
            "content": f"Describe this near miss incident: {cleaned}"
        }
    ]

    result = call_groq(messages, temperature=0.3)

    return jsonify({
        "description": result["content"],
        "is_fallback": result["is_fallback"],
        "generated_at": get_current_time()
    }), 200


@app.route("/recommend", methods=["POST"])
@limiter.limit("30 per minute")
def recommend():
    data = request.get_json()
    cleaned, error_response, status_code = get_sanitised_input(data)
    if error_response is not None and status_code is not None:
        return error_response, status_code

    messages = [
        {
            "role": "system",
            "content": """You are a workplace safety expert.
Return exactly 3 recommendations as a JSON array.
Each item must have: action_type, description, priority (High/Medium/Low).
Return only valid JSON, no extra text."""
        },
        {
            "role": "user",
            "content": f"Give 3 safety recommendations for this incident: {cleaned}"
        }
    ]

    result = call_groq(messages, temperature=0.3)

    return jsonify({
        "recommendations": result["content"],
        "is_fallback": result["is_fallback"],
        "generated_at": get_current_time()
    }), 200


@app.route("/generate-report", methods=["POST"])
@limiter.limit("30 per minute")
def generate_report():
    data = request.get_json()
    cleaned, error_response, status_code = get_sanitised_input(data)
    if error_response is not None and status_code is not None:
        return error_response, status_code

    messages = [
        {
            "role": "system",
            "content": """You are a workplace safety report writer.
Generate a structured report as JSON with these fields:
title, summary, overview, key_findings (array), recommendations (array).
Return only valid JSON, no extra text."""
        },
        {
            "role": "user",
            "content": f"Generate a full safety report for this incident: {cleaned}"
        }
    ]

    result = call_groq(messages, temperature=0.3)

    return jsonify({
        "report": result["content"],
        "is_fallback": result["is_fallback"],
        "generated_at": get_current_time()
    }), 200


# Handle rate limit errors
@app.errorhandler(429)
def rate_limit_exceeded(e):
    return jsonify({
        "error": "Rate limit exceeded. Max 30 requests per minute.",
        "code": "RATE_LIMIT_EXCEEDED"
    }), 429


@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost'
    response.headers['Server'] = 'webserver'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)