"""
ATS Simulator Module
Simulates real Applicant Tracking System behavior for accurate CV scoring.

Real ATS systems parse CVs into structured data and match against job requirements
using section detection, semantic similarity, keyword density, and format validation.
This module replicates that pipeline.
"""

import re
import math
from collections import Counter, OrderedDict
from typing import Dict, List, Any, Optional, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

CUSTOM_STOP_WORDS = set(ENGLISH_STOP_WORDS).union({
    'remote', 'job', 'resume', 'compensation', 'qualifications', 'assessment', 'overview',
    'options', 'help', 'project', 'candidate', 'candidates', 'employer', 'employers',
    'experience', 'work', 'working', 'team', 'teams', 'role', 'roles', 'company', 'companies',
    'position', 'positions', 'responsibilities', 'duties', 'requirements', 'skills',
    'application', 'apply', 'employment', 'status', 'opportunity', 'opportunities',
    'equal', 'benefits', 'salary', 'pay', 'bonus', 'insurance', 'vacation', 'leave',
    'paid', 'time', 'off', 'flexible', 'schedule', 'hours', 'full-time', 'part-time',
    'contract', 'temporary', 'internship', 'location', 'locations', 'office', 'offices',
    'travel', 'required', 'preferred', 'desired', 'minimum', 'maximum', 'years', 'months',
    'degree', 'diploma', 'education', 'university', 'college', 'school', 'schools',
    'user', 'users', 'client', 'clients', 'customer', 'customers', 'service', 'services',
    'product', 'products', 'support', 'technical', 'technology', 'technologies', 'system',
    'systems', 'software', 'application', 'applications', 'program', 'programs', 'tool',
    'tools', 'platform', 'platforms', 'framework', 'frameworks', 'library', 'libraries',
    'environment', 'environments', 'development', 'developer', 'developers', 'engineer',
    'engineers', 'engineering', 'manager', 'managers', 'management', 'lead', 'leader',
    'leaders', 'leadership', 'teamwork', 'ability', 'abilities', 'capable', 'competent',
    'expert', 'professional', 'professionals', 'industry', 'industries', 'field', 'fields',
    'area', 'areas', 'day', 'days', 'week', 'weeks', 'month', 'months', 'year', 'years',
    'description', 'summary', 'detail', 'details', 'must', 'should', 'would', 'could',
    'want', 'need', 'needs', 'require', 'requires', 'preferred', 'plus', 'nice'
})


