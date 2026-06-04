# Dianelle AI CV Enhancer — Land Your Dream Job

An advanced, privacy-first AI CV optimizer and career preparation platform. Dianelle AI helps job seekers create ATS-optimized, recruiter-winning resumes, prepare for interviews, generate tailored cover letters, and optimize their LinkedIn profiles. Built with **Streamlit** and local LLM integration using **Ollama**, ensuring 100% data privacy—no data ever leaves your machine.

---

## 🚀 Key Features

### 1. Smart CV Analysis & ATS Simulation
* **ATS Compatibility Scoring**: Generates an instant, weighted score (0–100) based on:
  * **Keyword Match (35%)**: Relates CV content directly to target job descriptions.
  * **CV Structure (25%)**: Validates essential sections (Contact, Summary, Experience, Education, Skills).
  * **Content Quality (20%)**: Evaluates formatting, word usage, readability, and impact.
  * **Technical Skills (15%)**: Assesses technical competency gaps.
  * **ATS Formatting (5%)**: Checks parser-friendliness.
* **Skills Gap Analysis**: Scans your CV and target job description to highlight exact missing keywords and technical terms.
* **Formatting Audits**: Flags potential issues like incorrect date formats, missing contact info, or structural irregularities.

### 2. AI CV Rewriter (STAR & Google XYZ Rules)
* **Google XYZ Formula**: Automatically reformulates achievement bullet points: *"Accomplished [X], as measured by [Y], by doing [Z]"*.
* **STAR Methodology**: Emphasizes **S**ituation, **T**ask, **A**ction, and **R**esults for maximum professional impact.
* **ATS & Recruiter Double Test**: Balances dense keyword optimization for machine parsers with natural, compelling, human-readable language for real recruiters.
* **Human Tone Engine**: Completely eliminates typical AI-generated fluff words (e.g., *furthermore*, *tapestry*, *testament*, *spearheaded*) and guarantees emoji-free, professional output.

### 3. Hadrien-Style Cover Letter Generator
* **Direct 250-Word Formula**: Replaces long, generic templates with a direct, impactful 250-word cover letter.
* **Proactive Gap Addressing**: Intelligently identifies and addresses employment or skill gaps with positive, growth-oriented context.
* **Human-Written Feel**: Features a confident, concise tone that avoids standard AI clichés.

### 4. Interactive Interview Preparation
* **Role-Specific Simulator**: Generates dynamic interview questions tailored to your CV and target job description.
* **Interactive Mock Session**: Lets you answer questions directly in the app, with real-time response scoring, comprehensive feedback, and model answers.

### 5. LinkedIn Profile Optimizer
Structures your profile into Hadrien's 5 key recruiter-friendly sections:
1. **Headline**: Under 220 characters, highly searchable, highlighting core role + key value.
2. **About Section**: 3 paragraphs max, written in the first person (Who you are, Core achievements, Future focus).
3. **Experience**: Google XYZ bullet points completed by "What I learned" summaries.
4. **Skills & Featured**: Tailored selection based on job requirements.
5. **Consistency Audit**: Assesses alignment between your CV, cover letter, and LinkedIn profile to ensure a cohesive professional brand.

### 6. Salary Negotiation & Follow-ups
* **Hadrien Salary Negotiation Framework**: Generates structured, polite, yet firm salary negotiation emails.
* **Strategic Follow-up Templates**: Formulates professional follow-ups for post-application, post-interview, and active check-in scenarios.

### 7. Export Engine (Word & PDF)
* **Justified Layout**: Exports optimized CVs into perfectly formatted Word (`.docx`) and PDF documents with fully justified text alignment.
* **Clean Encoding**: Clears encoding glitches (no unknown characters or random question marks `?` in bullet points or contact lines).

### 8. Analytics Dashboard
* **Score Evolution**: Tracks your progress and ATS compatibility improvements over multiple iterations.
* **Competency Breakdown**: Visualizes soft vs. technical skill coverage, layout compliance, and content impact.

---

## 🛠️ Technology Stack

* **Frontend**: Streamlit (premium, dark-accented UI built with Inter font styling)
* **Local AI**: Ollama (supports any model, default: `llama3.2`)
* **Document Processing**: `PyPDF2`, `python-docx`
* **Natural Language Processing**: `NLTK` (Tokenization, Stopwords extraction), `scikit-learn` (TF-IDF vectorization)
* **Data Visualization**: `Plotly`

---

## ⚡ Quick Start

### Prerequisites
* **Python 3.9+** installed on your system.
* **Ollama** installed and running locally.

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/nguefackuriel/Dianelle-AI-CV-Enhancer.git
   cd Dianelle-AI-CV-Enhancer
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install NLTK Text Resources**:
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords')"
   ```

5. **Set Up Ollama**:
   Make sure Ollama is installed (download from [ollama.ai](https://ollama.ai)) and pull a model:
   ```bash
   # Pull the default recommended model
   ollama pull llama3.2:3b
   
   # Or any other model of your choice
   ollama pull llama3
   ollama pull mistral
   ```

---

## 运行 & Running the App

1. **Start the Ollama Local Server**:
   ```bash
   ollama serve
   ```

2. **Start the Streamlit Application**:
   ```bash
   streamlit run app.py
   ```

3. **Access the Web Interface**:
   Open your web browser and navigate to:
   ```text
   http://localhost:8501
   ```

---

## 📋 Privacy & Privacy-First Architecture

* **100% Offline Processing**: All file parsing, keyword scoring, analytics generation, and AI generation are executed locally.
* **No Telemetry / API Keys**: You do not need external API keys (OpenAI, Anthropic, etc.). Everything runs within your local Ollama runtime.
* **Volatile Session Storage**: Extracted CV contents and chat history reside in Streamlit's local session memory and are immediately cleared when you close the browser tab.

---

## 🔧 Configuration & Customization

* **Model Selection**: You can switch between any local Ollama models directly via the **Settings** page or by updating models in `utils/ollama_client.py`.
* **Temperature Slider**: Control the creativity vs. strictness of the rewrites and responses under the **Settings** menu.
* **Scoring Parameters**: Fine-tune the ATS criteria weights by editing `utils/scoring_system.py`.

---

## 🐞 Troubleshooting

### Ollama Connection Error
* Ensure the Ollama server is running by executing `ollama list` in your terminal. If it fails, start it with `ollama serve`.
* If you run a custom port/host, verify that Ollama is listening on `http://localhost:11434`.

### Character Encoding Glitches in PDF
* If you see random question marks `?` or unexpected symbol conversions in your exported PDF, ensure that the input CV text contains standard UTF-8 characters, and download the freshly generated file from the **Export CV** page where formatting cleanups are applied automatically.

### Performance Lag
* Large models (e.g. `llama3:8b`) may run slower on machines without dedicated GPU accelerators (such as Apple Silicon or NVIDIA cards). If processing is slow, run `ollama pull llama3.2` to download the highly optimized 3B parameters version.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](file:///Users/urielnguefackyefou/Downloads/Dianelle-AI-CV-Enhancer/LICENSE) file for details.

---

*Made with 💜 for ambitious builders and job seekers.*
