"""
dashboard.py
Author: Manjunath Chintha
Purpose: API endpoints for Neurowell dashboard
Integrated with: script.js frontend calls
"""
import sqlite3
from flask import Blueprint, jsonify, request
import json
from datetime import datetime
from data_processing import DataProcessor

# Create Flask Blueprint for analytics API
dashboard_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

# Initialize data processor
processor = DataProcessor()

# ==================== DASHBOARD ENDPOINTS ====================

@dashboard_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """
    Get complete dashboard data
    Called from: script.js chart initialization
    """
    try:
        user_id = request.args.get('user_id', 1, type=int)
        
        # Get all dashboard data
        dashboard_data = processor.get_dashboard_data(user_id)
        
        if dashboard_data['success']:
            # Format response for frontend
            response = {
                'success': True,
                'profile': {
                    'name': dashboard_data['user_info']['full_name'],
                    'email': dashboard_data['user_info']['email'],
                    'mood_score': dashboard_data['mood_score']
                },
                'charts': dashboard_data['charts'],
                'progress_bars': dashboard_data['progress'],
                'timestamp': dashboard_data['last_updated']
            }
            return jsonify(response)
        else:
            return jsonify(dashboard_data), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to load dashboard data'
        }), 500


@dashboard_bp.route('/profile', methods=['GET'])
def get_profile():
    """
    Get user profile data
    Called from: profile section in dashboard.html
    """
    try:
        user_id = request.args.get('user_id', 1, type=int)
        
        user_info = processor.get_user_info(user_id)
        mood_score = processor.calculate_mood_score(user_id)
        
        return jsonify({
            'success': True,
            'profile': {
                'name': user_info['full_name'],
                'email': user_info['email'],
                'age': user_info['age'],
                'phone': user_info['phone'],
                'gender': user_info['gender'],
                'member_since': user_info['member_since'],
                'mood_score': mood_score
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@dashboard_bp.route('/charts/radar', methods=['GET'])
def get_radar_chart():
    """
    Get radar chart data
    Called from: Chart.js initialization in script.js
    """
    try:
        user_id = request.args.get('user_id', 1, type=int)
        
        radar_data = processor.get_radar_chart_data(user_id)
        
        return jsonify({
            'success': True,
            'chart': {
                'type': 'radar',
                'data': radar_data
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@dashboard_bp.route('/charts/bar', methods=['GET'])
def get_bar_chart():
    """
    Get bar chart data
    Called from: Chart.js initialization in script.js
    """
    try:
        user_id = request.args.get('user_id', 1, type=int)
        
        bar_data = processor.get_bar_chart_data(user_id)
        
        return jsonify({
            'success': True,
            'chart': {
                'type': 'bar',
                'data': bar_data,
                'options': {
                    'scales': {
                        'y': {
                            'beginAtZero': True,
                            'max': 100
                        }
                    }
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@dashboard_bp.route('/charts/pie', methods=['GET'])
def get_pie_chart():
    """
    Get pie chart data
    Called from: Chart.js initialization in script.js
    """
    try:
        user_id = request.args.get('user_id', 1, type=int)
        
        pie_data = processor.get_pie_chart_data(user_id)
        
        return jsonify({
            'success': True,
            'chart': {
                'type': 'pie',
                'data': pie_data
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@dashboard_bp.route('/progress', methods=['GET'])
def get_progress():
    """
    Get progress bar data
    Called from: dashboard.html progress bars
    """
    try:
        user_id = request.args.get('user_id', 1, type=int)
        
        progress_data = processor.get_progress_data(user_id)
        
        # Format for HTML display
        progress_bars = []
        for emotion, data in progress_data.items():
            progress_bars.append({
                'name': data['label'],
                'value': data['score'],
                'width': data['width']
            })
        
        return jsonify({
            'success': True,
            'progress_bars': progress_bars
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== ANALYZER ENDPOINTS ====================

@dashboard_bp.route('/analyzer/log', methods=['POST'])
def log_emotion():
    """
    Log emotion from analyzer
    Called from: analyzer functions in script.js
    """
    try:
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        user_id = data.get('user_id', 1)
        emotion = data.get('emotion', '')
        source = data.get('source', 'text')
        confidence = data.get('confidence', 0.8)
        
        if not emotion:
            return jsonify({'success': False, 'error': 'Emotion not specified'}), 400
        
        # Log emotion
        result = processor.log_emotion(user_id, emotion, source, confidence)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': result['message'],
                'emotion': result['emotion'],
                'mood_score': result['mood_score']
            })
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@dashboard_bp.route('/analyzer/detect', methods=['POST'])
def detect_emotion():
    """
    Detect emotion from text (simulated)
    Called from: analyzeText() in script.js
    """
    try:
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        text = data.get('text', '')
        user_id = data.get('user_id', 1)
        
        # Simple emotion detection based on keywords
        emotions = {
            'happy': ['happy', 'joy', 'good', 'great', 'excited', 'love', 'awesome'],
            'sad': ['sad', 'bad', 'unhappy', 'depressed', 'cry', 'lonely', 'hurt'],
            'angry': ['angry', 'mad', 'hate', 'frustrated', 'annoyed', 'upset'],
            'calm': ['calm', 'peaceful', 'relaxed', 'chill', 'quiet', 'serene'],
            'anxious': ['anxious', 'worried', 'nervous', 'stressed', 'scared', 'fear']
        }
        
        detected_emotion = 'neutral'
        max_matches = 0
        
        text_lower = text.lower()
        for emotion, keywords in emotions.items():
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            if matches > max_matches:
                max_matches = matches
                detected_emotion = emotion
        
        # Log the detected emotion
        processor.log_emotion(user_id, detected_emotion, 'text', confidence=0.7)
        
        # Emotion display mapping
        emotion_display = {
            'happy': 'Happy 😊',
            'sad': 'Sad 😢',
            'angry': 'Angry 😡',
            'calm': 'Calm 😌',
            'anxious': 'Anxious 😟',
            'neutral': 'Neutral 😐'
        }
        
        return jsonify({
            'success': True,
            'detected_emotion': emotion_display.get(detected_emotion, 'Neutral 😐'),
            'raw_emotion': detected_emotion,
            'confidence': 0.7,
            'text_preview': text[:50] + '...' if len(text) > 50 else text
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== REPORT ENDPOINTS ====================

@dashboard_bp.route('/report/generate', methods=['POST'])
def generate_report():
    """
    Generate emotional report
    Called from: generateReport() in script.js
    """
    try:
        data = request.json or {}
        user_id = data.get('user_id', 1)
        report_type = data.get('report_type', 'weekly')
        
        # Generate report
        result = processor.generate_report(user_id, report_type)
        
        if result['success']:
            report = result['report']
            
            # Format HTML response for dashboard
            html_response = f"""
            <div class="report-content">
                <h3>📑 Neurowell Emotional Summary Report</h3>
                <p><strong>Report ID:</strong> {report['report_id']}</p>
                <p><strong>Generated:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                <p><strong>Period:</strong> {report['period']}</p>
                <hr>
                
                <h4>📊 Summary Metrics</h4>
                <div class="report-metrics">
                    <div class="metric">
                        <span class="metric-label">Average Mood Score</span>
                        <span class="metric-value">{report['summary']['average_mood_score']}%</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Dominant Emotion</span>
                        <span class="metric-value">{report['summary']['dominant_emotion']}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Weekly Average</span>
                        <span class="metric-value">{report['summary']['weekly_average']}%</span>
                    </div>
                </div>
                
                <h4>🎯 Detailed Breakdown</h4>
                <div class="breakdown">
                    <p>• Happiness Level: <strong>{report['summary']['happiness_level']}%</strong></p>
                    <p>• Calmness Level: <strong>{report['summary']['calmness_level']}%</strong></p>
                    <p>• Anxiety Level: <strong>{report['summary']['anxiety_level']}%</strong></p>
                </div>
                
                <h4>💡 Key Insights</h4>
                <ul class="insights-list">
            """
            
            for insight in report['insights']:
                html_response += f"<li>{insight}</li>"
            
            html_response += """
                </ul>
                
                <h4>✅ Recommendations</h4>
                <ul class="recommendations-list">
            """
            
            for rec in report['recommendations']:
                html_response += f"<li>{rec}</li>"
            
            html_response += """
                </ul>
                
                <hr>
                <div class="report-footer">
                    <p><em>This report is generated for emotional awareness and self-reflection purposes only. 
                    It does not constitute medical advice. If you're experiencing severe emotional distress, 
                    please consult a qualified mental health professional.</em></p>
                    <p><strong>Neurowell AI Emotion Companion</strong></p>
                </div>
            </div>
            """
            
            return jsonify({
                'success': True,
                'report': report,
                'html': html_response,
                'message': 'Report generated successfully'
            })
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to generate report'
        }), 500


@dashboard_bp.route('/report/list', methods=['GET'])
def list_reports():
    """List all generated reports for user"""
    try:
        user_id = request.args.get('user_id', 1, type=int)
        
        conn = sqlite3.connect(processor.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, report_type, generated_at 
        FROM reports 
        WHERE user_id = ?
        ORDER BY generated_at DESC
        ''', (user_id,))
        
        reports = cursor.fetchall()
        conn.close()
        
        report_list = []
        for report in reports:
            report_list.append({
                'id': report[0],
                'type': report[1],
                'generated_at': report[2]
            })
        
        return jsonify({
            'success': True,
            'reports': report_list,
            'count': len(report_list)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== STATISTICS ENDPOINTS ====================

@dashboard_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get user statistics"""
    try:
        user_id = request.args.get('user_id', 1, type=int)
        
        stats = processor.get_statistics(user_id)
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@dashboard_bp.route('/update-mood', methods=['POST'])
def update_mood():
    """Manually update mood score"""
    try:
        data = request.json
        user_id = data.get('user_id', 1)
        score = data.get('score', 50)
        emotion = data.get('emotion', 'neutral')
        
        # Log as manual entry
        result = processor.log_emotion(user_id, emotion, 'manual', confidence=1.0)
        
        # Get updated mood score
        mood_score = processor.calculate_mood_score(user_id)
        
        return jsonify({
            'success': True,
            'mood_score': mood_score,
            'message': f'Mood updated to {score}% ({emotion})'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== HEALTH AND INFO ENDPOINTS ====================

@dashboard_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'neurowell-analytics',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })


@dashboard_bp.route('/info', methods=['GET'])
def service_info():
    """Service information"""
    return jsonify({
        'service': 'Neurowell Analytics API',
        'author': 'Manjunath Chintha',
        'description': 'Data processing and analytics for Neurowell Emotion Tracker',
        'endpoints': {
            'dashboard': '/api/analytics/dashboard',
            'profile': '/api/analytics/profile',
            'charts': '/api/analytics/charts/[radar|bar|pie]',
            'analyzer': '/api/analytics/analyzer/[log|detect]',
            'report': '/api/analytics/report/generate',
            'stats': '/api/analytics/stats'
        },
        'database': 'SQLite (neurowell.db)'
    })


# Export
__all__ = ['dashboard_bp']