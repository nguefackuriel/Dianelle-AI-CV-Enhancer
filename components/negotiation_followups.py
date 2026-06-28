"""
Salary Negotiation and Follow-up Emails Component
AI-powered negotiation script writer and follow-up email generator based on Hadrien's CV guide.
"""

import streamlit as st
from utils.ollama_client import OllamaClient
from utils.translations import t


class NegotiationFollowups:
    """Salary negotiation and follow-up email template generator."""

    def __init__(self):
        self.ollama_client = OllamaClient()

    def display(self):
        """Display the Salary Negotiation & Follow-up page."""
        st.markdown(f"## {t('neg_follow_title')}")
        st.markdown(t('neg_follow_subtitle'))

        cv_text = st.session_state.get('cv_text', '')
        role_title = st.session_state.get('interview_role_title', '')
        company_name = st.session_state.get('interview_company_name', '')

        tabs = st.tabs([
            t("tab_salary_negotiation"),
            t("tab_followup_emails"),
        ])

        with tabs[0]:
            self._salary_negotiation_tab(role_title, company_name)
            
        with tabs[1]:
            self._followup_emails_tab(cv_text, role_title, company_name)

    # ------------------------------------------------------------------
    # Salary Negotiation
    # ------------------------------------------------------------------

    def _salary_negotiation_tab(self, default_role: str, default_company: str):
        """Salary negotiation scripts and strategy (Step 7)."""
        st.markdown(f"### {t('salary_neg_title')}")
        st.markdown(t('salary_neg_desc'))

        col1, col2 = st.columns(2)
        with col1:
            role_title = st.text_input(
                t("role_title_label"),
                value=default_role,
                placeholder="e.g., Senior Frontend Engineer",
                key="neg_role_title"
            )
            company_name = st.text_input(
                t("company_name_label"),
                value=default_company,
                placeholder="e.g., Tesla",
                key="neg_company_name"
            )
            base_salary = st.text_input(
                t("base_salary_label"),
                placeholder="e.g., $95,000 / year"
            )
        with col2:
            bonus = st.text_input(
                t("bonus_label"),
                placeholder="e.g., 10% performance bonus"
            )
            equity = st.text_input(
                t("equity_label"),
                placeholder="e.g., $20,000 stock options vested over 4 years"
            )
            benefits = st.text_input(
                t("benefits_label"),
                placeholder="e.g., 25 days PTO, healthcare, 4% match"
            )

        if st.button(t("gen_negotiation_btn"), type="primary", key="gen_negotiation_btn"):
            if not role_title or not company_name:
                st.warning(t("fill_role_company_warning"))
                return
            with st.spinner(t("analyzing_offer_spinner")):
                try:
                    if self.ollama_client.is_connected():
                        result = self.ollama_client.generate_salary_negotiation(
                            role_title, company_name, base_salary, bonus, equity, benefits
                        )
                        st.session_state['linkedin_salary_negotiation'] = result
                    else:
                        st.error("Ollama is disconnected. Unable to generate negotiation pack.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

        if 'linkedin_salary_negotiation' in st.session_state:
            st.markdown("---")
            st.markdown(t("custom_neg_plan_title"))
            
            negotiation_text = st.text_area(
                t("neg_pack_details_label"),
                st.session_state['linkedin_salary_negotiation'],
                height=400,
                key="edit_negotiation_pack"
            )
            
            st.download_button(
                t("download_neg_script_btn"),
                negotiation_text,
                file_name=f"negotiation_script_{company_name}.txt",
                mime="text/plain"
            )

    # ------------------------------------------------------------------
    # Follow-up Emails
    # ------------------------------------------------------------------

    def _followup_emails_tab(self, cv_text: str, default_role: str, default_company: str):
        """Create 3 follow-up email templates (Step 9)."""
        st.markdown(f"### {t('followup_emails_title')}")
        st.markdown(t('followup_emails_desc'))

        col1, col2 = st.columns(2)
        with col1:
            role_title = st.text_input(
                t("role_title_label"),
                value=default_role,
                placeholder="e.g., Product Manager",
                key="follow_role_title"
            )
            company_name = st.text_input(
                t("company_name_label"),
                value=default_company,
                placeholder="e.g., Stripe",
                key="follow_company_name"
            )
        with col2:
            interviewer_name = st.text_input(
                t("interviewer_name_label"),
                placeholder="e.g., Sarah Jenkins"
            )

        if st.button(t("gen_followup_btn"), type="primary", key="gen_followup_btn"):
            if not role_title or not company_name:
                st.warning(t("fill_role_company_warning"))
                return
            with st.spinner(t("drafting_followup_spinner")):
                try:
                    if self.ollama_client.is_connected():
                        result = self.ollama_client.generate_followup_emails(
                            role_title, company_name, cv_text or "General background", interviewer_name
                        )
                        st.session_state['linkedin_followup_emails'] = result
                    else:
                        st.error("Ollama is disconnected. Unable to generate emails.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

        if 'linkedin_followup_emails' in st.session_state:
            st.markdown("---")
            st.markdown(t("gen_email_templates_title"))
            
            emails_text = st.text_area(
                t("email_templates_details_label"),
                st.session_state['linkedin_followup_emails'],
                height=350,
                key="edit_followup_emails"
            )
            
            st.download_button(
                t("download_emails_btn"),
                emails_text,
                file_name=f"followup_emails_{company_name}.txt",
                mime="text/plain"
            )
