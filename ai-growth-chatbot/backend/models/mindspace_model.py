import sqlite3
import json
import os
from datetime import datetime, timedelta

class MindSpaceModel:
    def __init__(self):
        self.db_path = 'mindspace.db'
        self.init_database()
    
    def init_database(self):
        """Initialize the MindSpace database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                duration_minutes INTEGER,
                category TEXT,
                difficulty TEXT,
                instructor TEXT,
                image_url TEXT,
                audio_url TEXT,
                video_url TEXT,
                content_type TEXT DEFAULT 'audio',
                plays INTEGER DEFAULT 0,
                rating REAL DEFAULT 0,
                tags TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create user_sessions table for progress tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                session_id INTEGER NOT NULL,
                started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                completed_at DATETIME,
                progress_seconds INTEGER DEFAULT 0,
                is_completed BOOLEAN DEFAULT 0,
                rating INTEGER,
                notes TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            )
        ''')
        
        # Create user_progress table for overall stats
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL UNIQUE,
                total_sessions_completed INTEGER DEFAULT 0,
                total_minutes_practiced INTEGER DEFAULT 0,
                streak_days INTEGER DEFAULT 0,
                last_session_date DATE,
                favorite_category TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create categories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                icon TEXT,
                color TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Insert default categories if they don't exist
        self.insert_default_categories()
        
        # Insert sample sessions if none exist
        self.insert_sample_sessions()
    
    def insert_default_categories(self):
        """Insert default categories"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        categories = [
            ('Meditation', 'Guided mindfulness and meditation practices', 'heart', '#f97316'),
            ('Focus', 'Concentration and productivity sessions', 'zap', '#3b82f6'),
            ('Sleep', 'Relaxation and sleep-inducing content', 'moon', '#6366f1'),
            ('Energy', 'Energizing and motivating sessions', 'sun', '#eab308'),
            ('Nature', 'Natural sounds and environments', 'wind', '#22c55e'),
            ('Anxiety', 'Stress and anxiety relief', 'waves', '#06b6d4'),
        ]
        
        for name, description, icon, color in categories:
            cursor.execute('''
                INSERT OR IGNORE INTO categories (name, description, icon, color)
                VALUES (?, ?, ?, ?)
            ''', (name, description, icon, color))
        
        conn.commit()
        conn.close()
    
    def insert_sample_sessions(self):
        """Insert sample sessions if none exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM sessions')
        count = cursor.fetchone()[0]
        
        if count == 0:
            sample_sessions = [
                {
                    'title': 'Morning Mindfulness',
                    'description': 'Start your day with clarity and intention through guided mindfulness practice.',
                    'duration_minutes': 10,
                    'category': 'Meditation',
                    'difficulty': 'Beginner',
                    'instructor': 'Sarah Chen',
                    'image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&h=200&fit=crop',
                    'audio_url': '/audio/morning-mindfulness.mp3',
                    'content_type': 'audio',
                    'plays': 1250,
                    'rating': 4.8,
                    'tags': 'morning,mindfulness,beginner'
                },
                {
                    'title': 'Deep Focus Flow',
                    'description': 'Enhance concentration and productivity with binaural beats and ambient sounds.',
                    'duration_minutes': 25,
                    'category': 'Focus',
                    'difficulty': 'Intermediate',
                    'instructor': 'Michael Torres',
                    'image_url': 'https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=300&h=200&fit=crop',
                    'audio_url': '/audio/deep-focus.mp3',
                    'content_type': 'audio',
                    'plays': 890,
                    'rating': 4.9,
                    'tags': 'focus,productivity,binaural'
                },
                {
                    'title': 'Peaceful Sleep Journey',
                    'description': 'Drift into restful sleep with calming narration and gentle soundscapes.',
                    'duration_minutes': 30,
                    'category': 'Sleep',
                    'difficulty': 'Beginner',
                    'instructor': 'Emma Wilson',
                    'image_url': 'https://images.unsplash.com/photo-1517147177326-b37599372b73?w=300&h=200&fit=crop',
                    'audio_url': '/audio/sleep-journey.mp3',
                    'content_type': 'audio',
                    'plays': 2100,
                    'rating': 4.7,
                    'tags': 'sleep,relaxation,bedtime'
                },
                {
                    'title': 'Energy Boost Meditation',
                    'description': 'Revitalize your mind and body with energizing breathing techniques.',
                    'duration_minutes': 15,
                    'category': 'Energy',
                    'difficulty': 'Intermediate',
                    'instructor': 'David Kim',
                    'image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&h=200&fit=crop',
                    'audio_url': '/audio/energy-boost.mp3',
                    'content_type': 'audio',
                    'plays': 675,
                    'rating': 4.6,
                    'tags': 'energy,breathing,morning'
                },
                {
                    'title': 'Forest Sounds Relaxation',
                    'description': 'Immerse yourself in the tranquil sounds of nature for deep relaxation.',
                    'duration_minutes': 45,
                    'category': 'Nature',
                    'difficulty': 'Beginner',
                    'instructor': 'Nature Sounds',
                    'image_url': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=300&h=200&fit=crop',
                    'audio_url': '/audio/forest-sounds.mp3',
                    'content_type': 'audio',
                    'plays': 1800,
                    'rating': 4.9,
                    'tags': 'nature,forest,ambient'
                },
                {
                    'title': 'Ocean Waves Meditation',
                    'description': 'Let the rhythmic sounds of ocean waves guide you to inner peace.',
                    'duration_minutes': 20,
                    'category': 'Nature',
                    'difficulty': 'Beginner',
                    'instructor': 'Ocean Sounds',
                    'image_url': 'https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=300&h=200&fit=crop',
                    'audio_url': '/audio/ocean-waves.mp3',
                    'content_type': 'audio',
                    'plays': 1450,
                    'rating': 4.8,
                    'tags': 'ocean,waves,calming'
                },
                {
                    'title': 'Anxiety Relief Breathing',
                    'description': 'Calm your mind and reduce anxiety with guided breathing exercises.',
                    'duration_minutes': 12,
                    'category': 'Anxiety',
                    'difficulty': 'Beginner',
                    'instructor': 'Dr. Lisa Chen',
                    'image_url': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=300&h=200&fit=crop',
                    'audio_url': '/audio/anxiety-relief.mp3',
                    'video_url': '/video/breathing-exercise.mp4',
                    'content_type': 'video',
                    'plays': 950,
                    'rating': 4.7,
                    'tags': 'anxiety,breathing,stress-relief'
                }
            ]
            
            for session in sample_sessions:
                cursor.execute('''
                    INSERT INTO sessions (title, description, duration_minutes, category, difficulty, 
                                        instructor, image_url, audio_url, video_url, content_type, 
                                        plays, rating, tags)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    session['title'], session['description'], session['duration_minutes'],
                    session['category'], session['difficulty'], session['instructor'],
                    session['image_url'], session['audio_url'], session.get('video_url'),
                    session['content_type'], session['plays'], session['rating'], session['tags']
                ))
        
        conn.commit()
        conn.close()
    
    def get_all_sessions(self, category=None):
        """Get all sessions, optionally filtered by category"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if category and category != 'all':
            cursor.execute('SELECT * FROM sessions WHERE category = ? ORDER BY rating DESC', (category,))
        else:
            cursor.execute('SELECT * FROM sessions ORDER BY rating DESC')
        
        sessions = cursor.fetchall()
        conn.close()
        
        return [self._format_session(session) for session in sessions]
    
    def get_session_by_id(self, session_id):
        """Get a specific session by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM sessions WHERE id = ?', (session_id,))
        session = cursor.fetchone()
        conn.close()
        
        return self._format_session(session) if session else None
    
    def get_categories(self):
        """Get all categories"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM categories ORDER BY name')
        categories = cursor.fetchall()
        conn.close()
        
        return [{'id': cat[1].lower(), 'name': cat[1], 'description': cat[2], 'icon': cat[3], 'color': cat[4]} for cat in categories]
    
    def start_session(self, user_id, session_id):
        """Start a session for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if user already has an active session
        cursor.execute('''
            SELECT id FROM user_sessions 
            WHERE user_id = ? AND session_id = ? AND completed_at IS NULL
        ''', (user_id, session_id))
        
        existing = cursor.fetchone()
        
        if existing:
            return existing[0]
        
        # Create new session record
        cursor.execute('''
            INSERT INTO user_sessions (user_id, session_id, started_at)
            VALUES (?, ?, ?)
        ''', (user_id, session_id, datetime.now()))
        
        session_record_id = cursor.lastrowid
        
        # Update session play count
        cursor.execute('UPDATE sessions SET plays = plays + 1 WHERE id = ?', (session_id,))
        
        conn.commit()
        conn.close()
        
        return session_record_id
    
    def update_session_progress(self, user_id, session_id, progress_seconds):
        """Update session progress"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE user_sessions 
            SET progress_seconds = ?
            WHERE user_id = ? AND session_id = ? AND completed_at IS NULL
        ''', (progress_seconds, user_id, session_id))
        
        conn.commit()
        conn.close()
    
    def complete_session(self, user_id, session_id, rating=None, notes=None):
        """Mark a session as completed"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get session duration
        cursor.execute('SELECT duration_minutes, category FROM sessions WHERE id = ?', (session_id,))
        session_info = cursor.fetchone()
        
        if not session_info:
            conn.close()
            return False
        
        duration_minutes, category = session_info
        
        # Mark session as completed
        cursor.execute('''
            UPDATE user_sessions 
            SET completed_at = ?, is_completed = 1, rating = ?, notes = ?
            WHERE user_id = ? AND session_id = ? AND completed_at IS NULL
        ''', (datetime.now(), rating, notes, user_id, session_id))
        
        # Update or create user progress
        cursor.execute('SELECT * FROM user_progress WHERE user_id = ?', (user_id,))
        progress = cursor.fetchone()
        
        today = datetime.now().date()
        
        if progress:
            # Update existing progress
            last_session_date = datetime.strptime(progress[5], '%Y-%m-%d').date() if progress[5] else None
            new_streak = progress[4] + 1 if last_session_date and (today - last_session_date).days <= 1 else 1
            
            cursor.execute('''
                UPDATE user_progress 
                SET total_sessions_completed = total_sessions_completed + 1,
                    total_minutes_practiced = total_minutes_practiced + ?,
                    streak_days = ?,
                    last_session_date = ?,
                    favorite_category = ?,
                    updated_at = ?
                WHERE user_id = ?
            ''', (duration_minutes, new_streak, today, category, datetime.now(), user_id))
        else:
            # Create new progress record
            cursor.execute('''
                INSERT INTO user_progress 
                (user_id, total_sessions_completed, total_minutes_practiced, 
                 streak_days, last_session_date, favorite_category)
                VALUES (?, 1, ?, 1, ?, ?)
            ''', (user_id, duration_minutes, today, category))
        
        conn.commit()
        conn.close()
        return True
    
    def get_user_progress(self, user_id):
        """Get user's overall progress"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM user_progress WHERE user_id = ?', (user_id,))
        progress = cursor.fetchone()
        
        if not progress:
            conn.close()
            return {
                'total_sessions_completed': 0,
                'total_minutes_practiced': 0,
                'streak_days': 0,
                'favorite_category': None
            }
        
        conn.close()
        return {
            'total_sessions_completed': progress[2],
            'total_minutes_practiced': progress[3],
            'streak_days': progress[4],
            'favorite_category': progress[6]
        }
    
    def get_user_session_history(self, user_id, limit=10):
        """Get user's session history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT us.*, s.title, s.duration_minutes, s.category
            FROM user_sessions us
            JOIN sessions s ON us.session_id = s.id
            WHERE us.user_id = ?
            ORDER BY us.started_at DESC
            LIMIT ?
        ''', (user_id, limit))
        
        history = cursor.fetchall()
        conn.close()
        
        return [self._format_user_session(session) for session in history]
    
    def _format_session(self, session):
        """Format session data for API response"""
        if not session:
            return None
            
        return {
            'id': session[0],
            'title': session[1],
            'description': session[2],
            'duration': f"{session[3]} min",
            'duration_minutes': session[3],
            'category': session[4].lower(),
            'difficulty': session[5],
            'instructor': session[6],
            'image': session[7],
            'audio': session[8],
            'video': session[9],
            'content_type': session[10],
            'plays': session[11],
            'rating': session[12],
            'tags': session[13].split(',') if session[13] else []
        }
    
    def _format_user_session(self, session):
        """Format user session data for API response"""
        return {
            'id': session[0],
            'session_id': session[2],
            'started_at': session[3],
            'completed_at': session[4],
            'progress_seconds': session[5],
            'is_completed': bool(session[6]),
            'rating': session[7],
            'notes': session[8],
            'session_title': session[9],
            'duration_minutes': session[10],
            'category': session[11]
        }