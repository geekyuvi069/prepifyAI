import sqlite3
import hashlib
import json
from datetime import datetime

class Database:
    def __init__(self, db_name='prepify.db'):
        self.db_name = db_name
        self.init_db()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT,
                points INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Learning modules table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS modules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                content TEXT NOT NULL,
                order_index INTEGER
            )
        ''')
        
        # Quizzes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quizzes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_id INTEGER,
                title TEXT NOT NULL,
                questions TEXT NOT NULL,
                points INTEGER DEFAULT 10,
                FOREIGN KEY (module_id) REFERENCES modules (id)
            )
        ''')
        
        # Coding challenges table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS challenges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                starter_code TEXT,
                test_cases TEXT NOT NULL,
                hints TEXT,
                points INTEGER DEFAULT 20
            )
        ''')
        
        # User progress table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                module_id INTEGER,
                completed BOOLEAN DEFAULT 0,
                completed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (module_id) REFERENCES modules (id),
                UNIQUE(user_id, module_id)
            )
        ''')
        
        # Quiz attempts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quiz_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                quiz_id INTEGER,
                score INTEGER,
                total_questions INTEGER,
                attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (quiz_id) REFERENCES quizzes (id)
            )
        ''')
        
        # Challenge submissions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS challenge_submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                challenge_id INTEGER,
                code TEXT NOT NULL,
                status TEXT,
                passed_tests INTEGER,
                total_tests INTEGER,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (challenge_id) REFERENCES challenges (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # User methods
    def create_user(self, username, email, password, full_name):
        conn = self.get_connection()
        cursor = conn.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            cursor.execute('''
                INSERT INTO users (username, email, password, full_name)
                VALUES (?, ?, ?, ?)
            ''', (username, email, hashed_password, full_name))
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            conn.close()
            return None
    
    def authenticate_user(self, username, password):
        conn = self.get_connection()
        cursor = conn.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute('''
            SELECT * FROM users WHERE username = ? AND password = ?
        ''', (username, hashed_password))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None
    
    def get_user(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None
    
    def update_user_points(self, user_id, points):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET points = points + ? WHERE id = ?
        ''', (points, user_id))
        conn.commit()
        conn.close()
    
    # Module methods
    def add_module(self, title, category, difficulty, content, order_index):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO modules (title, category, difficulty, content, order_index)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, category, difficulty, content, order_index))
        conn.commit()
        module_id = cursor.lastrowid
        conn.close()
        return module_id
    
    def get_all_modules(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM modules ORDER BY order_index')
        modules = cursor.fetchall()
        conn.close()
        return [dict(module) for module in modules]
    
    def get_module(self, module_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM modules WHERE id = ?', (module_id,))
        module = cursor.fetchone()
        conn.close()
        return dict(module) if module else None
    
    # Quiz methods
    def add_quiz(self, module_id, title, questions, points):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO quizzes (module_id, title, questions, points)
            VALUES (?, ?, ?, ?)
        ''', (module_id, title, json.dumps(questions), points))
        conn.commit()
        quiz_id = cursor.lastrowid
        conn.close()
        return quiz_id
    
    def get_quiz(self, quiz_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM quizzes WHERE id = ?', (quiz_id,))
        quiz = cursor.fetchone()
        conn.close()
        if quiz:
            quiz_dict = dict(quiz)
            quiz_dict['questions'] = json.loads(quiz_dict['questions'])
            return quiz_dict
        return None
    
    def get_module_quiz(self, module_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM quizzes WHERE module_id = ?', (module_id,))
        quiz = cursor.fetchone()
        conn.close()
        if quiz:
            quiz_dict = dict(quiz)
            quiz_dict['questions'] = json.loads(quiz_dict['questions'])
            return quiz_dict
        return None
    
    def record_quiz_attempt(self, user_id, quiz_id, score, total_questions):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO quiz_attempts (user_id, quiz_id, score, total_questions)
            VALUES (?, ?, ?, ?)
        ''', (user_id, quiz_id, score, total_questions))
        conn.commit()
        conn.close()
    
    # Challenge methods
    def add_challenge(self, title, description, difficulty, starter_code, test_cases, hints, points):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO challenges (title, description, difficulty, starter_code, test_cases, hints, points)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, description, difficulty, starter_code, json.dumps(test_cases), hints, points))
        conn.commit()
        challenge_id = cursor.lastrowid
        conn.close()
        return challenge_id
    
    def get_all_challenges(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM challenges')
        challenges = cursor.fetchall()
        conn.close()
        result = []
        for challenge in challenges:
            challenge_dict = dict(challenge)
            challenge_dict['test_cases'] = json.loads(challenge_dict['test_cases'])
            result.append(challenge_dict)
        return result
    
    def get_challenge(self, challenge_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM challenges WHERE id = ?', (challenge_id,))
        challenge = cursor.fetchone()
        conn.close()
        if challenge:
            challenge_dict = dict(challenge)
            challenge_dict['test_cases'] = json.loads(challenge_dict['test_cases'])
            return challenge_dict
        return None
    
    def record_submission(self, user_id, challenge_id, code, status, passed_tests, total_tests):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO challenge_submissions (user_id, challenge_id, code, status, passed_tests, total_tests)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, challenge_id, code, status, passed_tests, total_tests))
        conn.commit()
        conn.close()
    
    # Progress methods
    def mark_module_complete(self, user_id, module_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO user_progress (user_id, module_id, completed, completed_at)
            VALUES (?, ?, 1, ?)
        ''', (user_id, module_id, datetime.now()))
        conn.commit()
        conn.close()
    
    def get_user_progress(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM user_progress WHERE user_id = ?
        ''', (user_id,))
        progress = cursor.fetchall()
        conn.close()
        return [dict(p) for p in progress]
    
    def get_user_stats(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Completed modules
        cursor.execute('''
            SELECT COUNT(*) as completed_modules FROM user_progress 
            WHERE user_id = ? AND completed = 1
        ''', (user_id,))
        completed_modules = cursor.fetchone()['completed_modules']
        
        # Quiz attempts
        cursor.execute('''
            SELECT COUNT(*) as quiz_count, AVG(score * 100.0 / total_questions) as avg_score
            FROM quiz_attempts WHERE user_id = ?
        ''', (user_id,))
        quiz_stats = cursor.fetchone()
        
        # Challenge submissions
        cursor.execute('''
            SELECT COUNT(*) as total_submissions,
                   SUM(CASE WHEN status = 'passed' THEN 1 ELSE 0 END) as passed_challenges
            FROM challenge_submissions WHERE user_id = ?
        ''', (user_id,))
        challenge_stats = cursor.fetchone()
        
        conn.close()
        
        return {
            'completed_modules': completed_modules,
            'quiz_attempts': quiz_stats['quiz_count'] or 0,
            'avg_quiz_score': round(quiz_stats['avg_score'] or 0, 2),
            'total_submissions': challenge_stats['total_submissions'] or 0,
            'passed_challenges': challenge_stats['passed_challenges'] or 0
        }
    
    # Leaderboard methods
    def get_leaderboard(self, limit=10):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, username, full_name, points FROM users
            ORDER BY points DESC LIMIT ?
        ''', (limit,))
        leaderboard = cursor.fetchall()
        conn.close()
        return [dict(user) for user in leaderboard]
