// Global state
let currentUser = null;
let currentModule = null;
let currentQuiz = null;
let currentChallenge = null;

// Check if user is authenticated
async function checkAuth() {
    try {
        const response = await fetch('/api/user');
        if (response.ok) {
            currentUser = await response.json();
            showAuthenticatedUI();
            return true;
        }
    } catch (error) {
        console.error('Auth check failed:', error);
    }
    showUnauthenticatedUI();
    return false;
}

// UI State Management
function showAuthenticatedUI() {
    document.getElementById('auth-buttons').classList.add('hidden');
    document.getElementById('nav-menu').classList.remove('hidden');
    document.getElementById('landing-page').classList.add('hidden');
    showPage('dashboard');
    loadDashboard();
}

function showUnauthenticatedUI() {
    document.getElementById('auth-buttons').classList.remove('hidden');
    document.getElementById('nav-menu').classList.add('hidden');
    document.getElementById('landing-page').classList.remove('hidden');
}

function showPage(page) {
    const pages = ['landing-page', 'learn-page', 'code-page', 'chatbot-page', 'dashboard-page', 'leaderboard-page'];
    pages.forEach(p => {
        document.getElementById(p).classList.add('hidden');
    });
    
    const pageMap = {
        'home': 'landing-page',
        'learn': 'learn-page',
        'code': 'code-page',
        'chatbot': 'chatbot-page',
        'dashboard': 'dashboard-page',
        'leaderboard': 'leaderboard-page'
    };
    
    const pageId = pageMap[page] || 'landing-page';
    document.getElementById(pageId).classList.remove('hidden');
    
    // Load data for specific pages
    if (page === 'learn') loadModules();
    if (page === 'code') loadChallenges();
    if (page === 'dashboard') loadDashboard();
    if (page === 'leaderboard') loadLeaderboard();
}

// Authentication
function showAuthModal(type) {
    document.getElementById('auth-modal').classList.remove('hidden');
    if (type === 'login') {
        document.getElementById('auth-modal-title').textContent = 'Login';
        document.getElementById('login-form').classList.remove('hidden');
        document.getElementById('register-form').classList.add('hidden');
    } else {
        document.getElementById('auth-modal-title').textContent = 'Sign Up';
        document.getElementById('login-form').classList.add('hidden');
        document.getElementById('register-form').classList.remove('hidden');
    }
}

function closeAuthModal() {
    document.getElementById('auth-modal').classList.add('hidden');
}

async function login() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password})
        });
        
        const data = await response.json();
        if (data.success) {
            currentUser = data.user;
            closeAuthModal();
            showAuthenticatedUI();
        } else {
            alert(data.error);
        }
    } catch (error) {
        alert('Login failed: ' + error.message);
    }
}

async function register() {
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const full_name = document.getElementById('register-fullname').value;
    const password = document.getElementById('register-password').value;
    
    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, email, full_name, password})
        });
        
        const data = await response.json();
        if (data.success) {
            alert('Registration successful! Please login.');
            showAuthModal('login');
        } else {
            alert(data.error);
        }
    } catch (error) {
        alert('Registration failed: ' + error.message);
    }
}

async function logout() {
    await fetch('/api/logout', {method: 'POST'});
    currentUser = null;
    showUnauthenticatedUI();
}

