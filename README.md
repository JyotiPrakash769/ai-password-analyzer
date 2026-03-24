# 🛡️ AI Password Strength Analyzer

Welcome to the **AI Password Strength Analyzer**! A cutting-edge, machine-learning-powered tool that doesn't just check if your password is long enough—it truly *understands* how secure it is.

![AI Password Analyzer Demo](./demo_recording.webp)

By extracting advanced features like Shannon Entropy, character distribution, and cryptographic strength, and running them through a Random Forest Classifier trained on thousands of data points, this project provides real-time, professional-grade security assessments. Whether you're a developer crafting secure applications or a user trying to protect your digital life, this analyzer detects weak patterns that traditional rules simply miss.

## 🚀 Features
- **Neural Password Analysis:** Real-time AI execution as you type.
- **Advanced Feature Extraction:** Uses `pandas` and `numpy` to compute Shannon Entropy, character density, and other ML properties.
- **Model Serialization:** Super-fast inference with `joblib`.
- **Interactive UI:** A highly dynamic and beautiful front-end powered by `streamlit`.
- **Automated ML Pipeline:** Full end-to-end dataset generation and pipeline training scripts included.

## 🛠️ Setup Instructions

1. **Navigate into the project repository**:
   ```bash
   cd ai-password-analyzer
   ```

2. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Train the Machine Learning Model**:
   Execute the training pipeline to generate synthetic data, extract features, and train the core classifier.
   ```bash
   python -m src.train_model
   ```

4. **Run the Application Locally**:
   Launch the user interface server to test passwords.
   ```bash
   streamlit run app.py
   ```

## 📁 Project Structure
- `src/` - Core application logic and ML pipelines.
  - `feature_extractor.py` - Mathematical feature extraction from raw strings.
  - `train_model.py` - Model training script.
  - `predictor.py` - Model loading and inference.
  - `utils.py` - Helper logic and functions.
- `app.py` - Frontend application file.
- `requirements.txt` - List of project dependencies.
