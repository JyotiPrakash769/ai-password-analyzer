import pandas as pd
import numpy as np
import string
from src.utils import calculate_entropy

def extract_features(passwords):
    """
    Extracts numerical features from a list of passwords for machine learning.
    
    Feature Engineering:
    We convert the raw text of a password into numerical attributes that a machine 
    learning model can learn from. The features are based on common password 
    complexity guidelines.
    
    Features engineered:
    1. length: Total number of characters.
    2. uppercase_count: Number of uppercase letters (A-Z).
    3. lowercase_count: Number of lowercase letters (a-z).
    4. digits_count: Number of numeric characters (0-9).
    5. special_count: Number of special characters (!@#$%^&* etc.).
    6. entropy: Shannon entropy score (randomness).
    
    Returns:
        pd.DataFrame: A pandas DataFrame containing the extracted features.
    """
    features = []
    
    for pwd in passwords:
        if not isinstance(pwd, str):
            pwd = str(pwd)
            
        # 1. Feature: Length
        length = len(pwd)
        
        # 2. Feature: Uppercase count
        upper_count = sum(1 for c in pwd if c.isupper())
        
        # 3. Feature: Lowercase count
        lower_count = sum(1 for c in pwd if c.islower())
        
        # 4. Feature: Digits count
        digit_count = sum(1 for c in pwd if c.isdigit())
        
        # 5. Feature: Special characters count
        special_count = sum(1 for c in pwd if c in string.punctuation)
        
        # 6. Feature: Shannon entropy
        entropy = calculate_entropy(pwd)
        
        # Pack everything neatly into a dictionary
        features.append({
            'length': length,
            'uppercase_count': upper_count,
            'lowercase_count': lower_count,
            'digits_count': digit_count,
            'special_count': special_count,
            'entropy': entropy
        })
        
    # We use pandas DataFrame to easily feed the features into scikit-learn
    return pd.DataFrame(features)