// Learning Modules
async function loadModules() {
    try {
        const response = await fetch('/api/modules');
        const modules = await response.json();
        
        const container = document.getElementById('modules-container');
        container.innerHTML = modules.map(module => `
            <div class="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition cursor-pointer" onclick="openModule(${module.id})">
                <span class="inline-block px-3 py-1 rounded text-xs font-semibold mb-2 
                    ${module.difficulty === 'Beginner' ? 'bg-green-200 text-green-800' : 
                      module.difficulty === 'Intermediate' ? 'bg-yellow-200 text-yellow-800' : 
                      'bg-red-200 text-red-800'}">
                    ${module.difficulty}
                </span>
                <h3 class="text-xl font-bold mb-2">${module.title}</h3>
                <p class="text-gray-600 text-sm mb-2">${module.category}</p>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to load modules:', error);
    }
}

async function openModule(moduleId) {
    try {
        const response = await fetch(`/api/modules/${moduleId}`);
        currentModule = await response.json();
        
        document.getElementById('module-title').textContent = currentModule.title;
        document.getElementById('module-content').innerHTML = currentModule.content;
        document.getElementById('module-modal').classList.remove('hidden');
    } catch (error) {
        console.error('Failed to load module:', error);
    }
}

function closeModuleModal() {
    document.getElementById('module-modal').classList.add('hidden');
}

async function completeModule() {
    if (!currentModule) return;
    
    try {
        await fetch(`/api/modules/${currentModule.id}/complete`, {method: 'POST'});
        alert('Module completed! +5 points');
        closeModuleModal();
        loadDashboard();
    } catch (error) {
        console.error('Failed to complete module:', error);
    }
}

async function startQuiz() {
    if (!currentModule) return;
    
    try {
        const response = await fetch(`/api/quiz/${currentModule.id}`);
        currentQuiz = await response.json();
        
        document.getElementById('quiz-title').textContent = currentQuiz.title;
        
        const questionsHTML = currentQuiz.questions.map((q, index) => `
            <div class="mb-6 p-4 bg-gray-50 rounded">
                <p class="font-semibold mb-3">${index + 1}. ${q.question}</p>
                ${q.options.map((option, optIndex) => `
                    <label class="block mb-2 cursor-pointer hover:bg-gray-100 p-2 rounded">
                        <input type="radio" name="question-${index}" value="${optIndex}" class="mr-2">
                        ${option}
                    </label>
                `).join('')}
            </div>
        `).join('');
        
        document.getElementById('quiz-questions').innerHTML = questionsHTML;
        document.getElementById('module-modal').classList.add('hidden');
        document.getElementById('quiz-modal').classList.remove('hidden');
    } catch (error) {
        console.error('Failed to load quiz:', error);
    }
}

async function submitQuiz() {
    if (!currentQuiz) return;
    
    const answers = {};
    currentQuiz.questions.forEach((q, index) => {
        const selected = document.querySelector(`input[name="question-${index}"]:checked`);
        if (selected) {
            answers[index] = parseInt(selected.value);
        }
    });
    
    try {
        const response = await fetch('/api/quiz/submit', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                quiz_id: currentQuiz.id,
                answers: answers
            })
        });
        
        const result = await response.json();
        
        const resultsHTML = `
            <div class="text-center mb-6">
                <p class="text-4xl font-bold mb-2">${result.percentage}%</p>
                <p class="text-xl">Score: ${result.score}/${result.total}</p>
                <p class="text-green-600 font-semibold">+${result.points_earned} points earned!</p>
            </div>
            <div class="space-y-3">
                ${result.results.map(r => `
                    <div class="p-3 rounded ${r.correct ? 'bg-green-50' : 'bg-red-50'}">
                        <p class="font-semibold">${r.question}</p>
                        <p class="text-sm">
                            ${r.correct ? 
                                '<span class="text-green-600">✓ Correct</span>' : 
                                `<span class="text-red-600">✗ Wrong - Correct answer: ${r.correct_answer}</span>`
                            }
                        </p>
                    </div>
                `).join('')}
            </div>
        `;
        
        document.getElementById('quiz-results').innerHTML = resultsHTML;
        document.getElementById('quiz-modal').classList.add('hidden');
        document.getElementById('quiz-result-modal').classList.remove('hidden');
        loadDashboard();
    } catch (error) {
        console.error('Failed to submit quiz:', error);
    }
}

function closeQuizResult() {
    document.getElementById('quiz-result-modal').classList.add('hidden');
}

// Coding Challenges
async function loadChallenges() {
    try {
        const response = await fetch('/api/challenges');
        const challenges = await response.json();
        
        const container = document.getElementById('challenges-list');
        container.innerHTML = challenges.map(challenge => `
            <div class="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition cursor-pointer" onclick="openChallenge(${challenge.id})">
                <div class="flex justify-between items-start">
                    <div class="flex-1">
                        <h3 class="text-xl font-bold mb-2">${challenge.title}</h3>
                        <p class="text-gray-600 mb-2">${challenge.description.substring(0, 100)}...</p>
                    </div>
                    <div class="ml-4">
                        <span class="inline-block px-3 py-1 rounded text-xs font-semibold
                            ${challenge.difficulty === 'Easy' ? 'bg-green-200 text-green-800' : 
                              challenge.difficulty === 'Medium' ? 'bg-yellow-200 text-yellow-800' : 
                              'bg-red-200 text-red-800'}">
                            ${challenge.difficulty}
                        </span>
                        <p class="text-sm text-gray-500 mt-2">${challenge.points} points</p>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to load challenges:', error);
    }
}

async function openChallenge(challengeId) {
    try {
        const response = await fetch(`/api/challenges/${challengeId}`);
        currentChallenge = await response.json();
        
        document.getElementById('challenge-title').textContent = currentChallenge.title;
        document.getElementById('challenge-difficulty').textContent = currentChallenge.difficulty;
        document.getElementById('challenge-difficulty').className = `inline-block px-3 py-1 rounded text-sm font-semibold mt-2
            ${currentChallenge.difficulty === 'Easy' ? 'bg-green-200 text-green-800' : 
              currentChallenge.difficulty === 'Medium' ? 'bg-yellow-200 text-yellow-800' : 
              'bg-red-200 text-red-800'}`;
        
        document.getElementById('challenge-description').textContent = currentChallenge.description;
        document.getElementById('challenge-hints').innerHTML = `<strong>💡 Hints:</strong> ${currentChallenge.hints}`;
        document.getElementById('code-editor').value = currentChallenge.starter_code || '';
        document.getElementById('code-result').innerHTML = '';
        document.getElementById('challenge-modal').classList.remove('hidden');
    } catch (error) {
        console.error('Failed to load challenge:', error);
    }
}

function closeChallengeModal() {
    document.getElementById('challenge-modal').classList.add('hidden');
}

function resetCode() {
    if (currentChallenge) {
        document.getElementById('code-editor').value = currentChallenge.starter_code || '';
        document.getElementById('code-result').innerHTML = '';
    }
}

async function submitCode() {
    if (!currentChallenge) return;
    
    const code = document.getElementById('code-editor').value;
    
    try {
        const response = await fetch(`/api/challenges/${currentChallenge.id}/submit`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({code})
        });
        
        const result = await response.json();
        
        const resultHTML = `
            <div class="p-4 rounded ${result.status === 'passed' ? 'bg-green-100' : 'bg-red-100'}">
                <h4 class="font-bold text-lg mb-2">
                    ${result.status === 'passed' ? '✓ All Tests Passed!' : '✗ Some Tests Failed'}
                </h4>
                <p class="mb-3">Tests Passed: ${result.passed}/${result.total}</p>
                ${result.status === 'passed' ? `<p class="text-green-600 font-semibold">+${currentChallenge.points} points earned!</p>` : ''}
                <div class="mt-4 space-y-2">
                    ${result.test_results.map(test => `
                        <div class="p-2 bg-white rounded text-sm">
                            <p class="font-semibold">${test.input}</p>
                            ${test.error ? 
                                `<p class="text-red-600">Error: ${test.error}</p>` :
                                `<p>Expected: ${test.expected} | Got: ${test.actual} 
                                ${test.passed ? '<span class="text-green-600">✓</span>' : '<span class="text-red-600">✗</span>'}</p>`
                            }
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        
        document.getElementById('code-result').innerHTML = resultHTML;
        if (result.status === 'passed') {
            loadDashboard();
        }
    } catch (error) {
        console.error('Failed to submit code:', error);
    }
}

