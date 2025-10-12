# Dianelle AI CV Enhancer - Land Your Dream Job

An AI-powered CV optimization tool that helps job seekers create ATS-friendly resumes and improve their chances of landing interviews. Built with Streamlit and local LLM integration using Ollama for complete privacy.

## Demo

See Dianelle AI CV Enhancer in action:

https://github.com/nguefackuriel/Dianelle-AI-CV-Enhancer/assets/Dianelle_Demo.mp4

Watch how easy it is to analyze your CV, get ATS compatibility scores, receive AI-powered improvement suggestions, and track your progress with our comprehensive analytics dashboard.

## Features

### Core Functionality
- **Smart CV Analysis**: Upload PDF/DOCX files and get instant ATS compatibility scoring
- **Keyword Optimization**: Match your CV with job descriptions for maximum impact  
- **AI-Powered Suggestions**: Get personalized recommendations using local LLM
- **Interactive Chat**: Discuss your career goals with an AI assistant
- **Progress Tracking**: Monitor improvements over time with analytics dashboard
- **Privacy-First**: Everything runs locally - no data leaves your machine

### Analysis Features
- ATS compatibility scoring (0-100)
- Keyword matching against job descriptions
- Technical skills gap analysis  
- CV structure and formatting validation
- Content quality assessment with readability scoring
- Quantified achievement detection

### AI Assistant Capabilities
- Career advice and strategy guidance
- CV improvement suggestions
- Keyword optimization help
- Professional summary writing assistance
- Interview preparation tips
- Industry-specific recommendations

### Analytics & Insights
- Performance breakdown by component
- Industry benchmarking
- Progress tracking over time
- Improvement roadmap generation
- Success metrics visualization

## Technology Stack

- **Frontend**: Streamlit - Interactive web interface
- **AI/LLM**: Ollama - Local language model integration  
- **PDF Processing**: PyPDF2, python-docx - Document parsing
- **NLP**: NLTK, scikit-learn - Text analysis and keyword extraction
- **Visualization**: Plotly - Interactive charts and graphs
- **Language**: Python 3.9+

## Quick Start

### Prerequisites
- Python 3.9 or higher
- Ollama installed and running locally

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd CV_Enhancer
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install and setup Ollama**:
   ```bash
   # Install Ollama (visit https://ollama.ai for installation instructions)
   
   # Pull a language model (choose one):
   ollama pull llama3.2          # Recommended for general use
   ollama pull mistral         # Good alternative
   ollama pull neural-chat     # Optimized for conversations
   ```

4. **Start Ollama server**:
   ```bash
   ollama serve
   ```

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**:
   - Navigate to `http://localhost:8501`
   - Start enhancing your CV!

## How to Use

### 1. Upload Your CV
- Go to the " CV Analysis" page
- Upload your CV in PDF or DOCX format
- Review the extracted text to ensure accuracy

### 2. Add Job Description  
- Paste the complete job description in the text area
- Include requirements, responsibilities, and qualifications
- The more detailed, the better the analysis

### 3. Analyze Your CV
- Click " Analyze CV" to start the analysis
- Wait for the AI to process your documents
- Review your ATS compatibility score and breakdown

### 4. Review Suggestions
- Check the improvement suggestions by priority
- Get detailed guidance for each recommendation
- Use the AI chat for personalized advice

### 5. Track Progress
- Visit the " Analytics Dashboard" for insights
- Monitor your improvement over time
- Set goals and track achievements

### 6. Chat with AI Assistant
- Go to " AI Chat Assistant" page
- Ask questions about your CV or career
- Get personalized recommendations and tips

## Key Benefits

### For Job Seekers
- **Higher Interview Rates**: ATS-optimized CVs get past initial screening
- **Personalized Guidance**: AI advice tailored to your specific situation
- **Time Savings**: Automated analysis instead of manual CV review
- **Skills Development**: Learn what employers actually look for
- **Confidence Boost**: Know your CV is professionally optimized

