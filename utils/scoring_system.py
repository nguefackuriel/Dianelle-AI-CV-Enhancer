"""
Scoring System Module
Calculate and manage various CV scoring metrics
"""

import math
from typing import Dict, List, Any


class ScoringSystem:
    """Handle CV scoring calculations and metrics"""
    
    def __init__(self):
        self.weights = {
            'keyword_match': 0.35,      # 35% - Most important for ATS
            'structure': 0.25,          # 25% - CV organization
            'content_quality': 0.20,    # 20% - Writing quality and achievements  
            'technical_skills': 0.15,   # 15% - Technical skill matching
            'formatting': 0.05          # 5% - ATS-friendly formatting
        }
    
    def calculate_overall_score(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate overall CV score based on multiple factors
        
        Args:
            analysis_results: Complete analysis results from CV analyzer
            
        Returns:
            dict: Detailed scoring breakdown
        """
        scores = {}
        
        # Calculate individual component scores
        scores['keyword_match'] = self._calculate_keyword_score(analysis_results)
        scores['structure'] = self._calculate_structure_score(analysis_results)
        scores['content_quality'] = self._calculate_content_score(analysis_results)
        scores['technical_skills'] = self._calculate_technical_score(analysis_results)
        scores['formatting'] = self._calculate_formatting_score(analysis_results)
        
        # Calculate weighted overall score
        overall_score = sum(
            scores[component] * self.weights[component] 
            for component in scores.keys()
        )
        
        # Create detailed breakdown
        breakdown = {
            'overall_score': round(overall_score, 1),
            'component_scores': scores,
            'grade': self._get_grade(overall_score),
            'percentile': self._calculate_percentile(overall_score),
            'improvement_potential': 100 - overall_score,
            'strengths': self._identify_strengths(scores),
            'weaknesses': self._identify_weaknesses(scores),
            'next_steps': self._generate_next_steps(scores)
        }
        
        return breakdown
    
    def _calculate_keyword_score(self, analysis: Dict[str, Any]) -> float:
        """Calculate keyword matching score (0-100)"""
        match_percentage = analysis.get('keyword_match_percentage', 0)
        
        # Bonus for high match rates
        if match_percentage >= 80:
            return 95
        elif match_percentage >= 60:
            return 85
        elif match_percentage >= 40:
            return 70
        elif match_percentage >= 20:
            return 50
        else:
            return 30
    
    def _calculate_structure_score(self, analysis: Dict[str, Any]) -> float:
        """Calculate CV structure score (0-100)"""
        structure = analysis.get('structure_analysis', {})
        
        score = 0
        max_score = 100
        
        # Essential sections (40 points)
        if structure.get('has_contact_info', False):
            score += 10
        if structure.get('has_summary', False):
            score += 10
        if structure.get('has_experience', False):
            score += 15
        if structure.get('has_education', False):
            score += 5
        
        # Good practices (30 points)
        if structure.get('has_skills', False):
            score += 10
        if structure.get('uses_bullet_points', False):
            score += 10
        if structure.get('has_quantified_achievements', False):
            score += 10
        
        # Quality indicators (30 points)
        if structure.get('appropriate_length', False):
            score += 15
        
        section_count = structure.get('section_count', 0)
        if section_count >= 5:
            score += 15
        elif section_count >= 3:
            score += 10
        elif section_count >= 2:
            score += 5
        
        return min(score, max_score)
    
    def _calculate_content_score(self, analysis: Dict[str, Any]) -> float:
        """Calculate content quality score (0-100)"""
        score = 50  # Base score
        
        # Readability bonus
        readability = analysis.get('readability_score', 50)
        if readability >= 60:
            score += 20
        elif readability >= 40:
            score += 10
        
        # Word count appropriateness
        word_count = analysis.get('word_count', 0)
        if 300 <= word_count <= 800:
            score += 15
        elif 200 <= word_count <= 1000:
            score += 10
        else:
            score += 5
        
        # Enhancement opportunities penalty
        opportunities = analysis.get('enhancement_opportunities', [])
        penalty = min(len(opportunities) * 3, 15)
        score -= penalty
        
        return max(min(score, 100), 0)
    
    def _calculate_technical_score(self, analysis: Dict[str, Any]) -> float:
        """Calculate technical skills matching score (0-100)"""
        matched_tech = len(analysis.get('technical_skills_match', []))
        missing_tech = len(analysis.get('missing_technical_skills', []))
        
        if matched_tech + missing_tech == 0:
            return 70  # Default if no technical skills in job description
        
        match_ratio = matched_tech / (matched_tech + missing_tech)
        
        # Convert ratio to score with bonuses for high matches
        if match_ratio >= 0.8:
            return 95
        elif match_ratio >= 0.6:
            return 85
        elif match_ratio >= 0.4:
            return 70
        elif match_ratio >= 0.2:
            return 55
        else:
            return 35
    
    def _calculate_formatting_score(self, analysis: Dict[str, Any]) -> float:
        """Calculate ATS-friendly formatting score (0-100)"""
        structure = analysis.get('structure_analysis', {})
        formatting_issues = structure.get('formatting_issues', [])
        
        score = 100
        
        # Deduct for formatting issues
        score -= len(formatting_issues) * 15
        
        # Bonus for good practices
        if structure.get('uses_bullet_points', False):
            score += 0  # Already counted in structure
        
        return max(min(score, 100), 0)
    
    def _get_grade(self, score: float) -> str:
        """Convert numerical score to letter grade"""
        if score >= 90:
            return 'A+'
        elif score >= 85:
            return 'A'
        elif score >= 80:
            return 'A-'
        elif score >= 75:
            return 'B+'
        elif score >= 70:
            return 'B'
        elif score >= 65:
            return 'B-'
        elif score >= 60:
            return 'C+'
        elif score >= 55:
            return 'C'
        elif score >= 50:
            return 'C-'
        else:
            return 'D'
    
    def _calculate_percentile(self, score: float) -> int:
        """Calculate approximate percentile ranking"""
        # Rough approximation based on typical CV quality distribution
        if score >= 85:
            return 95
        elif score >= 75:
            return 80
        elif score >= 65:
            return 60
        elif score >= 55:
            return 40
        else:
            return 20
    
    def _identify_strengths(self, scores: Dict[str, float]) -> List[str]:
        """Identify CV strengths based on component scores"""
        strengths = []
        
        for component, score in scores.items():
            if score >= 80:
                strength_messages = {
                    'keyword_match': 'Excellent keyword optimization for ATS systems',
                    'structure': 'Well-organized CV with all essential sections',
                    'content_quality': 'High-quality, readable content with good flow',
                    'technical_skills': 'Strong technical skills alignment with job requirements',
                    'formatting': 'ATS-friendly formatting and structure'
                }
                strengths.append(strength_messages.get(component, f'Strong {component}'))
        
        if not strengths:
            # Find the best component even if not excellent
            best_component = max(scores.keys(), key=lambda k: scores[k])
            strengths.append(f'Relatively strong {best_component.replace("_", " ")}')
        
        return strengths
    
    def _identify_weaknesses(self, scores: Dict[str, float]) -> List[str]:
        """Identify areas needing improvement"""
        weaknesses = []
        
        for component, score in scores.items():
            if score < 60:
                weakness_messages = {
                    'keyword_match': 'Low keyword matching - missing important job-related terms',
                    'structure': 'CV structure needs improvement - missing key sections',
                    'content_quality': 'Content quality could be enhanced with better writing',
                    'technical_skills': 'Technical skills section needs strengthening',
                    'formatting': 'Formatting issues may cause ATS parsing problems'
                }
                weaknesses.append(weakness_messages.get(component, f'Weak {component}'))
        
        return weaknesses
    
    def _generate_next_steps(self, scores: Dict[str, float]) -> List[str]:
        """Generate prioritized next steps for improvement"""
        next_steps = []
        
        # Sort components by score (lowest first) to prioritize improvements
        sorted_components = sorted(scores.items(), key=lambda x: x[1])
        
        step_recommendations = {
            'keyword_match': [
                'Review job description and identify missing keywords',
                'Naturally incorporate relevant keywords throughout your CV',
                'Focus on industry-specific terminology and skills'
            ],
            'structure': [
                'Add missing essential sections (contact, summary, experience, education)',
                'Reorganize content with clear section headers',
                'Use consistent formatting throughout'
            ],
            'content_quality': [
                'Quantify achievements with specific numbers and metrics',
                'Use strong action verbs to start bullet points',
                'Improve clarity and conciseness of descriptions'
            ],
            'technical_skills': [
                'Add relevant technical skills mentioned in job posting',
                'Create dedicated skills section if missing',
                'Provide context for how you used technical skills'
            ],
            'formatting': [
                'Use simple, ATS-friendly formatting',
                'Avoid tables, graphics, and unusual fonts',
                'Ensure consistent spacing and alignment'
            ]
        }
        
        # Add top 3 improvement areas
        for component, score in sorted_components[:3]:
            if score < 80:  # Only suggest improvements for scores below 80
                recommendations = step_recommendations.get(component, [])
                if recommendations:
                    next_steps.extend(recommendations[:2])  # Take top 2 recommendations
        
        return next_steps[:5]  # Limit to 5 total steps
    
    def generate_score_report(self, analysis_results: Dict[str, Any]) -> str:
        """Generate a formatted score report"""
        scoring = self.calculate_overall_score(analysis_results)
        
        report = f"""
CV ASSESSMENT REPORT
====================

Overall Score: {scoring['overall_score']}/100 (Grade: {scoring['grade']})
Percentile Ranking: {scoring['percentile']}th percentile

COMPONENT BREAKDOWN:
• Keyword Match: {scoring['component_scores']['keyword_match']:.1f}/100
• CV Structure: {scoring['component_scores']['structure']:.1f}/100  
• Content Quality: {scoring['component_scores']['content_quality']:.1f}/100
• Technical Skills: {scoring['component_scores']['technical_skills']:.1f}/100
• ATS Formatting: {scoring['component_scores']['formatting']:.1f}/100

STRENGTHS:
"""
        
        for strength in scoring['strengths']:
            report += f"✓ {strength}\n"
        
        report += "\nAREAS FOR IMPROVEMENT:\n"
        for weakness in scoring['weaknesses']:
            report += f"• {weakness}\n"
        
        report += "\nNEXT STEPS:\n"
        for i, step in enumerate(scoring['next_steps'], 1):
            report += f"{i}. {step}\n"
        
        report += f"\nImprovement Potential: {scoring['improvement_potential']:.1f} points"
        
        return report
