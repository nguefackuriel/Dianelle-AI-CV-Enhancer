"""
Chat Interface Component
Interactive AI assistant for CV and career advice
"""

import streamlit as st
from utils.ollama_client import OllamaClient
from datetime import datetime


class ChatInterface:
    """Interactive chat interface for CV assistance"""
    
    def __init__(self):
        self.ollama_client = OllamaClient()
        
        # Predefined helpful prompts
        self.quick_prompts = [
            "How can I improve my CV for this job?",
            "What keywords should I add to my CV?",
            "How do I quantify my achievements?",
            "What's a good professional summary?",
            "How long should my CV be?",
            "What technical skills should I highlight?",
            "How do I format my CV for ATS?",
            "What action verbs should I use?",
        ]
        
        # Career advice templates
        self.advice_categories = {
            'cv_writing': {
                'title': ' CV Writing Tips',
                'prompts': [
                    "How do I write a compelling professional summary?",
                    "What's the best way to describe my work experience?",
                    "How should I format my education section?",
                    "What should I include in my skills section?"
                ]
            },
            'job_search': {
                'title': ' Job Search Strategy',
                'prompts': [
                    "How do I find the right jobs to apply for?",
                    "What's the best way to network professionally?",
                    "How should I prepare for interviews?",
                    "When should I follow up after applying?"
                ]
            },
            'career_development': {
                'title': ' Career Development',
                'prompts': [
                    "How can I advance in my current career?",
                    "What skills should I develop for my industry?",
                    "How do I transition to a new career field?",
                    "What certifications would help my career?"
                ]
            }
        }
    
    def display_chat_interface(self, cv_text: str = "", job_description: str = "", analysis_results: dict = None):
        """Display the main chat interface"""
        
        # Chat header with status
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### 💬 Chat with Dianelle")
            st.markdown("*Hi! I'm Dianelle, your AI career assistant. Ask me anything about your CV, career goals, or job search strategy*")
        
        with col2:
            if self.ollama_client.is_connected():
                st.success(" Dianelle Ready")
            else:
                st.error(" Dianelle Offline")
        
        # Quick action buttons
        if cv_text or job_description:
            st.markdown("#### Quick Actions")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button(" Explain My Score"):
                    if analysis_results:
                        self._explain_score(analysis_results)
            
            with col2:
                if st.button(" Improvement Tips"):
                    self._get_improvement_tips(cv_text, job_description)
            
            with col3:
                if st.button(" Keyword Help"):
                    self._get_keyword_help(cv_text, job_description)
        
        # Quick prompts
        with st.expander(" Quick Prompts - Click to get started"):
            self._display_quick_prompts()
        
        # Chat history display
        self._display_chat_history()
        
        # Chat input
        self._handle_chat_input(cv_text, job_description, analysis_results)
    
    def _display_quick_prompts(self):
        """Display categorized quick prompts"""
        
        for category, info in self.advice_categories.items():
            st.markdown(f"**{info['title']}**")
            
            cols = st.columns(2)
            for i, prompt in enumerate(info['prompts']):
                col = cols[i % 2]
                if col.button(prompt, key=f"{category}_{i}", use_container_width=True):
                    self._add_user_message(prompt)
                    self._generate_ai_response(prompt)
    
    def _display_chat_history(self):
        """Display chat message history"""
        
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Display messages
        for i, message in enumerate(st.session_state.chat_history):
            if message['role'] == 'user':
                with st.chat_message("user"):
                    st.write(message['content'])
            else:
                with st.chat_message("assistant"):
                    st.write(message['content'])
                    
                    # Add helpful actions for AI responses
                    if i == len(st.session_state.chat_history) - 1:  # Only for latest message
                        self._add_message_actions(message['content'])
    
    def _handle_chat_input(self, cv_text: str, job_description: str, analysis_results: dict):
        """Handle new chat input"""
        
        # Chat input
        if prompt := st.chat_input("Ask Dianelle anything about your CV or career..."):
            self._add_user_message(prompt)
            
            # Generate context-aware response
            full_prompt = self._build_context_prompt(prompt, cv_text, job_description, analysis_results)
            self._generate_ai_response(full_prompt, display_prompt=prompt)
    
    def _add_user_message(self, message: str):
        """Add user message to chat history"""
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        st.session_state.chat_history.append({
            'role': 'user',
            'content': message,
            'timestamp': datetime.now()
        })
    
    def _generate_ai_response(self, prompt: str, display_prompt: str = None):
        """Generate and display AI response"""
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    if self.ollama_client.is_connected():
                        response = self.ollama_client.generate_response(prompt, temperature=0.7)
                    else:
                        response = self._get_fallback_response(display_prompt or prompt)
                    
                    st.write(response)
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': response,
                        'timestamp': datetime.now()
                    })
                    
                    # Add helpful actions
                    self._add_message_actions(response)
                    
                except Exception as e:
                    error_message = f"I apologize, but I encountered an error: {str(e)}"
                    st.error(error_message)
                    
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': error_message,
                        'timestamp': datetime.now()
                    })
    
    def _build_context_prompt(self, user_prompt: str, cv_text: str, job_description: str, analysis_results: dict) -> str:
        """Build context-aware prompt for better responses"""
        
        context_parts = [
            "You are Dianelle, a helpful and friendly AI career advisor and CV expert. You provide practical, specific advice with a personal touch. Always be encouraging and supportive while being professional.",
            ""
        ]
        
        if cv_text:
            context_parts.extend([
                "USER'S CV CONTENT (first 1000 chars):",
                cv_text[:1000] + "..." if len(cv_text) > 1000 else cv_text,
                ""
            ])
        
        if job_description:
            context_parts.extend([
                "TARGET JOB DESCRIPTION (first 800 chars):",
                job_description[:800] + "..." if len(job_description) > 800 else job_description,
                ""
            ])
        
        if analysis_results:
            score = analysis_results.get('ats_score', 'N/A')
            matched = len(analysis_results.get('matched_keywords', []))
            missing = len(analysis_results.get('missing_keywords', []))
            
            context_parts.extend([
                f"CV ANALYSIS SUMMARY:",
                f"- ATS Score: {score}/100",
                f"- Matched Keywords: {matched}",
                f"- Missing Keywords: {missing}",
                ""
            ])
        
        context_parts.extend([
            f"USER QUESTION: {user_prompt}",
            "",
            "As Dianelle, provide a helpful, specific response with a friendly and encouraging tone. If relevant, reference their CV or job description. Keep it concise but actionable, and always be supportive of their career goals."
        ])
        
        return "\n".join(context_parts)
    
    def _add_message_actions(self, response_content: str):
        """Add helpful actions below AI responses"""
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button(" Helpful", key=f"helpful_{len(st.session_state.chat_history)}"):
                st.success("Thanks for the feedback!")
        
        with col2:
            if st.button(" Copy", key=f"copy_{len(st.session_state.chat_history)}"):
                st.info("Response copied to clipboard!")
        
        with col3:
            if st.button(" Regenerate", key=f"regen_{len(st.session_state.chat_history)}"):
                st.info("Feature coming soon!")
        
        with col4:
            if st.button(" Follow up", key=f"followup_{len(st.session_state.chat_history)}"):
                st.session_state['followup_active'] = True
    
    def _explain_score(self, analysis_results: dict):
        """Explain the CV score in detail"""
        score = analysis_results.get('ats_score', 0)
        
        explanation_prompt = f"""
        My CV received an ATS compatibility score of {score}/100. Can you explain what this score means and what factors contribute to it? Also, what should I focus on to improve this score?
        """
        
        self._add_user_message("Explain my CV score")
        self._generate_ai_response(explanation_prompt, display_prompt="Explain my CV score")
    
    def _get_improvement_tips(self, cv_text: str, job_description: str):
        """Get specific improvement tips"""
        
        tips_prompt = f"""
        Based on my CV and the job I'm targeting, what are the top 5 most important improvements I should make? Please be specific and actionable.
        """
        
        self._add_user_message("Give me improvement tips")
        full_prompt = self._build_context_prompt(tips_prompt, cv_text, job_description, None)
        self._generate_ai_response(full_prompt, display_prompt="Give me improvement tips")
    
    def _get_keyword_help(self, cv_text: str, job_description: str):
        """Get keyword optimization help"""
        
        keyword_prompt = f"""
        Help me optimize keywords in my CV for this job. What important keywords am I missing, and how should I naturally incorporate them?
        """
        
        self._add_user_message("Help with keywords")
        full_prompt = self._build_context_prompt(keyword_prompt, cv_text, job_description, None)
        self._generate_ai_response(full_prompt, display_prompt="Help with keywords")
    
    def _get_fallback_response(self, prompt: str) -> str:
        """Provide fallback responses when AI is unavailable"""
        
        fallback_responses = {
            'score': "Your ATS score indicates how well your CV is optimized for applicant tracking systems. Focus on including relevant keywords, clear formatting, and quantified achievements to improve it.",
            
            'keywords': "To optimize keywords: 1) Identify key terms from the job description, 2) Naturally incorporate them throughout your CV, 3) Focus on technical skills, action verbs, and industry terminology, 4) Avoid keyword stuffing.",
            
            'improve': "Key CV improvements: 1) Add quantified achievements with numbers/percentages, 2) Use strong action verbs (achieved, managed, led), 3) Include relevant keywords naturally, 4) Ensure clear formatting with bullet points, 5) Tailor content to the specific job.",
            
            'summary': "A strong professional summary should: 1) Be 2-3 sentences long, 2) Highlight your key qualifications, 3) Include years of experience, 4) Mention relevant skills/expertise, 5) Align with the target role.",
            
            'default': "Hi! I'm Dianelle, and I'd love to help you with your CV! Some general tips: use keywords from job descriptions, quantify achievements with numbers, use action verbs, keep formatting simple and ATS-friendly, and tailor your CV for each application. Feel free to ask me anything specific!"
        }
        
        # Simple keyword matching for responses
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['score', 'rating', 'grade']):
            return fallback_responses['score']
        elif any(word in prompt_lower for word in ['keyword', 'optimize', 'ats']):
            return fallback_responses['keywords']
        elif any(word in prompt_lower for word in ['improve', 'better', 'enhance']):
            return fallback_responses['improve']
        elif any(word in prompt_lower for word in ['summary', 'profile', 'objective']):
            return fallback_responses['summary']
        else:
            return fallback_responses['default']
    
    def get_response(self, user_input: str, cv_text: str = "", job_description: str = "", analysis_results: dict = None) -> str:
        """Get AI response for external use (backward compatibility)"""
        
        if self.ollama_client.is_connected():
            full_prompt = self._build_context_prompt(user_input, cv_text, job_description, analysis_results)
            return self.ollama_client.generate_response(full_prompt, temperature=0.7)
        else:
            return self._get_fallback_response(user_input)
    
    def clear_chat_history(self):
        """Clear the chat history"""
        if 'chat_history' in st.session_state:
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
