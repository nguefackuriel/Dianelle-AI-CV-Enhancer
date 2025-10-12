"""
Improvement Suggestions Component
Generate and display specific CV improvement recommendations
"""

import streamlit as st
from typing import List, Dict, Any
from utils.ollama_client import OllamaClient


class ImprovementSuggestions:
    """Generate and display CV improvement suggestions"""
    
    def __init__(self):
        self.ollama_client = OllamaClient()
        
        # Priority levels for suggestions
        self.priority_colors = {
            'high': '🔴',
            'medium': '🟡', 
            'low': '🟢'
        }
        
        # Category icons
        self.category_icons = {
            'keywords': '🔍',
            'structure': '📋',
            'content': '📝',
            'formatting': '🎨',
            'technical_skills': '⚙️',
            'achievements': '🏆',
            'language': '💬'
        }
    
    def display_suggestions(self, analysis_results: Dict[str, Any]):
        """Display improvement suggestions with interactive features"""
        
        st.markdown("## Personalized Improvement Suggestions")
        
        suggestions = analysis_results.get('suggestions', [])
        
        if not suggestions:
            st.info("Great job! No major improvement suggestions at this time.")
            return
        
        # Filter and sort suggestions
        high_priority = [s for s in suggestions if s.get('priority') == 'high']
        medium_priority = [s for s in suggestions if s.get('priority') == 'medium']
        low_priority = [s for s in suggestions if s.get('priority') == 'low']
        
        # Display priority sections
        if high_priority:
            st.markdown("### 🔴 High Priority - Address These First")
            self._display_suggestion_cards(high_priority, 'high')
        
        if medium_priority:
            st.markdown("### 🟡 Medium Priority - Important Improvements")
            self._display_suggestion_cards(medium_priority, 'medium')
        
        if low_priority:
            st.markdown("### 🟢 Low Priority - Nice to Have")
            with st.expander("View additional suggestions"):
                self._display_suggestion_cards(low_priority, 'low')
        
        # Additional AI-powered suggestions
        self._display_ai_suggestions(analysis_results)
        
        # Improvement roadmap
        self._display_improvement_roadmap(suggestions)
    
    def _display_suggestion_cards(self, suggestions: List[Dict], priority: str):
        """Display suggestion cards with actions"""
        
        for i, suggestion in enumerate(suggestions):
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    # Suggestion content
                    category = suggestion.get('category', 'general')
                    icon = self.category_icons.get(category, '💡')
                    
                    st.markdown(f"""
                    <div style="padding: 1rem; border-left: 4px solid {'#ff4444' if priority == 'high' else '#ffaa44' if priority == 'medium' else '#44aa44'}; background-color: #f8f9fa; margin: 0.5rem 0;">
                        <h4>{icon} {suggestion['title']}</h4>
                        <p>{suggestion['description']}</p>
                        <small>Category: {category.replace('_', ' ').title()}</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Action buttons
                    if st.button(" Get Help", key=f"help_{priority}_{i}"):
                        self._get_detailed_help(suggestion)
                    
                    if st.button(" Mark Done", key=f"done_{priority}_{i}"):
                        self._mark_suggestion_complete(suggestion)
    
    def _display_ai_suggestions(self, analysis_results: Dict[str, Any]):
        """Display AI-powered suggestions"""
        
        st.markdown("### Dianelle's AI-Powered Recommendations")
        
        with st.expander("Get personalized AI suggestions", expanded=False):
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                suggestion_type = st.selectbox(
                    "What would you like help with?",
                    [
                        "Overall CV improvement strategy",
                        "Specific section enhancement", 
                        "Keyword optimization",
                        "Achievement quantification",
                        "Professional summary writing",
                        "Skills section improvement",
                        "Industry-specific advice"
                    ]
                )
            
            with col2:
                if st.button("Ask Dianelle", type="primary"):
                    self._generate_ai_suggestion(suggestion_type, analysis_results)
    
    def _display_improvement_roadmap(self, suggestions: List[Dict]):
        """Display a roadmap for implementing improvements"""
        
        st.markdown("### Improvement Roadmap")
        
        with st.expander("View your improvement journey"):
            
            # Organize by timeline
            immediate = [s for s in suggestions if s.get('priority') == 'high']
            short_term = [s for s in suggestions if s.get('priority') == 'medium']
            long_term = [s for s in suggestions if s.get('priority') == 'low']
            
            timeline_data = [
                {"phase": " Immediate (Today)", "tasks": immediate, "color": "#ff4444"},
                {"phase": " Short-term (This Week)", "tasks": short_term, "color": "#ffaa44"},
                {"phase": " Long-term (This Month)", "tasks": long_term, "color": "#44aa44"}
            ]
            
            for phase_data in timeline_data:
                if phase_data["tasks"]:
                    st.markdown(f"**{phase_data['phase']}**")
                    
                    for task in phase_data["tasks"][:3]:  # Show top 3 for each phase
                        category = task.get('category', 'general')
                        icon = self.category_icons.get(category, '📝')
                        st.markdown(f"- {icon} {task['title']}")
                    
                    st.markdown("---")
            
            # Progress tracking
            total_suggestions = len(suggestions)
            completed = st.session_state.get('completed_suggestions', 0)
            
            if total_suggestions > 0:
                progress = completed / total_suggestions
                st.progress(progress)
                st.markdown(f"Progress: {completed}/{total_suggestions} suggestions completed ({progress*100:.1f}%)")
    
    def _get_detailed_help(self, suggestion: Dict):
        """Get detailed help for a specific suggestion"""
        
        with st.spinner("Getting detailed guidance..."):
            
            help_prompt = f"""
            The user needs detailed help with this CV improvement suggestion:
            
            Title: {suggestion['title']}
            Description: {suggestion['description']}
            Category: {suggestion.get('category', 'general')}
            
            Please provide:
            1. Step-by-step instructions on how to implement this improvement
            2. Specific examples of good vs. bad implementations
            3. Common mistakes to avoid
            4. Tools or resources that might help
            
            Keep it practical and actionable.
            """
            
            try:
                if self.ollama_client.is_connected():
                    help_response = self.ollama_client.generate_response(help_prompt, temperature=0.3)
                else:
                    help_response = self._get_fallback_help(suggestion)
                
                st.markdown("#### Detailed Guidance")
                st.markdown(help_response)
                
            except Exception as e:
                st.error(f"Unable to generate detailed help: {str(e)}")
                st.markdown("**General Tips:**")
                st.markdown(f"- Focus on: {suggestion['description']}")
                st.markdown(f"- Category: {suggestion.get('category', 'general').replace('_', ' ').title()}")
    
    def _mark_suggestion_complete(self, suggestion: Dict):
        """Mark a suggestion as completed"""
        
        if 'completed_suggestions' not in st.session_state:
            st.session_state.completed_suggestions = 0
        
        st.session_state.completed_suggestions += 1
        st.success(f" Marked '{suggestion['title']}' as complete!")
        
        # Celebration for milestones
        completed = st.session_state.completed_suggestions
        
        if completed == 1:
            st.balloons()
            st.success(" Great start! You've completed your first improvement!")
        elif completed % 5 == 0:
            st.balloons()
            st.success(f" Milestone reached! {completed} improvements completed!")
    
    def _generate_ai_suggestion(self, suggestion_type: str, analysis_results: Dict[str, Any]):
        """Generate AI-powered suggestions based on type"""
        
        cv_score = analysis_results.get('ats_score', 0)
        matched_keywords = analysis_results.get('matched_keywords', [])
        missing_keywords = analysis_results.get('missing_keywords', [])
        
        prompts = {
            "Overall CV improvement strategy": f"""
                Based on an ATS score of {cv_score}/100, with {len(matched_keywords)} matched keywords and {len(missing_keywords)} missing keywords, what's the best strategy to improve this CV? Provide a prioritized action plan.
            """,
            
            "Specific section enhancement": """
                Which section of the CV should be the top priority for improvement, and how should it be enhanced? Consider structure, content, and ATS optimization.
            """,
            
            "Keyword optimization": f"""
                The CV is missing these keywords: {', '.join(missing_keywords[:10])}. How should these be naturally incorporated without keyword stuffing?
            """,
            
            "Achievement quantification": """
                How can I better quantify my achievements with numbers, percentages, and metrics? What are some effective ways to make accomplishments more impactful?
            """,
            
            "Professional summary writing": """
                What makes an excellent professional summary that passes ATS screening and engages human recruiters? Provide a template and examples.
            """,
            
            "Skills section improvement": f"""
                How should I structure and optimize my skills section? The job requires these technical skills: {', '.join(missing_keywords[:5])}.
            """,
            
            "Industry-specific advice": """
                What are the most important CV optimization strategies specific to my industry and role level? Consider current market trends.
            """
        }
        
        prompt = prompts.get(suggestion_type, prompts["Overall CV improvement strategy"])
        
        with st.spinner("Generating personalized suggestions..."):
            try:
                if self.ollama_client.is_connected():
                    response = self.ollama_client.generate_response(prompt, temperature=0.5)
                else:
                    response = self._get_fallback_ai_suggestion(suggestion_type)
                
                st.markdown("#### Dianelle's Recommendation")
                st.markdown(response)
                
                # Add to chat history if available
                if 'chat_history' in st.session_state:
                    st.session_state.chat_history.append({
                        'role': 'user',
                        'content': f"AI suggestion request: {suggestion_type}"
                    })
                    st.session_state.chat_history.append({
                        'role': 'assistant', 
                        'content': response
                    })
                
            except Exception as e:
                st.error(f"Unable to generate AI suggestion: {str(e)}")
    
    def _get_fallback_help(self, suggestion: Dict) -> str:
        """Provide fallback help when AI is unavailable"""
        
        category = suggestion.get('category', 'general')
        
        help_texts = {
            'keywords': "Research the job description thoroughly and identify key terms. Use industry-specific language and incorporate relevant keywords naturally throughout your CV. Avoid overusing keywords - aim for natural integration.",
            
            'structure': "Organize your CV with clear sections: Contact Info, Professional Summary, Work Experience, Education, and Skills. Use consistent formatting and clear headings. Ensure logical flow from most to least relevant information.",
            
            'content': "Focus on achievements rather than just responsibilities. Use the STAR method (Situation, Task, Action, Result) to describe accomplishments. Include specific metrics and quantifiable results wherever possible.",
            
            'formatting': "Use simple, clean formatting that's ATS-friendly. Avoid tables, graphics, and unusual fonts. Stick to standard fonts like Arial or Calibri. Use consistent spacing and bullet points for easy scanning.",
            
            'technical_skills': "List technical skills relevant to the job. Group similar skills together. Include proficiency levels where appropriate. Provide context for how you've used these skills in real projects.",
            
            'achievements': "Quantify everything possible with numbers, percentages, dollar amounts, or timeframes. Use strong action verbs. Focus on results and impact rather than just tasks performed."
        }
        
        return help_texts.get(category, "Focus on making your CV clear, relevant, and results-oriented. Tailor content to the specific job and use quantifiable achievements to demonstrate your value.")
    
    def _get_fallback_ai_suggestion(self, suggestion_type: str) -> str:
        """Provide fallback AI suggestions when Ollama is unavailable"""
        
        suggestions = {
            "Overall CV improvement strategy": """
                **Priority Action Plan:**
                1. **Keywords First**: Add 5-7 missing job-relevant keywords naturally
                2. **Quantify Achievements**: Add numbers to at least 3 bullet points  
                3. **Professional Summary**: Write a compelling 2-3 sentence summary
                4. **Skills Section**: Reorganize skills to match job requirements
                5. **Format Review**: Ensure ATS-friendly formatting throughout
                
                Focus on high-impact changes that directly address the job requirements.
            """,
            
            "Keyword optimization": """
                **Keyword Integration Strategy:**
                - Research: Identify 10-15 key terms from job posting
                - Natural Integration: Work keywords into existing bullet points
                - Skills Section: Add technical keywords to skills list
                - Context: Use keywords within achievement descriptions
                - Avoid: Keyword stuffing or unnatural placement
            """,
            
            "Achievement quantification": """
                **Quantification Examples:**
                - "Managed team" → "Managed team of 8 developers"
                - "Improved process" → "Improved process efficiency by 30%"
                - "Increased sales" → "Increased sales by $50K in 6 months"
                - "Led project" → "Led $1M project delivered 2 weeks early"
                
                Add metrics to show scale, impact, and timeframe.
            """
        }
        
        return suggestions.get(suggestion_type, suggestions["Overall CV improvement strategy"])
