"""
Ollama Client Module
Interface for communicating with local Ollama LLM
"""

import requests
import json
import streamlit as st
from typing import Optional, Dict, Any


class OllamaClient:
    """Client for interacting with Ollama LLM server"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.available_models = []
        self._check_connection()
        
        # Determine model to use, prioritizing selected model from session state
        if 'selected_model' in st.session_state:
            self.model = st.session_state['selected_model']
        elif self.available_models:
            self.model = self.available_models[0]
            st.session_state['selected_model'] = self.model
        else:
            self.model = "llama3.2:3b"  # Default fallback
            st.session_state['selected_model'] = self.model
    
    def _check_connection(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models_data = response.json()
                self.available_models = [model['name'] for model in models_data.get('models', [])]
                return True
        except Exception:
            pass
        return False
    
    def is_connected(self) -> bool:
        """Check if connected to Ollama"""
        return self._check_connection()
    
    def get_available_models(self) -> list:
        """Get list of available models"""
        return self.available_models
    
    def set_model(self, model_name: str):
        """Set the model to use"""
        if model_name in self.available_models:
            self.model = model_name
            st.session_state['selected_model'] = model_name
        else:
            st.warning(f"Model {model_name} not available. Using {self.model}")
    
    def generate_response(self, prompt: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """
        Generate response from Ollama model
        
        Args:
            prompt: Input prompt
            temperature: Randomness of response (0.0 - 1.0)
            max_tokens: Maximum tokens in response
            
        Returns:
            str: Generated response
        """
        # Inject strict human-tone guidelines to avoid AI-generated styling and buzzwords
        tone_guidelines = (
            "\n\nCRITICAL WRITING STYLES DIRECTIVES:\n"
            "- Write in a completely natural, professional, human tone.\n"
            "- Avoid typical AI buzzwords, transitions, and phrases (e.g., 'delve', 'dive deep', 'tapestry', 'testament', "
            "'moreover', 'furthermore', 'leverage', 'synergy', 'paradigm', 'robust', 'foster', 'beacon', 'revolutionize', "
            "'cutting-edge', 'seamless', 'in conclusion').\n"
            "- Use active voice, varied sentence lengths, and concrete verbs rather than flowery adjectives.\n"
            "- Keep the writing direct, clean, and professional. Avoid fluff, filler, and dramatic intros/outros.\n"
            "- Sound like a top-tier professional executive or an experienced career coach, not an AI language model."
        )
        prompt_with_tone = prompt + tone_guidelines
        
        try:
            payload = {
                "model": self.model,
                "prompt": prompt_with_tone,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=300
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'No response generated')
            else:
                return f"Error: HTTP {response.status_code}"
                
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}"
    
    def analyze_cv_content(self, cv_text: str, job_description: str, ats_score: int = None) -> Dict[str, Any]:
        """
        Analyze CV content against job description using LLM
        
        Args:
            cv_text: CV content
            job_description: Job description
            ats_score: Calculated ATS score to keep AI analysis consistent with score dashboard
            
        Returns:
            dict: Analysis results
        """
        score_instruction = ""
        if ats_score is not None:
            score_instruction = f"""
        ATS OPTIMIZATION SCORE: {ats_score}/100
        - You MUST use EXACTLY the score '{ats_score}/100'. Provide a brief, supportive, and objective explanation for why the CV received this score of {ats_score} based on the alignment of skills, experience, and formatting.
"""
        else:
            score_instruction = """
        ATS OPTIMIZATION SCORE: X/100
        - Provide a score and brief explanation.
