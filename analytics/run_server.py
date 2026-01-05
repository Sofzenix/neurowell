"""
run_server.py
Run Flask server for Neurowell Analytics API
"""

from flask import Flask, jsonify
from dashboard import dashboard_bp
from data_processing import DataProcessor
import os

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Initialize database
    print("Initializing database...")
    processor = DataProcessor("neurowell.db")
    print("Database initialized successfully!")
    
    # Register blueprint
    app.register_blueprint(dashboard_bp)
    
    # Add index route
    @app.route('/')
    def index():
        return jsonify({
            'service': 'Neurowell Analytics API',
            'author': 'Manjunath Chintha',
            'version': '1.0.0',
            'endpoints': {
                'dashboard': '/api/analytics/dashboard?user_id=1',
                'profile': '/api/analytics/profile?user_id=1',
                'charts': {
                    'radar': '/api/analytics/charts/radar?user_id=1',
                    'bar': '/api/analytics/charts/bar?user_id=1',
                    'pie': '/api/analytics/charts/pie?user_id=1'
                },
                'progress': '/api/analytics/progress?user_id=1',
                'analyzer': {
                    'log': '/api/analytics/analyzer/log (POST)',
                    'detect': '/api/analytics/analyzer/detect (POST)'
                },
                'report': '/api/analytics/report/generate (POST)',
                'stats': '/api/analytics/stats?user_id=1',
                'health': '/api/analytics/health'
            },
            'database': 'SQLite (neurowell.db)',
            'status': 'running'
        })
    
    # Add a test endpoint
    @app.route('/test-data')
    def test_data():
        processor = DataProcessor("neurowell.db")
        dashboard_data = processor.get_dashboard_data(1)
        
        if dashboard_data['success']:
            return jsonify({
                'success': True,
                'message': 'Sample dashboard data loaded successfully',
                'data': {
                    'mood_score': dashboard_data['mood_score'],
                    'user': dashboard_data['user_info']['full_name'],
                    'charts_available': list(dashboard_data['charts'].keys())
                }
            })
        else:
            return jsonify(dashboard_data), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    print("\n" + "="*60)
    print("NEUROWELL ANALYTICS API SERVER")
    print("Author: Manjunath Chintha")
    print("="*60)
    print("\n📊 Available Endpoints:")
    print("  http://127.0.0.1:5001/")
    print("  http://127.0.0.1:5001/test-data")
    print("  http://127.0.0.1:5001/api/analytics/dashboard?user_id=1")
    print("  http://127.0.0.1:5001/api/analytics/profile?user_id=1")
    print("  http://127.0.0.1:5001/api/analytics/health")
    print("\n🚀 Server starting on http://127.0.0.1:5001")
    print("Press Ctrl+C to stop\n")
    
    app.run(debug=True, port=5001)