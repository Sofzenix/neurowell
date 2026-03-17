"""
run_server.py
Run Flask server for Neurowell Analytics API
"""

from flask import Flask, jsonify
from flask_cors import CORS
from dashboard import dashboard_bp
from data_processing import DataProcessor

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    CORS(app)
    
    # Initialize database
    print("Initializing database...")
    processor = DataProcessor("neurowell.db")
    print("Database initialized successfully!")
    
    # Register blueprint
    app.register_blueprint(dashboard_bp)
    
    # Index route with service info
    @app.route('/')
    def index():
        return jsonify({
            'service': 'Neurowell Analytics API',
            'author': 'Jayasri',
            'version': '1.0.0',
            'endpoints': {
                'dashboard': '/api/analytics/dashboard?user_id=1',
                'profile': '/api/analytics/profile?user_id=1',
                'charts': {
                    'radar': '/api/analytics/charts/radar?user_id=1',
                    'bar': '/api/analytics/charts/bar?user_id=1',
                    'pie': '/api/analytics/charts/pie?user_id=1'
                },
                'log_mood': '/api/analytics/log_mood (POST)',
                'report': '/api/analytics/report/generate?user_id=1',
                'health': '/api/analytics/health'
            },
            'database': 'SQLite (neurowell.db)',
            'status': 'running'
        })
    
    # Test endpoint for sample dashboard data
    @app.route('/test-data')
    def test_data():
        try:
            data = processor.prepare_dashboard_data("1")
            return jsonify({
                'success': True,
                'message': 'Sample dashboard data loaded successfully',
                'data': data
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    
    print("\n" + "="*60)
    print("NEUROWELL ANALYTICS API SERVER")
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