class ATSSimulator:
    """Simulates Applicant Tracking System parsing and scoring."""

    # Preferred section order for most ATS systems
    PREFERRED_SECTION_ORDER = [
        'contact', 'summary', 'experience', 'education',
        'skills', 'certifications', 'projects', 'awards',
        'publications', 'volunteer', 'languages', 'interests'
    ]

    # Section header patterns (case-insensitive)
    SECTION_PATTERNS = {
        'contact': [
            r'^(?:contact\s+(?:info(?:rmation)?|details))',
            r'^(?:personal\s+(?:info(?:rmation)?|details))',
        ],
        'summary': [
            r'^(?:(?:professional|executive|career)\s+)?summary',
            r'^(?:(?:professional|career)\s+)?profile',
            r'^(?:(?:career\s+)?objective)',
            r'^about\s*me',
            r'^overview',
        ],
        'experience': [
            r'^(?:(?:work|professional|employment|career)\s+)?experience',
            r'^(?:work|employment)\s+history',
            r'^(?:professional\s+)?background',
            r'^relevant\s+experience',
        ],
        'education': [
            r'^education(?:al)?\s*(?:background|history|qualifications)?',
            r'^academic\s+(?:background|qualifications|history)',
            r'^(?:degrees?\s+&\s+)?qualifications',
        ],
        'skills': [
            r'^(?:(?:technical|professional|core|key)\s+)?skills',
            r'^(?:areas?\s+of\s+)?(?:expertise|competenc(?:ies|e))',
            r'^(?:technical\s+)?proficienc(?:ies|y)',
            r'^tools?\s+(?:&|and)\s+technolog(?:ies|y)',
        ],
        'certifications': [
            r'^certifications?\s*(?:&\s*licens(?:es|ing))?',
            r'^licens(?:es|ing)\s*(?:&\s*certifications?)?',
            r'^professional\s+(?:certifications?|development)',
            r'^accreditations?',
        ],
        'projects': [
            r'^(?:(?:key|notable|selected|relevant)\s+)?projects?',
            r'^(?:personal|side)\s+projects?',
            r'^portfolio',
        ],
        'awards': [
            r'^(?:awards?\s*(?:&|and)?\s*)?(?:honors?|recognition|achievements?)',
            r'^accolades',
        ],
        'publications': [
            r'^publications?',
            r'^(?:research\s+)?papers?',
            r'^presentations?',
        ],
        'volunteer': [
            r'^volunteer(?:ing)?\s*(?:experience|work)?',
            r'^community\s+(?:service|involvement)',
            r'^extracurricular',
        ],
        'languages': [
            r'^languages?',
        ],
        'interests': [
            r'^(?:hobbies?\s*(?:&|and)?\s*)?interests?',
            r'^(?:personal\s+)?interests?(?:\s*&\s*hobbies?)?',
        ],
    }

    # Degree levels ranked by seniority
    DEGREE_LEVELS = OrderedDict([
        ('phd', 6), ('doctorate', 6), ('doctoral', 6), ('d.phil', 6),
        ('master', 5), ("master's", 5), ('mba', 5), ('msc', 5), ('ma', 5), ('ms', 5), ('m.s.', 5), ('m.eng', 5),
        ('bachelor', 4), ("bachelor's", 4), ('bsc', 4), ('ba', 4), ('b.s.', 4), ('b.a.', 4), ('b.eng', 4),
        ('associate', 3), ("associate's", 3), ('a.s.', 3), ('a.a.', 3),
        ('diploma', 2), ('certificate', 1), ('certification', 1),
    ])

    def __init__(self):
        self.tfidf = TfidfVectorizer(
            stop_words=list(CUSTOM_STOP_WORDS),
            ngram_range=(1, 3),
            max_features=500,
            sublinear_tf=True,
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def simulate_ats_parse(self, cv_text: str, job_description: str) -> Dict[str, Any]:
        """
        Run a full ATS simulation pipeline.

        Returns a dict with:
            - ats_score (0-100)
            - section_scores: per-section breakdown
            - parsed_sections: detected CV sections
            - semantic_similarity: cosine similarity score
            - keyword_analysis: detailed keyword matching
            - experience_analysis: years, timeline
            - education_analysis: degree match
            - formatting_analysis: ATS format issues
            - recommendations: prioritized improvement list
        """
        parsed_sections = self._parse_sections(cv_text)
        keyword_analysis = self._analyze_keywords_semantic(cv_text, job_description)
        experience_analysis = self._analyze_experience(cv_text, job_description)
        education_analysis = self._analyze_education(cv_text, job_description)
        formatting_analysis = self._analyze_formatting(cv_text)
        section_order_score = self._score_section_order(parsed_sections)
        semantic_sim = self._compute_semantic_similarity(cv_text, job_description)
        density_analysis = self._analyze_keyword_density(cv_text, keyword_analysis)

        # ----- composite score -----
        scores = {
            'semantic_relevance':       min(semantic_sim * 100, 100),        # 0-100
            'keyword_match':            keyword_analysis['match_score'],     # 0-100
            'keyword_density':          density_analysis['score'],           # 0-100
            'section_completeness':     self._score_section_completeness(parsed_sections),
            'section_order':            section_order_score,
            'experience_match':         experience_analysis['score'],
            'education_match':          education_analysis['score'],
            'formatting':               formatting_analysis['score'],
            'quantified_achievements':  self._score_achievements(cv_text),
            'action_verbs':             self._score_action_verbs(cv_text),
        }

        weights = {
            'semantic_relevance':       0.20,
            'keyword_match':            0.20,
            'keyword_density':          0.05,
            'section_completeness':     0.10,
            'section_order':            0.05,
            'experience_match':         0.12,
            'education_match':          0.08,
            'formatting':               0.05,
            'quantified_achievements':  0.08,
            'action_verbs':             0.07,
        }

        ats_score = sum(scores[k] * weights[k] for k in scores)
        ats_score = max(0, min(round(ats_score), 100))

        recommendations = self._generate_recommendations(scores, keyword_analysis, formatting_analysis, parsed_sections)

        return {
            'ats_score': ats_score,
            'component_scores': scores,
            'component_weights': weights,
            'parsed_sections': parsed_sections,
            'semantic_similarity': round(semantic_sim, 4),
            'keyword_analysis': keyword_analysis,
            'experience_analysis': experience_analysis,
            'education_analysis': education_analysis,
            'formatting_analysis': formatting_analysis,
            'density_analysis': density_analysis,
            'section_order_score': section_order_score,
            'recommendations': recommendations,
        }

    # ------------------------------------------------------------------
    # Section Parsing
    # ------------------------------------------------------------------

    def _parse_sections(self, cv_text: str) -> Dict[str, str]:
        """Parse CV text into named sections."""
        lines = cv_text.split('\n')
        sections: Dict[str, str] = {}
        current_section = 'header'
        current_lines: List[str] = []

        for line in lines:
            stripped = line.strip()
            if not stripped:
                current_lines.append('')
                continue

            detected = self._detect_section_header(stripped)
            if detected:
                # Save previous section
                if current_lines:
                    content = '\n'.join(current_lines).strip()
                    if content:
                        sections[current_section] = content
                current_section = detected
                current_lines = []
            else:
                current_lines.append(line)

        # Save last section
        if current_lines:
            content = '\n'.join(current_lines).strip()
            if content:
                sections[current_section] = content

        return sections

    def _detect_section_header(self, line: str) -> Optional[str]:
        """Detect if a line is a section header, return section name or None."""
        clean = re.sub(r'[^a-zA-Z\s&]', '', line).strip()
        if not clean or len(clean) > 60:
            return None

        # Check if line looks like a header (short, possibly uppercase or title case)
        words = clean.split()
        if len(words) > 6:
            return None

        for section_name, patterns in self.SECTION_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, clean, re.IGNORECASE):
                    return section_name

        return None

    # ------------------------------------------------------------------
    # Semantic Keyword Analysis
    # ------------------------------------------------------------------

    def _analyze_keywords_semantic(self, cv_text: str, job_description: str) -> Dict[str, Any]:
        """
        Semantic keyword analysis using TF-IDF.
        Extracts important terms from the JD and checks CV coverage.
        """
        # Extract key phrases from job description
        jd_phrases = self._extract_key_phrases(job_description)
        cv_lower = cv_text.lower()

        matched = []
        missing = []
        partial = []

        for phrase, importance in jd_phrases:
            phrase_lower = phrase.lower()
            if phrase_lower in cv_lower:
                matched.append({'phrase': phrase, 'importance': importance, 'match_type': 'exact'})
            else:
                # Check for partial matches (individual words)
                words = phrase_lower.split()
                if len(words) > 1:
                    word_matches = sum(1 for w in words if w in cv_lower)
                    if word_matches > 0:
                        partial.append({
                            'phrase': phrase,
                            'importance': importance,
                            'words_matched': word_matches,
                            'total_words': len(words),
                        })
                    else:
                        missing.append({'phrase': phrase, 'importance': importance})
                else:
                    missing.append({'phrase': phrase, 'importance': importance})

        total = len(jd_phrases)
        matched_count = len(matched) + len(partial) * 0.5
        match_score = (matched_count / total * 100) if total > 0 else 0
        match_score = min(match_score, 100)

        return {
            'matched': matched,
            'missing': missing,
            'partial': partial,
            'match_score': round(match_score, 1),
            'total_jd_phrases': total,
            'matched_keywords': [m['phrase'] for m in matched],
            'missing_keywords': [m['phrase'] for m in missing],
        }

    def _extract_key_phrases(self, text: str) -> List[Tuple[str, float]]:
        """Extract important phrases from text using TF-IDF."""
        sentences = re.split(r'[.!?\n]', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

        if not sentences:
            return []

        try:
            tfidf_matrix = self.tfidf.fit_transform(sentences)
            feature_names = self.tfidf.get_feature_names_out()

            # Average TF-IDF across all sentences
            avg_tfidf = np.asarray(tfidf_matrix.mean(axis=0)).flatten()

            # Get top phrases
            top_indices = avg_tfidf.argsort()[::-1][:50]
            phrases = []

            for idx in top_indices:
                phrase = feature_names[idx]
                importance = float(avg_tfidf[idx])
                if importance > 0.01 and len(phrase) > 2:
                    phrases.append((phrase, importance))

            return phrases
        except Exception:
            # Fallback to simple word frequency
            words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
            from nltk.corpus import stopwords
            try:
                stop = set(stopwords.words('english'))
            except Exception:
                stop = set()
            stop.update({
                'remote', 'job', 'resume', 'compensation', 'qualifications', 'assessment', 'overview',
                'options', 'help', 'project', 'candidate', 'candidates', 'employer', 'employers',
                'experience', 'work', 'working', 'team', 'teams', 'role', 'roles', 'company', 'companies',
                'position', 'positions', 'responsibilities', 'duties', 'requirements', 'skills',
                'application', 'apply', 'employment', 'status', 'opportunity', 'opportunities',
                'equal', 'benefits', 'salary', 'pay', 'bonus', 'insurance', 'vacation', 'leave',
                'paid', 'time', 'off', 'flexible', 'schedule', 'hours', 'full-time', 'part-time',
                'contract', 'temporary', 'internship', 'location', 'locations', 'office', 'offices',
                'travel', 'required', 'preferred', 'desired', 'minimum', 'maximum', 'years', 'months',
                'degree', 'diploma', 'education', 'university', 'college', 'school', 'schools',
                'user', 'users', 'client', 'clients', 'customer', 'customers', 'service', 'services',
                'product', 'products', 'support', 'technical', 'technology', 'technologies', 'system',
                'systems', 'software', 'application', 'applications', 'program', 'programs', 'tool',
                'tools', 'platform', 'platforms', 'framework', 'frameworks', 'library', 'libraries',
                'environment', 'environments', 'development', 'developer', 'developers', 'engineer',
                'engineers', 'engineering', 'manager', 'managers', 'management', 'lead', 'leader',
                'leaders', 'leadership', 'teamwork', 'ability', 'abilities', 'capable', 'competent',
                'expert', 'professional', 'professionals', 'industry', 'industries', 'field', 'fields',
                'area', 'areas', 'day', 'days', 'week', 'weeks', 'month', 'months', 'year', 'years',
                'description', 'summary', 'detail', 'details', 'must', 'should', 'would', 'could',
                'want', 'need', 'needs', 'require', 'requires', 'preferred', 'plus', 'nice'
            })
            filtered = [w for w in words if w not in stop]
            freq = Counter(filtered)
            return [(word, count / max(freq.values())) for word, count in freq.most_common(30)]

    # ------------------------------------------------------------------
    # Semantic Similarity
    # ------------------------------------------------------------------

    def _compute_semantic_similarity(self, cv_text: str, job_description: str) -> float:
        """Compute cosine similarity between CV and JD using TF-IDF."""
        try:
            vectorizer = TfidfVectorizer(
                stop_words='english',
                ngram_range=(1, 2),
                max_features=300,
            )
            vectors = vectorizer.fit_transform([cv_text, job_description])
            sim = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
            return float(sim)
        except Exception:
            return 0.0

    # ------------------------------------------------------------------
    # Experience Analysis
    # ------------------------------------------------------------------

    def _analyze_experience(self, cv_text: str, job_description: str) -> Dict[str, Any]:
        """Extract and analyze experience requirements vs. CV experience."""
        # Extract required years from JD
        required_years = self._extract_required_years(job_description)

        # Extract actual years from CV
        cv_years = self._extract_cv_years(cv_text)

        # Calculate career timeline
        dates = self._extract_dates(cv_text)
        timeline_years = 0
        if dates and len(dates) >= 2:
            years = [d[0] for d in dates if d[0]]
            if years:
                timeline_years = max(years) - min(years)

        # Score
        if required_years is None:
            score = 75  # No requirement specified
        elif cv_years is not None and cv_years >= required_years:
            score = 100
        elif cv_years is not None and cv_years >= required_years * 0.7:
            score = 75
        elif timeline_years >= required_years:
            score = 85
        elif timeline_years >= required_years * 0.7:
            score = 60
        else:
            score = 40

        return {
            'required_years': required_years,
            'stated_years': cv_years,
            'timeline_years': timeline_years,
            'dates_found': dates[:10],
            'score': score,
        }

    def _extract_required_years(self, job_description: str) -> Optional[int]:
        """Extract years of experience requirement from job description."""
        patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|exp)',
            r'(?:minimum|at\s+least|requires?)\s+(\d+)\s+(?:years?|yrs?)',
            r'(\d+)\s*-\s*\d+\s+(?:years?|yrs?)',
        ]
        for pattern in patterns:
            match = re.search(pattern, job_description, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return None

    def _extract_cv_years(self, cv_text: str) -> Optional[int]:
        """Extract explicitly stated years of experience from CV."""
        patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|exp)',
            r'over\s+(\d+)\s+(?:years?|yrs?)',
        ]
        for pattern in patterns:
            match = re.search(pattern, cv_text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return None

    def _extract_dates(self, cv_text: str) -> List[Tuple[Optional[int], Optional[int]]]:
        """Extract year ranges from CV text."""
        # Match patterns like "2019 - 2022", "Jan 2020 - Present", "2018-present"
        patterns = [
            r'(20\d{2}|19\d{2})\s*[-–—to]+\s*(20\d{2}|19\d{2}|[Pp]resent|[Cc]urrent)',
            r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(20\d{2}|19\d{2})',
        ]

        dates = []
        for pattern in patterns:
            for match in re.finditer(pattern, cv_text):
                groups = match.groups()
                try:
                    start_year = int(groups[0])
                    if len(groups) > 1:
                        end_str = groups[1]
                        if end_str.lower() in ('present', 'current'):
                            from datetime import datetime
                            end_year = datetime.now().year
                        else:
                            end_year = int(end_str)
                    else:
                        end_year = None
                    dates.append((start_year, end_year))
                except (ValueError, IndexError):
                    pass

        return dates

    # ------------------------------------------------------------------
    # Education Analysis
    # ------------------------------------------------------------------

    def _analyze_education(self, cv_text: str, job_description: str) -> Dict[str, Any]:
        """Analyze education requirements vs. CV education."""
        required_level = self._detect_degree_level(job_description)
        cv_level = self._detect_degree_level(cv_text)

        required_rank = self.DEGREE_LEVELS.get(required_level, 0) if required_level else 0
        cv_rank = self.DEGREE_LEVELS.get(cv_level, 0) if cv_level else 0

        if required_rank == 0:
            score = 80  # No specific requirement
        elif cv_rank >= required_rank:
            score = 100
        elif cv_rank >= required_rank - 1:
            score = 70
        else:
            score = 40

        return {
            'required_level': required_level,
            'cv_level': cv_level,
            'required_rank': required_rank,
            'cv_rank': cv_rank,
            'score': score,
        }

    def _detect_degree_level(self, text: str) -> Optional[str]:
        """Detect the highest degree level mentioned in text."""
        text_lower = text.lower()
        best_level = None
        best_rank = 0

        for keyword, rank in self.DEGREE_LEVELS.items():
            # Use word boundary matching to avoid false positives
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, text_lower):
                if rank > best_rank:
                    best_rank = rank
                    best_level = keyword

        return best_level

    # ------------------------------------------------------------------
    # Formatting Analysis
    # ------------------------------------------------------------------

    def _analyze_formatting(self, cv_text: str) -> Dict[str, Any]:
        """Detect ATS-unfriendly formatting."""
        issues = []
        score = 100

        # Check for excessive special characters (tables, graphics)
        special_count = len(re.findall(r'[│┃┆┊╎║├┤┬┴┼═╔╗╚╝╠╣╦╩╬]', cv_text))
        if special_count > 0:
            issues.append({'issue': 'Table/box characters detected', 'severity': 'high', 'penalty': 15})
            score -= 15

        # Check for excessive capitalization (header abuse)
        caps_lines = re.findall(r'^[A-Z\s]{20,}$', cv_text, re.MULTILINE)
        if len(caps_lines) > 5:
            issues.append({'issue': 'Excessive ALL-CAPS text', 'severity': 'medium', 'penalty': 5})
            score -= 5

        # Check for inconsistent bullet styles
        bullet_types = set()
        for match in re.finditer(r'^[\s]*([-•*▪▸►◆●○→»])', cv_text, re.MULTILINE):
            bullet_types.add(match.group(1))
        if len(bullet_types) > 2:
            issues.append({'issue': f'Inconsistent bullet styles ({len(bullet_types)} types)', 'severity': 'low', 'penalty': 5})
            score -= 5

        # Check for excessive whitespace (may indicate columns)
        wide_gaps = len(re.findall(r'[^\s]\s{5,}[^\s]', cv_text))
        if wide_gaps > 3:
            issues.append({'issue': 'Multi-column layout detected (wide gaps)', 'severity': 'high', 'penalty': 10})
            score -= 10

        # Check for very long lines (may indicate concatenated columns)
        long_lines = sum(1 for line in cv_text.split('\n') if len(line) > 150)
        if long_lines > 5:
            issues.append({'issue': 'Very long lines (possible parsing issues)', 'severity': 'medium', 'penalty': 5})
            score -= 5

        # Check for unusual characters that confuse ATS
        unusual = len(re.findall(r'[^\x00-\x7F]', cv_text))
        if unusual > 20:
            issues.append({'issue': f'Non-ASCII characters ({unusual})', 'severity': 'low', 'penalty': 3})
            score -= 3

        # Check for missing email
        if not re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', cv_text):
            issues.append({'issue': 'No email address found', 'severity': 'high', 'penalty': 10})
            score -= 10

        # Check for missing phone
        if not re.search(r'[\+]?[\d\s\-\(\)]{7,}', cv_text):
            issues.append({'issue': 'No phone number found', 'severity': 'medium', 'penalty': 5})
            score -= 5

        return {
            'issues': issues,
            'score': max(score, 0),
            'issue_count': len(issues),
        }

    # ------------------------------------------------------------------
    # Keyword Density
    # ------------------------------------------------------------------

    def _analyze_keyword_density(self, cv_text: str, keyword_analysis: Dict) -> Dict[str, Any]:
        """Analyze keyword density — penalize both under-use and stuffing."""
        matched = keyword_analysis.get('matched', [])
        cv_words = cv_text.lower().split()
        total_words = len(cv_words)

        if total_words == 0:
            return {'score': 0, 'density': 0, 'status': 'empty'}

        keyword_count = sum(
            cv_text.lower().count(m['phrase'].lower())
            for m in matched
        )

        density = keyword_count / total_words

        if 0.02 <= density <= 0.06:
            score = 100  # Ideal range
            status = 'optimal'
        elif density < 0.01:
            score = 40
            status = 'too_low'
        elif density < 0.02:
            score = 70
            status = 'low'
        elif density <= 0.08:
            score = 80
            status = 'slightly_high'
        else:
            score = 50
            status = 'keyword_stuffing'

        return {
            'score': score,
            'density': round(density, 4),
            'keyword_count': keyword_count,
            'total_words': total_words,
            'status': status,
        }

    # ------------------------------------------------------------------
    # Section Scoring
    # ------------------------------------------------------------------

    def _score_section_completeness(self, parsed_sections: Dict[str, str]) -> float:
        """Score based on presence of essential sections."""
        essential = {'summary': 15, 'experience': 30, 'education': 20, 'skills': 20}
        nice_to_have = {'certifications': 5, 'projects': 5, 'awards': 3, 'volunteer': 2}

        score = 0
        detected = set(parsed_sections.keys())

        for section, points in essential.items():
            if section in detected:
                score += points

        for section, points in nice_to_have.items():
            if section in detected:
                score += points

        # Contact info (check header for email/phone)
        header = parsed_sections.get('header', '')
        if re.search(r'@', header) or re.search(r'\d{3}', header):
            score += 15

        return min(score, 100)

    def _score_section_order(self, parsed_sections: Dict[str, str]) -> float:
        """Score section ordering against preferred ATS order."""
        detected_order = [s for s in parsed_sections.keys() if s != 'header']
        if not detected_order:
            return 50

        preferred_indices = {
            s: i for i, s in enumerate(self.PREFERRED_SECTION_ORDER)
        }

        inversions = 0
        total_pairs = 0
        for i in range(len(detected_order)):
            for j in range(i + 1, len(detected_order)):
                a = preferred_indices.get(detected_order[i], 99)
                b = preferred_indices.get(detected_order[j], 99)
                total_pairs += 1
                if a > b:
                    inversions += 1

        if total_pairs == 0:
            return 80

        order_ratio = 1 - (inversions / total_pairs)
        return round(order_ratio * 100)

    # ------------------------------------------------------------------
    # Content Quality Scoring
    # ------------------------------------------------------------------

    def _score_achievements(self, cv_text: str) -> float:
        """Score quantified achievements."""
        patterns = [
            r'\d+%',               # percentages
            r'\$[\d,]+',           # dollar amounts
            r'€[\d,]+',           # euro amounts
            r'\d+[kKmM]\b',        # shorthand amounts
            r'\d+\s*(?:million|billion|thousand)', 
            r'(?:increased|decreased|reduced|improved|grew|boosted|saved|generated|delivered).*?\d+',
        ]

        count = 0
        for pattern in patterns:
            count += len(re.findall(pattern, cv_text, re.IGNORECASE))

        if count >= 8:
            return 100
        elif count >= 5:
            return 85
        elif count >= 3:
            return 70
        elif count >= 1:
            return 50
        else:
            return 20

    def _score_action_verbs(self, cv_text: str) -> float:
        """Score use of strong action verbs."""
        action_verbs = {
            'achieved', 'accomplished', 'administered', 'advanced', 'analyzed',
            'architected', 'automated', 'boosted', 'built', 'championed',
            'collaborated', 'consolidated', 'created', 'decreased', 'delivered',
            'designed', 'developed', 'directed', 'drove', 'eliminated',
            'engineered', 'established', 'executed', 'expanded', 'expedited',
            'facilitated', 'founded', 'generated', 'grew', 'headed',
            'implemented', 'improved', 'increased', 'initiated', 'innovated',
            'integrated', 'launched', 'led', 'managed', 'maximized',
            'mentored', 'modernized', 'negotiated', 'optimized', 'orchestrated',
            'overhauled', 'pioneered', 'planned', 'produced', 'reduced',
            'redesigned', 'resolved', 'restructured', 'revamped', 'scaled',
            'secured', 'simplified', 'spearheaded', 'streamlined', 'strengthened',
            'supervised', 'surpassed', 'trained', 'transformed', 'tripled',
        }

        cv_words = set(re.findall(r'\b[a-z]+\b', cv_text.lower()))
        found = action_verbs.intersection(cv_words)

        if len(found) >= 10:
            return 100
        elif len(found) >= 7:
            return 85
        elif len(found) >= 4:
            return 70
        elif len(found) >= 2:
            return 50
        else:
            return 20

    # ------------------------------------------------------------------
    # Recommendations
    # ------------------------------------------------------------------

    def _generate_recommendations(
        self,
        scores: Dict[str, float],
        keyword_analysis: Dict,
        formatting_analysis: Dict,
        parsed_sections: Dict,
    ) -> List[Dict[str, str]]:
        """Generate prioritized ATS improvement recommendations."""
        recs = []

        # Keyword recommendations
        if scores['keyword_match'] < 60:
            missing = keyword_analysis.get('missing_keywords', [])[:5]
            if missing:
                recs.append({
                    'priority': 'high',
                    'category': 'keywords',
                    'title': 'Add Missing Keywords',
                    'description': f'Your CV is missing these important terms from the job description: {", ".join(missing)}. Naturally incorporate them into your experience and skills sections.',
                })

        if scores['semantic_relevance'] < 50:
            recs.append({
                'priority': 'high',
                'category': 'content',
                'title': 'Improve Content Relevance',
                'description': 'Your CV content has low semantic similarity to the job description. Rewrite your experience bullets to use language that mirrors the job posting.',
            })

        # Section recommendations
        essential_missing = []
        for section in ['summary', 'experience', 'education', 'skills']:
            if section not in parsed_sections:
                essential_missing.append(section.title())
        if essential_missing:
            recs.append({
                'priority': 'high',
                'category': 'structure',
                'title': 'Add Missing Sections',
                'description': f'Your CV is missing these essential sections: {", ".join(essential_missing)}. Most ATS systems expect these sections.',
            })

        # Achievement recommendations
        if scores['quantified_achievements'] < 60:
            recs.append({
                'priority': 'high',
                'category': 'content',
                'title': 'Quantify Your Achievements',
                'description': 'Add numbers, percentages, and metrics to your accomplishments. Instead of "improved sales", write "increased sales by 25% ($50K) in Q3 2024".',
            })

        # Action verb recommendations
        if scores['action_verbs'] < 60:
            recs.append({
                'priority': 'medium',
                'category': 'language',
                'title': 'Use Stronger Action Verbs',
                'description': 'Start bullet points with powerful verbs: "Spearheaded", "Architected", "Drove", "Optimized" instead of "Helped", "Worked on", "Was responsible for".',
            })

        # Formatting recommendations
        for issue in formatting_analysis.get('issues', []):
            if issue['severity'] == 'high':
                recs.append({
                    'priority': 'high',
                    'category': 'formatting',
                    'title': f'Fix: {issue["issue"]}',
                    'description': 'This formatting issue may prevent ATS systems from correctly parsing your CV.',
                })

        # Experience recommendations
        if scores['experience_match'] < 60:
            recs.append({
                'priority': 'medium',
                'category': 'experience',
                'title': 'Strengthen Experience Section',
                'description': 'Your experience may not match the job requirements. Emphasize relevant roles, transferable skills, and clearly state your years of experience.',
            })

        # Density recommendations
        if scores['keyword_density'] < 60:
            recs.append({
                'priority': 'medium',
                'category': 'keywords',
                'title': 'Adjust Keyword Density',
                'description': 'Your keyword density is outside the optimal range. Aim for naturally using job-relevant terms 2-6% of the time.',
            })

        # Sort by priority
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        recs.sort(key=lambda r: priority_order.get(r['priority'], 3))

        return recs
