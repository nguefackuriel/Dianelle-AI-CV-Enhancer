"""
CV Analyzer Module
Main analysis engine for CV optimization and scoring
"""

import re
import textstat
from collections import Counter
from utils.keyword_extractor import KeywordExtractor
from utils.ollama_client import OllamaClient


class CVAnalyzer:
    """Main CV analysis and optimization engine"""
    
    def __init__(self):
        self.keyword_extractor = KeywordExtractor()
        self.ollama_client = OllamaClient()
        
        # ATS-friendly formatting rules
        self.ats_rules = {
            'max_length': 2000,  # Maximum character length
            'min_sections': 4,   # Minimum number of sections
            'contact_info_required': True,
            'bullet_points_preferred': True,
            'avoid_tables': True,
            'avoid_graphics': True
        }
    
    def analyze_cv(self, cv_text: str, job_description: str) -> dict:
        """
        Perform comprehensive CV analysis
        
        Args:
            cv_text: CV content text
            job_description: Target job description
            
        Returns:
            dict: Complete analysis results
        """
        # Extract keywords from both texts
        cv_keywords = self.keyword_extractor.extract_keywords_from_cv(cv_text)
        job_keywords = self.keyword_extractor.extract_keywords_from_job_description(job_description)
        
        # Compare keywords
        keyword_comparison = self.keyword_extractor.compare_keywords(cv_keywords, job_keywords)
        
        # Analyze CV structure and formatting
        structure_analysis = self._analyze_structure(cv_text)
        
        # Calculate ATS compatibility score
        ats_score = self._calculate_ats_score(cv_text, job_description, keyword_comparison, structure_analysis)
        
        # Get AI-powered analysis
        ai_analysis = self._get_ai_analysis(cv_text, job_description)
        
        # Generate improvement suggestions
        suggestions = self._generate_suggestions(cv_text, job_description, keyword_comparison, structure_analysis)
        
        # Compile results
        results = {
            'ats_score': ats_score,
            'keyword_match_percentage': keyword_comparison['match_percentage'],
            'matched_keywords': keyword_comparison['matched_keywords'],
            'missing_keywords': keyword_comparison['missing_keywords'],
            'technical_skills_match': keyword_comparison['matched_technical'],
            'missing_technical_skills': keyword_comparison['missing_technical'],
            'structure_analysis': structure_analysis,
            'suggestions': suggestions,
            'ai_analysis': ai_analysis,
            'readability_score': self._calculate_readability(cv_text),
            'word_count': len(cv_text.split()),
            'sections_detected': self._detect_sections(cv_text),
            'enhancement_opportunities': self._find_enhancement_opportunities(cv_text, job_description)
        }
        
        return results
    
    def _analyze_structure(self, cv_text: str) -> dict:
        """Analyze CV structure and formatting"""
        
        analysis = {
            'has_contact_info': self._has_contact_info(cv_text),
            'has_summary': self._has_summary_section(cv_text),
            'has_experience': self._has_experience_section(cv_text),
            'has_education': self._has_education_section(cv_text),
            'has_skills': self._has_skills_section(cv_text),
            'uses_bullet_points': self._uses_bullet_points(cv_text),
            'has_quantified_achievements': self._has_quantified_achievements(cv_text),
            'appropriate_length': self._check_length(cv_text),
            'section_count': len(self._detect_sections(cv_text)),
            'formatting_issues': self._detect_formatting_issues(cv_text)
        }
        
        return analysis
    
    def _calculate_ats_score(self, cv_text: str, job_description: str, keyword_comparison: dict, structure_analysis: dict) -> int:
        """Calculate overall ATS compatibility score (0-100)"""
        
        score = 0
        
        # Keyword matching (40% of score)
        keyword_score = min(keyword_comparison['match_percentage'], 40)
        score += keyword_score
        
        # Structure and formatting (30% of score)
        structure_score = 0
        if structure_analysis['has_contact_info']:
            structure_score += 5
        if structure_analysis['has_summary']:
            structure_score += 3
        if structure_analysis['has_experience']:
            structure_score += 5
        if structure_analysis['has_education']:
            structure_score += 3
        if structure_analysis['has_skills']:
            structure_score += 4
        if structure_analysis['uses_bullet_points']:
            structure_score += 3
        if structure_analysis['has_quantified_achievements']:
            structure_score += 4
        if structure_analysis['appropriate_length']:
            structure_score += 3
        
        score += structure_score
        
        # Technical skills match (20% of score)
        tech_skills_score = min(len(keyword_comparison['matched_technical']) * 2, 20)
        score += tech_skills_score
        
        # Content quality (10% of score)
        content_score = 0
        if self._has_action_verbs(cv_text):
            content_score += 5
        if len(cv_text.split()) >= 200:  # Minimum content
            content_score += 5
        
        score += content_score
        
        return min(score, 100)
    
    def _get_ai_analysis(self, cv_text: str, job_description: str) -> dict:
        """Get AI-powered analysis from Ollama"""
        try:
            if self.ollama_client.is_connected():
                return self.ollama_client.analyze_cv_content(cv_text, job_description)
            else:
                return {
                    'score': 70,
                    'analysis_text': 'AI analysis unavailable - Ollama not connected',
                    'sections': {}
                }
        except Exception as e:
            return {
                'score': 70,
                'analysis_text': f'AI analysis error: {str(e)}',
                'sections': {}
            }
    
    def _generate_suggestions(self, cv_text: str, job_description: str, keyword_comparison: dict, structure_analysis: dict) -> list:
        """Generate specific improvement suggestions"""
        
        suggestions = []
        
        # Keyword-based suggestions
        if keyword_comparison['match_percentage'] < 50:
            suggestions.append({
                'title': 'Improve Keyword Matching',
                'description': f'Your CV matches only {keyword_comparison["match_percentage"]:.1f}% of job keywords. Consider incorporating these missing keywords: {", ".join(keyword_comparison["missing_keywords"][:5])}',
                'priority': 'high',
                'category': 'keywords'
            })
        
        if keyword_comparison['missing_technical']:
            suggestions.append({
                'title': 'Add Technical Skills',
                'description': f'Include these technical skills if you have experience: {", ".join(keyword_comparison["missing_technical"][:3])}',
                'priority': 'high',
                'category': 'technical_skills'
            })
        
        # Structure-based suggestions
        if not structure_analysis['has_summary']:
            suggestions.append({
                'title': 'Add Professional Summary',
                'description': 'Include a 2-3 sentence professional summary at the top of your CV highlighting your key qualifications.',
                'priority': 'medium',
                'category': 'structure'
            })
        
        if not structure_analysis['uses_bullet_points']:
            suggestions.append({
                'title': 'Use Bullet Points',
                'description': 'Format your experience and achievements using bullet points for better ATS readability.',
                'priority': 'medium',
                'category': 'formatting'
            })
        
        if not structure_analysis['has_quantified_achievements']:
            suggestions.append({
                'title': 'Quantify Your Achievements',
                'description': 'Add numbers, percentages, and metrics to your accomplishments (e.g., "Increased sales by 25%").',
                'priority': 'high',
                'category': 'content'
            })
        
        # Content quality suggestions
        if not self._has_action_verbs(cv_text):
            suggestions.append({
                'title': 'Use Strong Action Verbs',
                'description': 'Start bullet points with action verbs like "achieved," "managed," "developed," "implemented."',
                'priority': 'medium',
                'category': 'content'
            })
        
        # Length suggestions
        word_count = len(cv_text.split())
        if word_count < 200:
            suggestions.append({
                'title': 'Expand Content',
                'description': 'Your CV is quite short. Consider adding more detail about your experience and achievements.',
                'priority': 'medium',
                'category': 'content'
            })
        elif word_count > 800:
            suggestions.append({
                'title': 'Reduce Length',
                'description': 'Your CV is quite long. Consider condensing content to focus on the most relevant information.',
                'priority': 'low',
                'category': 'content'
            })
        
        return suggestions
    
    def _detect_sections(self, cv_text: str) -> list:
        """Detect sections in CV"""
        section_keywords = [
            'summary', 'profile', 'objective', 'about',
            'experience', 'employment', 'work history',
            'education', 'academic', 'qualifications',
            'skills', 'technical skills', 'competencies',
            'projects', 'certifications', 'achievements'
        ]
        
        detected_sections = []
        cv_lower = cv_text.lower()
        
        for keyword in section_keywords:
            if keyword in cv_lower:
                detected_sections.append(keyword)
        
        return list(set(detected_sections))
    
    def _has_contact_info(self, cv_text: str) -> bool:
        """Check if CV has contact information"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        
        has_email = bool(re.search(email_pattern, cv_text))
        has_phone = bool(re.search(phone_pattern, cv_text))
        
        return has_email or has_phone
    
    def _has_summary_section(self, cv_text: str) -> bool:
        """Check if CV has summary/profile section"""
        summary_keywords = ['summary', 'profile', 'objective', 'about me']
        cv_lower = cv_text.lower()
        return any(keyword in cv_lower for keyword in summary_keywords)
    
    def _has_experience_section(self, cv_text: str) -> bool:
        """Check if CV has experience section"""
        exp_keywords = ['experience', 'employment', 'work history', 'professional experience']
        cv_lower = cv_text.lower()
        return any(keyword in cv_lower for keyword in exp_keywords)
    
    def _has_education_section(self, cv_text: str) -> bool:
        """Check if CV has education section"""
        edu_keywords = ['education', 'academic', 'qualifications', 'degree']
        cv_lower = cv_text.lower()
        return any(keyword in cv_lower for keyword in edu_keywords)
    
    def _has_skills_section(self, cv_text: str) -> bool:
        """Check if CV has skills section"""
        skills_keywords = ['skills', 'technical skills', 'competencies', 'expertise']
        cv_lower = cv_text.lower()
        return any(keyword in cv_lower for keyword in skills_keywords)
    
    def _uses_bullet_points(self, cv_text: str) -> bool:
        """Check if CV uses bullet points"""
        bullet_patterns = [r'[•\-\*]', r'^\s*[-*+]\s', r'^\s*\d+\.\s']
        return any(re.search(pattern, cv_text, re.MULTILINE) for pattern in bullet_patterns)
    
    def _has_quantified_achievements(self, cv_text: str) -> bool:
        """Check if CV has quantified achievements"""
        number_patterns = [
            r'\d+%',  # percentages
            r'\$\d+',  # dollar amounts
            r'\d+\s*(million|thousand|k)',  # large numbers
            r'increased.*\d+',  # increased by X
            r'reduced.*\d+',  # reduced by X
            r'managed.*\d+'  # managed X people/projects
        ]
        return any(re.search(pattern, cv_text, re.IGNORECASE) for pattern in number_patterns)
    
    def _check_length(self, cv_text: str) -> bool:
        """Check if CV length is appropriate"""
        word_count = len(cv_text.split())
        return 200 <= word_count <= 1000  # Reasonable range
    
    def _detect_formatting_issues(self, cv_text: str) -> list:
        """Detect potential formatting issues"""
        issues = []
        
        # Check for excessive capitalization
        if len(re.findall(r'[A-Z]{3,}', cv_text)) > 10:
            issues.append('Excessive capitalization detected')
        
        # Check for inconsistent spacing
        if len(re.findall(r'\s{3,}', cv_text)) > 5:
            issues.append('Inconsistent spacing detected')
        
        # Check for special characters that might confuse ATS
        special_chars = re.findall(r'[^\w\s.,;:()\-@]', cv_text)
        if len(special_chars) > 20:
            issues.append('Too many special characters')
        
        return issues
    
    def _has_action_verbs(self, cv_text: str) -> bool:
        """Check if CV uses action verbs"""
        action_verbs = [
            'achieved', 'managed', 'led', 'developed', 'implemented', 'created',
            'designed', 'improved', 'increased', 'reduced', 'optimized'
        ]
        cv_lower = cv_text.lower()
        return any(verb in cv_lower for verb in action_verbs)
    
    def _calculate_readability(self, cv_text: str) -> float:
        """Calculate readability score using Flesch Reading Ease"""
        try:
            return textstat.flesch_reading_ease(cv_text)
        except:
            return 50.0  # Average score if calculation fails
    
    def _find_enhancement_opportunities(self, cv_text: str, job_description: str) -> list:
        """Find specific opportunities for CV enhancement"""
        opportunities = []
        
        # Look for weak language
        weak_words = ['responsible for', 'duties included', 'helped with']
        for weak_word in weak_words:
            if weak_word in cv_text.lower():
                opportunities.append(f'Replace "{weak_word}" with stronger action verbs')
        
        # Look for missing quantification opportunities
        quantifiable_verbs = ['managed', 'led', 'increased', 'reduced', 'improved']
        for verb in quantifiable_verbs:
            if verb in cv_text.lower() and not re.search(rf'{verb}.*\d+', cv_text, re.IGNORECASE):
                opportunities.append(f'Add numbers/metrics to "{verb}" statements')
        
        return opportunities
