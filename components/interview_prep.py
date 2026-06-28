"""
Interview Preparation Component
Generate interview questions, STAR responses, and elevator pitches
based on CV analysis and job description.
"""

import streamlit as st
from typing import Dict, List, Any
from utils.ollama_client import OllamaClient
from utils.translations import t


class InterviewPrep:
    """Interview preparation interface and question generation."""

    def __init__(self):
        self.ollama_client = OllamaClient()

    def display(self):
        """Display the interview preparation page."""
        st.markdown(f"## {t('interview_prep_title')}")
        st.markdown(t('interview_prep_subtitle'))

        if not st.session_state.get('cv_text'):
            st.warning(t("please_upload_first"))
            return

        cv_text = st.session_state['cv_text']
        job_description = st.session_state.get('job_description', '')
        analysis = st.session_state.get('analysis_results', {})

        # Role and Company inputs for customization
        st.markdown(f"### {t('target_role_details')}")
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input(
                t("company_name_label"),
                value=st.session_state.get('interview_company_name', ''),
                placeholder=t("company_name_placeholder"),
                key="interview_company_input"
            )
            st.session_state['interview_company_name'] = company_name
        with col2:
            role_title = st.text_input(
                t("role_title_label"),
                value=st.session_state.get('interview_role_title', ''),
                placeholder=t("role_title_placeholder"),
                key="interview_role_input"
            )
            st.session_state['interview_role_title'] = role_title

        tabs = st.tabs([
            t("tab_complete_prep"),
            t("tab_mock_interview"),
            t("tab_star_builder"),
            t("tab_behavioral_tech"),
            t("tab_elevator_pitch_framing"),
        ])

        with tabs[0]:
            self._complete_prep_pack(cv_text, job_description, company_name, role_title)
        with tabs[1]:
            self._mock_interview(cv_text, job_description, company_name, role_title)
        with tabs[2]:
            self._star_builder(cv_text, job_description)
        with tabs[3]:
            self._behavioral_tech_questions(cv_text, job_description, analysis)
        with tabs[4]:
            self._elevator_pitch_and_framing(cv_text, job_description, analysis)

    # ------------------------------------------------------------------
    # Common Questions
    # ------------------------------------------------------------------

    def _common_questions(self, cv_text: str, job_description: str, analysis: Dict):
        """Generate likely interview questions."""
        st.markdown("### Likely Interview Questions")
        st.markdown("Based on your CV and the job description, here are questions you'll likely face:")

        if st.button("Generate Questions", type="primary", key="gen_common"):
            with st.spinner("Generating interview questions..."):
                questions = self._generate_questions(cv_text, job_description, 'common')
                st.session_state['interview_common_questions'] = questions

        if 'interview_common_questions' in st.session_state:
            questions = st.session_state['interview_common_questions']
            if questions:
                for i, q in enumerate(questions, 1):
                    with st.expander(f"Q{i}: {q['question']}", expanded=(i <= 3)):
                        st.markdown(t("why_ask_label", reason=q['reason']))
                        st.markdown(f"**Suggested approach:** {q['approach']}")
                        if q.get('sample_answer'):
                            st.markdown(f"**Sample answer framework:** {q['sample_answer']}")

    # ------------------------------------------------------------------
    # STAR Builder
    # ------------------------------------------------------------------

    def _star_builder(self, cv_text: str, job_description: str):
        """Interactive STAR response builder."""
        st.markdown(f"### {t('tab_star_builder')}")
        st.markdown(
            "Structure your answers using the **S**ituation → **T**ask → **A**ction → **R**esult framework."
        )

        st.info("STAR responses are the gold standard for behavioral interviews.")

        scenario = st.text_area(
            "Describe a work achievement or challenge:",
            height=100,
            placeholder="e.g., I led a project to migrate our database to the cloud...",
        )

        if st.button("Build STAR Response", type="primary", key="build_star"):
            if not scenario.strip():
                st.warning("Please describe a scenario.")
                return

            with st.spinner("Building your STAR response..."):
                star = self._build_star_response(scenario, job_description)
                st.session_state['interview_star_response'] = star

        if 'interview_star_response' in st.session_state:
            star = st.session_state['interview_star_response']
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### Situation")
                st.markdown(star.get('situation', 'Describe the context...'))

                st.markdown("#### Task")
                st.markdown(star.get('task', 'Describe your responsibility...'))

            with col2:
                st.markdown("#### Action")
                st.markdown(star.get('action', 'Describe what you did...'))

                st.markdown("#### Result")
                st.markdown(star.get('result', 'Describe the outcome with metrics...'))

            st.markdown("---")
            st.markdown("#### Complete STAR Response")
            full_response = (
                f"{star.get('situation', '')}\n\n"
                f"{star.get('task', '')}\n\n"
                f"{star.get('action', '')}\n\n"
                f"{star.get('result', '')}"
            )
            st.text_area("Copy and practice:", full_response, height=200)

    # ------------------------------------------------------------------
    # Behavioral Questions
    # ------------------------------------------------------------------

    def _behavioral_questions(self, cv_text: str, job_description: str):
        """Generate role-specific behavioral questions."""
        st.markdown(f"### {t('behavioral_questions_title')}")
        st.markdown(t('behavioral_questions_desc'))

        category = st.selectbox(
            t("focus_area_label"),
            ['Leadership', 'Teamwork', 'Problem Solving', 'Conflict Resolution',
             'Adaptability', 'Communication', 'Time Management', 'All'],
        )

        if st.button(t("gen_behavioral_btn"), type="primary", key="gen_behavioral"):
            with st.spinner(t("generating_questions_spinner")):
                questions = self._generate_behavioral_questions(
                    cv_text, job_description, category
                )
                st.session_state['interview_behavioral_questions'] = questions

        if 'interview_behavioral_questions' in st.session_state:
            questions = st.session_state['interview_behavioral_questions']
            for i, q in enumerate(questions, 1):
                with st.container():
                    st.markdown(f"""
                    <div style="padding: 0.8rem; border-left: 4px solid #7c4dff; background: #f3e8ff; margin: 0.5rem 0; border-radius: 4px;">
                        <strong>Q{i}:</strong> {q}<br>
                        <small style="color: #666;">{t('star_method_caption')}</small>
                    </div>
                    """, unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # Technical Questions
    # ------------------------------------------------------------------

    def _technical_questions(self, cv_text: str, job_description: str, analysis: Dict):
        """Generate technical questions based on required skills."""
        st.markdown(f"### {t('technical_questions_title')}")
        st.markdown(t('technical_questions_desc'))

        tech_skills = analysis.get('technical_skills_match', []) + analysis.get('missing_technical_skills', [])

        if not tech_skills:
            st.info(t("no_tech_skills_detected"))
            tech_skills = ['general']

        selected_skill = st.selectbox(t("focus_skill_label"), tech_skills[:15])

        difficulty = st.select_slider(
            t("difficulty_level_label"),
            options=['Basic', 'Intermediate', 'Advanced'],
            value='Intermediate',
        )

        if st.button(t("gen_technical_btn"), type="primary", key="gen_tech"):
            with st.spinner(t("generating_tech_spinner")):
                questions = self._generate_technical_questions(
                    selected_skill, difficulty, job_description
                )
                st.session_state['interview_technical_questions'] = questions

        if 'interview_technical_questions' in st.session_state:
            questions = st.session_state['interview_technical_questions']
            for i, q in enumerate(questions, 1):
                with st.container():
                    st.markdown(f"""
                    <div style="padding: 0.8rem; border-left: 4px solid #00bcd4; background: #e0f7fa; margin: 0.5rem 0; border-radius: 4px;">
                        <strong>Q{i}:</strong> {q}
                    </div>
                    """, unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # Elevator Pitch
    # ------------------------------------------------------------------

    def _elevator_pitch(self, cv_text: str, job_description: str):
        """Generate elevator pitches."""
        st.markdown(f"### {t('elevator_pitch_title')}")
        st.markdown(t('elevator_pitch_desc'))

        col1, col2 = st.columns(2)
        with col1:
            pitch_length = st.selectbox(
                t("pitch_length_label"),
                ['30 seconds (~75 words)', '60 seconds (~150 words)', '90 seconds (~225 words)'],
            )
        with col2:
            context = st.selectbox(
                t("context_label"),
                ['Job Interview', 'Networking Event', 'Career Fair', 'LinkedIn Message'],
            )

        if st.button(t("gen_pitch_btn"), type="primary", key="gen_pitch"):
            with st.spinner(t("generating_pitch_spinner")):
                pitch = self._generate_elevator_pitch(
                    cv_text, job_description, pitch_length, context
                )
                st.session_state['interview_elevator_pitch'] = pitch

        if 'interview_elevator_pitch' in st.session_state:
            pitch = st.session_state['interview_elevator_pitch']
            st.markdown(t("your_elevator_pitch_title"))
            st.markdown(f"""
            <div style="padding: 1.5rem; background: linear-gradient(135deg, #667eea20, #764ba220); border-radius: 10px; border: 1px solid #667eea40;">
                {pitch}
            </div>
            """, unsafe_allow_html=True)

            word_count = len(pitch.split())
            st.caption(f"{word_count} words")

            st.download_button(
                t("download_pitch_btn"),
                pitch,
                file_name="elevator_pitch.txt",
                mime="text/plain",
            )

    # ------------------------------------------------------------------
    # Weakness/Strength Framing
    # ------------------------------------------------------------------

    def _weakness_strength_framing(self, cv_text: str, analysis: Dict):
        """Help frame weaknesses as growth opportunities."""
        st.markdown(f"### {t('weakness_framing_title')}")
        st.markdown(t('weakness_framing_desc'))

        gaps = analysis.get('missing_keywords', [])[:5]
        missing_skills = analysis.get('missing_technical_skills', [])[:5]

        all_gaps = gaps + missing_skills

        if all_gaps:
            st.warning(t("potential_interview_concerns", gaps=', '.join(all_gaps[:8])))

        weakness = st.text_input(
            t("enter_weakness_label"),
            placeholder=t("enter_weakness_placeholder"),
        )

        if st.button(t("frame_it_btn"), type="primary", key="frame_weakness"):
            if not weakness.strip():
                st.warning("Please enter a weakness to frame.")
                return

            with st.spinner(t("crafting_response_spinner")):
                framing = self._frame_weakness(weakness, cv_text)
                st.session_state['interview_weakness_framing'] = framing

        if 'interview_weakness_framing' in st.session_state:
            st.markdown(t("positive_framing_title"))
            st.success(st.session_state['interview_weakness_framing'])

    # ------------------------------------------------------------------
    # AI Generation Methods
    # ------------------------------------------------------------------

    def _generate_questions(self, cv_text: str, job_description: str, q_type: str) -> List[Dict]:
        """Generate interview questions using AI."""
        prompt = f"""Based on this CV and job description, generate 7 likely interview questions.

CV (highlights): {cv_text[:1500]}
Job Description: {job_description[:1500]}

For each question, provide:
1. The question
2. Why the interviewer would ask it
3. A suggested approach to answering
4. A brief sample answer framework

Format each question as:
QUESTION: [question text]
REASON: [why they ask]
APPROACH: [how to answer]
SAMPLE: [framework]
---"""

        try:
            if self.ollama_client.is_connected():
                response = self.ollama_client.generate_response(prompt, temperature=0.5, max_tokens=1500)
                return self._parse_questions(response)
        except Exception:
            pass

        # Fallback questions
        return [
            {'question': 'Tell me about yourself and why you\'re interested in this role.',
             'reason': 'Opening question to assess communication and motivation',
             'approach': 'Use a present-past-future structure: where you are, how you got here, where you want to go',
             'sample_answer': 'Start with your current role, then highlight 2-3 relevant achievements, end with why this opportunity excites you.'},
            {'question': 'What\'s your greatest professional achievement?',
             'reason': 'Assesses impact and self-awareness',
             'approach': 'Use STAR format with specific metrics',
             'sample_answer': 'Choose an achievement relevant to this role. Include numbers and business impact.'},
            {'question': 'Why are you leaving your current position?',
             'reason': 'Checks for red flags and motivation',
             'approach': 'Focus on growth and new opportunities, never badmouth',
             'sample_answer': 'Frame it as seeking growth, new challenges, or better alignment with career goals.'},
            {'question': 'Where do you see yourself in 5 years?',
             'reason': 'Assesses ambition and retention potential',
             'approach': 'Show ambition that aligns with the company\'s growth',
             'sample_answer': 'Describe growth within the company/industry. Show you\'re thinking long-term.'},
            {'question': 'Describe a challenging situation and how you handled it.',
             'reason': 'Behavioral question testing problem-solving',
             'approach': 'STAR method with emphasis on the Result',
             'sample_answer': 'Pick a relevant challenge. Focus on your specific actions and measurable outcomes.'},
        ]

    def _parse_questions(self, response: str) -> List[Dict]:
        """Parse AI-generated questions."""
        questions = []
        blocks = response.split('---')

        for block in blocks:
            q = {}
            for line in block.strip().split('\n'):
                line = line.strip()
                if line.startswith('QUESTION:'):
                    q['question'] = line[9:].strip()
                elif line.startswith('REASON:'):
                    q['reason'] = line[7:].strip()
                elif line.startswith('APPROACH:'):
                    q['approach'] = line[9:].strip()
                elif line.startswith('SAMPLE:'):
                    q['sample_answer'] = line[7:].strip()

            if q.get('question'):
                q.setdefault('reason', 'Standard interview question')
                q.setdefault('approach', 'Use specific examples from your experience')
                questions.append(q)

        return questions if questions else self._generate_questions('', '', 'fallback')

    def _build_star_response(self, scenario: str, job_description: str) -> Dict[str, str]:
        """Build a STAR response from a scenario."""
        prompt = f"""Help structure this scenario into a STAR interview response.

Scenario: {scenario}
Target role context: {job_description[:500]}

Provide each component:
SITUATION: [2-3 sentences setting the context]
TASK: [1-2 sentences about your responsibility]
ACTION: [3-4 sentences about what you did — use strong action verbs]
RESULT: [2-3 sentences with quantified outcomes]"""

        try:
            if self.ollama_client.is_connected():
                response = self.ollama_client.generate_response(prompt, temperature=0.4, max_tokens=600)
                parts = {}
                for key in ['SITUATION', 'TASK', 'ACTION', 'RESULT']:
                    import re
                    match = re.search(rf'{key}:\s*(.+?)(?=(?:SITUATION|TASK|ACTION|RESULT):|$)', response, re.DOTALL)
                    if match:
                        parts[key.lower()] = match.group(1).strip()
                return parts
        except Exception:
            pass

        return {
            'situation': 'Describe the context and challenge you faced.',
            'task': 'Explain your specific responsibility in this situation.',
            'action': 'Detail the specific steps you took. Use strong action verbs.',
            'result': 'Share the measurable outcome. Include numbers if possible.',
        }

    def _generate_behavioral_questions(self, cv_text: str, job_description: str, category: str) -> List[str]:
        """Generate behavioral questions by category."""
        prompt = f"""Generate 6 behavioral interview questions for the "{category}" category.
Context: {job_description[:800]}

These should be "Tell me about a time when..." style questions.
Output one question per line, numbered 1-6:"""

        try:
            if self.ollama_client.is_connected():
                response = self.ollama_client.generate_response(prompt, temperature=0.5, max_tokens=500)
                lines = [l.strip().lstrip('0123456789.-) ') for l in response.strip().split('\n') if l.strip()]
                return [l for l in lines if len(l) > 20][:6]
        except Exception:
            pass

        defaults = {
            'Leadership': [
                'Tell me about a time you led a team through a difficult project.',
                'Describe a situation where you had to motivate a disengaged team member.',
                'How have you handled disagreements with team members about approach?',
            ],
            'Teamwork': [
                'Describe a successful collaboration with a cross-functional team.',
                'Tell me about a time you had to work with someone difficult.',
                'How do you handle situations where team consensus is hard to reach?',
            ],
        }
        return defaults.get(category, [
            'Tell me about a time you overcame a significant challenge at work.',
            'Describe a situation where you had to learn something quickly.',
            'How do you handle pressure and tight deadlines?',
        ])

    def _generate_technical_questions(self, skill: str, difficulty: str, job_description: str) -> List[str]:
        """Generate technical questions for a specific skill."""
        prompt = f"""Generate 5 {difficulty}-level technical interview questions about {skill}.
Job context: {job_description[:500]}
Output one question per line:"""

        try:
            if self.ollama_client.is_connected():
                response = self.ollama_client.generate_response(prompt, temperature=0.4, max_tokens=500)
                lines = [l.strip().lstrip('0123456789.-) ') for l in response.strip().split('\n') if l.strip()]
                return [l for l in lines if len(l) > 15][:5]
        except Exception:
            pass

        return [
            f'Explain how you would use {skill} to solve a real-world problem.',
            f'What are the key best practices when working with {skill}?',
            f'Describe a project where you used {skill} and what challenges you faced.',
            f'How do you stay updated with the latest developments in {skill}?',
            f'Compare {skill} with its alternatives and when you would choose each.',
        ]

    def _generate_elevator_pitch(self, cv_text: str, job_description: str,
                                  length: str, context: str) -> str:
        """Generate an elevator pitch."""
        word_target = 75 if '30' in length else 150 if '60' in length else 225

        prompt = f"""Create a {context.lower()} elevator pitch (~{word_target} words).

CV highlights: {cv_text[:1000]}
Target role: {job_description[:500]}

Requirements:
1. Start with a memorable hook
2. Highlight your unique value
3. Include 1-2 specific achievements with metrics
4. End with a clear call to action
5. Keep it natural and conversational
6. About {word_target} words

Write ONLY the pitch:"""

        try:
            if self.ollama_client.is_connected():
                return self.ollama_client.generate_response(prompt, temperature=0.5, max_tokens=word_target * 2)
        except Exception:
            pass

        return (
            "Hi, I'm a results-driven professional with expertise in delivering impactful solutions. "
            "In my most recent role, I led initiatives that drove measurable improvements in key metrics. "
            "I'm passionate about solving complex challenges and would love to discuss how my experience "
            "could contribute to your team's success."
        )

    def _frame_weakness(self, weakness: str, cv_text: str) -> str:
        """Frame a weakness as a growth opportunity."""
        prompt = f"""Help frame this weakness/gap for a job interview:

Weakness: {weakness}
Candidate's CV context: {cv_text[:500]}

Provide a response that:
1. Acknowledges the gap honestly (but briefly)
2. Shows self-awareness
3. Demonstrates proactive steps taken to address it
4. Frames it as a growth opportunity
5. Pivots to a related strength

Write a natural, conversational interview response (~100 words):"""

        try:
            if self.ollama_client.is_connected():
                return self.ollama_client.generate_response(prompt, temperature=0.4, max_tokens=200)
        except Exception:
            pass

        return (
            f'While I\'m still developing my skills in "{weakness}", I\'ve been actively working to close this gap '
            f'through self-study, online courses, and hands-on projects. What I\'ve found is that my strong '
            f'foundation in related areas allows me to pick up new skills quickly. I see this as an exciting '
            f'growth opportunity rather than a limitation.'
        )

    def _complete_prep_pack(self, cv_text: str, job_description: str, company_name: str, role_title: str):
        """Generate a complete prep pack (company research, 10 predicted questions with traps/STAR answers, and questions to ask)."""
        st.markdown(f"### {t('recruiter_prep_pack')}")
        st.markdown(t('recruiter_prep_pack_desc'))
        
        # Verify inputs
        if not company_name or not role_title:
            st.info(t("fill_role_details_info"))
            return

        if st.button(t("gen_prep_pack_btn"), type="primary", key="gen_prep_pack"):
            with st.spinner(t("analyzing_company_spinner")):
                prompt = f"""You are Dianelle, an expert career coach and corporate headhunter.
Help me prepare for my interview for the position "{role_title}" at "{company_name}".

CV (highlights): {cv_text[:1500]}
Job Description: {job_description[:1500]}

Please generate a comprehensive, highly customized Prep Pack in the following structure:

# COMPANY RESEARCH & BRIEF
Provide a brief on:
- What they do and how they make money.
- Their biggest current business challenge or product opportunity.
- Main competitors and how they differentiate.
- Culture and key values.

# 10 PREDICTED QUESTIONS, TRAPS, & ANSWERS
Predict 10 highly likely interview questions (behavioral, technical, situational). For each question, provide:
- QUESTION [number]: [Question text]
- WHY THEY ASK: [Why the recruiter asks this]
- TRAP: [The subtle trap or common mistake to avoid in the response]
- ANSWER: [A strong, persuasive 60-90 second response using specific metrics from my CV]

# 5 BUSINESS-SAVVY QUESTIONS TO ASK
Provide 5 high-impact questions I should ask the interviewer that prove I understand their business, economics, or product strategy. Avoid generic questions like "What is a typical day like?".

Format the section headers EXACTLY as:
# COMPANY RESEARCH & BRIEF
# 10 PREDICTED QUESTIONS, TRAPS, & ANSWERS
# 5 BUSINESS-SAVVY QUESTIONS TO ASK
"""
                try:
                    if self.ollama_client.is_connected():
                        response = self.ollama_client.generate_response(prompt, temperature=0.5, max_tokens=2500)
                        st.session_state['interview_prep_pack_raw'] = response
                    else:
                        st.session_state['interview_prep_pack_raw'] = "Ollama is disconnected. Unable to generate prep pack."
                except Exception as e:
                    st.session_state['interview_prep_pack_raw'] = f"Generation error: {str(e)}"

        if 'interview_prep_pack_raw' in st.session_state:
            raw_pack = st.session_state['interview_prep_pack_raw']
            
            if "Ollama is disconnected" in raw_pack or "Generation error" in raw_pack:
                st.error(raw_pack)
                return
                
            parts = self._parse_prep_pack(raw_pack)
            
            # Display Research
            st.markdown(t("company_research_brief_title"))
            st.info(parts['research'] or "Research brief not found.")
            
            # Display Questions
            st.markdown(t("predicted_questions_title"))
            if parts['questions']:
                parsed_qs = self._parse_individual_questions(parts['questions'])
                if parsed_qs:
                    for i, q in enumerate(parsed_qs, 1):
                        with st.expander(f"Q{i}: {q['question']}", expanded=(i <= 2)):
                            st.markdown(t("why_ask_label", reason=q['reason']))
                            st.warning(t("trap_label", trap=q['trap']))
                            st.success(t("strong_star_answer_label", answer=q['answer']))
                else:
                    st.markdown(parts['questions'])
            else:
                st.info("Questions content not found.")
                
            # Display Questions to Ask
            st.markdown(t("questions_to_ask_them_title"))
            st.markdown(parts['to_ask'] or "Questions to ask not found.")

    def _parse_prep_pack(self, response: str) -> Dict[str, str]:
        parts = {
            'research': '',
            'questions': '',
            'to_ask': ''
        }
        import re
        research_match = re.search(r'# COMPANY RESEARCH & BRIEF(.*?)(?=# 10 PREDICTED|$)', response, re.DOTALL | re.IGNORECASE)
        questions_match = re.search(r'# 10 PREDICTED QUESTIONS, TRAPS, & ANSWERS(.*?)(?=# 5 BUSINESS-SAVVY|$)', response, re.DOTALL | re.IGNORECASE)
        to_ask_match = re.search(r'# 5 BUSINESS-SAVVY QUESTIONS TO ASK(.*)', response, re.DOTALL | re.IGNORECASE)
        
        if research_match:
            parts['research'] = research_match.group(1).strip()
        if questions_match:
            parts['questions'] = questions_match.group(1).strip()
        if to_ask_match:
            parts['to_ask'] = to_ask_match.group(1).strip()
            
        # Fallback if parsing fails
        if not parts['research'] and not parts['questions'] and not parts['to_ask']:
            parts['questions'] = response
            
        return parts

    def _parse_individual_questions(self, questions_text: str) -> List[Dict[str, str]]:
        import re
        q_blocks = re.split(r'QUESTION\s*(?:\[?\d+\]?)?:\s*', questions_text, flags=re.IGNORECASE)
        parsed_qs = []
        for block in q_blocks:
            block = block.strip()
            if not block:
                continue
                
            lines = block.split('\n')
            q_text = lines[0].strip()
            
            why_match = re.search(r'WHY THEY ASK:\s*(.*?)(?=(?:TRAP:|ANSWER:|$))', block, re.DOTALL | re.IGNORECASE)
            trap_match = re.search(r'TRAP:\s*(.*?)(?=(?:ANSWER:|$))', block, re.DOTALL | re.IGNORECASE)
            answer_match = re.search(r'ANSWER:\s*(.*)', block, re.DOTALL | re.IGNORECASE)
            
            parsed_qs.append({
                'question': q_text,
                'reason': why_match.group(1).strip() if why_match else 'To assess suitability for the role',
                'trap': trap_match.group(1).strip() if trap_match else 'Giving a generic or unprepared response',
                'answer': answer_match.group(1).strip() if answer_match else 'Highlight a relevant accomplishment from your CV.'
            })
        return parsed_qs

    def _mock_interview(self, cv_text: str, job_description: str, company_name: str, role_title: str):
        """Interactive Mock Interview chatbot tab."""
        st.markdown(f"### {t('mock_interview_title')}")
        st.markdown(t('mock_interview_desc'))
        
        # Verify inputs
        if not company_name or not role_title:
            st.info(t("mock_fill_details_info"))
            return

        if 'mock_chat_history' not in st.session_state:
            st.session_state['mock_chat_history'] = []

        # Display history
        for msg in st.session_state['mock_chat_history']:
            if msg['role'] == 'user':
                with st.chat_message("user"):
                    st.write(msg['content'])
            else:
                with st.chat_message("assistant"):
                    st.write(msg['content'])

        # Start button
        if not st.session_state['mock_chat_history']:
            if st.button(t("start_mock_btn"), type="primary", key="start_mock_btn"):
                with st.spinner(t("setting_up_room_spinner")):
                    prompt = f"""You are Dianelle, an expert recruiter conducting a 15-minute mock interview for the position "{role_title}" at "{company_name}".
Please welcome the candidate, state the role, and ask the first question based on their CV and target job requirements. Ask ONLY one question.

Candidate's CV: {cv_text[:1000]}
Job Description: {job_description[:800]}
"""
                    try:
                        if self.ollama_client.is_connected():
                            first_q = self.ollama_client.generate_response(prompt, temperature=0.6)
                            st.session_state['mock_chat_history'].append({
                                'role': 'assistant',
                                'content': first_q
                            })
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error starting interview: {str(e)}")

        # Chat input (only if active)
        if st.session_state['mock_chat_history']:
            user_response = st.chat_input(t("mock_chat_placeholder"), key="mock_chat_input")
            if user_response:
                st.session_state['mock_chat_history'].append({
                    'role': 'user',
                    'content': user_response
                })
                
                # Format conversation history
                history_str = ""
                for msg in st.session_state['mock_chat_history']:
                    history_str += f"{msg['role'].upper()}: {msg['content']}\n\n"
                
                with st.spinner(t("evaluating_mock_spinner")):
                    prompt = f"""You are Dianelle, an expert recruiter conducting a mock interview for the position "{role_title}" at "{company_name}".
The candidate has just answered your question.

Please evaluate their response and provide brief constructive feedback in 2 parts:
1. WHAT WAS STRONG:
2. WHAT TO IMPROVE:
Then, ask the next logical interview question (keep track, ask 5 questions in total, current question number is {len(st.session_state['mock_chat_history']) // 2 + 1}).

Candidate's CV: {cv_text[:1000]}
Job Description: {job_description[:800]}

Here is the conversation history:
{history_str}
"""
                    try:
                        if self.ollama_client.is_connected():
                            next_response = self.ollama_client.generate_response(prompt, temperature=0.5)
                            st.session_state['mock_chat_history'].append({
                                'role': 'assistant',
                                'content': next_response
                            })
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error generating feedback: {str(e)}")

            if st.button(t("reset_interview_btn"), key="reset_mock_btn"):
                st.session_state['mock_chat_history'] = []
                st.rerun()

    def _behavioral_tech_questions(self, cv_text: str, job_description: str, analysis: Dict):
        """Combine Behavioral and Technical questions in one view."""
        col1, col2 = st.columns(2)
        with col1:
            self._behavioral_questions(cv_text, job_description)
        with col2:
            self._technical_questions(cv_text, job_description, analysis)

    def _elevator_pitch_and_framing(self, cv_text: str, job_description: str, analysis: Dict):
        """Combine Elevator Pitch and Weakness Framing in one view."""
        col1, col2 = st.columns(2)
        with col1:
            self._elevator_pitch(cv_text, job_description)
        with col2:
            self._weakness_strength_framing(cv_text, analysis)
