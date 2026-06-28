"""
LinkedIn Profile Optimizer Component
Generate optimized LinkedIn headlines, summaries, and consistency checks following Hadrien's guidelines.
"""

import streamlit as st
import re
from typing import Dict, List, Any
from utils.ollama_client import OllamaClient
from utils.translations import t


class LinkedInOptimizer:
    """LinkedIn profile optimization interface."""

    def __init__(self):
        self.ollama_client = OllamaClient()

    def display(self):
        """Display the LinkedIn optimizer page."""
        st.markdown(f"## {t('linkedin_optimizer_title')}")
        st.markdown(t('linkedin_optimizer_subtitle'))

        if not st.session_state.get('cv_text'):
            st.warning(t("please_upload_first"))
            return

        cv_text = st.session_state['cv_text']
        job_description = st.session_state.get('job_description', '')
        analysis = st.session_state.get('analysis_results', {})
        parsed_sections = analysis.get('parsed_sections', {}) if analysis else {}

        tabs = st.tabs([
            t("tab_headline_optimizer"),
            t("tab_about_section"),
            t("tab_experience_optimizer"),
            t("tab_skills_featured"),
            t("tab_consistency_check"),
        ])

        with tabs[0]:
            self._headline_generator(cv_text, job_description)
        with tabs[1]:
            self._about_section_writer(cv_text, job_description)
        with tabs[2]:
            self._experience_optimizer(parsed_sections, job_description)
        with tabs[3]:
            self._skills_featured_optimizer(cv_text, job_description)
        with tabs[4]:
            self._consistency_checker(cv_text)

    # ------------------------------------------------------------------
    # Headline Generator
    # ------------------------------------------------------------------

    def _headline_generator(self, cv_text: str, job_description: str):
        """Generate LinkedIn headlines under 220 chars."""
        st.markdown(f"### {t('linkedin_headline_optimizer')}")
        st.markdown(t('linkedin_headline_desc'))

        col1, col2 = st.columns(2)
        with col1:
            current_title = st.text_input(t("current_job_title_label"), placeholder="e.g., Software Engineer")
        with col2:
            target_title = st.text_input(t("target_job_title_label"), placeholder="e.g., Senior Data Scientist")

        if st.button(t("generate_headlines_btn"), type="primary", key="gen_headlines"):
            with st.spinner(t("crafting_headlines_spinner")):
                headlines = self._generate_headlines(
                    cv_text, current_title, target_title, job_description
                )
                st.session_state['linkedin_headlines'] = headlines

        if 'linkedin_headlines' in st.session_state:
            st.markdown(t("choose_favorite_title"))
            for i, headline in enumerate(st.session_state['linkedin_headlines'], 1):
                char_count = len(headline)
                color = "#2e7d32" if char_count <= 220 else "#f44336"
                st.markdown(f"""
                <div style="padding: 0.8rem; border: 1px solid #e0e0e0; border-radius: 8px; margin: 0.5rem 0; background-color: #fafafa;">
                    <strong>{i}.</strong> {headline}
                    <span style="color: {color}; float: right; font-size: 0.8rem; font-weight: bold;">{char_count}/220 {t('chars_label')}</span>
                </div>
                """, unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # About Section Writer
    # ------------------------------------------------------------------

    def _about_section_writer(self, cv_text: str, job_description: str):
        """Generate LinkedIn About section based on Hadrien's 3-paragraph rule."""
        st.markdown(f"### {t('about_section_writer')}")
        st.markdown(t('about_section_desc'))

        if st.button(t("generate_about_btn"), type="primary", key="gen_about"):
            with st.spinner(t("writing_about_spinner")):
                about = self._generate_about_section(cv_text, job_description)
                st.session_state['linkedin_about'] = about

        if 'linkedin_about' in st.session_state:
            edited = st.text_area(t("edit_about_label"), st.session_state['linkedin_about'], height=300, key="about_edit")

            char_count = len(edited)
            color = "#2e7d32" if char_count <= 2600 else "#f44336"
            st.caption(f"{t('character_count_label')} <span style='color:{color}'>{char_count}/2,600</span>",
                       unsafe_allow_html=True)

            st.download_button(
                t("download_about_btn"),
                edited,
                file_name="linkedin_about.txt",
                mime="text/plain",
            )

    # ------------------------------------------------------------------
    # Experience Optimizer
    # ------------------------------------------------------------------

    def _experience_optimizer(self, parsed_sections: Dict[str, str], job_description: str):
        """Optimize experiences for LinkedIn (Google XYZ + conversational + what was learned)."""
        st.markdown(f"### {t('experience_optimizer_title_li')}")
        st.markdown(t('experience_optimizer_desc_li'))

        current_exp = parsed_sections.get('experience', '')
        if not current_exp:
            st.info(t("no_parsed_experience_info"))

        exp_to_optimize = st.text_area(
            t("current_experience_label"),
            value=current_exp,
            height=200,
            placeholder="Paste your job details here..."
        )

        if st.button(t("optimize_experience_btn"), type="primary", key="optimize_exp_btn"):
            if not exp_to_optimize.strip():
                st.warning("Please paste your experience section first.")
                return
            with st.spinner(t("optimizing_experiences_spinner")):
                try:
                    if self.ollama_client.is_connected():
                        optimized = self.ollama_client.generate_linkedin_experience(exp_to_optimize, job_description)
                        st.session_state['linkedin_optimized_experience'] = optimized
                    else:
                        st.error("Ollama is disconnected. Unable to generate optimized experiences.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

        if 'linkedin_optimized_experience' in st.session_state:
            st.markdown(f"**{t('optimized_experience_title_li')}**")
            edited_exp = st.text_area(
                t("edit_optimized_experience_label"),
                st.session_state['linkedin_optimized_experience'],
                height=300,
                key="edit_optimized_exp"
            )
            st.download_button(
                t("download_experiences_btn"),
                edited_exp,
                file_name="linkedin_experience.txt",
                mime="text/plain"
            )

    # ------------------------------------------------------------------
    # Skills & Featured
    # ------------------------------------------------------------------

    def _skills_featured_optimizer(self, cv_text: str, job_description: str):
        """Suggest pinned skills and Featured section items."""
        st.markdown(f"### {t('skills_featured_title')}")
        st.markdown(t('skills_featured_desc'))

        if st.button(t("generate_recommendations_btn"), type="primary", key="gen_skills_featured"):
            with st.spinner(t("generating_recommendations_spinner")):
                try:
                    if self.ollama_client.is_connected():
                        recommendations = self.ollama_client.generate_linkedin_skills_featured(cv_text, job_description)
                        st.session_state['linkedin_skills_featured'] = recommendations
                    else:
                        st.error("Ollama is disconnected.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

        if 'linkedin_skills_featured' in st.session_state:
            st.markdown(st.session_state['linkedin_skills_featured'])

    # ------------------------------------------------------------------
    # Consistency Checker
    # ------------------------------------------------------------------

    def _consistency_checker(self, cv_text: str):
        """Check CV-LinkedIn consistency."""
        st.markdown(f"### {t('consistency_check_title')}")
        st.markdown(t('consistency_check_desc'))

        linkedin_text = st.text_area(
            t("paste_linkedin_label"),
            height=200,
            placeholder="Paste your LinkedIn About section or job details here...",
        )

        if st.button(t("check_consistency_btn"), type="primary", key="check_consistency"):
            if not linkedin_text.strip():
                st.warning("Please paste your LinkedIn text.")
                return

            with st.spinner(t("checking_consistency_spinner")):
                issues = self._check_consistency(cv_text, linkedin_text)
                st.session_state['linkedin_consistency_issues'] = issues
                st.session_state['linkedin_consistency_checked'] = True

        if st.session_state.get('linkedin_consistency_checked'):
            issues = st.session_state.get('linkedin_consistency_issues', [])
            if not issues:
                st.success(t("linkedin_consistency_success"))
            else:
                st.warning(t("linkedin_inconsistencies_found", count=len(issues)))
                for issue in issues:
                    st.markdown(f"""
                    <div style="padding: 0.5rem; border-left: 3px solid #ff9800; background: #fff3e0; margin: 0.3rem 0; border-radius: 4px;">
                        {issue}
                    </div>
                    """, unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # AI Generation Methods
    # ------------------------------------------------------------------

    def _generate_headlines(self, cv_text: str, current_title: str,
                            target_title: str, job_description: str) -> List[str]:
        """Generate LinkedIn headlines under 220 chars."""
        prompt = f"""Generate 3 compelling LinkedIn headlines (max 220 chars each).

Current title: {current_title or 'Professional'}
Target title: {target_title or current_title or 'Professional'}
CV highlights: {cv_text[:800]}
Target role: {job_description[:400]}

Requirements:
1. Max 220 characters each
2. Prioritize relevant keywords recruiters search for
3. Show value proposition and results/specialties, not just job titles
4. Use | or • as separators
5. Do NOT include any emojis

Output exactly 3 headlines, one per line:"""

        try:
            if self.ollama_client.is_connected():
                response = self.ollama_client.generate_response(prompt, temperature=0.6, max_tokens=400)
                headlines = []
                for l in response.strip().split('\n'):
                    l = l.strip()
                    if not l:
                        continue
                    clean = re.sub(r'^(?:option\s*\d*[:.-]*|headline\s*\d*[:.-]*|\d+[:.-]*)\s*', '', l, flags=re.IGNORECASE).strip()
                    if clean.lower().startswith((
                        "here are", "sure,", "below are", "i've generated", "i have generated", 
                        "here's", "here is", "these headline", "these options", "as a", "note"
                    )):
                        continue
                    if clean.endswith(':'):
                        continue
                    if len(clean) > 10:
                        if len(clean) > 220:
                            clean = clean[:217].rsplit(' ', 1)[0] + '...'
                        headlines.append(clean)
                if headlines:
                    return headlines[:3]
        except Exception:
            pass

        title = target_title or current_title or "Professional"
        return [
            f"{title} | Driving Results Through Innovation & Leadership | PMP Certified",
            f"{title} • Specializing in Scalable Solutions & Team Mentorship",
            f"Results-Driven {title} | Building High-Performance Teams & Optimizing Workflows",
        ]

    def _generate_about_section(self, cv_text: str, job_description: str) -> str:
        """Generate LinkedIn About section following Hadrien's 3-paragraph rule."""
        prompt = f"""Write a LinkedIn About section (max 1500 chars) based on the candidate's CV and target role.

CV: {cv_text[:1500]}
Target role: {job_description[:500]}

Rules (Hadrien's 3-paragraph formula):
1. Write in the first person.
2. Structure exactly in 3 short paragraphs:
   - Paragraph 1: An attention-grabbing hook. DO NOT use generic openings like "Passionné par..." or "Experienced professional with...". Hook the reader with a strong statement or central problem you solve.
   - Paragraph 2: A summary of your professional journey and 2-3 metric-driven achievements from your CV.
   - Paragraph 3: A clear Call to Action (CTA) explaining who you are looking to connect with or what opportunities you are open to.
3. Keep it conversational, authentic, and human. Avoid AI clichés (e.g. "beacon", "testament", "delve").
4. Strictly NO emojis.

Write ONLY the About section:"""

        try:
            if self.ollama_client.is_connected():
                about = self.ollama_client.generate_response(prompt, temperature=0.5, max_tokens=800)
                # Ensure no emojis exist in the generated about section
                about = re.sub(r'[\u2700-\u27BF]|[\uE000-\uF8FF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|[\u2011-\u26FF]|\uD83E[\uDC00-\uDFFF]', '', about)
                return about
        except Exception:
            pass

        return (
            "I solve complex engineering challenges by refactoring database structures and leading high-performing software teams. "
            "During my time as a software development lead, I reduced release cycles by 40% and mentored 5 junior engineers to improve overall team velocity. "
            "I'm open to discussing senior technical roles and connecting with fellow technology leaders. Feel free to message me here."
        )

    def _check_consistency(self, cv_text: str, linkedin_text: str) -> List[str]:
        """Check for inconsistencies between CV and LinkedIn."""
        issues = []
        cv_lower = cv_text.lower()
        li_lower = linkedin_text.lower()

        # Check for different job titles
        cv_titles = re.findall(r'(?:^|\n)\s*([A-Z][A-Za-z\s]+(?:Manager|Engineer|Developer|Director|Analyst|Designer|Lead|Specialist|Coordinator|Consultant))', cv_text)
        for title in cv_titles[:3]:
            if title.lower() not in li_lower:
                issues.append(t("inconsistency_title", title=title))

        # Check for company names
        companies = re.findall(r'(?:at|@)\s+([A-Z][A-Za-z\s&]+?)(?:\s+[-–]|\s+\d)', cv_text)
        for company in companies[:3]:
            if company.strip().lower() not in li_lower:
                issues.append(t("inconsistency_company", company=company.strip()))

        # Check for degree mentions
        degrees = re.findall(r'(Bachelor|Master|PhD|MBA|B\.S\.|M\.S\.)', cv_text, re.IGNORECASE)
        for degree in set(degrees):
            if degree.lower() not in li_lower:
                issues.append(t("inconsistency_degree", degree=degree))

        # Check year consistency
        cv_years = set(re.findall(r'20\d{2}', cv_text))
        li_years = set(re.findall(r'20\d{2}', linkedin_text))
        cv_only_years = cv_years - li_years
        if cv_only_years and len(cv_only_years) > 2:
            issues.append(t("inconsistency_years", years=", ".join(sorted(cv_only_years)[:3])))

        return issues