"""

        prompt = f"""
        You are Dianelle, an expert senior recruiter and ATS optimization specialist. Please analyze the following CV against the job description and provide detailed feedback:

        JOB DESCRIPTION:
        {job_description[:2500]}

        CV CONTENT:
        {cv_text[:3000]}

        Please provide your analysis in the following format:

        STRENGTHS:
        - List 3-5 key strengths of this CV
        
        AREAS FOR IMPROVEMENT:
        - List 3-5 specific areas that need improvement
        
        RED FLAGS / SIGNAUX D'ALARME:
        - List 3 critical red flags that a recruiter or an automated parser would spot in under 10 seconds (e.g. unexplained gaps, lack of metrics, formatting traps, wordiness)
        
        MISSING KEYWORDS:
        - List important keywords from the job description that are missing from the CV
        {score_instruction}
        SPECIFIC RECOMMENDATIONS:
        - Provide 3-5 specific, actionable recommendations to improve this CV
        """
        
        response = self.generate_response(prompt, temperature=0.3, max_tokens=1500)
        return self._parse_cv_analysis(response)
    
    def enhance_cv_section(self, section_content: str, section_type: str, job_requirements: str) -> str:
        """
        Enhance a specific section of the CV
        
        Args:
            section_content: Current section content
            section_type: Type of section (summary, experience, skills, etc.)
            job_requirements: Relevant job requirements
            
        Returns:
            str: Enhanced section content
        """
        prompt = f"""
        You are Dianelle, a professional AI career advisor and CV writer. Please enhance the following {section_type} section to better match the job requirements while maintaining truthfulness and providing encouraging guidance.

        CURRENT {section_type.upper()} SECTION:
        {section_content}

        JOB REQUIREMENTS:
        {job_requirements}

        Please rewrite this section to:
        1. Include relevant keywords naturally
        2. Use strong action verbs
        3. Quantify achievements where possible
        4. Make it more ATS-friendly
        5. Keep it professional and truthful

        Enhanced {section_type} section:
        """
        
        return self.generate_response(prompt, temperature=0.4, max_tokens=800)
    
    def generate_cover_letter(self, cv_text: str, job_description: str, company_name: str = "") -> str:
        """
        Generate a personalized cover letter
        
        Args:
            cv_text: CV content
            job_description: Job description
            company_name: Company name (optional)
            
        Returns:
            str: Generated cover letter
        """
        prompt = f"""
        You are Dianelle, a professional AI career advisor and cover letter writer. Create a compelling and personalized cover letter based on the following information:

        CV SUMMARY:
        {cv_text[:1500]}

        JOB DESCRIPTION:
        {job_description[:1500]}

        COMPANY: {company_name if company_name else "[Company Name]"}

        Please write a professional cover letter that:
        1. Shows enthusiasm for the role
        2. Highlights relevant experience from the CV
        3. Addresses key job requirements
        4. Is written in a natural, conversational, and authentic human tone (avoiding robotic phrasing, buzzwords, or clichés like "Furthermore", "Moreover", "In conclusion", "Testament to", "I am thrilled to")
        5. Is personalized and engaging
        6. Is approximately 300-400 words

        Cover Letter:
        """
        
        return self.generate_response(prompt, temperature=0.5, max_tokens=1000)
    
    def chat_about_career(self, user_message: str, cv_context: str = "", job_context: str = "") -> str:
        """
        Chat about career-related topics
        
        Args:
            user_message: User's question/message
            cv_context: CV context (optional)
            job_context: Job description context (optional)
            
        Returns:
            str: AI response
        """
        context = ""
        if cv_context:
            context += f"CV Context: {cv_context[:800]}\n\n"
        if job_context:
            context += f"Job Context: {job_context[:800]}\n\n"
        
        prompt = f"""
        You are Dianelle, a helpful and friendly AI career advisor and CV expert. You provide practical, actionable advice with an encouraging and supportive tone to help people advance their careers and improve their job applications.

        {context}

        User Question: {user_message}

        Please provide a helpful, specific response that addresses the user's question. If relevant, reference their CV or the job they're interested in. Keep your response concise but informative.

        Response:
        """
        
        return self.generate_response(prompt, temperature=0.6, max_tokens=800)
    
    def _parse_cv_analysis(self, analysis_text: str) -> Dict[str, Any]:
        """Parse the structured analysis response"""
        try:
            # Extract score using regex
            import re
            score_match = re.search(r'SCORE:\s*(\d+)', analysis_text)
            score = int(score_match.group(1)) if score_match else 70
            
            # Split into sections
            sections = {}
            current_section = None
            current_content = []
            
            headers = ('STRENGTHS:', 'AREAS FOR IMPROVEMENT:', 'RED FLAGS / SIGNAUX D\'ALARME:', 'RED FLAGS:', 'MISSING KEYWORDS:', 'RECOMMENDATIONS:', 'SPECIFIC RECOMMENDATIONS:')
            
            for line in analysis_text.split('\n'):
                line = line.strip()
                upper_line = line.upper()
                
                matched_header = None
                for header in headers:
                    if upper_line.startswith(header):
                        matched_header = header
                        break
                        
                if matched_header:
                    if current_section:
                        sections[current_section] = '\n'.join(current_content).strip()
                    
                    sec_lower = matched_header.lower()
                    if 'red flags' in sec_lower or 'signaux' in sec_lower:
                        current_section = 'red_flags'
                    elif 'strengths' in sec_lower:
                        current_section = 'strengths'
                    elif 'improvement' in sec_lower:
                        current_section = 'areas_for_improvement'
                    elif 'keywords' in sec_lower:
                        current_section = 'missing_keywords'
                    elif 'recommendations' in sec_lower:
                        current_section = 'recommendations'
                    else:
                        current_section = sec_lower.rstrip(':').replace(' ', '_')
                    current_content = []
                elif line and current_section:
                    current_content.append(line)
            
            # Add last section
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            
            return {
                'score': score,
                'analysis_text': analysis_text,
                'sections': sections
            }
            
        except Exception:
            return {
                'score': 70,
                'analysis_text': analysis_text,
                'sections': {}
            }

    def generate_hadrien_cover_letter(
        self,
        cv_text: str,
        job_description: str,
        company_name: str,
        hiring_manager: str,
        role_title: str,
        company_notes: str = '',
        why_company: str = '',
        gap_text: str = '',
    ) -> str:
        """
        Generate a cover letter following Hadrien's Step 5 formula.
        """
        prompt = f"""You are an expert career advisor and professional writer.