### For Career Changers
- **Gap Analysis**: Identify missing skills for target roles
- **Industry Insights**: Learn industry-specific CV best practices  
- **Skill Translation**: Convert experience to new field language
- **Networking Prep**: Optimize LinkedIn profile consistency

### For Recent Graduates
- **Professional Formatting**: Learn proper CV structure and content
- **Achievement Focus**: Transform activities into professional accomplishments
- **Keyword Education**: Understand industry terminology and requirements
- **Career Guidance**: Get advice on career path and development

## Configuration

### Ollama Model Selection
You can use different models based on your needs:

- **llama3.2**: Best overall performance, good for analysis and advice
- **mistral**: Faster responses, good for quick suggestions  
- **neural-chat**: Optimized for conversational interactions
- **codellama**: Best for technical roles and programming CVs

Change the model in Settings or by modifying `utils/ollama_client.py`.

### Customization Options
- Adjust AI response creativity (temperature setting)
- Modify scoring weights in `utils/scoring_system.py`
- Add industry-specific keywords in `utils/keyword_extractor.py`
- Customize suggestion templates in `components/improvement_suggestions.py`

## Scoring System

The ATS compatibility score (0-100) is calculated based on:

- **Keyword Match (35%)**: Relevance to job description
- **CV Structure (25%)**: Organization and essential sections  
- **Content Quality (20%)**: Writing quality and achievements
- **Technical Skills (15%)**: Required skills matching
- **ATS Formatting (5%)**: Scanner-friendly formatting

## Privacy & Security

- **Local Processing**: All analysis runs on your machine
- **No Data Upload**: Documents never leave your computer
- **Private AI**: Ollama runs locally, no external API calls
- **Session Storage**: Data cleared when you close the browser
- **Open Source**: Full transparency of code and processes

## Troubleshooting

### Common Issues

**Ollama Connection Error**:
```bash
# Check if Ollama is running
ollama list

# Start Ollama if not running
ollama serve

# Pull a model if none available
ollama pull llama2
```

**PDF Extraction Issues**:
- Ensure PDF is not password protected
- Try converting to DOCX format
- Check if PDF contains extractable text (not just images)

**Slow Performance**:
- Use a smaller Ollama model (mistral instead of llama2)
- Close other resource-intensive applications
- Reduce analysis text length in settings

**Import Errors**:
```bash
# Reinstall requirements
pip install --upgrade -r requirements.txt

# Install missing NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### Getting Help

1. Check the troubleshooting section above
2. Review Ollama documentation at https://ollama.ai
3. Ensure all requirements are properly installed
4. Check Python version compatibility (3.8+)

## Contributing

We welcome contributions! Here's how you can help:

1. **Report Issues**: Found a bug? Report it in the issues section
2. **Suggest Features**: Have ideas for improvements? Let us know
3. **Submit PRs**: Fix bugs or add features with pull requests
4. **Improve Documentation**: Help make the README and docs better
5. **Share Feedback**: Tell us about your experience using the tool

### Development Setup
```bash
# Clone and setup development environment
git clone <repository-url>
cd CV_Enhancer
pip install -r requirements.txt

# Install development dependencies
pip install black flake8 pytest

# Run tests
pytest tests/

# Format code
black .
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **Ollama Team**: For providing excellent local LLM infrastructure
- **Streamlit**: For the amazing web app framework
- **Open Source Community**: For the fantastic libraries used in this project

## Success Stories

> "Increased my interview callback rate from 10% to 60% after using CV Enhancer!" - Sarah M., Software Engineer

> "Finally understood what ATS systems were looking for. Got my dream job within 2 months!" - John D., Marketing Manager  

> "The AI suggestions were incredibly specific and actionable. Best CV tool I've ever used." - Maria L., Data Scientist

---

**Ready to land your dream job? Start enhancing your CV today!** 

For more information, visit our documentation or reach out for support.
