"""
Dianelle AI CV Enhancer - Main Streamlit Application
Author: CV Enhancement Team
Description: ATS-optimized CV enhancement tool with local LLM integration.

Major upgrade: Real ATS simulation, AI rewriting, DOCX/PDF export,
cover letter generation, interview prep, LinkedIn optimization.
"""

import streamlit as st
import os
from pathlib import Path

# Configure Streamlit page
st.set_page_config(
    page_title="Dianelle AI CV Enhancer — Land Your Dream Job",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS — Professional dark-accented theme
st.markdown("""
<style>
    /* === Typography === */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, .stApp, .main, .block-container {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* === Main Header === */
    .main-header {
        font-size: 2.2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    .sub-header {
        text-align: center;
        color: #888;
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }

    /* === Score Display === */
    .score-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        color: white;
        font-size: 2rem;
        font-weight: bold;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }

    /* === Improvement Cards === */
    .improvement-box {
        background-color: #f8f9ff;
        color: #333;
        padding: 1rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 0.8rem 0;
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .improvement-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }

    .improvement-box strong {
        color: #667eea;
        font-weight: 600;
    }

    /* === Workflow Stepper === */
    .stepper-container {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        margin: 1.5rem 0;
        flex-wrap: wrap;
    }

    .step {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.5rem 1rem;
        border-radius: 24px;
        font-size: 0.85rem;
        font-weight: 500;
        transition: all 0.3s;
    }

    .step-active {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }

    .step-done {
        background: #e8f5e9;
        color: #2e7d32;
        border: 1px solid #a5d6a7;
    }

    .step-pending {
        background: #f5f5f5;
        color: #999;
        border: 1px solid #e0e0e0;
    }

    .step-arrow {
        color: #ccc;
        font-size: 1.2rem;
    }

    /* === Sidebar === */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }

    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stSelectbox label {
        color: #e0e0e0 !important;
    }

    /* === Buttons === */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 10px;
        font-weight: 600;
        letter-spacing: 0.3px;
        transition: all 0.3s;
    }

    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        transform: translateY(-1px);
    }

    /* === Tabs === */
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea20, #764ba220);
    }

    /* === Metrics === */
    [data-testid="stMetricValue"] {
        font-weight: 700;
        color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Import custom modules
from utils.pdf_processor import PDFProcessor
from utils.cv_analyzer import CVAnalyzer
from utils.keyword_extractor import KeywordExtractor
from utils.ollama_client import OllamaClient
from utils.job_matcher import JobMatcher
from utils.translations import t
from components.chat_interface import ChatInterface
from components.improvement_suggestions import ImprovementSuggestions
from components.analytics_dashboard import AnalyticsDashboard
from components.rewrite_page import RewritePage
from components.export_page import ExportPage
from components.cover_letter_page import CoverLetterPage
from components.interview_prep import InterviewPrep
from components.linkedin_optimizer import LinkedInOptimizer
from components.negotiation_followups import NegotiationFollowups
def navigate_to(page_name):
    """Callback to programmatically navigate to a page"""
    st.session_state['current_page'] = page_name


def main():
    """Main application function"""

    # Header
    st.markdown('<h1 class="main-header">Dianelle AI CV Enhancer</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">{t("main_subtitle")}</p>', unsafe_allow_html=True)

    # Initialize session state
    defaults = {
        'cv_text': '',
        'job_description': '',
        'analysis_results': None,
        'chat_history': [],
        'accepted_rewrites': {},
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

    # Workflow stepper
    _display_workflow_stepper()

    # Sidebar navigation
    with st.sidebar:
        # Language selection
        if 'language' not in st.session_state:
            st.session_state['language'] = 'Français'
            
        lang_choice = st.selectbox(
            "Language / Langue",
            options=["Français", "English"],
            index=0 if st.session_state['language'] == 'Français' else 1,
            key="language_selector"
        )
        if lang_choice != st.session_state['language']:
            st.session_state['language'] = lang_choice
            st.rerun()

        st.markdown(f"## {t('Navigation')}")

        if 'current_page' not in st.session_state:
            st.session_state['current_page'] = "Home"

        page = st.selectbox(
            t("choose_feature"),
            [
                "Home",
                "CV Analysis",
                "CV Rewriter",
                "Cover Letter",
                "Export CV",
                "AI Chat Assistant",
                "Interview Prep",
                "LinkedIn Optimizer",
                "Negotiation & Follow-ups",
                "Analytics Dashboard",
                "Settings",
            ],
            format_func=t,
            key="current_page"
        )

        st.markdown("---")
        st.markdown(f"### {t('sys_status')}")

        # Check Ollama connection
        try:
            ollama_client = OllamaClient()
            if ollama_client.is_connected():
                st.success(t("ollama_online"))
                models = ollama_client.get_available_models()
                if models:
                    if 'selected_model' not in st.session_state:
                        st.session_state['selected_model'] = models[0]
                    
                    if st.session_state['selected_model'] not in models:
                        st.session_state['selected_model'] = models[0]
                        
                    model_idx = models.index(st.session_state['selected_model'])
                    
                    st.caption(t("active_model"))
                    selected_model = st.selectbox(
                        "Active Model Selection",
                        options=models,
                        index=model_idx,
                        key="selected_model_selector",
                        label_visibility="collapsed"
                    )
                    if selected_model != st.session_state['selected_model']:
                        st.session_state['selected_model'] = selected_model
                        st.rerun()
            else:
                st.error(t("ollama_offline"))
                st.info("Run: `ollama serve`")
        except Exception:
            st.error(t("ollama_unavailable"))
            st.info("Install: https://ollama.ai")

        # Quick stats
        st.markdown("---")
        st.markdown(f"### {t('session')}")
        has_stats = False
        if st.session_state.get('analysis_results'):
            score = st.session_state['analysis_results'].get('ats_score', 0)
            st.metric(t("ats_score"), f"{score}/100")
            has_stats = True
        if st.session_state.get('accepted_rewrites'):
            st.metric(t("enhanced_sections"), len(st.session_state['accepted_rewrites']))
            has_stats = True
        
        if not has_stats:
            st.caption(t("no_session_data"))

    # Main content based on selected page
    if page == "Home":
        show_home_page()
    elif page == "CV Analysis":
        show_cv_analysis_page()
    elif page == "CV Rewriter":
        RewritePage().display()
    elif page == "Cover Letter":
        CoverLetterPage().display()
    elif page == "Export CV":
        ExportPage().display()
    elif page == "AI Chat Assistant":
        show_chat_page()
    elif page == "Interview Prep":
        InterviewPrep().display()
    elif page == "LinkedIn Optimizer":
        LinkedInOptimizer().display()
    elif page == "Negotiation & Follow-ups":
        NegotiationFollowups().display()
    elif page == "Analytics Dashboard":
        show_analytics_page()
    elif page == "Settings":
        show_settings_page()


def _display_workflow_stepper():
    """Display the workflow progress stepper."""
    has_cv = bool(st.session_state.get('cv_text'))
    has_jd = bool(st.session_state.get('job_description'))
    has_analysis = st.session_state.get('analysis_results') is not None
    has_rewrites = bool(st.session_state.get('accepted_rewrites'))

    steps = [
        ("1", t("step_upload"), has_cv),
        ("2", t("step_jd"), has_jd),
        ("3", t("step_analyze"), has_analysis),
        ("4", t("step_enhance"), has_rewrites),
        ("5", t("step_export"), False),
    ]

    html_parts = ['<div class="stepper-container">']
    for i, (icon, label, done) in enumerate(steps):
        if done:
            css_class = "step step-done"
        elif i == 0 or (i > 0 and steps[i-1][2]):
            css_class = "step step-active"
        else:
            css_class = "step step-pending"

        html_parts.append(f'<span class="{css_class}">{icon} {label}</span>')
        if i < len(steps) - 1:
            html_parts.append('<span class="step-arrow">→</span>')

    html_parts.append('</div>')
    st.markdown(''.join(html_parts), unsafe_allow_html=True)


def show_home_page():
    """Display the home page with introduction and features"""

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(t("home_intro_markdown"))

    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)

        # Quick stats if available
        if st.session_state.get('analysis_results'):
            score = st.session_state['analysis_results'].get('ats_score', 0)
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 1.5rem; border-radius: 16px; text-align: center; color: white; margin-bottom: 1rem;">
                <h3 style="margin:0; color:white;">{t("ats_score")}</h3>
                <h1 style="margin:0; font-size: 3rem; color:white;">{score}</h1>
                <p style="margin:0; color:rgba(255,255,255,0.8);">{t("out_of_100")}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea15, #764ba215); padding: 1.5rem; border-radius: 16px 16px 0 0; text-align: center; border: 2px dashed #667eea; border-bottom: none; margin-bottom: 0px;">
                <h3 style="margin:0; color: #667eea; font-weight: 600;">{t("get_started_header")}</h3>
                <p style="margin:0.5rem 0 0 0; color: #aaa; font-size: 0.9rem;">{t("get_started_desc")}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <style>
            div.get-started-btn button {
                border-top-left-radius: 0px !important;
                border-top-right-radius: 0px !important;
                border-bottom-left-radius: 16px !important;
                border-bottom-right-radius: 16px !important;
                margin-top: -16px !important;
                padding: 0.75rem !important;
                font-size: 1rem !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="get-started-btn">', unsafe_allow_html=True)
            st.button(
                t("start_analysis_btn"),
                type="primary",
                use_container_width=True,
                on_click=navigate_to,
                args=("CV Analysis",)
            )
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(t("home_tips_markdown"))


def show_cv_analysis_page():
    """Display the CV analysis page"""

    st.markdown(f"## {t('cv_analysis_title')}")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"### {t('upload_cv')}")
        uploaded_file = st.file_uploader(
            t("choose_file"),
            type=['pdf', 'docx', 'txt'],
            help=t("file_uploader_help")
        )

        if uploaded_file is not None:
            try:
                pdf_processor = PDFProcessor()
                cv_text = pdf_processor.extract_text(uploaded_file)
                st.session_state.cv_text = cv_text

                with st.expander(t("cv_preview")):
                    preview = cv_text[:1500] + ("..." if len(cv_text) > 1500 else "")
                    st.text_area("CV Content", preview, height=200, disabled=True)

                word_count = len(cv_text.split())
                st.success(t("cv_processed_success", word_count=word_count))

            except Exception as e:
                st.error(t("error_processing_cv", error=str(e)))

    with col2:
        st.markdown(f"### {t('job_desc_title')}")
        job_description = st.text_area(
            t("paste_jd"),
            value=st.session_state.job_description,
            height=300,
            placeholder=t("jd_placeholder")
        )

        if job_description:
            st.session_state.job_description = job_description

    # Analysis button
    if st.session_state.cv_text and st.session_state.job_description:

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            if st.button(t("analyze_cv_btn"), type="primary", use_container_width=True):
                with st.spinner(t("running_ats_spinner")):

                    try:
                        cv_analyzer = CVAnalyzer()
                        job_matcher = JobMatcher()

                        # Core analysis
                        results = cv_analyzer.analyze_cv(
                            st.session_state.cv_text,
                            st.session_state.job_description
                        )

                        # Job fit scoring
                        fit_results = job_matcher.compute_fit_score(
                            st.session_state.cv_text,
                            st.session_state.job_description
                        )
                        results['job_fit'] = fit_results

                        # Clear old AI generation outputs to prevent stale displays
                        for key in list(st.session_state.keys()):
                            if key.startswith(('linkedin_', 'interview_', 'bullet_optimizer_', 'generated_summary_', 'optimized_skills_', 'weak_language_', 'quantification_', 'cover_letter_')):
                                del st.session_state[key]

                        st.session_state.analysis_results = results
                        st.success(t("analysis_complete"))

                    except Exception as e:
                        st.error(t("analysis_failed", error=str(e)))

    # Display results
    if st.session_state.analysis_results:
        display_analysis_results(st.session_state.analysis_results)


def display_analysis_results(results):
    """Display the analysis results"""

    st.markdown("---")
    st.markdown(f"## {t('ats_simulation_results')}")

    # ATS Score + Job Fit
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        score = results.get('ats_score', 0)
        score_color = "#00c851" if score >= 80 else "#ffa500" if score >= 60 else "#ff4b4b"
        score_text = t("score_excellent") if score >= 80 else t("score_good") if score >= 60 else t("score_improve")
        st.markdown(f"""
        <div style="background: {score_color}; padding: 1.5rem; border-radius: 16px; text-align: center; margin: 1rem 0;">
            <h3 style="color: white; margin: 0;">{t("ats_score")}</h3>
            <h1 style="color: white; margin: 8px 0; font-size: 3rem;">{score}/100</h1>
            <p style="color: white; margin: 0; font-size: 1rem;">
                {score_text}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        sim = results.get('semantic_similarity', 0)
        st.markdown(f"""
        <div style="background: #f0f4ff; padding: 1.5rem; border-radius: 16px; text-align: center; margin: 1rem 0; border: 2px solid #667eea;">
            <h3 style="color: #667eea; margin: 0;">{t("semantic_match")}</h3>
            <h1 style="color: #667eea; margin: 8px 0; font-size: 3rem;">{sim*100:.0f}%</h1>
            <p style="color: #888; margin: 0; font-size: 0.9rem;">{t("content_relevance_desc")}</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        fit = results.get('job_fit', {})
        fit_score = fit.get('overall_fit', 0)
        fit_level = fit.get('fit_level', 'N/A')
        # Translate fit level if it exists in translation catalog
        fit_level_translated = t(f"fit_level_{fit_level.lower().replace(' ', '_')}")
        if fit_level_translated == f"fit_level_{fit_level.lower().replace(' ', '_')}":
            fit_level_translated = fit_level # Fallback
            
        st.markdown(f"""
        <div style="background: #f0fff0; padding: 1.5rem; border-radius: 16px; text-align: center; margin: 1rem 0; border: 2px solid #00c851;">
            <h3 style="color: #00c851; margin: 0;">{t("job_fit")}</h3>
            <h1 style="color: #00c851; margin: 8px 0; font-size: 3rem;">{fit_score:.0f}%</h1>
            <p style="color: #888; margin: 0; font-size: 0.9rem;">{fit_level_translated}</p>
        </div>
        """, unsafe_allow_html=True)

    # Component scores breakdown
    component_scores = results.get('component_scores', {})
    if component_scores:
        st.markdown(f"### {t('score_breakdown')}")
        cols = st.columns(5)
        score_labels = {
            'semantic_relevance': t('relevance_label'),
            'keyword_match': t('keywords_label'),
            'section_completeness': t('sections_label'),
            'experience_match': t('experience_label'),
            'quantified_achievements': t('metrics_label'),
        }
        for i, (key, label) in enumerate(score_labels.items()):
            if key in component_scores:
                with cols[i % 5]:
                    st.metric(label, f"{component_scores[key]:.0f}/100")

    # Recruiter Red Flags Warning
    ai_analysis = results.get('ai_analysis', {})
    sections = ai_analysis.get('sections', {})
    red_flags = sections.get('red_flags', '')
    if red_flags:
        st.markdown(f"### {t('red_flags_title')}")
        st.error(red_flags)

    # Detailed breakdown
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"### {t('matched_keywords')}")
        matched_keywords = results.get('matched_keywords', [])
        missing_keywords = results.get('missing_keywords', [])

        if matched_keywords:
            for keyword in matched_keywords[:10]:
                st.markdown(f"- {keyword}")
        else:
            st.info(t("no_matched_keywords"))

        if missing_keywords:
            st.markdown(f"### {t('missing_keywords')}")
            for keyword in missing_keywords[:10]:
                st.markdown(f"- **{keyword}**")

    with col2:
        st.markdown(f"### {t('improvement_areas')}")
        suggestions = results.get('suggestions', [])
        for i, suggestion in enumerate(suggestions[:6], 1):
            priority_color = {'high': '#ff4444', 'medium': '#ffa500', 'low': '#00c851'}.get(
                suggestion.get('priority', 'medium'), '#667eea'
            )
            # Try to translate suggestion title / description if key exists, but usually dynamically computed in French/English by ollama or ats simulator. We display as is.
            st.markdown(f"""
            <div class="improvement-box" style="border-left-color: {priority_color};">
                <strong>{i}. {suggestion['title']}</strong><br>
                {suggestion['description']}
            </div>
            """, unsafe_allow_html=True)

    # Experience & Education Analysis
    exp = results.get('experience_analysis', {})
    edu = results.get('education_analysis', {})

    if exp or edu:
        st.markdown(f"### {t('requirements_match')}")
        col1, col2 = st.columns(2)

        with col1:
            if exp:
                req = exp.get('required_years')
                cv = exp.get('stated_years') or exp.get('timeline_years')
                status_key = "status_met" if exp.get('score', 0) >= 70 else "status_gap"
                status = t(status_key)
                req_text = f" ({t('required')}: {req}+)" if req else ''
                st.markdown(f"**[{status}] {t('experience_label')}:** {cv or 'N/A'} {t('years_label')}{req_text}")

        with col2:
            if edu:
                req = edu.get('required_level', 'N/A')
                cv = edu.get('cv_level', 'N/A')
                status_key = "status_met" if edu.get('score', 0) >= 70 else "status_gap"
                status = t(status_key)
                req_text = f" ({t('required')}: {req})" if req and req != 'N/A' else ''
                st.markdown(f"**[{status}] {t('education_label')}:** {cv or 'N/A'}{req_text}")

    # Transferable skills
    fit = results.get('job_fit', {})
    transferable = fit.get('transferable_skills', [])
    if transferable:
        st.markdown(f"### {t('transferable_skills')}")
        for ts in transferable[:5]:
            st.markdown(t("transferable_skill_relates", your_skill=ts['your_skill'], job_needs=ts['job_needs']))

    # AI Analysis
    ai = results.get('ai_analysis', {})
    ai_text = ai.get('analysis_text', '')
    if ai_text:
        if 'unavailable' in ai_text.lower() or 'error' in ai_text.lower():
            st.warning(t("ollama_warning"))
        else:
            with st.expander(t("ai_analysis_title"), expanded=False):
                st.markdown(ai_text)

    # Call to action
    st.markdown("---")
    st.info(t("next_step_rewriter"))


def show_chat_page():
    """Display the chat interface"""

    st.markdown(f"## {t('chat_title')}")

    if not st.session_state.cv_text:
        st.warning(t("please_upload_analyze_first"))
        return

    chat_interface = ChatInterface()

    # Display chat history
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.chat_message("user").write(message['content'])
        else:
            st.chat_message("assistant").write(message['content'])

    # Chat input
    if prompt := st.chat_input(t("chat_input_placeholder")):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):
            with st.spinner(t("thinking_spinner")):
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
                    error_msg = t("chat_error", error=str(e))
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})


def show_analytics_page():
    """Display the analytics dashboard"""

    st.markdown(f"## {t('Analytics Dashboard')}")

    if not st.session_state.analysis_results:
        st.warning(t("please_analyze_first"))
        return

    analytics_dashboard = AnalyticsDashboard()
    analytics_dashboard.display(st.session_state.analysis_results)


def show_settings_page():
    """Display the settings page"""

    st.markdown(f"## {t('Settings')}")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"### {t('ai_model_settings')}")

        try:
            ollama_client = OllamaClient()
            available = ollama_client.get_available_models()
            if available:
                if 'selected_model' not in st.session_state:
                    st.session_state['selected_model'] = available[0]
                
                if st.session_state['selected_model'] not in available:
                    st.session_state['selected_model'] = available[0]
                    
                default_idx = available.index(st.session_state['selected_model'])
                model_name = st.selectbox(t("choose_ai_model"), available, index=default_idx, key="settings_model_selector")
                if model_name != st.session_state['selected_model']:
                    st.session_state['selected_model'] = model_name
                    st.rerun()
            else:
                st.selectbox(
                    t("choose_ai_model"),
                    ["llama3.2", "mistral", "codellama", "neural-chat"],
                    disabled=True
                )
        except Exception:
            st.selectbox(
                t("choose_ai_model"),
                ["llama3.2", "mistral", "codellama", "neural-chat"],
                disabled=True
            )

        temperature = st.slider(
            t("response_creativity"),
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            help=t("creativity_help")
        )

    with col2:
        st.markdown(f"### {t('interface_settings')}")

        st.info(t("theme_info"))

        show_advanced = st.checkbox(
            t("show_advanced"),
            help=t("advanced_help")
        )

    st.markdown(f"### {t('data_management')}")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button(t("export_analysis_btn")):
            if st.session_state.get('analysis_results'):
                import json
                analysis_json = json.dumps(
                    {k: v for k, v in st.session_state.analysis_results.items()
                     if k not in ('cv_text', 'job_description')},
                     indent=2, default=str
                )
                st.download_button(
                    t("download_json_btn"),
                    analysis_json,
                    file_name="cv_analysis.json",
                    mime="application/json",
                )
            else:
                st.info(t("no_analysis_export"))

    with col2:
        if st.button(t("clear_session_btn")):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success(t("session_cleared"))
            st.rerun()

    with col3:
        if st.button(t("help_support_btn")):
            st.info(t("contact_support_desc"))


if __name__ == "__main__":
    main()