// AI Chatbot
async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (!message) return;
    
    const chatMessages = document.getElementById('chat-messages');
    
    // Add user message
    chatMessages.innerHTML += `
        <div class="flex justify-end">
            <div class="bg-indigo-600 text-white rounded-lg px-4 py-2 max-w-lg">
                ${message}
            </div>
        </div>
    `;
    
    input.value = '';
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Add loading indicator
    chatMessages.innerHTML += `
        <div id="bot-loading" class="flex justify-start">
            <div class="bg-gray-200 rounded-lg px-4 py-2">
                <i class="fas fa-spinner fa-spin"></i> Thinking...
            </div>
        </div>
    `;
    
    try {
        const response = await fetch('/api/chatbot', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message})
        });
        
        const data = await response.json();
        
        // Remove loading indicator
        const loadingEl = document.getElementById('bot-loading');
        if (loadingEl) loadingEl.remove();
        
        // Add bot response
        chatMessages.innerHTML += `
            <div class="flex justify-start">
                <div class="bg-gray-200 rounded-lg px-4 py-2 max-w-lg">
                    ${data.response ? data.response.replace(/\n/g, '<br>') : 'Error: No response from AI'}
                </div>
            </div>
        `;
        
        chatMessages.scrollTop = chatMessages.scrollHeight;
    } catch (error) {
        const loadingEl = document.getElementById('bot-loading');
        if (loadingEl) loadingEl.remove();
        chatMessages.innerHTML += `
            <div class="flex justify-start">
                <div class="bg-red-200 rounded-lg px-4 py-2 max-w-lg">
                    Error: ${error.message}
                </div>
            </div>
        `;
    }
}

