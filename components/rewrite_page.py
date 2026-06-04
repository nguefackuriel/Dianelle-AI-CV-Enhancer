"""
CV Rewrite Page Component
Interactive UI for AI-powered CV rewriting with before/after comparison.
"""

import streamlit as st
from typing import Dict, List, Any
from utils.rewrite_engine import RewriteEngine


class RewritePage:
    """Interactive CV rewriting interface."""

    def __init__(self):
        self.rewrite_engine = RewriteEngine()

    def display(self):
        """Display the rewrite page."""
        st.markdown("## AI CV Rewriter — Powered by Dianelle")
        st.markdown(
            "*Transform your CV into an ATS-optimized powerhouse. "
            "Dianelle rewrites your sections while keeping everything truthful.*"
        )

        # Check prerequisites
        if not st.session_state.get('cv_text'):
            st.warning("Please upload and analyze your CV first on the **CV Analysis** page!")
            return

        if not st.session_state.get('analysis_results'):
            st.warning("Please run the CV analysis first to get personalized rewrites!")
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
            "Section Rewriter",
            "Bullet Optimizer",
            "Summary Generator",
            "Skills Optimizer",
            "Weak Language Scan",
            "Quantification Helper",
            "ATS & Recruiter Double Test",
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
                <h3 style="margin:0; color:white;">Current ATS Score</h3>
                <h1 style="margin:0; color:white;">{score}/100</h1>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            missing = len(analysis.get('missing_keywords', []))
            st.metric("Missing Keywords", missing, delta=f"-{missing}" if missing else "0")

        with col3:
            improvement = 100 - score
            st.metric("Improvement Potential", f"+{improvement} pts",
                       delta=f"{improvement} points available")

    # ------------------------------------------------------------------
    # Section Rewriter
    # ------------------------------------------------------------------

    def _section_rewriter(self, parsed_sections: Dict, job_description: str,
                          missing_keywords: List[str], cv_text: str):
        """Section-by-section rewriting interface."""
        st.markdown("### Section-by-Section Rewriter")
        st.markdown("Select sections to rewrite. Dianelle will optimize each one for ATS compatibility.")

        if not parsed_sections or len(parsed_sections) <= 1:
            st.info("No distinct sections detected. Using full CV text instead.")
            parsed_sections = {'full_cv': cv_text}

        # Section selection
        available_sections = [s for s in parsed_sections.keys() if s not in ('header', 'contact')]
        if not available_sections:
            available_sections = list(parsed_sections.keys())

        selected_sections = st.multiselect(
            "Choose sections to rewrite:",
            available_sections,
            default=available_sections[:2] if len(available_sections) >= 2 else available_sections,
        )

        col1, col2 = st.columns([1, 1])
        with col1:
            tone = st.selectbox("Tone:", ["professional", "confident", "concise"])
        with col2:
            st.markdown(f"**Missing keywords to inject:** {', '.join(missing_keywords[:8]) if missing_keywords else 'None'}")

        if st.button("Rewrite Selected Sections", type="primary", use_container_width=True):
            if not selected_sections:
                st.warning("Please select at least one section.")
                return

            with st.spinner("Dianelle is rewriting your CV sections..."):
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
        st.markdown("### Rewrite Results")

        for section_name, result in results.items():
            with st.expander(f"{section_name.replace('_', ' ').title()}", expanded=True):
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Original**")
                    st.text_area(
                        "Original",
                        result['original'],
                        height=200,
                        disabled=True,
                        key=f"orig_{section_name}",
                        label_visibility="collapsed",
                    )

                with col2:
                    st.markdown("**Enhanced**")
                    edited = st.text_area(
                        "Enhanced",
                        result['rewritten'],
                        height=200,
                        key=f"new_{section_name}",
                        label_visibility="collapsed",
                    )

                # Changes summary
                if result['changes_made']:
                    st.markdown("**Changes made:**")
                    for change in result['changes_made']:
                        st.markdown(f"- {change}")

                if result['keywords_added']:
                    st.success(f"Keywords added: {', '.join(result['keywords_added'])}")

                # Action buttons
                bcol1, bcol2, bcol3 = st.columns(3)
                with bcol1:
                    if st.button("Accept", key=f"accept_{section_name}"):
                        if 'accepted_rewrites' not in st.session_state:
                            st.session_state['accepted_rewrites'] = {}
                        st.session_state['accepted_rewrites'][section_name] = edited
                        st.success(f"Accepted rewrite for {section_name}!")

                with bcol2:
                    if st.button("Reject", key=f"reject_{section_name}"):
                        st.info(f"Keeping original {section_name}.")

                with bcol3:
                    if st.button("Re-generate", key=f"regen_{section_name}"):
                        st.info("Re-generating... Please click 'Rewrite Selected Sections' again.")

        # Apply All button
        st.markdown("---")
        if st.button("Accept All Rewrites", type="primary", use_container_width=True):
            if 'accepted_rewrites' not in st.session_state:
                st.session_state['accepted_rewrites'] = {}
            for section_name, result in results.items():
                st.session_state['accepted_rewrites'][section_name] = result['rewritten']
            st.success("All rewrites accepted! Go to **Export** to download your enhanced CV.")
            st.balloons()

    # ------------------------------------------------------------------
    # Bullet Optimizer
    # ------------------------------------------------------------------

    def _bullet_optimizer(self, cv_text: str, job_description: str):
        """Optimize individual bullet points."""
        st.markdown("### Bullet Point Optimizer")
        st.markdown("Paste bullet points from your experience section to optimize them individually.")

        bullets_input = st.text_area(
            "Enter your bullet points (one per line):",
            height=200,
            placeholder="- Responsible for managing the team\n- Helped with project delivery\n- Worked on improving processes",
        )

        if st.button("Optimize Bullets", type="primary"):
            if not bullets_input.strip():
                st.warning("Please enter some bullet points.")
                return

            with st.spinner("Optimizing bullet points..."):
                results = self.rewrite_engine.optimize_bullets(bullets_input, job_description)
                st.session_state['bullet_optimizer_results'] = results

        if 'bullet_optimizer_results' in st.session_state:
            results = st.session_state['bullet_optimizer_results']
            for i, result in enumerate(results, 1):
                with st.container():
                    st.markdown(f"**Bullet #{i}**")
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"*Original:* {result['original']}")

                    with col2:
                        st.markdown(f"*Optimized:* {result['optimized']}")

                    if result['improvement_notes']:
                        for note in result['improvement_notes']:
                            st.caption(f"{note}")

                    st.markdown("---")

    # ------------------------------------------------------------------
    # Summary Generator
    # ------------------------------------------------------------------

    def _summary_generator(self, cv_text: str, job_description: str, analysis: Dict):
        """Generate professional summary."""
        st.markdown("### Professional Summary Generator")
        st.markdown("Generate an ATS-optimized professional summary tailored to the job.")

        col1, col2 = st.columns(2)
        with col1:
            years = st.number_input("Years of Experience:", min_value=0, max_value=50, value=5)
        with col2:
            st.info("A strong summary is one of the most impactful ATS elements.")

        if st.button("Generate Summary", type="primary"):
            with st.spinner("Crafting your professional summary..."):
                summary = self.rewrite_engine.generate_summary(cv_text, job_description, years)
                st.session_state['generated_summary_result'] = summary

        if 'generated_summary_result' in st.session_state:
            st.markdown("**Generated Professional Summary:**")
            edited_summary = st.text_area(
                "Edit your summary:",
                st.session_state['generated_summary_result'],
                height=120,
                key="generated_summary_edit",
            )

            if st.button("Use This Summary", key="use_summary_btn"):
                if 'accepted_rewrites' not in st.session_state:
                    st.session_state['accepted_rewrites'] = {}
                st.session_state['accepted_rewrites']['summary'] = edited_summary
                st.success("Summary saved!")

    # ------------------------------------------------------------------
    # Skills Optimizer
    # ------------------------------------------------------------------

    def _skills_optimizer(self, parsed_sections: Dict, job_description: str, analysis: Dict):
        """Optimize skills section."""
        st.markdown("### Skills Section Optimizer")
        st.markdown("Reorganize and optimize your skills to match the job requirements.")

        current_skills = parsed_sections.get('skills', '')
        if not current_skills:
            current_skills = st.text_area(
                "Enter your current skills:",
                height=150,
                placeholder="Python, Java, SQL, Project Management, Team Leadership...",
            )

        matched = analysis.get('technical_skills_match', [])
        missing = analysis.get('missing_technical_skills', [])

        if missing:
            st.warning(f"Missing technical skills: {', '.join(missing[:10])}")

        if st.button("Optimize Skills", type="primary"):
            if not current_skills:
                st.warning("Please enter your skills.")
                return

            with st.spinner("Optimizing skills section..."):
                result = self.rewrite_engine.optimize_skills(
                    current_skills, job_description, matched, missing
                )
                st.session_state['optimized_skills_result'] = result

        if 'optimized_skills_result' in st.session_state:
            result = st.session_state['optimized_skills_result']
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Current Skills**")
                st.text_area("Current", result['original'], height=200,
                             disabled=True, key="skills_orig", label_visibility="collapsed")
            with col2:
                st.markdown("**Optimized Skills**")
                edited = st.text_area("Optimized", result['optimized'], height=200,
                                       key="skills_new", label_visibility="collapsed")

            if result['skills_added']:
                st.success(f"Skills integrated: {', '.join(result['skills_added'])}")

            if st.button("Accept Skills", key="accept_skills_btn"):
                if 'accepted_rewrites' not in st.session_state:
                    st.session_state['accepted_rewrites'] = {}
                st.session_state['accepted_rewrites']['skills'] = edited
                st.success("Skills section saved!")

    # ------------------------------------------------------------------
    # Weak Language Scan
    # ------------------------------------------------------------------

    def _weak_language_scan(self, cv_text: str):
        """Scan for and highlight weak language."""
        st.markdown("### Weak Language Scanner")
        st.markdown("Find and replace passive, weak language with powerful action-driven alternatives.")

        if st.button("Scan CV", type="primary"):
            with st.spinner("Scanning CV..."):
                findings = self.rewrite_engine.detect_weak_language(cv_text)
                st.session_state['weak_language_results'] = findings
                st.session_state['weak_language_scanned'] = True

        if st.session_state.get('weak_language_scanned'):
            findings = st.session_state.get('weak_language_results', [])
            if not findings:
                st.success("Great job! No weak language patterns detected.")
                return

            st.warning(f"Found {len(findings)} weak phrase(s) to improve:")

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
        st.markdown("### Achievement Quantification Helper")
        st.markdown("Identify vague statements and get prompts to add impactful metrics.")

        if st.button("Find Quantification Opportunities", type="primary"):
            with st.spinner("Scanning for metrics..."):
                suggestions = self.rewrite_engine.suggest_quantification(cv_text)
                st.session_state['quantification_results'] = suggestions
                st.session_state['quantification_scanned'] = True

        if st.session_state.get('quantification_scanned'):
            suggestions = st.session_state.get('quantification_results', [])
            if not suggestions:
                st.success("Your CV already has good quantification!")
                return

            st.info(f"Found {len(suggestions)} statements that could be strengthened with numbers:")

            for i, suggestion in enumerate(suggestions, 1):
                with st.container():
                    st.markdown(f"""
                    <div style="padding: 0.8rem; border-left: 4px solid #2196F3; background: #f3f9ff; margin: 0.5rem 0; border-radius: 4px;">
                        <strong>Statement:</strong> {suggestion['original_line']}<br>
                        <span style="color: #1565C0;"><strong>{suggestion['question']}</strong></span>
                    </div>
                    """, unsafe_allow_html=True)

                    user_input = st.text_input(
                        f"Add your metric:",
                        key=f"quant_{i}",
                        placeholder="e.g., 25%, $50K, 10 team members",
                    )

    # ------------------------------------------------------------------
    # ATS & Recruiter Double Test
    # ------------------------------------------------------------------

    def _double_test_tab(self, cv_text: str, job_description: str):
        """Step 3 Double Test scan (ATS filter + human recruiter 200-CV scanner)."""
        st.markdown("### ATS & Recruiter Double Test Scan")
        st.markdown(
            "This scanner analyzes your CV against the job description simultaneously from the perspective of "
            "an automated ATS parsing filter and a tired human recruiter reviewing 200 CVs in a row."
        )
        
        cv_to_scan = cv_text
        if st.session_state.get('accepted_rewrites'):
            st.info("Applying your accepted rewrites to the scanned CV text for an accurate assessment.")
            merged_parts = []
            parsed_sections = st.session_state['analysis_results'].get('parsed_sections', {})
            for sec_name, sec_content in parsed_sections.items():
                if sec_name in st.session_state['accepted_rewrites']:
                    merged_parts.append(f"## {sec_name.upper()}\n{st.session_state['accepted_rewrites'][sec_name]}")
                else:
                    merged_parts.append(f"## {sec_name.upper()}\n{sec_content}")
            cv_to_scan = "\n\n".join(merged_parts)

        if st.button("Run Double Test Scan", type="primary", key="run_double_test_btn"):
            if not job_description:
                st.warning("Please add a job description first.")
                return
                
            with st.spinner("Pressure testing your CV against ATS and recruiters..."):
                try:
                    if self.rewrite_engine.ollama_client.is_connected():
                        result = self.rewrite_engine.ollama_client.run_double_test_scan(cv_to_scan, job_description)
                        st.session_state['double_test_scan_result'] = result
                    else:
                        st.error("Ollama is disconnected. Unable to run scan.")
                except Exception as e:
                    st.error(f"Error running scan: {str(e)}")

        if 'double_test_scan_result' in st.session_state:
            st.markdown("#### Double Test Diagnostic Results:")
            st.markdown(st.session_state['double_test_scan_result'])
