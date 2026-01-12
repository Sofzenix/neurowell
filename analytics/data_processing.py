"""
data_processing.py
Author: Manjunath Chintha
Purpose: Process and analyze emotional data for Neurowell dashboard
Integrated with: index.html, dashboard.html, create_profile.html, script.js
"""

import json
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import statistics

class DataProcessor:
    """Process emotional data for Neurowell dashboard"""
    
    def __init__(self, db_path: str = "neurowell.db"):
        """
        Initialize data processor with database connection
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        self._init_database()
        self._ensure_sample_data()
    
    def _init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # User profiles (from create_profile.html)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT,
            email TEXT,
            age INTEGER,
            phone TEXT,
            gender TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
        ''')
        
        # Emotion logs from analyzer (face, voice, text)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS emotion_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            emotion TEXT NOT NULL,
            source TEXT NOT NULL,  -- 'face', 'voice', 'text', 'manual'
            confidence FLOAT DEFAULT 0.8,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        # Daily mood scores (for bar chart)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_mood (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date DATE NOT NULL,
            mood_score INTEGER,  -- 0-100
            dominant_emotion TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE(user_id, date)
        )
        ''')
        
        # Generated reports
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            report_type TEXT,  -- 'weekly', 'monthly', 'custom'
            report_data TEXT,  -- JSON data
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def _ensure_sample_data(self):
        """Ensure sample data exists for dashboard (user_id = 1 = Arib Khan)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if user exists (Arib Khan from dashboard.html)
        cursor.execute("SELECT id FROM users WHERE username = 'aribkhan'")
        if cursor.fetchone() is None:
            # Create sample user matching dashboard.html
            cursor.execute('''
            INSERT INTO users (username, password, full_name, email, age, phone, gender)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                'aribkhan',
                'hashed_password',  # In real app, hash this
                'Arib Khan',
                'khanarib075@gmail.com',
                25,
                '+1234567890',
                'Male'
            ))
            user_id = cursor.lastrowid
        else:
            cursor.execute("SELECT id FROM users WHERE username = 'aribkhan'")
            user_id = cursor.fetchone()[0]
        
        # Check if we have emotion logs for radar chart
        cursor.execute("SELECT COUNT(*) FROM emotion_logs WHERE user_id = ?", (user_id,))
        if cursor.fetchone()[0] == 0:
            # Insert sample emotion data matching radar chart: [82, 40, 25, 70, 35]
            emotions = ['happy', 'sad', 'angry', 'calm', 'anxious']
            # Create multiple entries for each emotion with appropriate weights
            sample_data = [
                ('happy', 82, 10),    # 10 entries for happy with score 82
                ('sad', 40, 6),       # 6 entries for sad with score 40
                ('angry', 25, 4),     # 4 entries for angry with score 25
                ('calm', 70, 8),      # 8 entries for calm with score 70
                ('anxious', 35, 5)    # 5 entries for anxious with score 35
            ]
            
            for emotion, score, count in sample_data:
                for _ in range(count):
                    cursor.execute('''
                    INSERT INTO emotion_logs (user_id, emotion, source, confidence)
                    VALUES (?, ?, ?, ?)
                    ''', (user_id, emotion, 'sample', score/100))
        
        # Check if we have daily mood data for bar chart
        cursor.execute("SELECT COUNT(*) FROM daily_mood WHERE user_id = ?", (user_id,))
        if cursor.fetchone()[0] == 0:
            # Insert 7 days of data matching bar chart: [70, 75, 60, 82, 68, 80, 77]
            daily_scores = [70, 75, 60, 82, 68, 80, 77]
            days_ago = 6  # Last 7 days including today
            
            for i, score in enumerate(daily_scores):
                date = (datetime.now() - timedelta(days=days_ago-i)).strftime('%Y-%m-%d')
                cursor.execute('''
                INSERT OR REPLACE INTO daily_mood (user_id, date, mood_score, dominant_emotion)
                VALUES (?, ?, ?, ?)
                ''', (user_id, date, score, self._score_to_emotion(score)))
        
        conn.commit()
        conn.close()
    
    def _score_to_emotion(self, score: int) -> str:
        """Convert mood score (0-100) to emotion label"""
        if score >= 80:
            return 'happy'
        elif score >= 60:
            return 'calm'
        elif score >= 40:
            return 'neutral'
        elif score >= 20:
            return 'sad'
        else:
            return 'anxious'
    
    # ==================== USER AUTHENTICATION ====================
    
    def create_user(self, user_data: Dict) -> Dict:
        """
        Create new user profile (from create_profile.html)
        Args:
            user_data: Dictionary with user info
        Returns:
            Dictionary with result
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO users (username, password, full_name, email, age, phone, gender)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_data.get('username'),
                user_data.get('password'),  # Note: Hash this in production!
                user_data.get('full_name'),
                user_data.get('email'),
                user_data.get('age'),
                user_data.get('phone'),
                user_data.get('gender')
            ))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'user_id': user_id,
                'message': f"Profile created for {user_data.get('full_name')}"
            }
            
        except sqlite3.IntegrityError:
            return {
                'success': False,
                'error': 'Username already exists'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def authenticate_user(self, username: str, password: str) -> Dict:
        """
        Authenticate user login (from index.html)
        Args:
            username: Username from login form
            password: Password from login form
        Returns:
            Dictionary with authentication result
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT id, full_name, email FROM users 
            WHERE username = ? AND password = ?
            ''', (username, password))  # Note: Use hashed passwords in production!
            
            user = cursor.fetchone()
            
            if user:
                # Update last login
                cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
                ''', (user[0],))
                conn.commit()
                
                return {
                    'success': True,
                    'user_id': user[0],
                    'full_name': user[1],
                    'email': user[2]
                }
            else:
                return {
                    'success': False,
                    'error': 'Invalid username or password'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            conn.close()
    
    # ==================== DASHBOARD DATA PROCESSING ====================
    
    def get_dashboard_data(self, user_id: int = 1) -> Dict:
        """
        Get all data needed for dashboard display
        Returns data in format needed by dashboard.html charts
        """
        try:
            # Get user info
            user_info = self.get_user_info(user_id)
            
            # Get chart data
            radar_data = self.get_radar_chart_data(user_id)
            bar_data = self.get_bar_chart_data(user_id)
            pie_data = self.get_pie_chart_data(user_id)
            progress_data = self.get_progress_data(user_id)
            
            # Calculate overall mood score (from profile in dashboard.html)
            mood_score = self.calculate_mood_score(user_id)
            
            return {
                'success': True,
                'user_info': user_info,
                'mood_score': mood_score,
                'charts': {
                    'radar': radar_data,
                    'bar': bar_data,
                    'pie': pie_data
                },
                'progress': progress_data,
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_radar_chart_data(self, user_id: int) -> Dict:
        """
        Get data for emotion radar chart
        Returns: {'labels': [], 'datasets': [{'data': [], ...}]}
        """
        conn = sqlite3.connect(self.db_path)
        
        # Get average confidence for each emotion (convert to percentage)
        query = '''
        SELECT emotion, AVG(confidence * 100) as avg_score
        FROM emotion_logs 
        WHERE user_id = ?
        GROUP BY emotion
        ORDER BY CASE emotion
            WHEN 'happy' THEN 1
            WHEN 'sad' THEN 2
            WHEN 'angry' THEN 3
            WHEN 'calm' THEN 4
            WHEN 'anxious' THEN 5
            ELSE 6
        END
        '''
        
        df = pd.read_sql_query(query, conn, params=(user_id,))
        conn.close()
        
        # Default data from dashboard.html: [82, 40, 25, 70, 35]
        default_data = {
            'happy': 82,
            'sad': 40,
            'angry': 25,
            'calm': 70,
            'anxious': 35
        }
        
        labels = ['Happiness', 'Sadness', 'Anger', 'Calmness', 'Anxiety']
        data = []
        
        for label, emotion in zip(labels, ['happy', 'sad', 'angry', 'calm', 'anxious']):
            emotion_data = df[df['emotion'] == emotion]
            if not emotion_data.empty:
                score = round(float(emotion_data.iloc[0]['avg_score']), 1)
                data.append(score)
            else:
                data.append(default_data.get(emotion, 50))
        
        return {
            'labels': labels,
            'datasets': [{
                'label': 'Mood %',
                'data': data,
                'backgroundColor': 'rgba(44, 182, 125, 0.3)',
                'borderColor': '#2cb67d',
                'borderWidth': 2
            }]
        }
    
    def get_bar_chart_data(self, user_id: int) -> Dict:
        """
        Get data for weekly mood bar chart
        Returns: {'labels': [], 'datasets': [{'data': [], ...}]}
        """
        conn = sqlite3.connect(self.db_path)
        
        # Get last 7 days of mood scores
        query = '''
        SELECT date, mood_score 
        FROM daily_mood 
        WHERE user_id = ?
        ORDER BY date DESC 
        LIMIT 7
        '''
        
        df = pd.read_sql_query(query, conn, params=(user_id,))
        conn.close()
        
        if df.empty or len(df) < 7:
            # Return default data from dashboard.html: [70, 75, 60, 82, 68, 80, 77]
            labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            data = [70, 75, 60, 82, 68, 80, 77]
        else:
            # Ensure we have data for last 7 days
            df = df.sort_values('date').tail(7)
            # Convert dates to day names
            labels = []
            for date_str in df['date']:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                labels.append(date_obj.strftime('%a'))
            data = df['mood_score'].tolist()
        
        return {
            'labels': labels,
            'datasets': [{
                'label': 'Mood %',
                'data': data,
                'backgroundColor': '#2cb67d'
            }]
        }
    
    def get_pie_chart_data(self, user_id: int) -> Dict:
        """
        Get data for emotion distribution pie chart
        Returns: {'labels': [], 'datasets': [{'data': [], 'backgroundColor': []}]}
        """
        conn = sqlite3.connect(self.db_path)
        
        # Get emotion distribution (percentage)
        query = '''
        SELECT emotion, COUNT(*) as count
        FROM emotion_logs 
        WHERE user_id = ?
        GROUP BY emotion
        '''
        
        df = pd.read_sql_query(query, conn, params=(user_id,))
        conn.close()
        
        if df.empty:
            # Default data from dashboard.html: [40, 25, 15, 10, 10]
            labels = ['Happy', 'Calm', 'Sad', 'Angry', 'Anxious']
            data = [40, 25, 15, 10, 10]
            colors = ["#2cb67d", "#7f5af0", "#f65a5a", "#f5a623", "#23a26f"]
        else:
            # Calculate percentages
            total = df['count'].sum()
            df['percentage'] = (df['count'] / total * 100).round(1)
            
            # Map emotion names
            emotion_map = {
                'happy': 'Happy',
                'calm': 'Calm',
                'sad': 'Sad',
                'angry': 'Angry',
                'anxious': 'Anxious'
            }
            
            labels = []
            data = []
            colors = []
            
            # Color mapping
            color_map = {
                'Happy': "#2cb67d",
                'Calm': "#7f5af0",
                'Sad': "#f65a5a",
                'Angry': "#f5a623",
                'Anxious': "#23a26f"
            }
            
            for _, row in df.iterrows():
                emotion = emotion_map.get(row['emotion'], row['emotion'].capitalize())
                labels.append(emotion)
                data.append(float(row['percentage']))
                colors.append(color_map.get(emotion, '#8e8e93'))
        
        return {
            'labels': labels,
            'datasets': [{
                'data': data,
                'backgroundColor': colors
            }]
        }
    
    def get_progress_data(self, user_id: int) -> Dict:
        """
        Get progress bar data for dashboard
        Returns: {'happiness': %, 'calmness': %, 'anxiety': %}
        """
        conn = sqlite3.connect(self.db_path)
        
        # Get latest scores for specific emotions
        query = '''
        SELECT emotion, AVG(confidence * 100) as avg_score
        FROM emotion_logs 
        WHERE user_id = ? 
          AND emotion IN ('happy', 'calm', 'anxious')
        GROUP BY emotion
        '''
        
        df = pd.read_sql_query(query, conn, params=(user_id,))
        conn.close()
        
        # Default values from dashboard.html
        default_scores = {
            'happy': 82,
            'calm': 70,
            'anxious': 35
        }
        
        progress_data = {}
        for emotion in ['happy', 'calm', 'anxious']:
            emotion_df = df[df['emotion'] == emotion]
            if not emotion_df.empty:
                score = round(float(emotion_df.iloc[0]['avg_score']), 1)
            else:
                score = default_scores.get(emotion, 50)
            
            label = 'Happiness' if emotion == 'happy' else 'Calmness' if emotion == 'calm' else 'Anxiety'
            progress_data[emotion] = {
                'score': score,
                'label': label,
                'width': f"{score}%"
            }
        
        return progress_data
    
    def calculate_mood_score(self, user_id: int) -> float:
        """
        Calculate overall mood score (0-100)
        Used in profile section of dashboard.html
        """
        conn = sqlite3.connect(self.db_path)
        
        # Get average of last 7 daily mood scores
        query = '''
        SELECT AVG(mood_score) as avg_score
        FROM daily_mood 
        WHERE user_id = ?
        ORDER BY date DESC 
        LIMIT 7
        '''
        
        cursor = conn.cursor()
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0]:
            return round(float(result[0]), 1)
        else:
            return 82.0  # Default from dashboard.html
    
    def get_user_info(self, user_id: int) -> Dict:
        """Get user information for profile display"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT full_name, email, age, phone, gender, created_at
        FROM users WHERE id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'full_name': result[0],
                'email': result[1],
                'age': result[2],
                'phone': result[3],
                'gender': result[4],
                'member_since': result[5]
            }
        else:
            # Return default data from dashboard.html
            return {
                'full_name': 'Arib Khan',
                'email': 'khanarib075@gmail.com',
                'age': 25,
                'phone': '+1234567890',
                'gender': 'Male',
                'member_since': '2024-01-01'
            }
    
    # ==================== ANALYZER INTEGRATION ====================
    
    def log_emotion(self, user_id: int, emotion: str, source: str = 'text', confidence: float = 0.8) -> Dict:
        """
        Log emotion from analyzer (face, voice, text)
        Args:
            user_id: User ID
            emotion: Emotion detected
            source: 'face', 'voice', or 'text'
            confidence: Detection confidence (0-1)
        Returns:
            Dictionary with result
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Insert emotion log
            cursor.execute('''
            INSERT INTO emotion_logs (user_id, emotion, source, confidence)
            VALUES (?, ?, ?, ?)
            ''', (user_id, emotion.lower(), source, confidence))
            
            # Update today's mood score
            today = datetime.now().strftime('%Y-%m-%d')
            
            # Convert emotion to mood score
            emotion_scores = {
                'happy': 80,
                'joy': 85,
                'excited': 75,
                'calm': 70,
                'relaxed': 75,
                'peaceful': 80,
                'neutral': 50,
                'sad': 30,
                'depressed': 20,
                'angry': 25,
                'frustrated': 30,
                'anxious': 35,
                'stressed': 30,
                'worried': 40
            }
            
            mood_score = emotion_scores.get(emotion.lower(), 50)
            
            # Update or insert daily mood
            cursor.execute('''
            SELECT id FROM daily_mood WHERE user_id = ? AND date = ?
            ''', (user_id, today))
            
            if cursor.fetchone():
                # Update existing entry (average with previous)
                cursor.execute('''
                UPDATE daily_mood 
                SET mood_score = (mood_score + ?) / 2,
                    dominant_emotion = ?
                WHERE user_id = ? AND date = ?
                ''', (mood_score, emotion, user_id, today))
            else:
                # Insert new entry
                cursor.execute('''
                INSERT INTO daily_mood (user_id, date, mood_score, dominant_emotion)
                VALUES (?, ?, ?, ?)
                ''', (user_id, today, mood_score, emotion))
            
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'emotion': emotion,
                'mood_score': mood_score,
                'message': f'Emotion logged: {emotion} from {source}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    # ==================== REPORT GENERATION ====================
    
    def generate_report(self, user_id: int, report_type: str = 'weekly') -> Dict:
        """
        Generate emotional analysis report
        Returns data for report section in dashboard.html
        """
        try:
            # Get user info
            user_info = self.get_user_info(user_id)
            
            # Get analysis data
            mood_score = self.calculate_mood_score(user_id)
            
            # Get emotion distribution
            pie_data = self.get_pie_chart_data(user_id)
            dominant_emotion = pie_data['labels'][0] if pie_data['labels'] else 'Happiness'
            
            # Get weekly trend
            bar_data = self.get_bar_chart_data(user_id)
            weekly_avg = sum(bar_data['datasets'][0]['data']) / len(bar_data['datasets'][0]['data'])
            
            # Get progress data
            progress_data = self.get_progress_data(user_id)
            
            # Generate report
            report = {
                'report_id': f"NW_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'user_id': user_id,
                'user_name': user_info['full_name'],
                'report_type': report_type,
                'generated_at': datetime.now().isoformat(),
                'period': 'Last 7 days',
                'summary': {
                    'average_mood_score': round(mood_score, 1),
                    'dominant_emotion': dominant_emotion,
                    'weekly_average': round(weekly_avg, 1),
                    'happiness_level': progress_data.get('happy', {}).get('score', 0),
                    'calmness_level': progress_data.get('calm', {}).get('score', 0),
                    'anxiety_level': progress_data.get('anxious', {}).get('score', 0)
                },
                'insights': self._generate_insights(mood_score, dominant_emotion, weekly_avg),
                'recommendations': self._generate_recommendations(mood_score, dominant_emotion)
            }
            
            # Save report to database
            self._save_report(user_id, report_type, report)
            
            return {
                'success': True,
                'report': report
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _generate_insights(self, mood_score: float, dominant_emotion: str, weekly_avg: float) -> List[str]:
        """Generate insights based on mood data"""
        insights = []
        
        if mood_score >= 80:
            insights.append("Excellent emotional well-being! Your mood scores are consistently high.")
        elif mood_score >= 60:
            insights.append("Good emotional balance. You're maintaining healthy emotional patterns.")
        else:
            insights.append("We notice room for emotional improvement. Consider mindfulness practices.")
        
        if weekly_avg > mood_score:
            insights.append("Positive trend detected! Your mood has improved this week.")
        elif weekly_avg < mood_score:
            insights.append("Slight decline detected. Consider stress-reduction techniques.")
        
        emotion_insights = {
            'Happy': "Happiness is your dominant emotion. You're radiating positive energy!",
            'Calm': "Calmness dominates your emotional state. Great emotional regulation!",
            'Sad': "Sadness is detected. Remember, it's okay to feel sad sometimes.",
            'Anxious': "Anxiety is prominent. Try breathing exercises to manage stress.",
            'Angry': "Anger is detected. Physical activity can help channel this energy."
        }
        
        insights.append(emotion_insights.get(dominant_emotion, "Keep tracking your emotions for better awareness."))
        
        return insights
    
    def _generate_recommendations(self, mood_score: float, dominant_emotion: str) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = [
            "Practice 10 minutes of mindfulness meditation daily",
            "Maintain a consistent sleep schedule (7-8 hours)",
            "Engage in 30 minutes of physical activity daily",
            "Keep a gratitude journal and write 3 things you're thankful for each day"
        ]
        
        if mood_score < 60:
            recommendations.append("Consider talking to a friend or loved one about your feelings")
            recommendations.append("Try progressive muscle relaxation before bed")
        
        if dominant_emotion in ['Anxious', 'Sad']:
            recommendations.append("Practice deep breathing exercises when feeling overwhelmed")
            recommendations.append("Limit caffeine intake and increase water consumption")
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def _save_report(self, user_id: int, report_type: str, report_data: Dict):
        """Save generated report to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO reports (user_id, report_type, report_data)
        VALUES (?, ?, ?)
        ''', (user_id, report_type, json.dumps(report_data)))
        
        conn.commit()
        conn.close()
    
    # ==================== STATISTICS AND ANALYTICS ====================
    
    def get_statistics(self, user_id: int) -> Dict:
        """Get overall statistics for user"""
        conn = sqlite3.connect(self.db_path)
        
        # Get total emotion logs
        cursor = conn.cursor()
        cursor.execute('''
        SELECT COUNT(*) as total_logs,
               COUNT(DISTINCT DATE(timestamp)) as active_days,
               MIN(timestamp) as first_log,
               MAX(timestamp) as last_log
        FROM emotion_logs WHERE user_id = ?
        ''', (user_id,))
        
        stats = cursor.fetchone()
        
        # Get emotion frequency
        query = '''
        SELECT emotion, COUNT(*) as count,
               AVG(confidence * 100) as avg_confidence
        FROM emotion_logs 
        WHERE user_id = ?
        GROUP BY emotion
        ORDER BY count DESC
        '''
        
        df = pd.read_sql_query(query, conn, params=(user_id,))
        conn.close()
        
        if stats:
            return {
                'total_logs': stats[0],
                'active_days': stats[1],
                'first_log': stats[2],
                'last_log': stats[3],
                'emotion_stats': df.to_dict('records') if not df.empty else []
            }
        else:
            return {
                'total_logs': 0,
                'active_days': 0,
                'emotion_stats': []
            }


# Export
__all__ = ['DataProcessor']