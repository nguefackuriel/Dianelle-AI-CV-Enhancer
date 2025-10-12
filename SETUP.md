# CV Enhancer Setup Instructions

## Prerequisites Setup

1. **Install Ollama**:
   - macOS: `brew install ollama`
   - Or download from: https://ollama.ai
   - Start with: `ollama serve`

2. **Pull an AI model**:
   ```bash
   ollama pull llama3.2
   # or
   ollama pull mistral
   ```

3. **Verify installation**:
   ```bash
   ollama list
   ```

## Python Environment Setup

1. **Create virtual environment** (recommended):
   ```bash
   python -m venv cv_enhancer_env
   source cv_enhancer_env/bin/activate  # On macOS/Linux
   # or
   cv_enhancer_env\Scripts\activate  # On Windows
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data**:
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

## Running the Application

1. **Start Ollama** (in separate terminal):
   ```bash
   ollama serve
   ```

2. **Run the app**:
   ```bash
   streamlit run app.py
   ```

3. **Open browser**: Navigate to `http://localhost:8501`

## Troubleshooting

- **Ollama not found**: Ensure ollama is in your PATH
- **Model not loaded**: Run `ollama pull llama3.2`  
- **Import errors**: Check Python version (3.9+) and reinstall requirements
- **Performance issues**: Try a smaller model like `mistral`

For more help, see the main README.md file.
