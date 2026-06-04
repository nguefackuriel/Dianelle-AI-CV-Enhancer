"""
Export Page Component
Template selection, customization, and download interface for CV export.
"""

import streamlit as st
from typing import Dict, List, Any
from utils.cv_exporter import CVExporter


class ExportPage:
    """CV export interface with template gallery and download."""

    def __init__(self):
        self.exporter = CVExporter()

    def display(self):
        """Display the export page."""
        st.markdown("## Export Your Enhanced CV")
        st.markdown(
            "*Download your ATS-optimized CV in professional templates. "
            "All templates are tested for ATS compatibility.*"
        )

        # Check prerequisites
        if not st.session_state.get('cv_text'):
            st.warning("Please upload your CV first on the **CV Analysis** page.")
            return

        cv_text = st.session_state['cv_text']
        analysis = st.session_state.get('analysis_results', {})
        parsed_sections = analysis.get('parsed_sections', {})
        accepted_rewrites = st.session_state.get('accepted_rewrites', {})

        # Show what we're working with
        self._display_content_summary(parsed_sections, accepted_rewrites)

        st.markdown("---")

        # Template Selection
        st.markdown("### Choose Your Template")
        templates = self.exporter.get_template_info()

        cols = st.columns(3)
        selected_template = 'classic'

        for i, tmpl in enumerate(templates):
            with cols[i]:
                selected = st.button(
                    f"{'[Selected] ' if i == 0 else ''}{tmpl['name']}",
                    key=f"tmpl_{tmpl['id']}",
                    use_container_width=True,
                )
                st.caption(tmpl['description'])
                st.caption(f"Font: {tmpl['font']} | Color: {tmpl['color']}")

                if selected:
                    selected_template = tmpl['id']
                    st.session_state['selected_template'] = tmpl['id']

        selected_template = st.session_state.get('selected_template', 'classic')

        st.markdown("---")

        # Customization
        st.markdown("### Customization")
        col1, col2 = st.columns(2)

        with col1:
            font_size = st.slider("Font Size", 10, 13, 11)
            accent = st.selectbox(
                "Accent Color",
                ['classic', 'modern', 'minimal', 'professional', 'executive'],
                format_func=lambda x: {
                    'classic': 'Navy Blue',
                    'modern': 'Dark Slate',
                    'minimal': 'Dark Gray',
                    'professional': 'Teal Blue',
                    'executive': 'Dark Red',
                }.get(x, x),
            )

        with col2:
            # Section selection
            available_sections = [
                s for s in parsed_sections.keys()
                if s not in ('header', 'contact') and parsed_sections[s].strip()
            ]

            if not available_sections:
                available_sections = ['full_cv']

            include_sections = st.multiselect(
                "Sections to include:",
                available_sections,
                default=available_sections,
            )

        # Contact info editor
        st.markdown("### Contact Information")
        st.caption("Edit your contact details for the CV header:")

        c1, c2, c3 = st.columns(3)
        with c1:
            name = st.text_input("Full Name", value=st.session_state.get('cv_name', ''))
            email = st.text_input("Email", value=st.session_state.get('cv_email', ''))
        with c2:
            phone = st.text_input("Phone", value=st.session_state.get('cv_phone', ''))
            location = st.text_input("Location", value=st.session_state.get('cv_location', ''))
        with c3:
            linkedin = st.text_input("LinkedIn URL", value=st.session_state.get('cv_linkedin', ''))
            website = st.text_input("Website/Portfolio", value=st.session_state.get('cv_website', ''))

        contact_info = {
            'name': name, 'email': email, 'phone': phone,
            'location': location, 'linkedin': linkedin, 'website': website,
        }

        st.markdown("---")

        # Download buttons
        st.markdown("### Download")

        if accepted_rewrites:
            st.success(f"Including {len(accepted_rewrites)} enhanced section(s) from the Rewriter.")
        else:
            st.info("Tip: Use the **CV Rewriter** page first to enhance your sections before exporting.")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Generate DOCX", type="primary", use_container_width=True):
                with st.spinner("Generating DOCX..."):
                    try:
                        docx_buffer = self.exporter.generate_docx_from_text(
                            cv_text=cv_text,
                            parsed_sections=parsed_sections,
                            accepted_rewrites=accepted_rewrites,
                            template=selected_template,
                            contact_info={k: v for k, v in contact_info.items() if v},
                        )

                        st.session_state['docx_buffer'] = docx_buffer
                        st.success("DOCX generated!")
                    except Exception as e:
                        st.error(f"Error generating DOCX: {str(e)}")

        with col2:
            if st.button("Generate PDF", use_container_width=True):
                with st.spinner("Generating PDF..."):
                    try:
                        # Build cv_data for PDF
                        sections = dict(parsed_sections)
                        if accepted_rewrites:
                            sections.update(accepted_rewrites)
                        sections.pop('header', None)
                        sections.pop('contact', None)

                        cv_data = {
                            'name': contact_info.get('name', 'Your Name'),
                            'contact': {k: v for k, v in contact_info.items() if v and k != 'name'},
                            'sections': sections,
                        }

                        pdf_buffer = self.exporter.generate_pdf(cv_data, template=selected_template)

                        if pdf_buffer:
                            st.session_state['pdf_buffer'] = pdf_buffer
                            st.success("PDF generated!")
                        else:
                            st.warning("PDF generation requires `fpdf2`. Install with: `pip install fpdf2`")
                    except Exception as e:
                        st.error(f"Error generating PDF: {str(e)}")

        with col3:
            st.markdown("**ATS Safety**")
            st.markdown("""
            <div style="background: #e8f5e9; padding: 0.5rem; border-radius: 5px; text-align: center;">
                <span style="color: #2e7d32; font-weight: bold;">ATS-Safe Templates</span><br>
                <small>No tables, no graphics, no text boxes</small>
            </div>
            """, unsafe_allow_html=True)

        # Download links
        if st.session_state.get('docx_buffer'):
            st.download_button(
                label="Download DOCX",
                data=st.session_state['docx_buffer'],
                file_name=f"CV_{name.replace(' ', '_') if name else 'Enhanced'}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )

        if st.session_state.get('pdf_buffer'):
            st.download_button(
                label="Download PDF",
                data=st.session_state['pdf_buffer'],
                file_name=f"CV_{name.replace(' ', '_') if name else 'Enhanced'}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

    def _display_content_summary(self, parsed_sections: Dict, accepted_rewrites: Dict):
        """Show summary of what content will be exported."""
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Detected Sections:**")
            for section in parsed_sections:
                if section != 'header':
                    is_rewritten = section in accepted_rewrites
                    marker = "*" if is_rewritten else "-"
                    label = "Enhanced" if is_rewritten else "Original"
                    st.caption(f"{marker} {section.replace('_', ' ').title()} ({label})")

        with col2:
            total = len([s for s in parsed_sections if s != 'header'])
            enhanced = len(accepted_rewrites)
            st.metric("Total Sections", total)
            st.metric("Enhanced Sections", enhanced)