Write a highly personalized cover letter based on the following candidate CV and target role.

CANDIDATE CV (highlights):
{cv_text[:2000]}

JOB DESCRIPTION:
{job_description[:1500]}

DETAILS:
- Company: {company_name}
- Hiring Manager: {hiring_manager or 'Hiring Manager'}
- Role: {role_title}
{'- Company notes/culture: ' + company_notes if company_notes else ''}
{'- Why candidate wants this company: ' + why_company if why_company else ''}
{'- Candidate gap/weakness to address head-on: ' + gap_text if gap_text else ''}

Rules:
1. Address to {hiring_manager or 'Hiring Manager'} at {company_name}.
2. Paragraph 1: Hook showing that the candidate understands the company's biggest current business problem or opportunity (use the job description as an index).
3. Paragraph 2: 2 or 3 specific examples of achievements from the CV that correspond directly to what they seek.
4. Paragraph 3: Address a potential gap or weakness (e.g. career gap, missing technology, career change) head-on and reframe it positively as a strength (e.g., adaptability, rapid learning rate).
5. Paragraph 4: Conclude with a very specific, genuine business reason for wanting to work at THIS company specifically.
6. Tone: Confident, direct, authentic, zero AI buzzwords, zero fluff, zero emojis.
7. Length: Keep it strictly under 250 words.
8. Do NOT make it sound like it was written by an AI.

Write ONLY the cover letter body. Do not include any preambles, introductory commentary, or postambles:"""

        return self.generate_response(prompt, temperature=0.5, max_tokens=600)

    def run_double_test_scan(self, cv_text: str, job_description: str) -> str:
        """
        Run the Step 3 Double Test scan (ATS filter + human recruiter 200-CV scanner).
        """
        prompt = f"""You are acting simultaneously as:
1. A strict automated ATS filter checking for keyword alignment, formatting issues, and structural parsing.
2. A senior recruiter who has read 200 CVs today and is looking for any excuse to skip or reject.

Analyze the candidate's CV against the job description. Identify which sections of this CV would be ignored or skimmed over, and explain why. Then, suggest how to rewrite them to make them "scroll-stoppers" (hooks, metric-driven achievements, high-impact statements).

CV TEXT:
{cv_text}

JOB DESCRIPTION:
{job_description}

Please format your response clearly. Use these headers:

### SECTIONS AT RISK OF BEING IGNORED
Provide a direct and honest analysis of what is weak or easily ignorable.

### SCROLL-STOPPER RECOMMENDATIONS & REWRITES
Provide specific guidelines and draft examples of how to rewrite those weak parts to force a recruiter to stop scrolling.

Write your response directly with no AI preambles or chat commentary:"""

        return self.generate_response(prompt, temperature=0.4, max_tokens=1000)

    def generate_linkedin_experience(self, cv_experience: str, job_description: str) -> str:
        """
        Optimize CV experiences for LinkedIn (Step 8, Section 3).
        Uses Google XYZ formula, a more conversational tone, and adds "What I learned" per role.
        """
        prompt = f"""You are a senior recruiter. Help me optimize my professional experiences section for my LinkedIn profile.

CV EXPERIENCE SECTION:
{cv_experience}

TARGET ROLE CONTEXT:
{job_description[:1000]}

Rules:
1. Apply the Google XYZ formula ("Accomplished X, measured by Y, by doing Z") for accomplishments.
2. Write in first person, but in a slightly more conversational tone than the raw CV bullet points.
3. For each role/position, include 1 line at the end summarizing "What I learned" or "Key takeaway" during that experience.
4. Eliminate recruiter red flags and typical AI buzzwords.
5. Do NOT include any emojis.

