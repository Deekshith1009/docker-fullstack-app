import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Load the .env file from the project folder (one level above backend)
load_dotenv(Path(__file__).resolve().parent.parent / ".env", encoding="utf-8-sig")

MONGO_URL = os.getenv("MONGO_URL")
if not MONGO_URL:
    raise RuntimeError("MONGO_URL is missing. Check your .env file.")

app = Flask(__name__)

client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
db = client["flask_and_mongodb"]
collection = db["todo_items"]


@app.route("/")
def health():
    return jsonify({"status": "Backend is running"})


@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    item_name = request.form.get("itemName", "").strip()
    item_description = request.form.get("itemDescription", "").strip()

    if not item_name or not item_description:
        return jsonify({"error": "itemName and itemDescription are required"}), 400

    try:
        collection.insert_one({
            "itemName": item_name,
            "itemDescription": item_description,
        })
    except PyMongoError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    return jsonify({"message": "To-Do item saved"}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)