// Allow Enter key to send message
document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.getElementById('chat-input');
    if (chatInput) {
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    }
});

// Dashboard
let progressChart = null;

async function loadDashboard() {
    try {
        const [progressResponse, userResponse] = await Promise.all([
            fetch('/api/progress'),
            fetch('/api/user')
        ]);
        
        const progressData = await progressResponse.json();
        const userData = await userResponse.json();
        
        document.getElementById('total-points').textContent = userData.points;
        document.getElementById('completed-modules').textContent = progressData.stats.completed_modules;
        document.getElementById('avg-quiz-score').textContent = progressData.stats.avg_quiz_score + '%';
        document.getElementById('passed-challenges').textContent = progressData.stats.passed_challenges;
        
        // Update chart
        const ctx = document.getElementById('progress-chart');
        if (ctx) {
            if (progressChart) {
                progressChart.destroy();
            }
            
            progressChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Modules', 'Quizzes', 'Challenges', 'Total Points'],
                    datasets: [{
                        label: 'Your Progress',
                        data: [
                            progressData.stats.completed_modules,
                            progressData.stats.quiz_attempts,
                            progressData.stats.passed_challenges,
                            userData.points
                        ],
                        backgroundColor: [
                            'rgba(34, 197, 94, 0.5)',
                            'rgba(59, 130, 246, 0.5)',
                            'rgba(168, 85, 247, 0.5)',
                            'rgba(99, 102, 241, 0.5)'
                        ],
                        borderColor: [
                            'rgb(34, 197, 94)',
                            'rgb(59, 130, 246)',
                            'rgb(168, 85, 247)',
                            'rgb(99, 102, 241)'
                        ],
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
    } catch (error) {
        console.error('Failed to load dashboard:', error);
    }
}

// Leaderboard
async function loadLeaderboard() {
    try {
        const response = await fetch('/api/leaderboard');
        const leaderboard = await response.json();
        
        const tbody = document.getElementById('leaderboard-body');
        tbody.innerHTML = leaderboard.map((user, index) => `
            <tr class="${index < 3 ? 'bg-yellow-50' : 'hover:bg-gray-50'}">
                <td class="px-6 py-4">
                    ${index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : index + 1}
                </td>
                <td class="px-6 py-4 font-semibold">${user.full_name || 'Anonymous'}</td>
                <td class="px-6 py-4">${user.username}</td>
                <td class="px-6 py-4">
                    <span class="inline-block bg-indigo-100 text-indigo-800 px-3 py-1 rounded font-semibold">
                        ${user.points} pts
                    </span>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Failed to load leaderboard:', error);
    }
}

// Initialize
checkAuth();
