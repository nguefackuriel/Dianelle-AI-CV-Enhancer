"""
Keyword Extractor Module
Extract and analyze keywords from job descriptions and CVs
"""

import re
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import string


class KeywordExtractor:
    """Extract and analyze keywords for CV optimization"""
    
    def __init__(self):
        self._setup_nltk()
        self.stop_words = set(stopwords.words('english'))
        
        # Common technical skills and keywords
        self.technical_skills = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift'],
            'web': ['html', 'css', 'react', 'vue', 'angular', 'node.js', 'express', 'django', 'flask'],
            'data': ['sql', 'mongodb', 'postgresql', 'mysql', 'pandas', 'numpy', 'scikit-learn', 'tensorflow'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins'],
            'tools': ['git', 'jira', 'confluence', 'slack', 'figma', 'photoshop', 'excel'],
        }
        
        # Action verbs commonly used in CVs
        self.action_verbs = [
            'achieved', 'managed', 'led', 'developed', 'implemented', 'created', 'designed',
            'improved', 'increased', 'reduced', 'optimized', 'collaborated', 'coordinated',
            'supervised', 'trained', 'analyzed', 'evaluated', 'researched', 'planned'
        ]
    
    def _setup_nltk(self):
        """Setup NLTK data"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)
    
    def extract_keywords_from_job_description(self, job_description: str, top_n: int = 20) -> dict:
        """
        Extract important keywords from job description
        
        Args:
            job_description: Job description text
            top_n: Number of top keywords to return
            
        Returns:
            dict: Dictionary with different types of keywords
        """
        # Clean and tokenize
        cleaned_text = self._clean_text(job_description)
        tokens = self._tokenize_and_filter(cleaned_text)
        
        # Extract different types of keywords
        results = {
            'all_keywords': self._get_top_keywords(tokens, top_n),
            'technical_skills': self._extract_technical_skills(job_description),
            'requirements': self._extract_requirements(job_description),
            'qualifications': self._extract_qualifications(job_description),
            'soft_skills': self._extract_soft_skills(job_description)
        }
        
        return results
    
    def extract_keywords_from_cv(self, cv_text: str, top_n: int = 20) -> dict:
        """
        Extract keywords from CV text
        
        Args:
            cv_text: CV text content
            top_n: Number of top keywords to return
            
        Returns:
            dict: Dictionary with CV keywords
        """
        cleaned_text = self._clean_text(cv_text)
        tokens = self._tokenize_and_filter(cleaned_text)
        
        results = {
            'all_keywords': self._get_top_keywords(tokens, top_n),
            'technical_skills': self._extract_technical_skills(cv_text),
            'action_verbs': self._extract_action_verbs(cv_text),
            'achievements': self._extract_achievements(cv_text)
        }
        
        return results
    
    def compare_keywords(self, cv_keywords: dict, job_keywords: dict) -> dict:
        """
        Compare CV keywords with job description keywords
        
        Args:
            cv_keywords: Keywords from CV
            job_keywords: Keywords from job description
            
        Returns:
            dict: Comparison results with matches and gaps
        """
        # Get all keyword lists
        cv_all = set([kw.lower() for kw in cv_keywords.get('all_keywords', [])])
        job_all = set([kw.lower() for kw in job_keywords.get('all_keywords', [])])
        
        cv_tech = set([skill.lower() for skill in cv_keywords.get('technical_skills', [])])
        job_tech = set([skill.lower() for skill in job_keywords.get('technical_skills', [])])
        
        # Calculate matches and gaps
        matched_keywords = list(cv_all.intersection(job_all))
        missing_keywords = list(job_all - cv_all)
        
        matched_technical = list(cv_tech.intersection(job_tech))
        missing_technical = list(job_tech - cv_tech)
        
        # Calculate match percentage
        total_important_keywords = len(job_all)
        matched_count = len(matched_keywords)
        match_percentage = (matched_count / total_important_keywords * 100) if total_important_keywords > 0 else 0
        
        return {
            'matched_keywords': matched_keywords,
            'missing_keywords': missing_keywords,
            'matched_technical': matched_technical,
            'missing_technical': missing_technical,
            'match_percentage': round(match_percentage, 2),
            'keyword_density': self._calculate_keyword_density(cv_keywords, job_keywords)
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean text for processing"""
        # Remove special characters and normalize
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _tokenize_and_filter(self, text: str) -> list:
        """Tokenize text and filter out stop words"""
        tokens = word_tokenize(text)
        
        # Filter tokens
        filtered_tokens = [
            token for token in tokens 
            if token not in self.stop_words 
            and len(token) > 2 
            and not token.isdigit()
        ]
        
        return filtered_tokens
    
    def _get_top_keywords(self, tokens: list, top_n: int) -> list:
        """Get top N keywords by frequency"""
        word_freq = Counter(tokens)
        return [word for word, count in word_freq.most_common(top_n)]
    
    def _extract_technical_skills(self, text: str) -> list:
        """Extract technical skills from text"""
        text_lower = text.lower()
        found_skills = []
        
        for category, skills in self.technical_skills.items():
            for skill in skills:
                if skill in text_lower:
                    found_skills.append(skill)
        
        return list(set(found_skills))
    
    def _extract_requirements(self, job_description: str) -> list:
        """Extract requirements from job description"""
        requirements_pattern = r'(?i)(?:requirements?|must have|essential|mandatory):?\s*(.+?)(?:\n\n|\n[A-Z]|$)'
        matches = re.findall(requirements_pattern, job_description, re.DOTALL)
        
        requirements = []
        for match in matches:
            # Split by bullet points or line breaks
            items = re.split(r'[•\-\*]|\n', match)
            for item in items:
                item = item.strip()
                if len(item) > 10:  # Filter out too short items
                    requirements.append(item)
        
        return requirements[:10]  # Return top 10
    
    def _extract_qualifications(self, job_description: str) -> list:
        """Extract qualifications from job description"""
        qual_pattern = r'(?i)(?:qualifications?|education|degree):?\s*(.+?)(?:\n\n|\n[A-Z]|$)'
        matches = re.findall(qual_pattern, job_description, re.DOTALL)
        
        qualifications = []
        for match in matches:
            items = re.split(r'[•\-\*]|\n', match)
            for item in items:
                item = item.strip()
                if len(item) > 5:
                    qualifications.append(item)
        
        return qualifications[:5]
    
    def _extract_soft_skills(self, text: str) -> list:
        """Extract soft skills from text"""
        soft_skills_keywords = [
            'communication', 'leadership', 'teamwork', 'problem solving', 'analytical',
            'creative', 'adaptable', 'organized', 'detail oriented', 'time management',
            'collaboration', 'critical thinking', 'interpersonal', 'presentation'
        ]
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in soft_skills_keywords:
            if skill in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def _extract_action_verbs(self, cv_text: str) -> list:
        """Extract action verbs used in CV"""
        text_lower = cv_text.lower()
        found_verbs = []
        
        for verb in self.action_verbs:
            if verb in text_lower:
                found_verbs.append(verb)
        
        return found_verbs
    
    def _extract_achievements(self, cv_text: str) -> list:
        """Extract quantified achievements from CV"""
        # Look for patterns with numbers and percentages
        achievement_patterns = [
            r'(\d+)%\s+\w+',  # X% improvement
            r'increased\s+\w+\s+by\s+(\d+)',  # increased something by X
            r'reduced\s+\w+\s+by\s+(\d+)',  # reduced something by X
            r'managed\s+(\d+)\s+\w+',  # managed X people/projects
            r'led\s+(\d+)\s+\w+',  # led X team members
        ]
        
        achievements = []
        for pattern in achievement_patterns:
            matches = re.findall(pattern, cv_text, re.IGNORECASE)
            achievements.extend(matches)
        
        return achievements[:10]  # Return top 10
    
    def _calculate_keyword_density(self, cv_keywords: dict, job_keywords: dict) -> dict:
        """Calculate keyword density metrics"""
        cv_total = len(cv_keywords.get('all_keywords', []))
        job_total = len(job_keywords.get('all_keywords', []))
        
        return {
            'cv_keyword_count': cv_total,
            'job_keyword_count': job_total,
            'density_ratio': round(cv_total / job_total, 2) if job_total > 0 else 0
        }
