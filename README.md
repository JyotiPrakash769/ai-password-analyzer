# AI Password Strength Analyzer

This is a production-ready Python project that evaluates password strength using a machine learning model. It extracts various features from passwords and classifies them into `weak`, `medium`, or `strong` using a Random Forest Classifier trained with `scikit-learn`.

## Features
- Modular application architecture.
- Feature extraction using `pandas` and `numpy`:
  - Length
  - Uppercase letters count
  - Lowercase letters count
  - Digits count
  - Special characters count
  - Shannon entropy
- Model serialization using `joblib`.
- Interactive web UI using `streamlit`.
- Automated dataset generation and training pipeline.

## Setup Instructions

1. **Navigate to the project directory** (set this folder as your active workspace if using an IDE):
   ```bash
   cd C:\Users\jyoti\.gemini\antigravity\scratch\ai_password_analyzer
   ```

2. **Install the dependencies**:
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Train the Machine Learning Model**:
   Execute the training pipeline to generate synthetic data, extract features, and train the classifier. The model will be saved in the `model/` directory.
   ```bash
   python -m src.train_model
   ```

4. **Run the Streamlit Application**:
   Launch the user interface to test passwords.
   ```bash
   streamlit run app.py
   ```

## Project Structure
- `src/` - Contains the core application logic.
  - `feature_extractor.py` - Extracts analytical features from raw text.
  - `train_model.py` - The model training pipeline and dataset generator.
  - `predictor.py` - Handles model loading and inference.
  - `utils.py` - Helper utilities like Shannon entropy calculation.
- `app.py` - The frontend application using Streamlit.
- `requirements.txt` - Python package dependencies.

---

## 🚀 Easy Deployment (Streamlit Community Cloud)

Since this project builds entirely on Python and Streamlit, it can be deployed to the cloud for free in under two minutes!

1. **Push your code to GitHub.** Ensure `requirements.txt` and `model/rf_model.joblib` are pushed.
2. Visit [share.streamlit.io](https://share.streamlit.io/).
3. Log in with your GitHub account.
4. Click **New app**.
5. Select your GitHub repository containing this project.
6. Set the `Main file path` to `app.py`.
7. Click **Deploy!**

In about 60 seconds, your Pro-Level Password Analyzer will be live on the internet!
