"""
CV Rewrite Engine
AI-powered CV section rewriting for ATS optimization.
Generates improved versions of CV sections while maintaining truthfulness.
"""

import re
from typing import Dict, List, Any, Optional
from utils.ollama_client import OllamaClient


class RewriteEngine:
    """AI-powered CV rewriter that optimizes content for ATS systems."""

    # Weak phrases that should be replaced with stronger alternatives
    WEAK_PHRASES = {
        'responsible for': 'Led / Managed / Directed',
        'duties included': 'Delivered / Executed / Accomplished',
        'helped with': 'Contributed to / Supported / Facilitated',
        'assisted with': 'Collaborated on / Co-led / Drove',
        'worked on': 'Developed / Built / Engineered',
        'involved in': 'Played a key role in / Drove / Spearheaded',
        'tasked with': 'Owned / Championed / Delivered',
        'in charge of': 'Directed / Oversaw / Managed',
        'participated in': 'Contributed to / Drove results in',
        'was part of': 'Served as a core member of',
    }

    # STAR format template
    STAR_TEMPLATE = (
        "**Situation**: [Context — what was the challenge or opportunity?]\n"
        "**Task**: [Your specific responsibility]\n"
        "**Action**: [What you did — use strong verbs]\n"
        "**Result**: [Quantified outcome — numbers, %, $, time saved]"
    )

    def __init__(self):
        self.ollama_client = OllamaClient()

    # ------------------------------------------------------------------
    # Section-by-Section Rewriting
    # ------------------------------------------------------------------

    def clean_conversational_text(self, text: str) -> str:
        """Clean conversational preambles and postambles from AI output."""
        text = text.strip()
        
        # Remove markdown quotes
        if text.startswith('"""') and text.endswith('"""'):
            text = text.strip('"""').strip()
        if text.startswith('```') and text.endswith('```'):
            lines = text.split('\n')
            if lines[0].startswith('```'):
                lines = lines[1:]
            if lines and lines[-1].strip() == '```':
                lines = lines[:-1]
            text = '\n'.join(lines).strip()
            
        # Common preamble patterns (multi-line or single line)
        preamble_patterns = [
            r'^(?:here is|here\'s|sure, here is|sure, here\'s|below is|below are|i\'ve rewritten|i have rewritten|i\'ve optimized|i have optimized|here is the optimized|here is the rewritten|here is an enhanced|as an expert|dianelle|hello|hi)[^\n]*?(?:section|summary|experience|education|skills|bullet points?|cv|resume)[^\n]*?:\s*',
            r'^i\'ve incorporated[^\n]*?truthfulness\.\s*',
            r'^i\'ve also\s*followed[^\n]*?weak phrases\.\s*',
            r'^here\'s a rewritten[^\n]*?:\s*',
            r'^here is a rewritten[^\n]*?:\s*'
        ]
        
        changed = True
        while changed:
            changed = False
            for pattern in preamble_patterns:
                new_text = re.sub(pattern, '', text, flags=re.IGNORECASE)
                if new_text != text:
                    text = new_text.strip()
                    changed = True
                    
        # Remove specific conversational sentences that frequently show up at the start/end
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            trimmed = line.strip()
            # Skip AI preamble / postamble lines
            if trimmed.lower().startswith((
                "i've incorporated", "i have incorporated", "i've also followed", 
                "i have also followed", "i've rewritten", "i have rewritten",
                "this rewrite", "here is the", "let me know if",
                "i've ensured", "i have ensured", "i've maintained",
                "note:", "note that",
            )) and len(trimmed) > 40:
                continue
            # Strip structured labels that the LLM sometimes injects
            label_pattern = r'^\*{0,2}(Key Achievements|Required Skills (?:&|and) Experience|Nice to Have|Core Competencies|Professional Summary|Summary|Areas of Expertise|Qualifications)[:\*]*\s*'
            line_cleaned = re.sub(label_pattern, '', trimmed, flags=re.IGNORECASE)
            if line_cleaned != trimmed:
                # If the label was the entire line, skip it
                if not line_cleaned.strip():
                    continue
                cleaned_lines.append(line_cleaned)
            else:
                cleaned_lines.append(line)
            
        text = '\n'.join(cleaned_lines).strip()
        return text

    def rewrite_section(
        self,
        section_content: str,
        section_name: str,
        job_description: str,
        missing_keywords: List[str] = None,
        tone: str = 'professional',
    ) -> Dict[str, Any]:
        """
        Rewrite a CV section for ATS optimization.

        Args:
            section_content: Current section text
            section_name: Type of section (summary, experience, skills, education)
            job_description: Target job description
            missing_keywords: Keywords to naturally incorporate
            tone: Writing tone (professional, confident, concise)

        Returns:
            dict with 'original', 'rewritten', 'changes_made', 'keywords_added'
        """
        if not section_content.strip():
            return {
                'original': section_content,
                'rewritten': section_content,
                'changes_made': [],
                'keywords_added': [],
            }

        missing_kw = missing_keywords or []

        # Build rewrite prompt
        prompt = self._build_rewrite_prompt(
            section_content, section_name, job_description, missing_kw, tone
        )

        # Get AI rewrite
        try:
            if self.ollama_client.is_connected():
                rewritten = self.ollama_client.generate_response(
                    prompt, temperature=0.3, max_tokens=1200
                )
            else:
                rewritten = self._rule_based_rewrite(section_content, missing_kw)
        except Exception:
            rewritten = self._rule_based_rewrite(section_content, missing_kw)

        cleaned_rewritten = self.clean_conversational_text(rewritten)

        # Analyze changes
        changes = self._analyze_changes(section_content, cleaned_rewritten)
        keywords_added = [kw for kw in missing_kw if kw.lower() in cleaned_rewritten.lower()]

        return {
            'original': section_content,
            'rewritten': cleaned_rewritten,
            'changes_made': changes,
            'keywords_added': keywords_added,
        }

    def rewrite_all_sections(
        self,
        parsed_sections: Dict[str, str],
        job_description: str,
        missing_keywords: List[str] = None,
        sections_to_rewrite: List[str] = None,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Rewrite multiple CV sections.

        Args:
            parsed_sections: Dict of section_name -> content
            job_description: Target JD
            missing_keywords: Keywords to incorporate
            sections_to_rewrite: Which sections to rewrite (None = all)

        Returns:
            Dict of section_name -> rewrite result
        """
        targets = sections_to_rewrite or list(parsed_sections.keys())
        results = {}

        for section_name in targets:
            content = parsed_sections.get(section_name, '')
            if content and section_name not in ('header', 'contact'):
                results[section_name] = self.rewrite_section(
                    content, section_name, job_description, missing_keywords
                )

        return results

    # ------------------------------------------------------------------
    # Bullet Point Optimizer
    # ------------------------------------------------------------------

    def optimize_bullets(self, bullets_text: str, job_description: str) -> List[Dict[str, str]]:
        """
        Optimize individual bullet points for impact.

        Returns list of {original, optimized, improvement_notes}
        """
        bullets = self._extract_bullets(bullets_text)
        results = []

        for bullet in bullets:
            optimized = self._optimize_single_bullet(bullet, job_description)
            results.append(optimized)

        return results

    def _extract_bullets(self, text: str) -> List[str]:
        """Extract individual bullet points from text."""
        lines = text.strip().split('\n')
        bullets = []
        current_bullet = ''

        for line in lines:
            stripped = line.strip()
            if re.match(r'^[-•*▪▸►◆●○→»]\s*', stripped) or re.match(r'^\d+[.)]\s*', stripped):
                if current_bullet:
                    bullets.append(current_bullet.strip())
                current_bullet = re.sub(r'^[-•*▪▸►◆●○→»\d.)]+\s*', '', stripped)
            elif stripped:
                if current_bullet:
                    current_bullet += ' ' + stripped
                else:
                    bullets.append(stripped)

        if current_bullet:
            bullets.append(current_bullet.strip())

        return bullets

    def _optimize_single_bullet(self, bullet: str, job_description: str) -> Dict[str, str]:
        """Optimize a single bullet point."""
        notes = []
        optimized = bullet

        # Check for weak phrases
        for weak, strong in self.WEAK_PHRASES.items():
            if weak in optimized.lower():
                notes.append(f'Replaced "{weak}" with stronger verb')
                pattern = re.compile(re.escape(weak), re.IGNORECASE)
                optimized = pattern.sub(strong.split(' / ')[0], optimized, count=1)

        # Check if bullet starts with action verb
        first_word = optimized.split()[0].lower() if optimized.split() else ''
        if not self._is_action_verb(first_word):
            notes.append('Consider starting with a strong action verb')

        # Check for quantification
        if not re.search(r'\d+', optimized):
            notes.append('Add metrics: numbers, percentages, or dollar amounts')

        # Check length
        if len(optimized.split()) < 5:
            notes.append('Bullet is too short — add more detail and impact')
        elif len(optimized.split()) > 30:
            notes.append('Bullet is too long — consider splitting or condensing')

        return {
            'original': bullet,
            'optimized': optimized,
            'improvement_notes': notes,
        }

    # ------------------------------------------------------------------
    # Professional Summary Generator
    # ------------------------------------------------------------------

    def generate_summary(
        self,
        cv_text: str,
        job_description: str,
        years_experience: Optional[int] = None,
    ) -> str:
        """Generate an ATS-optimized professional summary."""
        prompt = f"""You are Dianelle, an expert CV writer and ATS optimization specialist.

Write a compelling 3-4 sentence professional summary for this candidate based on their CV and the target job description.

CV CONTENT:
{cv_text[:2000]}

TARGET JOB DESCRIPTION:
{job_description[:1500]}

{f"Years of experience: {years_experience}" if years_experience else ""}

Requirements for the summary:
1. Start with job title and years of experience
2. Highlight 2-3 most relevant skills/achievements
3. Include 3-4 keywords from the job description naturally
4. End with value proposition (what you bring to the company)
5. Keep it to 3-4 sentences, 50-80 words
6. Use present tense for current capabilities
7. Do NOT include personal pronouns (I, my, me)
8. Write as flowing prose sentences only. Do NOT use labels, subheadings, or structured sections such as "Key Achievements:", "Required Skills:", "Nice to Have:", "Core Competencies:", etc.
9. Do NOT use bullet points in the summary

Write ONLY the summary paragraph, nothing else:"""

        try:
            if self.ollama_client.is_connected():
                summary = self.ollama_client.generate_response(prompt, temperature=0.4, max_tokens=200)
                return self.clean_conversational_text(summary)
            else:
                return self._generate_fallback_summary(cv_text, job_description)
        except Exception:
            return self._generate_fallback_summary(cv_text, job_description)

    # ------------------------------------------------------------------
    # Skills Section Optimizer
    # ------------------------------------------------------------------

    def optimize_skills(
        self,
        current_skills: str,
        job_description: str,
        matched_skills: List[str] = None,
        missing_skills: List[str] = None,
    ) -> Dict[str, Any]:
        """
        Optimize the skills section: reorder, categorize, and add missing skills.

        Returns dict with categorized_skills, added_skills, reordered flag
        """
        prompt = f"""You are Dianelle, an ATS optimization expert.

Reorganize and optimize this skills section to maximize ATS compatibility for the target job.

CURRENT SKILLS SECTION:
{current_skills}

JOB DESCRIPTION:
{job_description[:1500]}

{f"Already matched skills: {', '.join(matched_skills[:10])}" if matched_skills else ""}
{f"Missing important skills: {', '.join(missing_skills[:10])}" if missing_skills else ""}

Instructions:
1. Group skills into categories (Technical Skills, Tools & Technologies, Soft Skills, etc.)
2. Put the most job-relevant skills first in each category
3. Include missing skills ONLY if they could reasonably be added (don't fabricate skills)
4. Use exact terminology from the job description where applicable
5. Remove irrelevant skills that don't match the target role
6. Format as a clean, ATS-parseable list

Output the optimized skills section:"""

        try:
            if self.ollama_client.is_connected():
                optimized = self.ollama_client.generate_response(prompt, temperature=0.3, max_tokens=500)
            else:
                optimized = current_skills
        except Exception:
            optimized = current_skills

        cleaned_optimized = self.clean_conversational_text(optimized)

        return {
            'original': current_skills,
            'optimized': cleaned_optimized,
            'skills_added': [s for s in (missing_skills or []) if s.lower() in cleaned_optimized.lower()],
        }

    # ------------------------------------------------------------------
    # Weak Language Detector
    # ------------------------------------------------------------------

    def detect_weak_language(self, cv_text: str) -> List[Dict[str, str]]:
        """Detect and suggest replacements for weak language."""
        findings = []

        for weak, suggestions in self.WEAK_PHRASES.items():
            occurrences = [m.start() for m in re.finditer(re.escape(weak), cv_text, re.IGNORECASE)]
            for pos in occurrences:
                # Get surrounding context (±50 chars)
                start = max(0, pos - 50)
                end = min(len(cv_text), pos + len(weak) + 50)
                context = cv_text[start:end]

                findings.append({
                    'weak_phrase': weak,
                    'suggestions': suggestions,
                    'context': f'...{context}...',
                    'position': pos,
                })

        return findings

    # ------------------------------------------------------------------
    # Achievement Quantifier
    # ------------------------------------------------------------------

    def suggest_quantification(self, cv_text: str) -> List[Dict[str, str]]:
        """
        Find statements that could be quantified and suggest metric prompts.
        """
        quantifiable_patterns = [
            (r'(?:managed|led|supervised)\s+(?:a\s+)?(?:team|group|department)', 'How many people?'),
            (r'(?:improved|enhanced|optimized|increased)\s+\w+', 'By what percentage or amount?'),
            (r'(?:reduced|decreased|cut|minimized)\s+\w+', 'By how much? (%, $, time)'),
            (r'(?:developed|built|created|designed)\s+\w+', 'How many? What was the impact?'),
            (r'(?:trained|mentored|coached)\s+\w+', 'How many people? Over what period?'),
            (r'(?:generated|produced|delivered)\s+\w+', 'What was the value? ($, units, users)'),
            (r'(?:saved|recovered|reclaimed)\s+\w+', 'How much? ($, hours, resources)'),
            (r'(?:launched|deployed|released)\s+\w+', 'To how many users? In what timeframe?'),
            (r'(?:processed|handled|resolved)\s+\w+', 'How many? How quickly?'),
        ]

        suggestions = []
        lines = cv_text.split('\n')

        for line in lines:
            stripped = line.strip()
            if not stripped or len(stripped) < 20:
                continue

            # Skip lines that already have numbers
            if re.search(r'\d+', stripped):
                continue

            for pattern, question in quantifiable_patterns:
                if re.search(pattern, stripped, re.IGNORECASE):
                    suggestions.append({
                        'original_line': stripped,
                        'question': question,
                        'pattern_matched': pattern,
                    })
                    break  # One suggestion per line

        return suggestions

    # ------------------------------------------------------------------
    # Diff Generator
    # ------------------------------------------------------------------

    def generate_diff(self, original: str, rewritten: str) -> List[Dict[str, Any]]:
        """
        Generate a line-by-line diff between original and rewritten text.

        Returns list of {type: 'unchanged'|'removed'|'added'|'modified', original, new}
        """
        orig_lines = original.strip().split('\n')
        new_lines = rewritten.strip().split('\n')
        diff = []

        max_len = max(len(orig_lines), len(new_lines))

        for i in range(max_len):
            orig = orig_lines[i].strip() if i < len(orig_lines) else ''
            new = new_lines[i].strip() if i < len(new_lines) else ''

            if orig == new:
                diff.append({'type': 'unchanged', 'original': orig, 'new': new})
            elif not orig:
                diff.append({'type': 'added', 'original': '', 'new': new})
            elif not new:
                diff.append({'type': 'removed', 'original': orig, 'new': ''})
            else:
                diff.append({'type': 'modified', 'original': orig, 'new': new})

        return diff

    # ------------------------------------------------------------------
    # Private Helpers
    # ------------------------------------------------------------------

    def _build_rewrite_prompt(
        self,
        content: str,
        section_name: str,
        job_description: str,
        missing_keywords: List[str],
        tone: str,
    ) -> str:
        """Build the LLM prompt for section rewriting."""
        kw_instruction = ''
        if missing_keywords:
            kw_instruction = f"""
IMPORTANT — Naturally incorporate these missing keywords where truthful:
{', '.join(missing_keywords[:10])}
"""

        # Section-specific structure and rules instructions
        struct_instruction = ''
        rules = ''
        
        sec_lower = section_name.lower()
        if sec_lower in ('experience', 'projects', 'full_cv'):
            struct_instruction = """
10. VERY IMPORTANT: Keep all original job titles, project names, companies, and dates exactly as they are. DO NOT remove, merge, or change them.
11. Only rewrite and enhance the bullet points under each job/project header. Do not turn the job/project titles themselves into action-verb bullets.
12. Maintain a clear separation and format for different projects/jobs so they don't get mixed together.
13. Preserve the same level of detail as the original content. Do NOT aggressively shorten descriptions. Keep the full scope of each point.
"""
            rules = """
1. Start every bullet point with a strong action verb (achieved, managed, developed, etc.)
2. Use the Google XYZ formula for accomplishments: "Accomplished [X], as measured by [Y], by doing [Z]".
   - X: The concrete result/outcome (e.g. "Increased database query speed by 40%").
   - Y: How it was measured or verified (e.g. "using APM latency metrics").
   - Z: The concrete action/implementation details (e.g. "by refactoring legacy queries and indexing foreign keys").
3. Ensure every accomplishment is highly quantitative and structured, using numbers, percentages, and metrics.
4. Eliminate recruiter red flags (such as passive phrasing, vague timeline references, or unstructured listings).
5. Remove filler words and weak phrases.
6. Keep each bullet concise (1-2 lines).
7. DO NOT fabricate experience or skills — only optimize existing content.
8. Maintain the same overall meaning and truthfulness.
9. Use present tense for current role, past tense for previous roles.
"""
        elif sec_lower == 'skills':
            struct_instruction = """
10. VERY IMPORTANT: Do NOT use action verbs, STAR format, or write full sentences.
11. Do NOT delete existing skills. Group all original skills into logical, clean categories (e.g., Programming Languages, Frameworks, Tools, Soft Skills).
12. Format each category in bold followed by a clean comma-separated list of skills, or list them clearly in a bulleted/categorized list.
"""
            rules = """
1. Group/categorize skills logically.
2. Format as a clean, structured list. Use bold headings for categories.
3. Mirror language/skills from the job description naturally by placing relevant skills in the correct categories.
4. Keep the categories neat, readable, and highly searchable.
"""
        else: # education, certifications, etc.
            struct_instruction = """
10. VERY IMPORTANT: Keep all degrees, credentials, school/organization names, and dates intact. Do NOT remove or modify them.
11. Do NOT use action verbs or STAR format for these academic/certification entries.
"""
            rules = """
1. Format entries cleanly and professionally.
2. Keep the information concise, structured, and easy to parse.
"""

        # Prevent summary-style labels from being injected
        label_instruction = """
14. Do NOT add any structured labels like "Key Achievements:", "Required Skills & Experience:", "Nice to Have:", "Core Competencies:", or similar headings. Write the content directly without section sub-labels.
"""

        return f"""You are Dianelle, an expert ATS optimization specialist and professional CV writer.

Rewrite the following {section_name.upper()} section to maximize ATS compatibility while keeping content truthful and {tone}.

ORIGINAL {section_name.upper()} SECTION:
{content}

TARGET JOB DESCRIPTION:
{job_description[:1500]}
{kw_instruction}

Rewriting rules:
{rules}{struct_instruction}{label_instruction}
Write ONLY the rewritten section, no labels or explanations:"""

    def _rule_based_rewrite(self, content: str, missing_keywords: List[str]) -> str:
        """Fallback rewrite using rule-based transformations when AI is unavailable."""
        rewritten = content

        # Replace weak phrases
        for weak, strong in self.WEAK_PHRASES.items():
            replacement = strong.split(' / ')[0]
            pattern = re.compile(re.escape(weak), re.IGNORECASE)
            rewritten = pattern.sub(replacement, rewritten)

        return rewritten

    def _analyze_changes(self, original: str, rewritten: str) -> List[str]:
        """Summarize what changed between original and rewritten text."""
        changes = []

        # Check for weak phrase removal
        for weak in self.WEAK_PHRASES:
            if weak in original.lower() and weak not in rewritten.lower():
                changes.append(f'Replaced weak phrase "{weak}"')

        # Check for added quantification
        orig_numbers = len(re.findall(r'\d+', original))
        new_numbers = len(re.findall(r'\d+', rewritten))
        if new_numbers > orig_numbers:
            changes.append(f'Added {new_numbers - orig_numbers} quantified metrics')

        # Check word count change
        orig_words = len(original.split())
        new_words = len(rewritten.split())
        if abs(new_words - orig_words) > 10:
            if new_words > orig_words:
                changes.append(f'Expanded content (+{new_words - orig_words} words)')
            else:
                changes.append(f'Condensed content (-{orig_words - new_words} words)')

        if not changes:
            changes.append('Content restructured and optimized')

        return changes

    def _is_action_verb(self, word: str) -> bool:
        """Check if a word is a strong action verb."""
        action_verbs = {
            'achieved', 'accomplished', 'administered', 'advanced', 'analyzed',
            'architected', 'automated', 'boosted', 'built', 'championed',
            'collaborated', 'consolidated', 'created', 'decreased', 'delivered',
            'designed', 'developed', 'directed', 'drove', 'eliminated',
            'engineered', 'established', 'executed', 'expanded', 'facilitated',
            'founded', 'generated', 'grew', 'headed', 'implemented',
            'improved', 'increased', 'initiated', 'innovated', 'integrated',
            'launched', 'led', 'managed', 'maximized', 'mentored',
            'modernized', 'negotiated', 'optimized', 'orchestrated', 'pioneered',
            'planned', 'produced', 'reduced', 'redesigned', 'resolved',
            'restructured', 'revamped', 'scaled', 'secured', 'simplified',
            'spearheaded', 'streamlined', 'strengthened', 'supervised', 'trained',
            'transformed', 'tripled',
        }
        return word.lower().rstrip('ed').rstrip('d') in action_verbs or word.lower() in action_verbs

    def _generate_fallback_summary(self, cv_text: str, job_description: str) -> str:
        """Generate a basic summary when AI is unavailable."""
        return (
            "Results-driven professional with a proven track record of delivering "
            "impactful solutions. Skilled in collaborating with cross-functional teams "
            "to drive measurable outcomes. Seeking to leverage expertise in a challenging "
            "new role that aligns with career growth objectives."
        )
