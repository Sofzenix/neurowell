"""
data_processing.py
Author: Jayasri
Purpose: Process and analyze emotional data for NeuroWell dashboard
Integrated with: index.html, dashboard.html, create_profile.html, script.js
"""

import json
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
import statistics
from fpdf import FPDF  # pip install fpdf2

class DataProcessor:
    """Process emotional data for NeuroWell dashboard"""
    
    def __init__(self, db_path: str = "neurowell.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.insert_sample_user()

    def create_tables(self):
        """Create the necessary tables if they don't exist"""
        # Moods table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS moods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            emotion TEXT,
            intensity INTEGER,
            timestamp TEXT
        )
        """)
        
        # Users table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER,
            phone TEXT,
            gender TEXT,
            member_since TEXT
        )
        """)
        
        # Reports table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            report_type TEXT,
            generated_at TEXT,
            summary TEXT,
            insights TEXT,
            recommendations TEXT
        )
        """)
        
        self.conn.commit()

    def insert_sample_user(self):
        """Insert a default user if none exists"""
        self.cursor.execute("SELECT COUNT(*) FROM users")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute("""
            INSERT INTO users (full_name, email, age, phone, gender, member_since)
            VALUES (?, ?, ?, ?, ?, ?)
            """, ("Jayasri", "jayasri@example.com", 21, "1234567890", "Female", datetime.now().date()))
            self.conn.commit()

    def insert_mood(self, user_id: str, emotion: str, intensity: int, timestamp: str = None):
        """Insert a new mood entry"""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        self.cursor.execute("""
        INSERT INTO moods (user_id, emotion, intensity, timestamp)
        VALUES (?, ?, ?, ?)
        """, (user_id, emotion, intensity, timestamp))
        self.conn.commit()
    
    def fetch_user_data(self, user_id: str) -> pd.DataFrame:
        """Fetch all mood data for a user as a DataFrame"""
        self.cursor.execute("SELECT emotion, intensity, timestamp FROM moods WHERE user_id=?", (user_id,))
        rows = self.cursor.fetchall()
        df = pd.DataFrame(rows, columns=["emotion", "intensity", "timestamp"])
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    
    def daily_mood_summary(self, user_id: str) -> Dict[str, Any]:
        """Calculate daily mood summary"""
        df = self.fetch_user_data(user_id)
        if df.empty:
            return {}
        df['date'] = df['timestamp'].dt.date
        daily_summary = df.groupby('date').agg({
            'intensity': ['mean', 'max'],
            'emotion': lambda x: x.value_counts().idxmax()
        })
        daily_summary.columns = ['avg_intensity', 'max_intensity', 'dominant_emotion']
        return daily_summary.reset_index().to_dict(orient='records')
    
    def weekly_trends(self, user_id: str) -> Dict[str, Any]:
        """Calculate weekly trends"""
        df = self.fetch_user_data(user_id)
        if df.empty:
            return {}
        df['week'] = df['timestamp'].dt.isocalendar().week
        weekly_summary = df.groupby('week').agg({
            'intensity': ['mean', 'max'],
            'emotion': lambda x: x.value_counts().idxmax()
        })
        weekly_summary.columns = ['avg_intensity', 'max_intensity', 'dominant_emotion']
        return weekly_summary.reset_index().to_dict(orient='records')
    
    def emotion_frequency(self, user_id: str) -> Dict[str, int]:
        """Calculate frequency of each emotion"""
        df = self.fetch_user_data(user_id)
        if df.empty:
            return {}
        return df['emotion'].value_counts().to_dict()
    
    def prepare_dashboard_data(self, user_id: str) -> Dict[str, Any]:
        """Prepare all data needed for dashboard visualization"""
        return {
            "daily_summary": self.daily_mood_summary(user_id),
            "weekly_trends": self.weekly_trends(user_id),
            "emotion_frequency": self.emotion_frequency(user_id)
        }
    
    def generate_pdf_report(self, user_id: str, filename: str = None):
        """Generate doctor-style PDF report"""
        data = self.prepare_dashboard_data(user_id)
        if filename is None:
            filename = f"{user_id}_mood_report.pdf"
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"NeuroWell Mood Report - User: {user_id}", ln=True, align="C")
        pdf.ln(10)
        
        # Daily Summary
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Daily Mood Summary", ln=True)
        pdf.set_font("Arial", "", 12)
        for day in data.get("daily_summary", []):
            pdf.cell(0, 8, f"{day['date']}: {day['dominant_emotion']} (Avg: {day['avg_intensity']:.1f}, Max: {day['max_intensity']})", ln=True)
        pdf.ln(5)
        
        # Weekly Trends
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Weekly Mood Trends", ln=True)
        pdf.set_font("Arial", "", 12)
        for week in data.get("weekly_trends", []):
            pdf.cell(0, 8, f"Week {week['week']}: {week['dominant_emotion']} (Avg: {week['avg_intensity']:.1f}, Max: {week['max_intensity']})", ln=True)
        pdf.ln(5)
        
        # Emotion Frequency
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Emotion Frequency", ln=True)
        pdf.set_font("Arial", "", 12)
        for emotion, count in data.get("emotion_frequency", {}).items():
            pdf.cell(0, 8, f"{emotion}: {count}", ln=True)
        
        pdf.output(filename)
        return filename
    
    def close(self):
        """Close database connection"""
        self.conn.close()


# ----------------------------
# Example usage:
# ----------------------------
if __name__ == "__main__":
    dp = DataProcessor()
    dp.insert_mood("1", "happy", 8)
    dp.insert_mood("1", "sad", 4)
    print(dp.prepare_dashboard_data("1"))
    dp.generate_pdf_report("1")
    dp.close()