Output the optimized experiences section directly with no introductory or concluding text:"""

        return self.generate_response(prompt, temperature=0.4, max_tokens=1000)

    def generate_linkedin_skills_featured(self, cv_text: str, job_description: str) -> str:
        """
        Suggest top 5 search-priority LinkedIn skills to pin and Featured section items (Step 8, Sections 4 & 5).
        """
        prompt = f"""Analyze this candidate CV and target job description to recommend optimized LinkedIn profile settings.

CV:
{cv_text[:2000]}

JOB DESCRIPTION:
{job_description[:1000]}

Please output exactly:
1. TOP 5 SKILLS TO EPIN / PIN: Recommend the top 5 high-priority search keywords/skills that recruiters search for, ordered by search priority.
2. FEATURED SECTION SUGGESTIONS: Recommend 2-3 specific items (e.g. articles, Github repos, presentations, portfolios) the candidate could display in their Featured section to arrest a recruiter's attention.

Format your output clearly with markdown headers:
### TOP 5 PINNED SKILLS
### FEATURED SECTION RECOMMENDATIONS

Write only the recommendations:"""

        return self.generate_response(prompt, temperature=0.4, max_tokens=500)

    def generate_salary_negotiation(
        self,
        role_title: str,
        company_name: str,
        base_salary: str,
        bonus: str,
        equity: str,
        benefits: str,
    ) -> str:
        """
        Generate a salary negotiation pack (Step 7).
        """
        prompt = f"""You are an expert salary negotiation coach and headhunter.
Help the candidate negotiate a job offer for the position "{role_title}" at "{company_name}".

OFFER DETAILS:
- Base Salary: {base_salary}
- Bonus: {bonus}
- Equity/Stock Options: {equity}
- Benefits/Other: {benefits}

Please structure your response with these exact headers:

### MARKET ANALYSIS & TARGET
Suggest where this offer stands compared to the market and suggest a target counter-offer with precise business justification.

### EMAIL NEGOTIATION SCRIPT
Write the exact, professional, polite, yet confident email to send to the recruiter/hiring manager. Express sincere excitement for the role, cite market alignment research, and ask for a specific, single target number (do not give a range). Keep it natural, human, and free of AI buzzwords and emojis.

### PHONE NEGOTIATION SCRIPT
Provide word-for-word scripts for:
1. Opening the conversation.
2. Stating the counter-proposal.
3. Handling the objection: "This is our final offer."
4. Pivoting to negotiate non-financial items (sign-on bonus, extra PTO, remote work flexibility, accelerated review) if base salary is truly fixed.

### WALK-AWAY STRATEGY
Advise on setting a walk-away threshold and how to evaluate non-financial compensation.

Write ONLY the negotiation pack with these headers. No AI chat preambles:"""

        return self.generate_response(prompt, temperature=0.4, max_tokens=1500)

    def generate_followup_emails(
        self,
        role_title: str,
        company_name: str,
        cv_summary: str,
        interviewer_name: str = '',
    ) -> str:
        """
        Generate 3 follow-up email templates (Step 9).
        """
        prompt = f"""You are a professional career coach. Write 3 highly effective follow-up emails for the position of "{role_title}" at "{company_name}".

CANDIDATE CV CONTEXT:
{cv_summary[:1000]}

Please generate exactly these 3 templates:

### TEMPLATE 1: POST-APPLICATION (Send 3 days after applying)
- Target: Under 60 words.
- Focus: Reference a specific detail of the role or team, restate your fit in 1 sentence, and request a next step.
- Tone: Confident, direct, direct human voice.

### TEMPLATE 2: POST-INTERVIEW THANK-YOU (Send within 24 hours of interview)
- Target: Under 100 words.
- Focus: Address {interviewer_name or 'the interviewer'} by name, reference a specific moment from the conversation, and reinforce your strongest relevant accomplishment.
- Tone: Warm, professional, organic.

### TEMPLATE 3: TIMELINE CHECK-IN (Send 7 days after interview if no news)
- Target: Under 80 words.
- Focus: Polite, value-add check-in (mention a relevant article, sector trend, or brief thought), and give them a polite out ("If the timeline has shifted, I completely understand").
- Tone: Professional, no desperation.

Rules:
1. No emojis in any email.
2. Absolutely no AI buzzwords or cliché transitions.
3. Keep them strictly under the word targets.

Write only the templates under their respective headers. No introductory or concluding text:"""

        return self.generate_response(prompt, temperature=0.4, max_tokens=800)
