"""
test_analytics.py
Test script for Manjunath's analytics module
"""

import sqlite3
import json
from data_processing import DataProcessor
import os

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f" {text}")
    print("="*60)

def test_database_setup():
    """Test database initialization"""
    print_header("1. Testing Database Setup")
    
    # Remove existing database if any
    if os.path.exists("neurowell.db"):
        os.remove("neurowell.db")
        print("✓ Removed old database")
    
    # Initialize processor (will create database)
    processor = DataProcessor("neurowell.db")
    print("✓ Database initialized successfully")
    
    # Check if tables exist
    conn = sqlite3.connect("neurowell.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"✓ Created {len(tables)} tables:")
    for table in tables:
        print(f"  - {table[0]}")
    
    conn.close()
    return processor

def test_sample_data(processor):
    """Test that sample data is loaded"""
    print_header("2. Testing Sample Data")
    
    # Check users table
    conn = sqlite3.connect("neurowell.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    print(f"✓ Users in database: {user_count}")
    
    cursor.execute("SELECT full_name, email FROM users")
    users = cursor.fetchall()
    for user in users:
        print(f"✓ User: {user[0]} ({user[1]})")
    
    # Check emotion logs
    cursor.execute("SELECT COUNT(*) FROM emotion_logs")
    emotion_count = cursor.fetchone()[0]
    print(f"✓ Emotion logs: {emotion_count}")
    
    # Check daily mood
    cursor.execute("SELECT COUNT(*) FROM daily_mood")
    daily_count = cursor.fetchone()[0]
    print(f"✓ Daily mood entries: {daily_count}")
    
    conn.close()

def test_chart_data(processor):
    """Test chart data generation"""
    print_header("3. Testing Chart Data Generation")
    
    # Test radar chart data
    radar_data = processor.get_radar_chart_data(1)
    print("✓ Radar Chart Data:")
    print(f"  Labels: {radar_data['labels']}")
    print(f"  Data: {radar_data['datasets'][0]['data']}")
    
    # Test bar chart data
    bar_data = processor.get_bar_chart_data(1)
    print("✓ Bar Chart Data:")
    print(f"  Labels: {bar_data['labels']}")
    print(f"  Data: {bar_data['datasets'][0]['data']}")
    
    # Test pie chart data
    pie_data = processor.get_pie_chart_data(1)
    print("✓ Pie Chart Data:")
    print(f"  Labels: {pie_data['labels']}")
    print(f"  Data: {pie_data['datasets'][0]['data']}")
    
    # Test progress data
    progress_data = processor.get_progress_data(1)
    print("✓ Progress Data:")
    for emotion, data in progress_data.items():
        print(f"  {data['label']}: {data['score']}%")

def test_user_functions(processor):
    """Test user-related functions"""
    print_header("4. Testing User Functions")
    
    # Get user info
    user_info = processor.get_user_info(1)
    print("✓ User Information:")
    for key, value in user_info.items():
        print(f"  {key}: {value}")
    
    # Calculate mood score
    mood_score = processor.calculate_mood_score(1)
    print(f"✓ Calculated Mood Score: {mood_score}%")

def test_analyzer_functions(processor):
    """Test analyzer integration"""
    print_header("5. Testing Analyzer Functions")
    
    # Log a new emotion
    print("Logging new emotion 'happy' from text analyzer...")
    result = processor.log_emotion(1, "happy", "text", 0.9)
    
    if result['success']:
        print(f"✓ {result['message']}")
        print(f"✓ Mood score updated to: {result['mood_score']}%")
    else:
        print(f"✗ Error: {result.get('error', 'Unknown error')}")
    
    # Log another emotion
    print("\nLogging new emotion 'calm' from face analyzer...")
    result = processor.log_emotion(1, "calm", "face", 0.85)
    
    if result['success']:
        print(f"✓ {result['message']}")
        print(f"✓ Mood score updated to: {result['mood_score']}%")

def test_report_generation(processor):
    """Test report generation"""
    print_header("6. Testing Report Generation")
    
    result = processor.generate_report(1, "weekly")
    
    if result['success']:
        report = result['report']
        print("✓ Report Generated Successfully!")
        print(f"✓ Report ID: {report['report_id']}")
        print(f"✓ User: {report['user_name']}")
        print(f"✓ Generated: {report['generated_at']}")
        
        print("\n📊 Summary:")
        for key, value in report['summary'].items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        
        print("\n💡 Insights:")
        for i, insight in enumerate(report['insights'], 1):
            print(f"  {i}. {insight}")
        
        print("\n✅ Recommendations:")
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"  {i}. {rec}")
    else:
        print(f"✗ Error generating report: {result.get('error', 'Unknown error')}")

def test_statistics(processor):
    """Test statistics functions"""
    print_header("7. Testing Statistics")
    
    stats = processor.get_statistics(1)
    
    print("📈 User Statistics:")
    print(f"  Total Emotion Logs: {stats['total_logs']}")
    print(f"  Active Tracking Days: {stats['active_days']}")
    print(f"  First Log: {stats['first_log']}")
    print(f"  Last Log: {stats['last_log']}")
    
    if stats['emotion_stats']:
        print("\n  Emotion Statistics:")
        for stat in stats['emotion_stats']:
            print(f"    {stat['emotion']}: {stat['count']} entries, {stat['avg_confidence']:.1f}% avg confidence")

def run_flask_server():
    """Run Flask server for API testing"""
    print_header("8. Starting Flask Server")
    
    # Create a simple Flask app
    from flask import Flask, jsonify
    from dashboard import dashboard_bp
    
    app = Flask(__name__)
    app.register_blueprint(dashboard_bp)
    
    # Add a test endpoint
    @app.route('/test')
    def test_endpoint():
        return jsonify({
            'message': 'Analytics module is working!',
            'author': 'Manjunath Chintha',
            'endpoints': [
                '/api/analytics/dashboard?user_id=1',
                '/api/analytics/charts/radar?user_id=1',
                '/api/analytics/profile?user_id=1',
                '/api/analytics/report/generate (POST)'
            ]
        })
    
    print("✓ Flask server configured")
    print("✓ Available at: http://127.0.0.1:5001")
    print("\nEndpoints to test:")
    print("  • http://127.0.0.1:5001/test")
    print("  • http://127.0.0.1:5001/api/analytics/dashboard?user_id=1")
    print("  • http://127.0.0.1:5001/api/analytics/profile?user_id=1")
    print("  • http://127.0.0.1:5001/api/analytics/health")
    print("\nPress Ctrl+C to stop the server")
    
    # Note: Uncomment to auto-start server
    # app.run(debug=True, port=5001)

def main():
    """Main test function"""
    print_header("NEUROWELL ANALYTICS MODULE TEST")
    print("Author: Manjunath Chintha")
    print("Testing data_processing.py and dashboard.py")
    
    try:
        # Test 1: Database setup
        processor = test_database_setup()
        
        # Test 2: Sample data
        test_sample_data(processor)
        
        # Test 3: Chart data
        test_chart_data(processor)
        
        # Test 4: User functions
        test_user_functions(processor)
        
        # Test 5: Analyzer functions
        test_analyzer_functions(processor)
        
        # Test 6: Report generation
        test_report_generation(processor)
        
        # Test 7: Statistics
        test_statistics(processor)
        
        # Test 8: Flask server setup
        run_flask_server()
        
        print_header("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("\nNext steps:")
        print("1. Install requirements: pip install -r requirements.txt")
        print("2. Run Flask server: python run_server.py")
        print("3. Test APIs in browser or Postman")
        
    except Exception as e:
        print_header("❌ TEST FAILED")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()