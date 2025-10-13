# Prepify - AI-Based ML Coding and Interview Preparation Platform

## Overview
Prepify is a comprehensive web-based AI-powered platform designed to help college students prepare for placements in Artificial Intelligence and Machine Learning fields. The platform integrates learning, coding practice, and interview readiness into a single intelligent environment with real-time AI assistance.

## Tech Stack
- **Frontend:** HTML5, TailwindCSS, Vanilla JavaScript, Chart.js
- **Backend:** Flask (Python 3.11)
- **Database:** SQLite
- **AI Integration:** OpenAI GPT-5 API
- **Code Execution:** Sandboxed Python execution

## Core Features Implemented

### 1. AI Chatbot Assistant
- 24/7 personal ML and coding assistant powered by OpenAI GPT-5
- Provides concept explanations, code examples, and debugging help
- Context-aware responses specialized for ML, data science, and Python

### 2. Interactive Learning Modules
- 5 comprehensive modules covering:
  - Introduction to Machine Learning
  - Linear Regression
  - Classification Algorithms
  - Neural Networks Basics
  - Clustering Algorithms
- Beginner to Advanced difficulty levels
- Rich HTML content with code examples

### 3. Quiz System
- Concept checkpoints with multiple-choice questions
- Instant scoring and detailed feedback
- Points-based gamification (10 points per quiz)
- Review of correct/incorrect answers

### 4. Coding Challenge Platform
- 5 Python coding challenges:
  - Calculate Mean of a List (Easy - 20 pts)
  - Euclidean Distance (Easy - 25 pts)
  - Normalize Data (Medium - 30 pts)
  - Train-Test Split (Medium - 35 pts)
  - Accuracy Score (Easy - 20 pts)
- Auto-evaluation with test cases
- Real-time code execution feedback
- Hints and starter code provided

### 5. Progress Dashboard
- Real-time statistics tracking:
  - Total points earned
  - Modules completed
  - Average quiz score
  - Challenges passed
- Visual progress chart using Chart.js
- Comprehensive performance overview

### 6. Leaderboard System
- Top 10 rankings by points
- Medal indicators for top 3 performers
- Competitive learning environment

### 7. User Authentication
- Secure registration and login
- Session management
- Password hashing with SHA-256
- User profiles with progress tracking

## Project Structure
```
prepify/
├── app.py                  # Main Flask application
├── database.py            # Database models and queries
├── seed_data.py          # Sample content and data seeding
├── templates/
│   └── index.html        # Single-page application
├── static/
│   └── js/
│       └── app.js        # Frontend JavaScript logic
├── prepify.db            # SQLite database (auto-generated)
└── replit.md             # This documentation
```

## Database Schema

### Tables
1. **users** - User accounts and points
2. **modules** - Learning module content
3. **quizzes** - Quiz questions and answers
4. **challenges** - Coding challenge definitions
5. **user_progress** - Module completion tracking
6. **quiz_attempts** - Quiz submission history
7. **challenge_submissions** - Code submission history

## API Endpoints

### Authentication
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `POST /api/logout` - User logout
- `GET /api/user` - Get current user

### Learning
- `GET /api/modules` - List all modules
- `GET /api/modules/<id>` - Get module details
- `POST /api/modules/<id>/complete` - Mark module complete

### Quizzes
- `GET /api/quiz/<module_id>` - Get quiz for module
- `POST /api/quiz/submit` - Submit quiz answers

### Coding Challenges
- `GET /api/challenges` - List all challenges
- `GET /api/challenges/<id>` - Get challenge details
- `POST /api/challenges/<id>/submit` - Submit code solution

### Progress & Leaderboard
- `GET /api/progress` - Get user progress stats
- `GET /api/leaderboard` - Get top 10 users
- `POST /api/chatbot` - Send message to AI assistant

## Points System
- Module completion: +5 points
- Quiz completion: Variable (based on score and quiz points)
- Challenge completion: 20-35 points (based on difficulty)

## Recent Changes (Oct 13, 2025)
- Initial implementation of all core features
- Database schema created and seeded with sample content
- OpenAI GPT-5 integration for chatbot
- **Code execution sandbox with security measures** (educational use only - see SECURITY.md)
- Complete frontend with TailwindCSS
- Chart.js integration for progress visualization
- Security hardening: password hash protection, whitelisted imports, restricted builtins

## Future Enhancements (Next Phase)
- AI Interview Analyzer with text-based answer evaluation
- Speech-to-text for audio-based interview practice
- Personalized learning recommendations based on weak topics
- Detailed feedback reports with improvement suggestions
- Collaborative features (study groups, peer code review)
- Export functionality for progress reports and certificates

## How to Run
The application is configured to run automatically via Replit workflows:
- Server runs on port 5000
- Access the web interface through the Replit webview
- Database is auto-initialized on first run

## Environment Variables Required
- `OPENAI_API_KEY` - sk-abcdef1234567890abcdef1234567890abcdef12
- `SESSION_SECRET` - Flask session secret (auto-generated in dev)

## Security Notes
- **Password Security**: Hashed using SHA-256, never exposed in API responses
- **Code Execution**: Restricted builtins sandbox with 5-second timeout per test
- **Data Protection**: Test cases hidden from frontend, only safe user data exposed
- **Authentication**: Session-based with secure secret key
- **CORS**: Enabled for API access

### Code Sandbox Security
- Limited to safe built-in functions only (no file I/O, no dangerous imports)
- 5-second execution timeout per test case
- Restricted execution environment (no `open`, `eval`, etc.)
- Note: Educational/development sandbox - see SECURITY.md for production recommendations

## User Workflow
1. Sign up / Login
2. Browse learning modules by difficulty
3. Study module content
4. Take quizzes to test understanding
5. Practice coding challenges
6. Get help from AI assistant
7. Track progress on dashboard
8. Compete on leaderboard
