"""
CV Analyzer Module
Main analysis engine for CV optimization and scoring.
Delegates to ATSSimulator for production-grade ATS analysis.
"""

import re
import textstat
from collections import Counter
from typing import Dict, Any, List
from utils.keyword_extractor import KeywordExtractor
from utils.ollama_client import OllamaClient
from utils.ats_simulator import ATSSimulator


class CVAnalyzer:
    """Main CV analysis and optimization engine"""

    def __init__(self):
        self.keyword_extractor = KeywordExtractor()
        self.ollama_client = OllamaClient()
        self.ats_simulator = ATSSimulator()

    def analyze_cv(self, cv_text: str, job_description: str) -> dict:
        """
        Perform comprehensive CV analysis.

        Args:
            cv_text: CV content text
            job_description: Target job description

        Returns:
            dict: Complete analysis results
        """
        # ---- ATS Simulation (core scoring) ----
        ats_results = self.ats_simulator.simulate_ats_parse(cv_text, job_description)

        # ---- Legacy keyword extraction (still useful for UI display) ----
        cv_keywords = self.keyword_extractor.extract_keywords_from_cv(cv_text)
        job_keywords = self.keyword_extractor.extract_keywords_from_job_description(job_description)
        keyword_comparison = self.keyword_extractor.compare_keywords(cv_keywords, job_keywords)

        # ---- Structure analysis ----
        structure_analysis = self._analyze_structure(cv_text)

        # ---- AI-powered analysis ----
        ai_analysis = self._get_ai_analysis(cv_text, job_description, ats_score=ats_results['ats_score'])

        # ---- Merge ATS recommendations with legacy suggestions ----
        suggestions = ats_results.get('recommendations', [])
        if not suggestions:
            suggestions = self._generate_suggestions(cv_text, job_description, keyword_comparison, structure_analysis)

        # ---- Compile comprehensive results ----
        results = {
            # Core scores
            'ats_score': ats_results['ats_score'],
            'component_scores': ats_results['component_scores'],
            'component_weights': ats_results['component_weights'],
            'semantic_similarity': ats_results['semantic_similarity'],

            # Keyword data
            'keyword_match_percentage': keyword_comparison['match_percentage'],
            'matched_keywords': (
                ats_results['keyword_analysis']['matched_keywords']
                or keyword_comparison['matched_keywords']
            ),
            'missing_keywords': (
                ats_results['keyword_analysis']['missing_keywords']
                or keyword_comparison['missing_keywords']
            ),
            'technical_skills_match': keyword_comparison['matched_technical'],
            'missing_technical_skills': keyword_comparison['missing_technical'],
            'keyword_analysis': ats_results['keyword_analysis'],

            # Structure
            'structure_analysis': structure_analysis,
            'parsed_sections': ats_results['parsed_sections'],
            'sections_detected': list(ats_results['parsed_sections'].keys()),

            # Experience & Education
            'experience_analysis': ats_results['experience_analysis'],
            'education_analysis': ats_results['education_analysis'],

            # Formatting
            'formatting_analysis': ats_results['formatting_analysis'],
            'density_analysis': ats_results['density_analysis'],

            # Suggestions
            'suggestions': suggestions,
            'ai_analysis': ai_analysis,

            # Content metrics
            'readability_score': self._calculate_readability(cv_text),
            'word_count': len(cv_text.split()),
            'enhancement_opportunities': self._find_enhancement_opportunities(cv_text, job_description),

            # CV text for downstream use
            'cv_text': cv_text,
            'job_description': job_description,
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

    def _get_ai_analysis(self, cv_text: str, job_description: str, ats_score: int = None) -> dict:
        """Get AI-powered analysis from Ollama"""
        try:
            if self.ollama_client.is_connected():
                return self.ollama_client.analyze_cv_content(cv_text, job_description, ats_score)
            else:
                return {
                    'score': ats_score if ats_score is not None else 70,
                    'analysis_text': 'AI analysis unavailable - Ollama not connected',
                    'sections': {}
                }
        except Exception as e:
            return {
                'score': ats_score if ats_score is not None else 70,
                'analysis_text': f'AI analysis error: {str(e)}',
                'sections': {}
            }

    def _generate_suggestions(self, cv_text: str, job_description: str, keyword_comparison: dict, structure_analysis: dict) -> list:
        """Generate specific improvement suggestions (fallback when ATS simulator recommendations are empty)"""

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
        except Exception:
            return 50.0  # Average score if calculation fails

    def _find_enhancement_opportunities(self, cv_text: str, job_description: str) -> list:
        """Find specific opportunities for CV enhancement"""
        opportunities = []

        # Look for weak language
        weak_words = ['responsible for', 'duties included', 'helped with', 'assisted with', 'worked on', 'involved in']
        for weak_word in weak_words:
            if weak_word in cv_text.lower():
                opportunities.append(f'Replace "{weak_word}" with stronger action verbs')

        # Look for missing quantification opportunities
        quantifiable_verbs = ['managed', 'led', 'increased', 'reduced', 'improved', 'developed', 'created']
        for verb in quantifiable_verbs:
            if verb in cv_text.lower() and not re.search(rf'{verb}.*\d+', cv_text, re.IGNORECASE):
                opportunities.append(f'Add numbers/metrics to "{verb}" statements')

        return opportunities
