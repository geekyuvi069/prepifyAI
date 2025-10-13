from database import Database

def seed_database():
    db = Database()
    
    # Add learning modules
    modules_data = [
        {
            'title': 'Introduction to Machine Learning',
            'category': 'Supervised Learning',
            'difficulty': 'Beginner',
            'content': '''
                <h2>What is Machine Learning?</h2>
                <p>Machine Learning is a subset of Artificial Intelligence that enables computers to learn from data without being explicitly programmed.</p>
                
                <h3>Key Concepts:</h3>
                <ul>
                    <li><strong>Training Data:</strong> The dataset used to train the model</li>
                    <li><strong>Features:</strong> Input variables used to make predictions</li>
                    <li><strong>Labels:</strong> The output or target variable we want to predict</li>
                    <li><strong>Model:</strong> The algorithm that learns patterns from data</li>
                </ul>
                
                <h3>Types of Machine Learning:</h3>
                <ol>
                    <li><strong>Supervised Learning:</strong> Learning from labeled data</li>
                    <li><strong>Unsupervised Learning:</strong> Finding patterns in unlabeled data</li>
                    <li><strong>Reinforcement Learning:</strong> Learning through trial and error</li>
                </ol>
                
                <h3>Example Use Cases:</h3>
                <p>Email spam detection, Image recognition, Recommendation systems, Fraud detection</p>
            ''',
            'order_index': 1
        },
        {
            'title': 'Linear Regression',
            'category': 'Supervised Learning',
            'difficulty': 'Beginner',
            'content': '''
                <h2>Linear Regression</h2>
                <p>Linear Regression is a fundamental supervised learning algorithm used for predicting continuous values.</p>
                
                <h3>The Linear Equation:</h3>
                <p><code>y = mx + b</code></p>
                <p>Where: y is the predicted value, m is the slope, x is the input feature, b is the y-intercept</p>
                
                <h3>How It Works:</h3>
                <ol>
                    <li>Start with random values for m and b</li>
                    <li>Calculate predictions for all data points</li>
                    <li>Measure the error (difference between predicted and actual values)</li>
                    <li>Adjust m and b to minimize error</li>
                    <li>Repeat until error is minimized</li>
                </ol>
                
                <h3>Python Example:</h3>
                <pre><code>from sklearn.linear_model import LinearRegression
import numpy as np

# Sample data
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])

# Create and train model
model = LinearRegression()
model.fit(X, y)

# Make predictions
prediction = model.predict([[6]])
print(f"Prediction for x=6: {prediction[0]}")</code></pre>
            ''',
            'order_index': 2
        },
        {
            'title': 'Classification Algorithms',
            'category': 'Supervised Learning',
            'difficulty': 'Intermediate',
            'content': '''
                <h2>Classification in Machine Learning</h2>
                <p>Classification is the task of predicting discrete categories or classes.</p>
                
                <h3>Popular Classification Algorithms:</h3>
                <ul>
                    <li><strong>Logistic Regression:</strong> Despite the name, it's used for classification</li>
                    <li><strong>Decision Trees:</strong> Tree-like model of decisions</li>
                    <li><strong>Random Forest:</strong> Ensemble of decision trees</li>
                    <li><strong>Support Vector Machines (SVM):</strong> Finds optimal decision boundary</li>
                    <li><strong>K-Nearest Neighbors (KNN):</strong> Classifies based on nearest neighbors</li>
                </ul>
                
                <h3>Logistic Regression Example:</h3>
                <pre><code>from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Binary classification example
X = [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6]]
y = [0, 0, 1, 1, 1]  # Binary labels

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LogisticRegression()
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f"Accuracy: {accuracy}")</code></pre>
                
                <h3>Evaluation Metrics:</h3>
                <p>Accuracy, Precision, Recall, F1-Score, Confusion Matrix</p>
            ''',
            'order_index': 3
        },
        {
            'title': 'Neural Networks Basics',
            'category': 'Deep Learning',
            'difficulty': 'Advanced',
            'content': '''
                <h2>Introduction to Neural Networks</h2>
                <p>Neural Networks are computing systems inspired by biological neural networks in animal brains.</p>
                
                <h3>Key Components:</h3>
                <ul>
                    <li><strong>Neurons:</strong> Basic computational units</li>
                    <li><strong>Layers:</strong> Input layer, Hidden layers, Output layer</li>
                    <li><strong>Weights:</strong> Parameters that get adjusted during training</li>
                    <li><strong>Activation Functions:</strong> ReLU, Sigmoid, Tanh</li>
                </ul>
                
                <h3>Forward Propagation:</h3>
                <ol>
                    <li>Input data enters the network through input layer</li>
                    <li>Each neuron computes weighted sum of inputs</li>
                    <li>Apply activation function to the sum</li>
                    <li>Pass result to next layer</li>
                    <li>Final layer produces prediction</li>
                </ol>
                
                <h3>Simple Neural Network with PyTorch:</h3>
                <pre><code>import torch
import torch.nn as nn

class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.layer1 = nn.Linear(10, 5)
        self.layer2 = nn.Linear(5, 1)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.layer2(x)
        return x

model = SimpleNN()
print(model)</code></pre>
            ''',
            'order_index': 4
        },
        {
            'title': 'Clustering Algorithms',
            'category': 'Unsupervised Learning',
            'difficulty': 'Intermediate',
            'content': '''
                <h2>Clustering in Machine Learning</h2>
                <p>Clustering is the task of grouping similar data points together without labeled data.</p>
                
                <h3>Popular Clustering Algorithms:</h3>
                <ul>
                    <li><strong>K-Means:</strong> Partitions data into K clusters</li>
                    <li><strong>Hierarchical Clustering:</strong> Creates tree of clusters</li>
                    <li><strong>DBSCAN:</strong> Density-based clustering</li>
                </ul>
                
                <h3>K-Means Algorithm:</h3>
                <ol>
                    <li>Choose number of clusters (K)</li>
                    <li>Initialize K random centroids</li>
                    <li>Assign each point to nearest centroid</li>
                    <li>Recalculate centroids as mean of assigned points</li>
                    <li>Repeat steps 3-4 until convergence</li>
                </ol>
                
                <h3>K-Means Example:</h3>
                <pre><code>from sklearn.cluster import KMeans
import numpy as np

# Sample data
X = np.array([[1, 2], [1.5, 1.8], [5, 8], [8, 8], [1, 0.6], [9, 11]])

# Create K-Means model with 2 clusters
kmeans = KMeans(n_clusters=2, random_state=0)
kmeans.fit(X)

# Get cluster labels
labels = kmeans.labels_
centroids = kmeans.cluster_centers_

print(f"Labels: {labels}")
print(f"Centroids: {centroids}")</code></pre>
            ''',
            'order_index': 5
        }
    ]
    
    module_ids = []
    for module in modules_data:
        module_id = db.add_module(**module)
        module_ids.append(module_id)
        print(f"Added module: {module['title']} (ID: {module_id})")
    
    # Add quizzes for each module
    quizzes_data = [
        {
            'module_id': module_ids[0],
            'title': 'ML Fundamentals Quiz',
            'questions': [
                {
                    'question': 'What is the main goal of Machine Learning?',
                    'options': ['To program computers explicitly', 'To enable computers to learn from data', 'To replace human intelligence', 'To create databases'],
                    'correct': 1
                },
                {
                    'question': 'Which type of learning uses labeled data?',
                    'options': ['Unsupervised Learning', 'Supervised Learning', 'Reinforcement Learning', 'Transfer Learning'],
                    'correct': 1
                },
                {
                    'question': 'What are features in ML?',
                    'options': ['Output variables', 'Input variables for predictions', 'Error metrics', 'Training algorithms'],
                    'correct': 1
                }
            ],
            'points': 10
        },
        {
            'module_id': module_ids[1],
            'title': 'Linear Regression Quiz',
            'questions': [
                {
                    'question': 'What does Linear Regression predict?',
                    'options': ['Categories', 'Continuous values', 'Clusters', 'Text labels'],
                    'correct': 1
                },
                {
                    'question': 'In y = mx + b, what does "m" represent?',
                    'options': ['Y-intercept', 'Slope', 'Error', 'Mean'],
                    'correct': 1
                },
                {
                    'question': 'What is the goal of training a linear regression model?',
                    'options': ['Maximize error', 'Minimize error', 'Find random values', 'Create more features'],
                    'correct': 1
                }
            ],
            'points': 10
        },
        {
            'module_id': module_ids[2],
            'title': 'Classification Quiz',
            'questions': [
                {
                    'question': 'What does classification predict?',
                    'options': ['Continuous numbers', 'Discrete categories', 'Probabilities only', 'Text strings'],
                    'correct': 1
                },
                {
                    'question': 'Which algorithm creates a tree-like model?',
                    'options': ['Logistic Regression', 'Decision Tree', 'Linear Regression', 'K-Means'],
                    'correct': 1
                },
                {
                    'question': 'What is a confusion matrix used for?',
                    'options': ['Training models', 'Evaluating classification performance', 'Feature selection', 'Data preprocessing'],
                    'correct': 1
                }
            ],
            'points': 10
        }
    ]
    
    for quiz in quizzes_data:
        quiz_id = db.add_quiz(**quiz)
        print(f"Added quiz: {quiz['title']} (ID: {quiz_id})")
    
    # Add coding challenges
    challenges_data = [
        {
            'title': 'Calculate Mean of a List',
            'description': 'Write a function called `calculate_mean` that takes a list of numbers and returns their mean (average).',
            'difficulty': 'Easy',
            'starter_code': '''def calculate_mean(numbers):
    # Your code here
    pass

# Test your function
print(calculate_mean([1, 2, 3, 4, 5]))''',
            'test_cases': [
                {
                    'description': 'Test 1: [1, 2, 3, 4, 5]',
                    'input': 'print(calculate_mean([1, 2, 3, 4, 5]))',
                    'expected': '3.0'
                },
                {
                    'description': 'Test 2: [10, 20, 30]',
                    'input': 'print(calculate_mean([10, 20, 30]))',
                    'expected': '20.0'
                }
            ],
            'hints': 'Sum all numbers and divide by the count of numbers.',
            'points': 20
        },
        {
            'title': 'Euclidean Distance',
            'description': 'Implement a function `euclidean_distance` that calculates the Euclidean distance between two points in 2D space.',
            'difficulty': 'Easy',
            'starter_code': '''def euclidean_distance(point1, point2):
    # Your code here
    # Formula: sqrt((x2-x1)^2 + (y2-y1)^2)
    pass

# Test your function
print(euclidean_distance([0, 0], [3, 4]))''',
            'test_cases': [
                {
                    'description': 'Test 1: (0,0) to (3,4)',
                    'input': 'print(euclidean_distance([0, 0], [3, 4]))',
                    'expected': '5.0'
                },
                {
                    'description': 'Test 2: (1,1) to (4,5)',
                    'input': 'print(euclidean_distance([1, 1], [4, 5]))',
                    'expected': '5.0'
                }
            ],
            'hints': 'Use the formula: sqrt((x2-x1)^2 + (y2-y1)^2). Import math module for sqrt.',
            'points': 25
        },
        {
            'title': 'Normalize Data',
            'description': 'Create a function `normalize` that performs min-max normalization on a list of numbers to scale them between 0 and 1.',
            'difficulty': 'Medium',
            'starter_code': '''def normalize(data):
    # Your code here
    # Formula: (x - min) / (max - min)
    pass

# Test your function
print(normalize([1, 2, 3, 4, 5]))''',
            'test_cases': [
                {
                    'description': 'Test 1: [1, 2, 3, 4, 5]',
                    'input': 'print(normalize([1, 2, 3, 4, 5]))',
                    'expected': '[0.0, 0.25, 0.5, 0.75, 1.0]'
                },
                {
                    'description': 'Test 2: [10, 20, 30, 40]',
                    'input': 'print(normalize([10, 20, 30, 40]))',
                    'expected': '[0.0, 0.3333333333333333, 0.6666666666666666, 1.0]'
                }
            ],
            'hints': 'Find min and max values, then apply formula (x - min) / (max - min) to each element.',
            'points': 30
        },
        {
            'title': 'Train-Test Split',
            'description': 'Implement a function `train_test_split_custom` that splits data into training and testing sets given a test_size ratio.',
            'difficulty': 'Medium',
            'starter_code': '''def train_test_split_custom(data, test_size=0.2):
    # Your code here
    # Return (train_data, test_data)
    pass

# Test your function
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
train, test = train_test_split_custom(data, 0.2)
print(len(train), len(test))''',
            'test_cases': [
                {
                    'description': 'Test 1: Split 10 items with 20% test size',
                    'input': 'data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]; train, test = train_test_split_custom(data, 0.2); print(len(train), len(test))',
                    'expected': '8 2'
                }
            ],
            'hints': 'Calculate split index as int(len(data) * (1 - test_size)), then slice the list.',
            'points': 35
        },
        {
            'title': 'Accuracy Score',
            'description': 'Write a function `accuracy_score` that calculates the accuracy of predictions compared to actual labels.',
            'difficulty': 'Easy',
            'starter_code': '''def accuracy_score(y_true, y_pred):
    # Your code here
    # Accuracy = (correct predictions) / (total predictions)
    pass

# Test your function
y_true = [1, 0, 1, 1, 0, 1]
y_pred = [1, 0, 1, 0, 0, 1]
print(accuracy_score(y_true, y_pred))''',
            'test_cases': [
                {
                    'description': 'Test 1: 5 out of 6 correct',
                    'input': 'y_true = [1, 0, 1, 1, 0, 1]; y_pred = [1, 0, 1, 0, 0, 1]; print(accuracy_score(y_true, y_pred))',
                    'expected': '0.8333333333333334'
                }
            ],
            'hints': 'Count how many predictions match the actual labels and divide by total count.',
            'points': 20
        }
    ]
    
    for challenge in challenges_data:
        challenge_id = db.add_challenge(**challenge)
        print(f"Added challenge: {challenge['title']} (ID: {challenge_id})")
    
    print("\nDatabase seeded successfully!")

if __name__ == '__main__':
    seed_database()
