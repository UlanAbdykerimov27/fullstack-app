from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

database_url = os.getenv("DATABASE_URL")

if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url or "sqlite:///local.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class AppItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(100), nullable=False)
    download_link = db.Column(db.String(300), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return {
        "student_name": "Ulan Abdykerimov",
        "student_id": "YOUR_ID",
        "message": "Super App Download API"
    }

@app.route("/api/data", methods=["GET"])
def get_items():
    items = AppItem.query.all()

    result = []

    for item in items:
        result.append({
            "id": item.id,
            "platform": item.platform,
            "download_link": item.download_link
        })

    return jsonify(result)

@app.route("/api/data", methods=["POST"])
def add_item():
    data = request.json

    new_item = AppItem(
        platform=data["platform"],
        download_link=data["download_link"]
    )

    db.session.add(new_item)
    db.session.commit()

    return jsonify({
        "message": "Item added successfully"
    }), 201

@app.route("/api/data/<int:item_id>", methods=["DELETE"])
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
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
