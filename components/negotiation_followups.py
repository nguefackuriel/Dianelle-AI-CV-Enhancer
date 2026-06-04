"""
Salary Negotiation and Follow-up Emails Component
AI-powered negotiation script writer and follow-up email generator based on Hadrien's CV guide.
"""

import streamlit as st
from utils.ollama_client import OllamaClient


class NegotiationFollowups:
    """Salary negotiation and follow-up email template generator."""

    def __init__(self):
        self.ollama_client = OllamaClient()

    def display(self):
        """Display the Salary Negotiation & Follow-up page."""
        st.markdown("## Negotiation & Follow-up Engine")
        st.markdown(
            "*Maximize your landing success. Dianelle writes market-backed salary negotiation scripts "
            "and writes high-impact follow-up emails for every stage of the process.*"
        )

        cv_text = st.session_state.get('cv_text', '')
        role_title = st.session_state.get('interview_role_title', '')
        company_name = st.session_state.get('interview_company_name', '')

        tabs = st.tabs([
            "Salary Negotiation Script",
            "Follow-up Email Templates",
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
        st.markdown("### Salary Negotiation Strategy (Hadrien's Formula)")
        st.markdown(
            "Almost all job offers have negotiation room. Recruiters expect you to negotiate. "
            "Enter details of the offer you received below to generate custom negotiation scripts."
        )

        col1, col2 = st.columns(2)
        with col1:
            role_title = st.text_input(
                "Job Title:",
                value=default_role,
                placeholder="e.g., Senior Frontend Engineer",
                key="neg_role_title"
            )
            company_name = st.text_input(
                "Company Name:",
                value=default_company,
                placeholder="e.g., Tesla",
                key="neg_company_name"
            )
            base_salary = st.text_input(
                "Base Salary Offered:",
                placeholder="e.g., $95,000 / year"
            )
        with col2:
            bonus = st.text_input(
                "Annual Bonus Structure (optional):",
                placeholder="e.g., 10% performance bonus"
            )
            equity = st.text_input(
                "Equity / RSU / Options (optional):",
                placeholder="e.g., $20,000 stock options vested over 4 years"
            )
            benefits = st.text_input(
                "Other Benefits (optional):",
                placeholder="e.g., 25 days PTO, healthcare, 4% match"
            )

        if st.button("Generate Negotiation Pack", type="primary", key="gen_negotiation_btn"):
            if not role_title or not company_name:
                st.warning("Please fill in Job Title and Company Name.")
                return
            with st.spinner("Analyzing offer and drafting scripts..."):
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
            st.markdown("### Your Custom Negotiation Plan")
            
            negotiation_text = st.text_area(
                "Negotiation Pack Details:",
                st.session_state['linkedin_salary_negotiation'],
                height=400,
                key="edit_negotiation_pack"
            )
            
            st.download_button(
                "Download Negotiation Script",
                negotiation_text,
                file_name=f"negotiation_script_{company_name}.txt",
                mime="text/plain"
            )

    # ------------------------------------------------------------------
    # Follow-up Emails
    # ------------------------------------------------------------------

    def _followup_emails_tab(self, cv_text: str, default_role: str, default_company: str):
        """Create 3 follow-up email templates (Step 9)."""
        st.markdown("### Follow-up Email Templates")
        st.markdown(
            "Relancing keeps you top of mind. Generating 3 templates: post-application (3 days, <60 words), "
            "thank-you email (24h, <100 words), and check-in relance (7 days, <80 words). No emojis."
        )

        col1, col2 = st.columns(2)
        with col1:
            role_title = st.text_input(
                "Job Title:",
                value=default_role,
                placeholder="e.g., Product Manager",
                key="follow_role_title"
            )
            company_name = st.text_input(
                "Company Name:",
                value=default_company,
                placeholder="e.g., Stripe",
                key="follow_company_name"
            )
        with col2:
            interviewer_name = st.text_input(
                "Interviewer Name (optional):",
                placeholder="e.g., Sarah Jenkins"
            )

        if st.button("Generate Follow-up Emails", type="primary", key="gen_followup_btn"):
            if not role_title or not company_name:
                st.warning("Please fill in Job Title and Company Name.")
                return
            with st.spinner("Drafting follow-ups..."):
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
            st.markdown("### Generated Email Templates")
            
            emails_text = st.text_area(
                "Email Templates Details:",
                st.session_state['linkedin_followup_emails'],
                height=350,
                key="edit_followup_emails"
            )
            
            st.download_button(
                "Download Emails",
                emails_text,
                file_name=f"followup_emails_{company_name}.txt",
                mime="text/plain"
            )
