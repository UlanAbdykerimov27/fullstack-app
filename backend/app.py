from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Получаем DATABASE_URL из Railway
database_url = os.getenv("DATABASE_URL")

# Railway иногда дает postgres:// вместо postgresql://
if database_url:
    database_url = database_url.replace("postgres://", "postgresql://", 1)

# Подключение PostgreSQL
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Модель таблицы
class AppItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(100), nullable=False)
    download_link = db.Column(db.String(300), nullable=False)

# Создание таблиц
with app.app_context():
    db.create_all()

# ---------------- ENDPOINT 1 ----------------
# GET all items

@app.route("/api/items", methods=["GET"])
def get_items():

    items = AppItem.query.all()

    result = []

    for item in items:
        result.append({
            "id": item.id,
            "platform": item.platform,
            "download_link": item.download_link
        })

    return jsonify(result), 200


# ---------------- ENDPOINT 2 ----------------
# POST new item

@app.route("/api/items", methods=["POST"])
def add_item():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No JSON data provided"
        }), 400

    if "platform" not in data or "download_link" not in data:
        return jsonify({
            "error": "platform and download_link are required"
        }), 400

    new_item = AppItem(
        platform=data["platform"],
        download_link=data["download_link"]
    )

    db.session.add(new_item)
    db.session.commit()

    return jsonify({
        "message": "Item added successfully"
    }), 201


# ---------------- ENDPOINT 3 ----------------
# DELETE item

@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):

    item = AppItem.query.get(item_id)

    if not item:
        return jsonify({
            "error": "Item not found"
        }), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({
        "message": "Item deleted successfully"
    }), 200


# Railway PORT
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
