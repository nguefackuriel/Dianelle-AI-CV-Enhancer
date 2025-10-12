"""
CV Enhancer - Main Streamlit Application
Author: CV Enhancement Team
Description: ATS-optimized CV enhancement tool with local LLM integration
"""

import streamlit as st
import os
from pathlib import Path

# Configure Streamlit page
st.set_page_config(
    page_title="CV Enhancer - Land Your Dream Job",
    #page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    
    .score-box {
        background: linear-gradient(90deg, #ff4b4b 0%, #ffa500 50%, #00c851 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-size: 2rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    .improvement-box {
        background-color: #f0f8ff;
        color: #333333;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    
    .improvement-box strong {
        color: #1f77b4;
        font-weight: bold;
    }
    
    .sidebar .sidebar-content {
        background-color: #f5f5f5;
    }
</style>
""", unsafe_allow_html=True)

# Import custom modules
from utils.pdf_processor import PDFProcessor
from utils.cv_analyzer import CVAnalyzer
from utils.keyword_extractor import KeywordExtractor
from utils.ollama_client import OllamaClient
from utils.scoring_system import ScoringSystem
from components.chat_interface import ChatInterface
from components.improvement_suggestions import ImprovementSuggestions
from components.analytics_dashboard import AnalyticsDashboard

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header"> CV Enhancer - Meet Dianelle, Your AI Career Assistant</h1>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'cv_text' not in st.session_state:
        st.session_state.cv_text = ""
    if 'job_description' not in st.session_state:
        st.session_state.job_description = ""
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Sidebar navigation
    with st.sidebar:
        st.title(" Navigation")
        page = st.selectbox(
            "Choose a feature:",
            [
                " Home",
                " CV Analysis",
                " AI Chat Assistant",
                " Analytics Dashboard",
                " Settings"
            ]
        )
        
        st.markdown("---")
        st.markdown("### System Status")
        
        # Check Ollama connection
        try:
            ollama_client = OllamaClient()
            if ollama_client.is_connected():
                st.success("✅ Ollama Connected")
            else:
                st.error("❌ Ollama Disconnected")
                st.info("Please ensure Ollama is running: `ollama serve`")
        except:
            st.error("❌ Ollama Not Available")
            st.info("Install Ollama: https://ollama.ai")
    
    # Main content based on selected page
    if page == " Home":
        show_home_page()
    elif page == " CV Analysis":
        show_cv_analysis_page()
    elif page == " AI Chat Assistant":
        show_chat_page()
    elif page == " Analytics Dashboard":
        show_analytics_page()
    elif page == " Settings":
        show_settings_page()

def show_home_page():
    """Display the home page with introduction and features"""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## Welcome to CV Enhancer! Meet Dianelle 
        
        Hi! I'm **Dianelle**, your personal AI career assistant. I'll help you transform your CV into an ATS-optimized masterpiece that gets you noticed by recruiters and hiring managers.
        
        ### Key Features:
        
        - **Smart CV Analysis**: Upload your CV and get instant ATS compatibility scoring
        - **Keyword Optimization**: Match your CV with job descriptions for maximum impact
        - **AI-Powered Suggestions**: Get personalized recommendations from Dianelle to improve your CV
        - **Interactive Chat**: Discuss your career goals directly with Dianelle, your AI assistant
        - **Analytics Dashboard**: Track your improvement over time
        - **Privacy First**: Everything runs locally - no data leaves your machine
        
        ### How It Works:
        
        1. **Upload** your current CV (PDF format)
        2. **Paste** the job description you're targeting
        3. **Analyze** and get your ATS compatibility score
        4. **Improve** with AI-generated suggestions
        5. **Chat** with Dianelle for personalized career advice
        6. **Download** your enhanced CV
        
        Ready to land your dream job? Let's get started!
        """)
    
    with col2:
        # Add some empty space at the top
        st.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
        
        st.markdown("""
        ### Quick Tips
        
        - Use action verbs (achieved, managed, led)
        - Quantify your accomplishments
        - Include relevant keywords
        - Keep formatting simple and clean
        - Tailor your CV for each application
        """)

def show_cv_analysis_page():
    """Display the CV analysis page"""
    
    st.markdown("## CV Analysis & Enhancement")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Upload Your CV")
        uploaded_file = st.file_uploader(
            "Choose your CV file",
            type=['pdf', 'docx'],
            help="Upload your CV in PDF or DOCX format"
        )
        
        if uploaded_file is not None:
            try:
                # Process the uploaded file
                pdf_processor = PDFProcessor()
                cv_text = pdf_processor.extract_text(uploaded_file)
                st.session_state.cv_text = cv_text
                
                with st.expander(" Extracted CV Text Preview"):
                    st.text_area("CV Content", cv_text[:1000] + "...", height=200, disabled=True)
                
                st.success("✅ CV successfully processed!")
                
            except Exception as e:
                st.error(f"❌ Error processing CV: {str(e)}")
    
    with col2:
        st.markdown("### Job Description")
        job_description = st.text_area(
            "Paste the job description here:",
            value=st.session_state.job_description,
            height=300,
            placeholder="Copy and paste the complete job description including requirements, responsibilities, and qualifications..."
        )
        
        if job_description:
            st.session_state.job_description = job_description
    
    # Analysis button
    if st.session_state.cv_text and st.session_state.job_description:
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button(" Analyze CV", type="primary", use_container_width=True):
                with st.spinner(" Analyzing your CV... This may take a moment"):
                    
                    try:
                        # Initialize analyzers
                        cv_analyzer = CVAnalyzer()
                        keyword_extractor = KeywordExtractor()
                        scoring_system = ScoringSystem()
                        
                        # Perform analysis
                        results = cv_analyzer.analyze_cv(
                            st.session_state.cv_text,
                            st.session_state.job_description
                        )
                        
                        st.session_state.analysis_results = results
                        st.success("✅ Analysis complete!")
                        
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}")
    
    # Display results
    if st.session_state.analysis_results:
        display_analysis_results(st.session_state.analysis_results)

def display_analysis_results(results):
    """Display the analysis results"""
    
    st.markdown("---")
    st.markdown("## Analysis Results")
    
    # ATS Compatibility Score
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        score = results.get('ats_score', 0)
        score_color = "#00c851" if score >= 80 else "#ffa500" if score >= 60 else "#ff4b4b"
        
        st.markdown(f"""
        <div style="background: {score_color}; padding: 2rem; border-radius: 15px; text-align: center; margin: 2rem 0;">
            <h2 style="color: white; margin: 0;">ATS Compatibility Score</h2>
            <h1 style="color: white; margin: 10px 0; font-size: 3rem;">{score}/100</h1>
            <p style="color: white; margin: 0; font-size: 1.2rem;">
                {" Excellent!" if score >= 80 else " Good Progress" if score >= 60 else " Let's Improve!"}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed breakdown
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Keyword Match Analysis")
        
        matched_keywords = results.get('matched_keywords', [])
        missing_keywords = results.get('missing_keywords', [])
        
        if matched_keywords:
            st.markdown("**✅ Found Keywords:**")
            for keyword in matched_keywords[:10]:
                st.markdown(f"- {keyword}")
        
        if missing_keywords:
            st.markdown("**❌ Missing Important Keywords:**")
            for keyword in missing_keywords[:10]:
                st.markdown(f"- {keyword}")
    
    with col2:
        st.markdown("### Improvement Areas")
        
        suggestions = results.get('suggestions', [])
        for i, suggestion in enumerate(suggestions[:5], 1):
            st.markdown(f"""
            <div class="improvement-box">
                <strong>{i}. {suggestion['title']}</strong><br>
                {suggestion['description']}
            </div>
            """, unsafe_allow_html=True)
    
    # Enhanced CV suggestion
    if 'enhanced_content' in results:
        st.markdown("### AI-Enhanced Content Suggestions")
        
        with st.expander("View Enhanced Content"):
            st.markdown(results['enhanced_content'])

def show_chat_page():
    """Display the chat interface"""
    
    st.markdown("## Chat with Dianelle - Your AI Career Assistant")
    
    if not st.session_state.cv_text:
        st.warning(" Please upload and analyze your CV first to get personalized advice!")
        return
    
    # Initialize chat interface
    chat_interface = ChatInterface()
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.chat_message("user").write(message['content'])
        else:
            st.chat_message("assistant").write(message['content'])
    
    # Chat input
    if prompt := st.chat_input("Ask Dianelle anything about your CV or career..."):
        
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = chat_interface.get_response(
                        prompt,
                        st.session_state.cv_text,
                        st.session_state.job_description,
                        st.session_state.analysis_results
                    )
                    
                    st.write(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})

def show_analytics_page():
    """Display the analytics dashboard"""
    
    st.markdown("## Analytics Dashboard")
    
    if not st.session_state.analysis_results:
        st.warning(" No analysis data available. Please analyze your CV first!")
        return
    
    analytics_dashboard = AnalyticsDashboard()
    analytics_dashboard.display(st.session_state.analysis_results)

def show_settings_page():
    """Display the settings page"""
    
    st.markdown("## Settings")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### AI Model Settings")
        
        model_name = st.selectbox(
            "Choose AI Model:",
            ["llama3.2", "mistral", "codellama", "neural-chat"],
            help="Select the Ollama model to use for analysis"
        )
        
        temperature = st.slider(
            "Response Creativity",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            help="Higher values make responses more creative but less focused"
        )
        
    with col2:
        st.markdown("### Interface Settings")
        
        theme = st.selectbox(
            "Color Theme:",
            ["Default", "Dark", "Professional"],
            help="Choose your preferred interface theme"
        )
        
        show_advanced = st.checkbox(
            "Show Advanced Features",
            help="Enable advanced CV analysis features"
        )
    
    st.markdown("### Data Management")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button(" Export Analysis"):
            st.info("Feature coming soon!")
    
    with col2:
        if st.button(" Clear Session"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("Session cleared!")
            st.experimental_rerun()
    
    with col3:
        if st.button(" Help & Support"):
            st.info("Contact support: nguefackuriel@gmail.com")

if __name__ == "__main__":
    main()
