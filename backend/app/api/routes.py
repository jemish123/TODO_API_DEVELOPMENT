# backend/app/routes/todos.py
from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.models.todo_model import get_all_todos, create_todo, update_todo_status, delete_todo
from app.utils.stats import get_stats

# Create Blueprint
todos_bp = Blueprint("todos", __name__)
CORS(todos_bp, origins=["http://localhost:5500", "http://127.0.0.1:5500"])  # Allow frontend origin

@todos_bp.route("/", methods=["GET"])
def get_todos():
    todos = get_all_todos()
    return jsonify(todos), 200

@todos_bp.route("/", methods=["POST"])
def post_todo():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    if not title:
        return jsonify({"error": "Title is required"}), 400
    todo = create_todo(title, description)
    return jsonify(todo), 201

@todos_bp.route("/<int:todo_id>", methods=["PUT"])
def put_todo(todo_id):
    data = request.get_json()
    status = data.get("status")
    if status not in ["pending", "completed", "cancelled"]:
        return jsonify({"error": "Invalid status"}), 400
    updated = update_todo_status(todo_id, status)
    if not updated:
        return jsonify({"error": "Todo not found"}), 404
    return jsonify(updated), 200

@todos_bp.route("/<int:todo_id>", methods=["DELETE"])
def delete_todo_item(todo_id):
    delete_todo(todo_id)
    return "", 204

@todos_bp.route('/stats', methods=['GET'])
def get_todo_stats():
    stats = get_stats()
    return jsonify(stats), 200
