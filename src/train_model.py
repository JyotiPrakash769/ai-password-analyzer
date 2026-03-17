import pandas as pd
import numpy as np
import os
import joblib
import random
import string
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from src.feature_extractor import extract_features

# Ensure the model directory exists relative to the project root
os.makedirs('model', exist_ok=True)
MODEL_PATH = 'model/rf_model.joblib'

def load_dataset():
    """
    Simulates a dataset loader.
    For this beginner-friendly project, we generate a synthetic dataset of 
    passwords with ground truth labels ('weak', 'medium', 'strong').
    In real life, you might read this from a sql database or pd.read_csv().
    """
    print("Generating synthetic dataset...")
    data = []
    
    # Class 1: Generate weak passwords (mostly short, lowercase, or simple)
    for _ in range(500):
        length = random.randint(3, 6)
        pwd = ''.join(random.choices(string.ascii_lowercase, k=length))
        data.append((pwd, 'weak'))
        
    # Class 2: Generate medium passwords (longer, mixed case, some numbers)
    for _ in range(500):
        length = random.randint(7, 10)
        pwd = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        data.append((pwd, 'medium'))
        
    # Class 3: Generate strong passwords (long, mixed case, numbers, special characters)
    for _ in range(500):
        length = random.randint(11, 16)
        pwd = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))
        data.append((pwd, 'strong'))
        
    # Create a pandas DataFrame
    df = pd.DataFrame(data, columns=['password', 'strength'])
    
    # Shuffle the dataset so the classes are mixed
    df = df.sample(frac=1).reset_index(drop=True)
    return df

def train_pipeline():
    """
    End-to-end training pipeline:
    1. Loads data.
    2. Extracts engineered features using pandas & numpy.
    3. Splits data into training and testing sets.
    4. Trains a scikit-learn classifier.
    5. Evaluates and saves the model using joblib.
    """
    df = load_dataset()
    
    print("Extracting features using pandas and numpy...")
    X = extract_features(df['password'])  # X represents our features DataFrame
    y = df['strength']                    # y represents our target labels
    
    # Split the dataset: 80% for training, 20% for testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Classifier...")
    # Initialize the Scikit-learn Random Forest model
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    print("Evaluating Model:")
    # Create predictions using the test split
    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    # Save the trained model to disk
    print(f"Saving model to {MODEL_PATH}...")
    joblib.dump(clf, MODEL_PATH)
    print("Training pipeline completed successfully.")

if __name__ == "__main__":
    train_pipeline()
