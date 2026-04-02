"""
dashboard.py
Author: Jayasri
Purpose: API endpoints for Neurowell dashboard
Integrated with: script.js frontend calls
"""
from flask import Blueprint, jsonify, request
from datetime import datetime
from .data_processing import DataProcessor

# Create Flask Blueprint for analytics API
dashboard_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

# Initialize data processor
processor = DataProcessor()

# -------------------- DASHBOARD ENDPOINTS --------------------

@dashboard_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Return complete dashboard data"""
    try:
        user_id = str(request.args.get('user_id', "1"))
        data = processor.prepare_dashboard_data(user_id)
        return jsonify({
            "success": True,
            "dashboard": data
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@dashboard_bp.route('/profile', methods=['GET'])
def get_profile():
    """Return user profile info"""
    try:
        user_id = str(request.args.get('user_id', "1"))
        processor.cursor.execute("SELECT full_name, email, age, phone, gender, member_since FROM users WHERE id=?",
                                 (user_id,))
        row = processor.cursor.fetchone()
        if not row:
            return jsonify({"success": False, "error": "User not found"}), 404
        profile = {
            "full_name": row[0],
            "email": row[1],
            "age": row[2],
            "phone": row[3],
            "gender": row[4],
            "member_since": row[5]
        }
        return jsonify({"success": True, "profile": profile})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -------------------- CHART ENDPOINTS --------------------

@dashboard_bp.route('/charts/radar', methods=['GET'])
def radar_chart():
    """Return simple radar chart data"""
    try:
        user_id = str(request.args.get('user_id', "1"))
        freq = processor.emotion_frequency(user_id)
        chart_data = {
            "labels": list(freq.keys()),
            "data": list(freq.values())
        }
        return jsonify({"success": True, "chart": chart_data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@dashboard_bp.route('/charts/bar', methods=['GET'])
def bar_chart():
    """Return simple bar chart data"""
    try:
        user_id = str(request.args.get('user_id', "1"))
        weekly = processor.weekly_trends(user_id)
        chart_data = {
            "labels": [w["week"] for w in weekly],
            "data": [w["avg_intensity"] for w in weekly]
        }
        return jsonify({"success": True, "chart": chart_data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@dashboard_bp.route('/charts/pie', methods=['GET'])
def pie_chart():
    """Return pie chart data"""
    try:
        user_id = str(request.args.get('user_id', "1"))
        freq = processor.emotion_frequency(user_id)
        chart_data = [{"emotion": k, "count": v} for k, v in freq.items()]
        return jsonify({"success": True, "chart": chart_data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -------------------- MOOD LOGGING --------------------

@dashboard_bp.route('/log_mood', methods=['POST'])
def log_mood():
    """Log new mood entry"""
    try:
        data = request.json
        user_id = str(data.get("user_id", "1"))
        emotion = data.get("emotion", "neutral")
        intensity = int(data.get("intensity", 5))
        source = data.get("source", "chat")
        processor.insert_mood(user_id, emotion, intensity, source=source)
        return jsonify({"success": True, "message": "Mood logged"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -------------------- PDF REPORT --------------------

@dashboard_bp.route('/report/generate', methods=['GET'])
def generate_report():
    """Generate PDF mood report"""
    try:
        user_id = str(request.args.get("user_id", "1"))
        html_content = processor.generate_pdf_report(user_id)
        return jsonify({"success": True, "html": html_content})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -------------------- PROGRESS & STATS --------------------

@dashboard_bp.route('/progress', methods=['GET'])
def progress():
    """Return progress bar data"""
    try:
        user_id = str(request.args.get("user_id", "1"))
        data = processor.get_progress_data(user_id)
        return jsonify({"success": True, "progress": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@dashboard_bp.route('/stats', methods=['GET'])
def stats():
    """Return statistics data"""
    try:
        user_id = str(request.args.get("user_id", "1"))
        data = processor.get_statistics(user_id)
        return jsonify({"success": True, "stats": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -------------------- HEALTH CHECK --------------------

@dashboard_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "neurowell-analytics",
        "timestamp": datetime.now().isoformat()
    })


# -------------------- CLOSE CONNECTION ON EXIT --------------------
import atexit
atexit.register(lambda: processor.close())