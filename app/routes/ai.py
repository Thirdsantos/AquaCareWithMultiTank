from flask import Blueprint, request, jsonify
from app.ai.gemini_service import ask_gemini

bp = Blueprint('ai', __name__, url_prefix='/')

@bp.route("/ask", methods=["POST"])
def ask_gemini_route():
    data = request.json
    text = data.get("question")
    image = data.get("image")
    aquarium_id = data.get("aquarium_id", "default")

    if not text and not image:
        return jsonify({"Error": "At least give a question or an image"}), 400

    # Call the service function
    response, status_code = ask_gemini(
        text=text,
        image=image,
        aquarium_id=aquarium_id
    )
    
    return jsonify(response), status_code
