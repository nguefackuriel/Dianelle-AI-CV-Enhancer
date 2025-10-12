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
        self.model = "llama3.2:3b"  # Default model - using available Llama 3.2
        self.available_models = []
        self._check_connection()
    
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
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'No response generated')
            else:
                return f"Error: HTTP {response.status_code}"
                
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}"
    
    def analyze_cv_content(self, cv_text: str, job_description: str) -> Dict[str, Any]:
        """
        Analyze CV content against job description using LLM
        
        Args:
            cv_text: CV content
            job_description: Job description
            
        Returns:
            dict: Analysis results
        """
        prompt = f"""
        You are Dianelle, an expert AI career advisor and ATS optimization specialist. You are friendly, encouraging, and provide practical advice. 
        
        Please analyze the following CV against the job description and provide detailed feedback:

        JOB DESCRIPTION:
        {job_description[:2500]}

        CV CONTENT:
        {cv_text[:3000]}

        Please provide your analysis in the following format:

        STRENGTHS:
        - List 3-5 key strengths of this CV
        
        AREAS FOR IMPROVEMENT:
        - List 3-5 specific areas that need improvement
        
        MISSING KEYWORDS:
        - List important keywords from the job description that are missing from the CV
        
        ATS OPTIMIZATION SCORE: X/100
        - Provide a score and brief explanation
        
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
        4. Is personalized and engaging
        5. Is approximately 300-400 words

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
            
            for line in analysis_text.split('\n'):
                line = line.strip()
                if line.upper().startswith(('STRENGTHS:', 'AREAS FOR IMPROVEMENT:', 'MISSING KEYWORDS:', 'RECOMMENDATIONS:')):
                    if current_section:
                        sections[current_section] = '\n'.join(current_content)
                    current_section = line.rstrip(':').lower().replace(' ', '_')
                    current_content = []
                elif line and current_section:
                    current_content.append(line)
            
            # Add last section
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            
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
