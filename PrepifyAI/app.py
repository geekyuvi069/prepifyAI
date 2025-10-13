from flask import Flask, request, jsonify, session, render_template
from flask_cors import CORS
from database import Database
import os
from openai import OpenAI
import sys
import io
import traceback
from contextlib import redirect_stdout, redirect_stderr

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')
CORS(app)

db = Database()

# the newest OpenAI model is "gpt-5" which was released August 7, 2025.
# do not change this unless explicitly requested by the user
openai_client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    user_id = db.create_user(
        data['username'],
        data['email'],
        data['password'],
        data['full_name']
    )
    if user_id:
        session['user_id'] = user_id
        return jsonify({'success': True, 'user_id': user_id})
    return jsonify({'success': False, 'error': 'Username or email already exists'}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = db.authenticate_user(data['username'], data['password'])
    if user:
        session['user_id'] = user['id']
        # Return only safe user data (exclude password hash)
        safe_user = {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'full_name': user['full_name'],
            'points': user['points']
        }
        return jsonify({'success': True, 'user': safe_user})
    return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'success': True})

@app.route('/api/user', methods=['GET'])
def get_user():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    user = db.get_user(session['user_id'])
    # Return only safe user data (exclude password hash)
    if user:
        safe_user = {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'full_name': user['full_name'],
            'points': user['points']
        }
        return jsonify(safe_user)
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/modules', methods=['GET'])
def get_modules():
    modules = db.get_all_modules()
    return jsonify(modules)

@app.route('/api/modules/<int:module_id>', methods=['GET'])
def get_module(module_id):
    module = db.get_module(module_id)
    if module:
        return jsonify(module)
    return jsonify({'error': 'Module not found'}), 404

