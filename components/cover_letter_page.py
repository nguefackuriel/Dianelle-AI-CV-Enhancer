"""
Cover Letter Page Component
AI-powered cover letter generation with tone selection, multiple variations, and export.
"""

import streamlit as st
from typing import Dict, List, Any
from utils.ollama_client import OllamaClient
from utils.cv_exporter import CVExporter
from utils.translations import t


class CoverLetterPage:
    """Cover letter generation interface."""

    TONES = {
        'professional': 'Professional — Formal, polished, corporate-ready',
        'enthusiastic': 'Enthusiastic — Energetic, passionate, shows excitement',
        'conversational': 'Conversational — Warm, personable, approachable',
        'formal': 'Formal — Traditional, executive-style, very structured',
    }

    LENGTHS = {
        'short': ('Short', '200-250 words', 200),
        'standard': ('Standard', '300-350 words', 350),
        'detailed': ('Detailed', '400-500 words', 500),
    }

    def __init__(self):
        self.ollama_client = OllamaClient()
        self.exporter = CVExporter()

    def display(self):
        """Display the cover letter page."""
        st.markdown(f"## {t('cl_title')}")
        st.markdown(t('cl_subtitle'))

        # Check prerequisites
        if not st.session_state.get('cv_text'):
            st.warning(t("please_upload_first_cl"))
            return

        cv_text = st.session_state['cv_text']
        job_description = st.session_state.get('job_description', '')
        analysis = st.session_state.get('analysis_results', {})

        # ----- Configuration -----
        st.markdown(f"### {t('cl_settings')}")

        use_hadrien_formula = st.checkbox(
            t("use_hadrien_formula"),
            value=True,
            help=t("hadrien_formula_help")
        )

        col1, col2 = st.columns(2)

        with col1:
            company_name = st.text_input(
                t("company_name_label"),
                placeholder=t("company_name_placeholder"),
            )
            hiring_manager = st.text_input(
                t("hiring_manager_label"),
                placeholder=t("hiring_manager_placeholder"),
            )
            role_title = st.text_input(
                t("role_title_label"),
                placeholder=t("role_title_placeholder"),
            )

        with col2:
            if use_hadrien_formula:
                st.caption(t("hadrien_locked_info"))
                gap_text = st.text_input(
                    t("gap_text_label"),
                    placeholder=t("gap_text_placeholder"),
                    help=t("gap_text_help")
                )
                tone = "professional"
                length = "short"
            else:
                tone = st.selectbox(
                    t("tone_label"),
                    list(self.TONES.keys()),
                    format_func=lambda x: self.TONES[x],
                )
                length = st.selectbox(
                    "Length:",
                    list(self.LENGTHS.keys()),
                    format_func=lambda x: f"{self.LENGTHS[x][0]} ({self.LENGTHS[x][1]})",
                )
                gap_text = ""
            num_variations = st.slider(t("num_variations_label"), 1, 3, 1)

        # Company research / culture notes
        with st.expander(t("company_research_title")):
            company_notes = st.text_area(
                t("company_notes_label"),
                height=100,
                placeholder=t("company_notes_placeholder"),
            )
            why_company = st.text_area(
                t("why_company_label"),
                height=80,
                placeholder=t("why_company_placeholder"),
            )

        st.markdown("---")

        # ----- Generate -----
        if st.button(t("generate_cl_btn"), type="primary", use_container_width=True):
            if not job_description:
                st.warning(t("please_add_jd_cl"))
                return

            with st.spinner(t("generating_cl_spinner")):
                variations = []
                for i in range(num_variations):
                    cover_letter = self._generate_cover_letter(
                        cv_text=cv_text,
                        job_description=job_description,
                        company_name=company_name or "[Company Name]",
                        hiring_manager=hiring_manager,
                        role_title=role_title or "the role",
                        tone=tone,
                        max_words=self.LENGTHS[length][2],
                        company_notes=company_notes,
                        why_company=why_company,
                        variation=i + 1,
                        use_hadrien=use_hadrien_formula,
                        gap_text=gap_text,
                    )
                    variations.append(cover_letter)

                st.session_state['cover_letter_variations'] = variations

        # ----- Display Results -----
        if 'cover_letter_variations' in st.session_state:
            variations = st.session_state['cover_letter_variations']

            if len(variations) == 1:
                self._display_single_variation(variations[0])
            else:
                self._display_multiple_variations(variations)

    # ------------------------------------------------------------------
    # Generation
    # ------------------------------------------------------------------

    def _generate_cover_letter(
        self,
        cv_text: str,
        job_description: str,
        company_name: str,
        hiring_manager: str,
        role_title: str,
        tone: str,
        max_words: int,
        company_notes: str = '',
        why_company: str = '',
        variation: int = 1,
        use_hadrien: bool = False,
        gap_text: str = '',
    ) -> str:
        """Generate a cover letter using AI."""
        if use_hadrien:
            try:
                if self.ollama_client.is_connected():
                    return self.ollama_client.generate_hadrien_cover_letter(
                        cv_text=cv_text,
                        job_description=job_description,
                        company_name=company_name,
                        hiring_manager=hiring_manager,
                        role_title=role_title,
                        company_notes=company_notes,
                        why_company=why_company,
                        gap_text=gap_text
                    )
                else:
                    return self._generate_fallback_cover_letter(
                        company_name, hiring_manager, role_title
                    )
            except Exception:
                return self._generate_fallback_cover_letter(
                    company_name, hiring_manager, role_title
                )

        tone_instructions = {
            'professional': 'Use a formal, polished, and confident tone. Be concise and results-oriented.',
            'enthusiastic': 'Show genuine excitement and passion for the role. Be energetic but professional.',
            'conversational': 'Write in a warm, personable style. Be approachable while remaining professional.',
            'formal': 'Use traditional business letter formatting. Be highly structured and executive-level.',
        }

        prompt = f"""You are Dianelle, an expert career advisor and cover letter writer.

Write a compelling, personalized cover letter for a job application.

CANDIDATE'S CV (key highlights):
{cv_text[:2000]}

JOB DESCRIPTION:
{job_description[:1500]}

DETAILS:
- Company: {company_name}
- Hiring Manager: {hiring_manager or 'Hiring Manager'}
- Role: {role_title}
- Tone: {tone_instructions.get(tone, tone_instructions['professional'])}
- Target length: approximately {max_words} words
{'- Company notes: ' + company_notes if company_notes else ''}
{'- Why this company: ' + why_company if why_company else ''}
- Variation: {variation} (if generating multiple, make this one {"more formal" if variation == 1 else "more narrative" if variation == 2 else "more achievement-focused"})

REQUIREMENTS:
1. Address to {hiring_manager or 'Hiring Manager'} at {company_name}
2. Opening paragraph: Hook with a compelling reason for applying
3. Body paragraph 1: Highlight 2-3 most relevant achievements from the CV
4. Body paragraph 2: Show knowledge of the company and explain fit
5. Closing paragraph: Call to action and enthusiasm for next steps
6. Include specific keywords from the job description naturally
7. Reference specific accomplishments with metrics where possible
8. DO NOT use generic filler phrases like "I am writing to express my interest"
9. Start with a compelling hook that shows you understand the company's challenges
10. Keep to approximately {max_words} words
11. Write in a natural, conversational, and human tone. Avoid robotic, overly formal, or predictable "AI writing" patterns.
12. DO NOT use flowery buzzwords or transition clichés (e.g., "Furthermore", "Moreover", "In conclusion", "Testament to", "I am thrilled to", "deep dive", "game-changer").

Write ONLY the cover letter, no labels, metadata, or meta-commentary:"""

        try:
            if self.ollama_client.is_connected():
                return self.ollama_client.generate_response(
                    prompt, temperature=0.5, max_tokens=max_words * 2
                )
            else:
                return self._generate_fallback_cover_letter(
                    company_name, hiring_manager, role_title
                )
        except Exception:
            return self._generate_fallback_cover_letter(
                company_name, hiring_manager, role_title
            )

    def _generate_fallback_cover_letter(
        self, company_name: str, hiring_manager: str, role_title: str
    ) -> str:
        """Fallback cover letter when AI is unavailable."""
        return f"""Dear {hiring_manager or 'Hiring Manager'},

I am excited to apply for the {role_title} position at {company_name}. With a strong track record of delivering impactful results, I am confident in my ability to contribute to your team's success.

Throughout my career, I have consistently demonstrated the ability to drive measurable outcomes. My experience aligns closely with the requirements outlined in the job description, and I am eager to bring my skills and passion to {company_name}.

What particularly draws me to {company_name} is your commitment to innovation and excellence. I believe my background in problem-solving and collaboration would make me a valuable addition to your team.

I would welcome the opportunity to discuss how my experience and skills can contribute to {company_name}'s continued success. Thank you for considering my application, and I look forward to speaking with you.

Best regards,
[Your Name]"""

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def _display_single_variation(self, cover_letter: str):
        """Display a single cover letter with editing and export."""
        st.markdown(f"### {t('your_cl_title')}")

        edited = st.text_area(
            t("edit_cl_label"),
            cover_letter,
            height=400,
            key="cover_letter_edit",
        )

        st.session_state['final_cover_letter'] = edited

        # Word count
        word_count = len(edited.split())
        st.caption(t("word_count_label", count=word_count))

        # Actions
        self._display_actions(edited)

    def _display_multiple_variations(self, variations: List[str]):
        """Display multiple variations in tabs."""
        st.markdown(f"### {t('cl_variations_title')}")
        st.info(t("compare_variations_info"))

        tabs = st.tabs([t("version_label", num=i+1) for i in range(len(variations))])

        for i, (tab, letter) in enumerate(zip(tabs, variations)):
            with tab:
                edited = st.text_area(
                    t("version_label", num=i+1) + ":",
                    letter,
                    height=350,
                    key=f"variation_{i}",
                )

                word_count = len(edited.split())
                st.caption(t("word_count_label", count=word_count))

                if st.button(t("use_version_btn", num=i+1), key=f"use_v{i}"):
                    st.session_state['final_cover_letter'] = edited
                    st.success(t("version_selected", num=i+1))

        # Actions for selected version
        if 'final_cover_letter' in st.session_state:
            st.markdown("---")
            self._display_actions(st.session_state['final_cover_letter'])

    def _display_actions(self, cover_letter: str):
        """Display action buttons for the cover letter."""
        st.markdown(f"### {t('export_cl_title')}")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button(t("refine_with_dianelle_btn"), use_container_width=True):
                with st.spinner(t("refining_spinner")):
                    refined = self._refine_cover_letter(cover_letter)
                    st.session_state['final_cover_letter'] = refined
                    st.rerun()

        with col2:
            st.download_button(
                label=t("download_txt_btn"),
                data=cover_letter,
                file_name="Cover_Letter.txt",
                mime="text/plain",
                use_container_width=True,
            )

        with col3:
            if st.button(t("download_docx_btn"), use_container_width=True):
                try:
                    docx_buffer = self._generate_cover_letter_docx(cover_letter)
                    st.session_state['cl_docx'] = docx_buffer
                except Exception as e:
                    st.error(f"Error: {str(e)}")

        if st.session_state.get('cl_docx'):
            st.download_button(
                label=t("save_docx_btn"),
                data=st.session_state['cl_docx'],
                file_name="Cover_Letter.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )

    def _refine_cover_letter(self, current: str) -> str:
        """Use AI to refine an existing cover letter."""
        prompt = f"""You are Dianelle, an expert career advisor and professional writer. Please refine this cover letter to sound natural, compelling, and authentic:

REFINEMENT RULES (CRITICAL FOR HUMAN TONE):
1. Avoid "AI-generated" tone or phrasing. Do not use flowery, overly formal, or robotic language.
2. Completely avoid AI buzzwords and transition clichés (e.g., "Furthermore," "Moreover," "In conclusion," "Testament to," "Indeed," "passion for," "thrilled to," "delighted to").
3. Use a conversational, warm, and professional human voice. Sound like an actual experienced professional, not a chatbot.
4. Tighten the language: remove filler words, weak phrases, and fluff.
5. Vary sentence lengths (some short and punchy, some naturally longer) to create a natural, organic rhythm.
6. Keep the exact same general content, structure, and factual details, but make the flow and word choice feel authentic and human.

CURRENT COVER LETTER:
{current}

Write ONLY the refined cover letter (no intro/outro text, labels, or conversational commentary):"""

        try:
            if self.ollama_client.is_connected():
                return self.ollama_client.generate_response(prompt, temperature=0.4, max_tokens=1000)
        except Exception:
            pass
        return current

    def _generate_cover_letter_docx(self, cover_letter: str) -> bytes:
        """Generate a DOCX file for the cover letter."""
        from docx import Document
        from docx.shared import Pt, Cm

        doc = Document()

        # Set margins
        for section in doc.sections:
            section.top_margin = Cm(2.5)
            section.bottom_margin = Cm(2.5)
            section.left_margin = Cm(2.5)
            section.right_margin = Cm(2.5)

        # Add content
        paragraphs = cover_letter.strip().split('\n\n')
        for para_text in paragraphs:
            para_text = para_text.strip()
            if not para_text:
                continue

            para = doc.add_paragraph(para_text)
            for run in para.runs:
                run.font.name = 'Calibri'
                run.font.size = Pt(11)

            para.paragraph_format.space_after = Pt(8)

        import io
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return buffer.getvalue()
