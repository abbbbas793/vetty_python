from flask import Flask, request, jsonify
import requests
from flask_swagger_ui import get_swaggerui_blueprint
from functools import wraps

app = Flask(__name__)

# Authentication Setup (Basic Token Authentication)
API_TOKEN = "CG-qt5vxr1oyaT8M9uNcfFfdRJ4"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or token.split(" ")[-1] != API_TOKEN:
            return jsonify({"message": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

# Swagger Setup
SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.json"
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

COINGECKO_API_BASE = "https://api.coingecko.com/api/v3"

@app.route("/api/coins", methods=["GET"])
@token_required
def list_coins():
    page = request.args.get("page_num", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    response = requests.get(f"{COINGECKO_API_BASE}/coins/markets", params={
        "vs_currency": "cad",
        "per_page": per_page,
        "page": page
    })
    return jsonify(response.json())

@app.route("/api/categories", methods=["GET"])
@token_required
def list_categories():
    response = requests.get(f"{COINGECKO_API_BASE}/coins/categories/list")
    return jsonify(response.json())

@app.route("/api/coins/<coin_id>", methods=["GET"])
@token_required
def get_coin(coin_id):
    response = requests.get(f"{COINGECKO_API_BASE}/coins/{coin_id}", params={"localization": "false"})
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
