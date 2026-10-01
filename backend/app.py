import os
import sqlite3
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get("DB_PATH", os.path.join(BASE_DIR, "deploys.db"))

app = Flask(__name__)
CORS(app)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS deployments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_name TEXT NOT NULL,
            version TEXT NOT NULL,
            env TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")


@app.route("/")
def home():
    index_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index_path):
        return send_from_directory(BASE_DIR, "index.html")
    return jsonify(message="DeployTrack backend is running"), 200


@app.route("/health")
def health():
    try:
        with get_db() as conn:
            conn.execute("SELECT 1")
        return jsonify(status="ok"), 200
    except Exception as e:
        return jsonify(status="error", detail=str(e)), 500


@app.route("/api/deployments", methods=["GET"])
def list_deployments():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM deployments ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/deployments", methods=["POST"])
def add_deployment():
    d = request.get_json(silent=True) or {}
    app_name = (d.get("app_name") or "").strip()
    version = (d.get("version") or "").strip()
    env = d.get("env", "Dev")
    status = d.get("status", "Success")
    if not app_name or not version:
        return jsonify(error="App name and version are required"), 400
    with get_db() as conn:
        conn.execute(
            "INSERT INTO deployments (app_name, version, env, status) VALUES (?,?,?,?)",
            (app_name, version, env, status))
    return jsonify(success=True), 201


@app.route("/api/deployments/<int:dep_id>", methods=["DELETE"])
def delete_deployment(dep_id):
    with get_db() as conn:
        conn.execute("DELETE FROM deployments WHERE id = ?", (dep_id,))
    return jsonify(success=True)


@app.route("/api/stats")
def stats():
    with get_db() as conn:
        total = conn.execute("SELECT COUNT(*) FROM deployments").fetchone()[0]
        failed = conn.execute(
            "SELECT COUNT(*) FROM deployments WHERE status='Failed'").fetchone()[0]
    return jsonify(total=total, failed=failed, success=total - failed)


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
