"""
CV Rewrite Page Component
Interactive UI for AI-powered CV rewriting with before/after comparison.
"""

import streamlit as st
from typing import Dict, List, Any
from utils.rewrite_engine import RewriteEngine
from utils.translations import t


class RewritePage:
    """Interactive CV rewriting interface."""

    def __init__(self):
        self.rewrite_engine = RewriteEngine()

    def display(self):
        """Display the rewrite page."""
        st.markdown(f"## {t('rewrite_title')}")
        st.markdown(t('rewrite_subtitle'))

        # Check prerequisites
        if not st.session_state.get('cv_text'):
            st.warning(t("please_upload_analyze_first_rewrite"))
            return

        if not st.session_state.get('analysis_results'):
            st.warning(t("please_run_analysis_first"))
            return

        cv_text = st.session_state['cv_text']
        analysis = st.session_state['analysis_results']
        job_description = st.session_state.get('job_description', '')
        parsed_sections = analysis.get('parsed_sections', {})
        missing_keywords = analysis.get('missing_keywords', [])

        # Display current score context
        self._display_score_context(analysis)

        st.markdown("---")

        # Tab layout for different rewrite features
        tabs = st.tabs([
            t("tab_section_rewriter"),
            t("tab_bullet_optimizer"),
            t("tab_summary_generator"),
            t("tab_skills_optimizer"),
            t("tab_weak_language_scan"),
            t("tab_quantification_helper"),
            t("tab_double_test"),
        ])

        with tabs[0]:
            self._section_rewriter(parsed_sections, job_description, missing_keywords, cv_text)

        with tabs[1]:
            self._bullet_optimizer(cv_text, job_description)

        with tabs[2]:
            self._summary_generator(cv_text, job_description, analysis)

        with tabs[3]:
            self._skills_optimizer(parsed_sections, job_description, analysis)

        with tabs[4]:
            self._weak_language_scan(cv_text)

        with tabs[5]:
            self._quantification_helper(cv_text)

        with tabs[6]:
            self._double_test_tab(cv_text, job_description)

    # ------------------------------------------------------------------
    # Score Context
    # ------------------------------------------------------------------

    def _display_score_context(self, analysis: Dict):
        """Show current score and what can be improved."""
        score = analysis.get('ats_score', 0)
        col1, col2, col3 = st.columns(3)

        with col1:
            score_color = "#00c851" if score >= 80 else "#ffa500" if score >= 60 else "#ff4b4b"
            st.markdown(f"""
            <div style="background: {score_color}; padding: 1rem; border-radius: 10px; text-align: center; color: white;">
                <h3 style="margin:0; color:white;">{t('current_ats_score')}</h3>
                <h1 style="margin:0; color:white;">{score}/100</h1>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            missing = len(analysis.get('missing_keywords', []))
            st.metric(t("missing_keywords"), missing, delta=f"-{missing}" if missing else "0")

        with col3:
            improvement = 100 - score
            st.metric(t("improvement_potential"), f"+{improvement} pts",
                       delta=t("points_available", improvement=improvement))

    # ------------------------------------------------------------------
    # Section Rewriter
    # ------------------------------------------------------------------

    def _section_rewriter(self, parsed_sections: Dict, job_description: str,
                          missing_keywords: List[str], cv_text: str):
        """Section-by-section rewriting interface."""
        st.markdown(f"### {t('section_rewriter_title')}")
        st.markdown(t('section_rewriter_desc'))

        if not parsed_sections or len(parsed_sections) <= 1:
            st.info(t('no_distinct_sections'))
            parsed_sections = {'full_cv': cv_text}

        # Section selection
        available_sections = [s for s in parsed_sections.keys() if s not in ('header', 'contact')]
        if not available_sections:
            available_sections = list(parsed_sections.keys())

        selected_sections = st.multiselect(
            t("choose_sections_to_rewrite"),
            available_sections,
            default=available_sections[:2] if len(available_sections) >= 2 else available_sections,
        )

        col1, col2 = st.columns([1, 1])
        with col1:
            tone = st.selectbox(t("tone_label"), ["professional", "confident", "concise"])
        with col2:
            kws = ', '.join(missing_keywords[:8]) if missing_keywords else 'None'
            st.markdown(t("missing_keywords_to_inject", keywords=kws))

        if st.button(t("rewrite_selected_btn"), type="primary", use_container_width=True):
            if not selected_sections:
                st.warning(t("please_select_one_section"))
                return

            with st.spinner(t("dianelle_rewriting_spinner")):
                results = self.rewrite_engine.rewrite_all_sections(
                    {s: parsed_sections[s] for s in selected_sections},
                    job_description,
                    missing_keywords,
                    selected_sections,
                )

                st.session_state['rewrite_results'] = results

        # Display results
        if 'rewrite_results' in st.session_state:
            self._display_rewrite_results(st.session_state['rewrite_results'])

    def _display_rewrite_results(self, results: Dict[str, Dict]):
        """Display before/after comparison for each section."""
        st.markdown("---")
        st.markdown(f"### {t('rewrite_results_title')}")

        for section_name, result in results.items():
            with st.expander(f"{section_name.replace('_', ' ').title()}", expanded=True):
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"**{t('original')}**")
                    st.text_area(
                        t("original"),
                        result['original'],
                        height=200,
                        disabled=True,
                        key=f"orig_{section_name}",
                        label_visibility="collapsed",
                    )

                with col2:
                    st.markdown(f"**{t('enhanced')}**")
                    edited = st.text_area(
                        t("enhanced"),
                        result['rewritten'],
                        height=200,
                        key=f"new_{section_name}",
                        label_visibility="collapsed",
                    )

                # Changes summary
                if result['changes_made']:
                    st.markdown(f"**{t('changes_made')}**")
                    for change in result['changes_made']:
                        st.markdown(f"- {change}")

                if result['keywords_added']:
                    kws = ', '.join(result['keywords_added'])
                    st.success(t("keywords_added", keywords=kws))

                # Action buttons
                bcol1, bcol2, bcol3 = st.columns(3)
                with bcol1:
                    if st.button(t("accept_btn"), key=f"accept_{section_name}"):
                        if 'accepted_rewrites' not in st.session_state:
                            st.session_state['accepted_rewrites'] = {}
                        st.session_state['accepted_rewrites'][section_name] = edited
                        st.success(t("accepted_success", section=section_name))

                with bcol2:
                    if st.button(t("reject_btn"), key=f"reject_{section_name}"):
                        st.info(t("keeping_original", section=section_name))

                with bcol3:
                    if st.button(t("regenerate_btn"), key=f"regen_{section_name}"):
                        st.info(t("regenerating_info"))

        # Apply All button
        st.markdown("---")
        if st.button(t("accept_all_rewrites_btn"), type="primary", use_container_width=True):
            if 'accepted_rewrites' not in st.session_state:
                st.session_state['accepted_rewrites'] = {}
            for section_name, result in results.items():
                st.session_state['accepted_rewrites'][section_name] = result['rewritten']
            st.success(t("all_rewrites_accepted"))
            st.balloons()

    # ------------------------------------------------------------------
    # Bullet Optimizer
    # ------------------------------------------------------------------

    def _bullet_optimizer(self, cv_text: str, job_description: str):
        """Optimize individual bullet points."""
        st.markdown(f"### {t('bullet_optimizer_title')}")
        st.markdown(t('bullet_optimizer_desc'))

        bullets_input = st.text_area(
            t("enter_bullets"),
            height=200,
            placeholder="- Responsible for managing the team\n- Helped with project delivery\n- Worked on improving processes",
        )

        if st.button(t("optimize_bullets_btn"), type="primary"):
            if not bullets_input.strip():
                st.warning(t("please_enter_bullets"))
                return

            with st.spinner(t("optimizing_bullets_spinner")):
                results = self.rewrite_engine.optimize_bullets(bullets_input, job_description)
                st.session_state['bullet_optimizer_results'] = results

        if 'bullet_optimizer_results' in st.session_state:
            results = st.session_state['bullet_optimizer_results']
            for i, result in enumerate(results, 1):
                with st.container():
                    st.markdown(f"**Bullet #{i}**")
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(t("bullet_original", text=result['original']))

                    with col2:
                        st.markdown(t("bullet_optimized", text=result['optimized']))

                    if result['improvement_notes']:
                        for note in result['improvement_notes']:
                            st.caption(f"{note}")

                    st.markdown("---")

    # ------------------------------------------------------------------
    # Summary Generator
    # ------------------------------------------------------------------

    def _summary_generator(self, cv_text: str, job_description: str, analysis: Dict):
        """Generate professional summary."""
        st.markdown(f"### {t('summary_generator_title')}")
        st.markdown(t('summary_generator_desc'))

        col1, col2 = st.columns(2)
        with col1:
            years = st.number_input(t("years_exp"), min_value=0, max_value=50, value=5)
        with col2:
            st.info(t("summary_info"))

        if st.button(t("generate_summary_btn"), type="primary"):
            with st.spinner(t("generating_summary_spinner")):
                summary = self.rewrite_engine.generate_summary(cv_text, job_description, years)
                st.session_state['generated_summary_result'] = summary

        if 'generated_summary_result' in st.session_state:
            st.markdown(t("generated_summary_title"))
            edited_summary = st.text_area(
                t("edit_summary"),
                st.session_state['generated_summary_result'],
                height=120,
                key="generated_summary_edit",
            )

            if st.button(t("use_summary_btn"), key="use_summary_btn"):
                if 'accepted_rewrites' not in st.session_state:
                    st.session_state['accepted_rewrites'] = {}
                st.session_state['accepted_rewrites']['summary'] = edited_summary
                st.success(t("summary_saved"))

    # ------------------------------------------------------------------
    # Skills Optimizer
    # ------------------------------------------------------------------

    def _skills_optimizer(self, parsed_sections: Dict, job_description: str, analysis: Dict):
        """Optimize skills section."""
        st.markdown(f"### {t('skills_optimizer_title')}")
        st.markdown(t('skills_optimizer_desc'))

        current_skills = parsed_sections.get('skills', '')
        if not current_skills:
            current_skills = st.text_area(
                t("enter_skills"),
                height=150,
                placeholder="Python, Java, SQL, Project Management, Team Leadership...",
            )

        matched = analysis.get('technical_skills_match', [])
        missing = analysis.get('missing_technical_skills', [])

        if missing:
            st.warning(t("missing_tech_skills", skills=', '.join(missing[:10])))

        if st.button(t("optimize_skills_btn"), type="primary"):
            if not current_skills:
                st.warning(t("please_enter_skills"))
                return

            with st.spinner(t("optimizing_skills_spinner")):
                result = self.rewrite_engine.optimize_skills(
                    current_skills, job_description, matched, missing
                )
                st.session_state['optimized_skills_result'] = result

        if 'optimized_skills_result' in st.session_state:
            result = st.session_state['optimized_skills_result']
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(t("current_skills_label"))
                st.text_area("Current", result['original'], height=200,
                             disabled=True, key="skills_orig", label_visibility="collapsed")
            with col2:
                st.markdown(t("optimized_skills_label"))
                edited = st.text_area("Optimized", result['optimized'], height=200,
                                       key="skills_new", label_visibility="collapsed")

            if result['skills_added']:
                st.success(t("skills_integrated", skills=', '.join(result['skills_added'])))

            if st.button(t("accept_skills_btn"), key="accept_skills_btn"):
                if 'accepted_rewrites' not in st.session_state:
                    st.session_state['accepted_rewrites'] = {}
                st.session_state['accepted_rewrites']['skills'] = edited
                st.success(t("skills_saved"))

    # ------------------------------------------------------------------
    # Weak Language Scan
    # ------------------------------------------------------------------

    def _weak_language_scan(self, cv_text: str):
        """Scan for and highlight weak language."""
        st.markdown(f"### {t('weak_language_title')}")
        st.markdown(t('weak_language_desc'))

        if st.button(t("scan_cv_btn"), type="primary"):
            with st.spinner(t("scanning_cv_spinner")):
                findings = self.rewrite_engine.detect_weak_language(cv_text)
                st.session_state['weak_language_results'] = findings
                st.session_state['weak_language_scanned'] = True

        if st.session_state.get('weak_language_scanned'):
            findings = st.session_state.get('weak_language_results', [])
            if not findings:
                st.success(t("no_weak_language"))
                return

            st.warning(t("weak_phrases_found", count=len(findings)))

            for i, finding in enumerate(findings, 1):
                with st.container():
                    st.markdown(f"""
                    <div style="padding: 0.8rem; border-left: 4px solid #ff6b6b; background: #fff5f5; margin: 0.5rem 0; border-radius: 4px;">
                        <strong>#{i}: "{finding['weak_phrase']}"</strong><br>
                        <span style="color: #666;">Context: {finding['context']}</span><br>
                        <span style="color: #2e7d32;">Try instead: <strong>{finding['suggestions']}</strong></span>
                    </div>
                    """, unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # Quantification Helper
    # ------------------------------------------------------------------

    def _quantification_helper(self, cv_text: str):
        """Help users add metrics to their achievements."""
        st.markdown(f"### {t('quant_helper_title')}")
        st.markdown(t('quant_helper_desc'))

        if st.button(t("find_quant_btn"), type="primary"):
            with st.spinner(t("scanning_metrics_spinner")):
                suggestions = self.rewrite_engine.suggest_quantification(cv_text)
                st.session_state['quantification_results'] = suggestions
                st.session_state['quantification_scanned'] = True

        if st.session_state.get('quantification_scanned'):
            suggestions = st.session_state.get('quantification_results', [])
            if not suggestions:
                st.success(t("good_quantification"))
                return

            st.info(t("quant_opportunities_found", count=len(suggestions)))

            for i, suggestion in enumerate(suggestions, 1):
                with st.container():
                    st.markdown(f"""
                    <div style="padding: 0.8rem; border-left: 4px solid #2196F3; background: #f3f9ff; margin: 0.5rem 0; border-radius: 4px;">
                        <strong>Statement:</strong> {suggestion['original_line']}<br>
                        <span style="color: #1565C0;"><strong>{suggestion['question']}</strong></span>
                    </div>
                    """, unsafe_allow_html=True)

                    user_input = st.text_input(
                        t("add_metric"),
                        key=f"quant_{i}",
                        placeholder="e.g., 25%, $50K, 10 team members",
                    )

    # ------------------------------------------------------------------
    # ATS & Recruiter Double Test
    # ------------------------------------------------------------------

    def _double_test_tab(self, cv_text: str, job_description: str):
        """Step 3 Double Test scan (ATS filter + human recruiter 200-CV scanner)."""
        st.markdown(f"### {t('double_test_title')}")
        st.markdown(t('double_test_desc'))
        
        cv_to_scan = cv_text
        if st.session_state.get('accepted_rewrites'):
            st.info(t("applying_rewrites_info"))
            merged_parts = []
            parsed_sections = st.session_state['analysis_results'].get('parsed_sections', {})
            for sec_name, sec_content in parsed_sections.items():
                if sec_name in st.session_state['accepted_rewrites']:
                    merged_parts.append(f"## {sec_name.upper()}\n{st.session_state['accepted_rewrites'][sec_name]}")
                else:
                    merged_parts.append(f"## {sec_name.upper()}\n{sec_content}")
            cv_to_scan = "\n\n".join(merged_parts)

        if st.button(t("run_double_test_btn"), type="primary", key="run_double_test_btn"):
            if not job_description:
                st.warning(t("please_add_jd_first"))
                return
                
            with st.spinner(t("double_test_spinner")):
                try:
                    if self.rewrite_engine.ollama_client.is_connected():
                        result = self.rewrite_engine.ollama_client.run_double_test_scan(cv_to_scan, job_description)
                        st.session_state['double_test_scan_result'] = result
                    else:
                        st.error(t("ollama_disconnected"))
                except Exception as e:
                    st.error(f"Error running scan: {str(e)}")

        if 'double_test_scan_result' in st.session_state:
            st.markdown(t("double_test_results"))
            st.markdown(st.session_state['double_test_scan_result'])
