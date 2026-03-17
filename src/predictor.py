import joblib
import os
from src.feature_extractor import extract_features

MODEL_PATH = 'model/rf_model.joblib'

class PasswordPredictor:
    def __init__(self):
        """
        Initializes the predictor. It loads the pre-trained scikit-learn model
        using joblib. If the model hasn't been trained yet, it raises an error.
        """
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Please run the train_model.py pipeline first.")
        
        # Load the saved model
        self.model = joblib.load(MODEL_PATH)
        
    def predict_strength(self, password):
        """
        Predicts the strength ('weak', 'medium', 'strong') of the given password.
        
        Returns:
            tuple: (predicted label, dictionary of features)
        """
        # We must extract features exactly the same way we did for training
        features_df = extract_features([password])
        
        # Get the prediction for the single password
        prediction = self.model.predict(features_df)[0]
        
        return prediction, features_df.iloc[0].to_dict()
        
    def get_suggestions(self, password, features):
        """
        Generates actionable improvement suggestions based on the features 
        we extracted from the user's password.
        """
        suggestions = []
        
        if features['length'] < 8:
            suggestions.append("Increase the length of your password to at least 8 characters.")
        
        if features['uppercase_count'] == 0:
            suggestions.append("Add at least one uppercase letter (A-Z).")
            
        if features['lowercase_count'] == 0:
            suggestions.append("Add at least one lowercase letter (a-z).")
            
        if features['digits_count'] == 0:
            suggestions.append("Include at least one number (0-9).")
            
        if features['special_count'] == 0:
            suggestions.append("Include at least one special character (e.g., !, @, #, $, etc.).")
            
        if features['entropy'] < 2.5:
            suggestions.append("Your password is too predictable. Avoid common patterns and mix characters.")
            
        if not suggestions:
            suggestions.append("Great job! Your password follows excellent security practices.")
            
        return suggestions
