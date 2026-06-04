"""
Job Matcher Module
Intelligent job-CV matching with gap analysis, fit scoring,
and transferable skills detection.
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from collections import Counter


class JobMatcher:
    """Advanced job-CV matching and gap analysis."""

    # Common transferable skill mappings
    TRANSFERABLE_SKILLS = {
        'project management': ['program management', 'product management', 'team leadership', 'coordination', 'planning'],
        'data analysis': ['data science', 'analytics', 'business intelligence', 'reporting', 'statistics'],
        'python': ['programming', 'scripting', 'automation', 'software development'],
        'leadership': ['management', 'mentoring', 'team building', 'supervision', 'coaching'],
        'communication': ['presentation', 'writing', 'stakeholder management', 'client relations'],
        'problem solving': ['troubleshooting', 'debugging', 'root cause analysis', 'critical thinking'],
        'agile': ['scrum', 'kanban', 'sprint planning', 'iterative development'],
        'sql': ['database', 'data querying', 'database management'],
        'machine learning': ['artificial intelligence', 'deep learning', 'predictive modeling', 'data science'],
        'cloud': ['aws', 'azure', 'gcp', 'cloud computing', 'infrastructure'],
        'javascript': ['frontend development', 'web development', 'react', 'node.js'],
        'customer service': ['client support', 'customer success', 'account management'],
        'sales': ['business development', 'revenue generation', 'client acquisition'],
        'marketing': ['digital marketing', 'content strategy', 'brand management', 'seo'],
        'finance': ['financial analysis', 'budgeting', 'forecasting', 'accounting'],
    }

    # Seniority level indicators
    SENIORITY_INDICATORS = {
        'intern': 0,
        'junior': 1, 'entry': 1, 'associate': 1, 'graduate': 1,
        'mid': 2, 'intermediate': 2,
        'senior': 3, 'sr': 3, 'lead': 3,
        'principal': 4, 'staff': 4, 'architect': 4,
        'manager': 4, 'head': 4,
        'director': 5, 'vp': 5, 'vice president': 5,
        'c-level': 6, 'cto': 6, 'ceo': 6, 'cfo': 6, 'coo': 6, 'chief': 6,
    }

    def __init__(self):
        pass

    def compute_fit_score(self, cv_text: str, job_description: str) -> Dict[str, Any]:
        """
        Compute a comprehensive fit score between CV and job description.

        Returns:
            Dict with overall_fit, category_scores, gaps, strengths, transferable_skills
        """
        # Parse job requirements
        job_reqs = self._parse_job_requirements(job_description)

        # Analyze CV against requirements
        required_match = self._match_requirements(cv_text, job_reqs['required'])
        preferred_match = self._match_requirements(cv_text, job_reqs['preferred'])

        # Experience match
        exp_match = self._match_experience(cv_text, job_description)

        # Education match
        edu_match = self._match_education(cv_text, job_description)

        # Seniority match
        seniority_match = self._match_seniority(cv_text, job_description)

        # Transferable skills
        transferable = self._find_transferable_skills(cv_text, job_reqs)

        # Calculate overall fit
        scores = {
            'required_skills': required_match['score'],
            'preferred_skills': preferred_match['score'],
            'experience': exp_match['score'],
            'education': edu_match['score'],
            'seniority': seniority_match['score'],
        }

        weights = {
            'required_skills': 0.35,
            'preferred_skills': 0.15,
            'experience': 0.25,
            'education': 0.15,
            'seniority': 0.10,
        }

        overall = sum(scores[k] * weights[k] for k in scores)

        # Generate gap analysis
        gaps = self._generate_gap_analysis(
            required_match, preferred_match, exp_match, edu_match, job_reqs
        )

        return {
            'overall_fit': round(overall, 1),
            'category_scores': scores,
            'gaps': gaps,
            'strengths': self._identify_strengths(required_match, preferred_match, cv_text),
            'transferable_skills': transferable,
            'job_requirements': job_reqs,
            'required_match': required_match,
            'preferred_match': preferred_match,
            'experience_match': exp_match,
            'education_match': edu_match,
            'seniority_match': seniority_match,
            'fit_level': self._get_fit_level(overall),
        }

    # ------------------------------------------------------------------
    # Requirement Parsing
    # ------------------------------------------------------------------

    def _parse_job_requirements(self, job_description: str) -> Dict[str, Any]:
        """Parse job description into required vs preferred requirements."""
        jd_lower = job_description.lower()

        required = []
        preferred = []

        # Split into sections
        lines = job_description.split('\n')
        current_category = 'required'

        # Detect requirement categories
        required_markers = [
            'required', 'must have', 'essential', 'mandatory',
            'minimum requirements', 'requirements', 'qualifications',
        ]
        preferred_markers = [
            'preferred', 'nice to have', 'desired', 'bonus',
            'additional', 'plus', 'advantageous', 'ideally',
        ]

        for line in lines:
            line_lower = line.strip().lower()

            # Check for category change
            if any(marker in line_lower for marker in required_markers):
                current_category = 'required'
                continue
            if any(marker in line_lower for marker in preferred_markers):
                current_category = 'preferred'
                continue

            # Extract requirement items
            stripped = line.strip()
            if stripped and len(stripped) > 10:
                # Clean bullet markers
                clean = re.sub(r'^[-•*▪▸►◆●○→»\d.)]+\s*', '', stripped).strip()
                if clean and len(clean) > 10:
                    if current_category == 'required':
                        required.append(clean)
                    else:
                        preferred.append(clean)

        # If nothing was parsed, treat all content as requirements
        if not required and not preferred:
            for line in lines:
                clean = re.sub(r'^[-•*▪▸►◆●○→»\d.)]+\s*', '', line.strip()).strip()
                if clean and len(clean) > 10:
                    required.append(clean)

        # Extract experience requirement
        exp_years = None
        for pattern in [r'(\d+)\+?\s*(?:years?|yrs?)', r'(\d+)\s*-\s*\d+\s*(?:years?|yrs?)']:
            match = re.search(pattern, jd_lower)
            if match:
                exp_years = int(match.group(1))
                break

        # Extract education requirement
        edu_level = self._detect_education_level(job_description)

        # Detect industry
        industry = self._detect_industry(job_description)

        # Detect role level
        role_level = self._detect_role_level(job_description)

        return {
            'required': required,
            'preferred': preferred,
            'experience_years': exp_years,
            'education_level': edu_level,
            'industry': industry,
            'role_level': role_level,
        }

    # ------------------------------------------------------------------
    # Matching
    # ------------------------------------------------------------------

    def _match_requirements(self, cv_text: str, requirements: List[str]) -> Dict[str, Any]:
        """Match CV against a list of requirements."""
        cv_lower = cv_text.lower()
        matched = []
        unmatched = []

        for req in requirements:
            req_lower = req.lower()
            # Extract key terms from the requirement
            key_terms = self._extract_key_terms(req)

            # Check if key terms are present in CV
            terms_found = sum(1 for term in key_terms if term in cv_lower)
            match_ratio = terms_found / len(key_terms) if key_terms else 0

            if match_ratio >= 0.5:
                matched.append({
                    'requirement': req,
                    'match_ratio': match_ratio,
                    'terms_found': terms_found,
                    'total_terms': len(key_terms),
                })
            else:
                unmatched.append({
                    'requirement': req,
                    'match_ratio': match_ratio,
                    'missing_terms': [t for t in key_terms if t not in cv_lower],
                })

        total = len(requirements)
        score = (len(matched) / total * 100) if total > 0 else 75

        return {
            'matched': matched,
            'unmatched': unmatched,
            'score': round(min(score, 100), 1),
            'total': total,
        }

    def _match_experience(self, cv_text: str, job_description: str) -> Dict[str, Any]:
        """Match experience requirements."""
        # Extract required years
        req_years = None
        for pattern in [r'(\d+)\+?\s*(?:years?|yrs?)', r'(\d+)\s*-\s*\d+\s*(?:years?|yrs?)']:
            match = re.search(pattern, job_description.lower())
            if match:
                req_years = int(match.group(1))
                break

        # Extract CV years
        cv_years = None
        for pattern in [r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)', r'over\s+(\d+)\s*(?:years?|yrs?)']:
            match = re.search(pattern, cv_text.lower())
            if match:
                cv_years = int(match.group(1))
                break

        if req_years is None:
            score = 80
            status = 'no_requirement'
        elif cv_years and cv_years >= req_years:
            score = 100
            status = 'exceeds'
        elif cv_years and cv_years >= req_years * 0.7:
            score = 70
            status = 'close'
        elif cv_years:
            score = 40
            status = 'under'
        else:
            score = 60
            status = 'unknown'

        return {
            'required_years': req_years,
            'cv_years': cv_years,
            'score': score,
            'status': status,
        }

    def _match_education(self, cv_text: str, job_description: str) -> Dict[str, Any]:
        """Match education requirements."""
        req_level = self._detect_education_level(job_description)
        cv_level = self._detect_education_level(cv_text)

        degree_ranks = {
            'phd': 6, 'doctorate': 6, 'master': 5, 'mba': 5,
            'bachelor': 4, 'associate': 3, 'diploma': 2, 'certificate': 1,
        }

        req_rank = degree_ranks.get(req_level, 0) if req_level else 0
        cv_rank = degree_ranks.get(cv_level, 0) if cv_level else 0

        if req_rank == 0:
            score = 80
        elif cv_rank >= req_rank:
            score = 100
        elif cv_rank >= req_rank - 1:
            score = 70
        else:
            score = 40

        return {
            'required': req_level,
            'cv_level': cv_level,
            'score': score,
        }

    def _match_seniority(self, cv_text: str, job_description: str) -> Dict[str, Any]:
        """Match seniority level."""
        jd_level = self._detect_role_level(job_description)
        cv_level = self._detect_role_level(cv_text)

        jd_rank = self.SENIORITY_INDICATORS.get(jd_level, 2) if jd_level else 2
        cv_rank = self.SENIORITY_INDICATORS.get(cv_level, 2) if cv_level else 2

        diff = abs(jd_rank - cv_rank)

        if diff == 0:
            score = 100
        elif diff == 1:
            score = 80
        elif diff == 2:
            score = 55
        else:
            score = 35

        return {
            'job_level': jd_level,
            'cv_level': cv_level,
            'score': score,
        }

    # ------------------------------------------------------------------
    # Transferable Skills
    # ------------------------------------------------------------------

    def _find_transferable_skills(self, cv_text: str, job_reqs: Dict) -> List[Dict[str, str]]:
        """Find transferable skills from CV that relate to job requirements."""
        cv_lower = cv_text.lower()
        transferable = []

        all_reqs = ' '.join(job_reqs.get('required', []) + job_reqs.get('preferred', [])).lower()

        for cv_skill, related_skills in self.TRANSFERABLE_SKILLS.items():
            if cv_skill in cv_lower:
                for related in related_skills:
                    if related in all_reqs and related not in cv_lower:
                        transferable.append({
                            'your_skill': cv_skill,
                            'job_needs': related,
                            'connection': f'Your {cv_skill} experience is transferable to {related}',
                        })

        return transferable

    # ------------------------------------------------------------------
    # Gap Analysis
    # ------------------------------------------------------------------

    def _generate_gap_analysis(
        self,
        required_match: Dict,
        preferred_match: Dict,
        exp_match: Dict,
        edu_match: Dict,
        job_reqs: Dict,
    ) -> List[Dict[str, Any]]:
        """Generate detailed gap analysis report."""
        gaps = []

        # Required skills gaps
        for item in required_match['unmatched']:
            gaps.append({
                'category': 'Required Skill',
                'gap': item['requirement'],
                'severity': 'high',
                'missing_terms': item.get('missing_terms', []),
                'action': f'Add relevant experience or training for: {item["requirement"][:100]}',
            })

        # Preferred skills gaps
        for item in preferred_match['unmatched'][:5]:
            gaps.append({
                'category': 'Preferred Skill',
                'gap': item['requirement'],
                'severity': 'medium',
                'missing_terms': item.get('missing_terms', []),
                'action': f'Consider adding if applicable: {item["requirement"][:100]}',
            })

        # Experience gap
        if exp_match['status'] == 'under':
            years_diff = (exp_match.get('required_years', 0) or 0) - (exp_match.get('cv_years', 0) or 0)
            gaps.append({
                'category': 'Experience',
                'gap': f'{years_diff} years below requirement',
                'severity': 'high',
                'action': 'Emphasize transferable experience and freelance/project work',
            })

        # Education gap
        if edu_match['score'] < 60:
            gaps.append({
                'category': 'Education',
                'gap': f'Required: {edu_match.get("required", "N/A")}, Your level: {edu_match.get("cv_level", "N/A")}',
                'severity': 'medium',
                'action': 'Highlight relevant certifications, courses, or equivalent experience',
            })

        # Sort by severity
        severity_order = {'high': 0, 'medium': 1, 'low': 2}
        gaps.sort(key=lambda g: severity_order.get(g['severity'], 3))

        return gaps

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _extract_key_terms(self, text: str) -> List[str]:
        """Extract key terms from a requirement line."""
        # Remove common filler words
        stop_words = {
            'a', 'an', 'the', 'and', 'or', 'with', 'in', 'of', 'to', 'for',
            'is', 'are', 'be', 'has', 'have', 'had', 'will', 'would', 'should',
            'can', 'could', 'may', 'must', 'shall', 'do', 'does', 'did',
            'at', 'by', 'on', 'from', 'as', 'into', 'through', 'between',
            'our', 'their', 'this', 'that', 'these', 'those', 'some', 'any',
            'experience', 'ability', 'skills', 'knowledge', 'understanding',
            'strong', 'excellent', 'good', 'proven', 'demonstrated',
        }

        words = re.findall(r'\b[a-z]+(?:[-./][a-z]+)*\b', text.lower())
        return [w for w in words if w not in stop_words and len(w) > 2]

    def _detect_education_level(self, text: str) -> Optional[str]:
        """Detect education level mentioned in text."""
        text_lower = text.lower()
        levels = [
            ('phd', r'\bph\.?d\.?\b|doctorate|doctoral'),
            ('master', r"\bmaster'?s?\b|\bm\.?s\.?\b|\bm\.?a\.?\b|\bmba\b|\bm\.eng\b"),
            ('bachelor', r"\bbachelor'?s?\b|\bb\.?s\.?\b|\bb\.?a\.?\b|\bb\.eng\b"),
            ('associate', r"\bassociate'?s?\b|\ba\.?s\.?\b|\ba\.?a\.?\b"),
            ('diploma', r'\bdiploma\b'),
            ('certificate', r'\bcertificat(?:e|ion)\b'),
        ]

        for level, pattern in levels:
            if re.search(pattern, text_lower):
                return level
        return None

    def _detect_industry(self, text: str) -> Optional[str]:
        """Auto-detect industry from text."""
        text_lower = text.lower()
        industries = {
            'technology': ['software', 'developer', 'engineer', 'tech', 'programming', 'cloud', 'saas'],
            'finance': ['banking', 'financial', 'investment', 'trading', 'fintech', 'accounting'],
            'healthcare': ['medical', 'health', 'clinical', 'pharmaceutical', 'biotech', 'patient'],
            'marketing': ['marketing', 'advertising', 'brand', 'campaign', 'digital marketing', 'seo'],
            'education': ['teaching', 'academic', 'education', 'curriculum', 'training'],
            'consulting': ['consulting', 'advisory', 'strategy', 'management consulting'],
            'manufacturing': ['manufacturing', 'production', 'supply chain', 'logistics', 'operations'],
            'retail': ['retail', 'ecommerce', 'merchandising', 'store', 'sales'],
        }

        scores = {}
        for industry, keywords in industries.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                scores[industry] = score

        if scores:
            return max(scores, key=scores.get)
        return None

    def _detect_role_level(self, text: str) -> Optional[str]:
        """Detect seniority level from text."""
        text_lower = text.lower()

        for level in ['chief', 'c-level', 'director', 'vp', 'vice president',
                       'principal', 'staff', 'senior', 'sr', 'lead',
                       'mid', 'junior', 'entry', 'intern', 'associate', 'graduate']:
            pattern = r'\b' + re.escape(level) + r'\b'
            if re.search(pattern, text_lower):
                return level
        return None

    def _identify_strengths(self, required_match: Dict, preferred_match: Dict, cv_text: str) -> List[str]:
        """Identify candidate strengths."""
        strengths = []

        if required_match['score'] >= 80:
            strengths.append("Strong alignment with required skills")
        if preferred_match['score'] >= 70:
            strengths.append("Good coverage of preferred qualifications")

        # Check for quantified achievements
        metrics_count = len(re.findall(r'\d+%|\$[\d,]+|\d+\s*(?:million|k\b)', cv_text, re.IGNORECASE))
        if metrics_count >= 5:
            strengths.append(f"Well-quantified achievements ({metrics_count} metrics found)")

        # Check for certifications
        if re.search(r'certif(?:ied|ication)', cv_text, re.IGNORECASE):
            strengths.append("Relevant certifications noted")

        return strengths

    def _get_fit_level(self, score: float) -> str:
        """Get fit level description."""
        if score >= 85:
            return 'Excellent Fit'
        elif score >= 70:
            return 'Strong Fit'
        elif score >= 55:
            return 'Moderate Fit'
        elif score >= 40:
            return 'Partial Fit'
        else:
            return 'Low Fit'