@app.route('/api/modules/<int:module_id>/complete', methods=['POST'])
def complete_module(module_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    db.mark_module_complete(session['user_id'], module_id)
    db.update_user_points(session['user_id'], 5)
    return jsonify({'success': True})

@app.route('/api/quiz/<int:module_id>', methods=['GET'])
def get_quiz(module_id):
    quiz = db.get_module_quiz(module_id)
    if quiz:
        return jsonify(quiz)
    return jsonify({'error': 'Quiz not found'}), 404

@app.route('/api/quiz/submit', methods=['POST'])
def submit_quiz():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    quiz_id = data['quiz_id']
    answers = data['answers']
    
    quiz = db.get_quiz(quiz_id)
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404
    
    score = 0
    total = len(quiz['questions'])
    results = []
    
    for i, question in enumerate(quiz['questions']):
        user_answer = answers.get(str(i))
        correct = user_answer == question['correct']
        if correct:
            score += 1
        results.append({
            'question': question['question'],
            'correct': correct,
            'user_answer': user_answer,
            'correct_answer': question['correct']
        })
    
    db.record_quiz_attempt(session['user_id'], quiz_id, score, total)
    
    points_earned = int((score / total) * quiz['points'])
    db.update_user_points(session['user_id'], points_earned)
    
    return jsonify({
        'score': score,
        'total': total,
        'percentage': round((score / total) * 100, 2),
        'points_earned': points_earned,
        'results': results
    })

@app.route('/api/challenges', methods=['GET'])
def get_challenges():
    challenges = db.get_all_challenges()
    # Don't send test cases to frontend for security
    for challenge in challenges:
        challenge.pop('test_cases', None)
    return jsonify(challenges)

@app.route('/api/challenges/<int:challenge_id>', methods=['GET'])
def get_challenge(challenge_id):
    challenge = db.get_challenge(challenge_id)
    if challenge:
        # Don't send test cases to frontend
        challenge.pop('test_cases', None)
        return jsonify(challenge)
    return jsonify({'error': 'Challenge not found'}), 404

@app.route('/api/challenges/<int:challenge_id>/submit', methods=['POST'])
def submit_challenge(challenge_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    code = data['code']
    
    challenge = db.get_challenge(challenge_id)
    if not challenge:
        return jsonify({'error': 'Challenge not found'}), 404
    
    # Execute code with test cases
    result = execute_code(code, challenge['test_cases'])
    
    # Record submission
    db.record_submission(
        session['user_id'],
        challenge_id,
        code,
        result['status'],
        result['passed'],
        result['total']
    )
    
    # Award points if all tests passed
    if result['status'] == 'passed':
        db.update_user_points(session['user_id'], challenge['points'])
    
    return jsonify(result)

def execute_code(code, test_cases):
    """Execute Python code with test cases in a restricted sandbox"""
    import signal
    import math
    import random
    
    # Safe modules whitelist for imports
    SAFE_MODULES = {'math', 'random', 'itertools', 'collections', 'functools'}
    
    # Custom import function that only allows whitelisted modules
    def safe_import(name, *args, **kwargs):
        if name not in SAFE_MODULES:
            raise ImportError(f"Import of '{name}' is not allowed. Only {SAFE_MODULES} are permitted.")
        return __import__(name, *args, **kwargs)
    
    # Restricted builtins - only allow safe functions
    # Note: This is a basic sandbox for educational use only
    # Block introspection methods that could access dangerous modules
    safe_builtins = {
        'abs': abs,
        'all': all,
        'any': any,
        'bool': bool,
        'dict': dict,
        'enumerate': enumerate,
        'float': float,
        'int': int,
        'len': len,
        'list': list,
        'max': max,
        'min': min,
        'pow': pow,
        'print': print,
        'range': range,
        'round': round,
        'set': set,
        'sorted': sorted,
        'str': str,
        'sum': sum,
        'tuple': tuple,
        'zip': zip,
        '__import__': safe_import,  # Restricted import with whitelist
        # Pre-import safe modules
        'math': math,
        'random': random,
        # Explicitly exclude: object, type, vars, dir, getattr, setattr, delattr, hasattr
        # to prevent introspection attacks
    }
    
    passed = 0
    total = len(test_cases)
    test_results = []
    
    for test_case in test_cases:
        try:
            # Timeout handler
            def timeout_handler(signum, frame):
                raise TimeoutError("Code execution timeout (5 seconds)")
            
            # Set 5 second timeout
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(5)
            
            # Create restricted execution environment with limited builtins
            exec_globals = {
                '__builtins__': safe_builtins,
                '__name__': '__main__',
                '__doc__': None
            }
            
            # Execute user code with restrictions
            exec(code, exec_globals)
            
            # Capture output
            output_buffer = io.StringIO()
            
            with redirect_stdout(output_buffer):
                # Execute test case
                exec(test_case['input'], exec_globals)
                output = output_buffer.getvalue().strip()
            
            # Cancel timeout
            signal.alarm(0)
            
            # Check if output matches expected
            expected = str(test_case['expected']).strip()
            actual = output
            
            if actual == expected:
                passed += 1
                test_results.append({
                    'input': test_case.get('description', 'Test case'),
                    'expected': expected,
                    'actual': actual,
                    'passed': True
                })
            else:
                test_results.append({
                    'input': test_case.get('description', 'Test case'),
                    'expected': expected,
                    'actual': actual,
                    'passed': False
                })
        except TimeoutError as e:
            signal.alarm(0)
            test_results.append({
                'input': test_case.get('description', 'Test case'),
                'error': 'Execution timeout (max 5 seconds)',
                'passed': False
            })
        except Exception as e:
            signal.alarm(0)
            test_results.append({
                'input': test_case.get('description', 'Test case'),
                'error': str(e),
                'passed': False
            })
    
    status = 'passed' if passed == total else 'failed'
    
    return {
        'status': status,
        'passed': passed,
        'total': total,
        'test_results': test_results
    }

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    user_message = data.get('message', '')
    
    try:
        # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
        # do not change this unless explicitly requested by the user
        response = openai_client.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant specialized in Machine Learning, Data Science, and Python programming. Help students understand ML concepts, debug code, and prepare for technical interviews. Provide clear explanations with examples when appropriate."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_completion_tokens=1000
        )
        
        bot_response = response.choices[0].message.content
        return jsonify({'response': bot_response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/progress', methods=['GET'])
def get_progress():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    stats = db.get_user_stats(session['user_id'])
    progress = db.get_user_progress(session['user_id'])
    
    return jsonify({
        'stats': stats,
        'progress': progress
    })

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    leaderboard = db.get_leaderboard(limit=10)
    return jsonify(leaderboard)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
