"""
Analytics Dashboard Component
Display analytics and insights about CV performance
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, List


class AnalyticsDashboard:
    """Analytics and insights dashboard for CV performance"""
    
    def __init__(self):
        self.score_ranges = {
            'Excellent': (90, 100),
            'Good': (75, 89),
            'Average': (60, 74),
            'Needs Improvement': (40, 59),
            'Poor': (0, 39)
        }
    
    def display(self, analysis_results: Dict[str, Any]):
        """Display the complete analytics dashboard"""
        
        st.markdown("## CV Analytics Dashboard")
        
        # Overview metrics
        self._display_overview_metrics(analysis_results)
        
        # Performance breakdown
        col1, col2 = st.columns([1, 1])
        
        with col1:
            self._display_score_breakdown(analysis_results)
            
        with col2:
            self._display_keyword_analysis(analysis_results)
        
        # Detailed insights
        self._display_detailed_insights(analysis_results)
        
        # Benchmarking
        self._display_benchmarking(analysis_results)
        
        # Progress tracking
        self._display_progress_tracking()
    
    def _display_overview_metrics(self, analysis_results: Dict[str, Any]):
        """Display key overview metrics"""
        
        st.markdown("### Key Performance Indicators")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            ats_score = analysis_results.get('ats_score', 0)
            score_color = self._get_score_color(ats_score)
            
            st.metric(
                label="ATS Compatibility Score",
                value=f"{ats_score}/100",
                delta=self._calculate_score_delta(ats_score),
                delta_color="normal"
            )
            
            st.markdown(f"""
            <div style="background: {score_color}; padding: 0.5rem; border-radius: 5px; text-align: center; color: white; margin-top: 0.5rem;">
                <strong>{self._get_score_grade(ats_score)}</strong>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            keyword_match = analysis_results.get('keyword_match_percentage', 0)
            
            st.metric(
                label="Keyword Match Rate",
                value=f"{keyword_match:.1f}%",
                delta=f"{keyword_match - 50:.1f}%" if keyword_match > 50 else f"{keyword_match - 50:.1f}%",
                delta_color="normal" if keyword_match > 50 else "inverse"
            )
        
        with col3:
            matched_keywords = len(analysis_results.get('matched_keywords', []))
            total_keywords = matched_keywords + len(analysis_results.get('missing_keywords', []))
            
            st.metric(
                label="Keywords Found", 
                value=f"{matched_keywords}/{total_keywords}",
                delta=f"{matched_keywords - (total_keywords//2)} vs avg"
            )
        
        with col4:
            word_count = analysis_results.get('word_count', 0)
            optimal_range = 300 <= word_count <= 800
            
            st.metric(
                label="Word Count",
                value=word_count,
                delta="Optimal" if optimal_range else "Review",
                delta_color="normal" if optimal_range else "inverse"
            )
    
    def _display_score_breakdown(self, analysis_results: Dict[str, Any]):
        """Display detailed score breakdown"""
        
        st.markdown("### Score Breakdown")
        
        # Create score breakdown data
        components = {
            'Keyword Match': analysis_results.get('keyword_match_percentage', 0) * 0.35,
            'CV Structure': self._calculate_structure_score(analysis_results) * 0.25,
            'Content Quality': 75 * 0.20,  # Placeholder
            'Technical Skills': self._calculate_tech_score(analysis_results) * 0.15,
            'ATS Format': 85 * 0.05  # Placeholder
        }
        
        # Create horizontal bar chart
        fig = go.Figure(go.Bar(
            y=list(components.keys()),
            x=list(components.values()),
            orientation='h',
            marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        ))
        
        fig.update_layout(
            title="Component Contribution to Overall Score",
            xaxis_title="Score Contribution",
            height=300,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Component details
        for component, score in components.items():
            percentage = (score / sum(components.values())) * 100
            st.markdown(f"**{component}**: {score:.1f} points ({percentage:.1f}%)")
    
    def _display_keyword_analysis(self, analysis_results: Dict[str, Any]):
        """Display keyword analysis visualization"""
        
        st.markdown("### Keyword Analysis")
        
        matched = len(analysis_results.get('matched_keywords', []))
        missing = len(analysis_results.get('missing_keywords', []))
        
        # Pie chart for keyword distribution
        fig = go.Figure(data=[go.Pie(
            labels=['Matched Keywords', 'Missing Keywords'],
            values=[matched, missing],
            hole=0.4,
            marker_colors=['#2ca02c', '#d62728']
        )])
        
        fig.update_layout(
            title="Keyword Match Distribution",
            height=300,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Top missing keywords
        missing_keywords = analysis_results.get('missing_keywords', [])[:5]
        if missing_keywords:
            st.markdown("**Top Missing Keywords:**")
            for keyword in missing_keywords:
                st.markdown(f"- {keyword}")
    
    def _display_detailed_insights(self, analysis_results: Dict[str, Any]):
        """Display detailed insights and recommendations"""
        
        st.markdown("### Dianelle's AI Insights")
        
        with st.expander("Detailed Analysis", expanded=True):
            
            # Readability analysis
            readability = analysis_results.get('readability_score', 50)
            st.markdown(f"**Readability Score**: {readability:.1f}")
            
            if readability >= 60:
                st.success("✅ Your CV is easy to read and understand")
            elif readability >= 40:
                st.warning("⚠️ Consider simplifying some sentences for better readability")
            else:
                st.error("❌ Your CV may be too complex - simplify language")
            
            # Section analysis
            sections = analysis_results.get('sections_detected', [])
            st.markdown(f"**Detected Sections**: {', '.join(sections) if sections else 'None detected'}")
            
            required_sections = ['experience', 'education', 'skills', 'summary']
            missing_sections = [s for s in required_sections if s not in [sec.lower() for sec in sections]]
            
            if missing_sections:
                st.warning(f"⚠️ Consider adding: {', '.join(missing_sections)}")
            
            # Enhancement opportunities
            opportunities = analysis_results.get('enhancement_opportunities', [])
            if opportunities:
                st.markdown("**Quick Enhancement Opportunities:**")
                for opp in opportunities[:3]:
                    st.markdown(f"- {opp}")
    
    def _display_benchmarking(self, analysis_results: Dict[str, Any]):
        """Display benchmarking against industry standards"""
        
        st.markdown("### Industry Benchmarking")
        
        ats_score = analysis_results.get('ats_score', 0)
        
        # Benchmark data (simulated industry averages)
        benchmark_data = {
            'Your CV': ats_score,
            'Industry Average': 65,
            'Top 25%': 80,
            'Top 10%': 90
        }
        
        fig = go.Figure(data=[go.Bar(
            x=list(benchmark_data.keys()),
            y=list(benchmark_data.values()),
            marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        )])
        
        fig.update_layout(
            title="Your CV vs Industry Benchmarks",
            yaxis_title="ATS Score",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Percentile calculation
        percentile = self._calculate_percentile(ats_score)
        st.markdown(f"**Your CV ranks in the {percentile}th percentile**")
        
        if percentile >= 80:
            st.success(" Excellent! Your CV is better than most candidates")
        elif percentile >= 60:
            st.info("👍 Good performance, with room for improvement")
        else:
            st.warning(" Focus on improvements to compete effectively")
    
    def _display_progress_tracking(self):
        """Display progress tracking over time"""
        
        st.markdown("### Progress Tracking")
        
        # Simulate historical data (in a real app, this would come from a database)
        if 'cv_history' not in st.session_state:
            st.session_state.cv_history = []
        
        # Add current session to history
        current_time = datetime.now()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if len(st.session_state.cv_history) > 1:
                # Create trend chart
                df = pd.DataFrame(st.session_state.cv_history)
                
                fig = px.line(df, x='date', y='score', 
                             title='CV Score Progress Over Time',
                             markers=True)
                
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(" Upload and analyze your CV multiple times to see progress trends")
        
        with col2:
            # Progress summary
            st.markdown("**Progress Summary**")
            
            if len(st.session_state.cv_history) >= 2:
                latest_score = st.session_state.cv_history[-1]['score']
                previous_score = st.session_state.cv_history[-2]['score']
                improvement = latest_score - previous_score
                
                if improvement > 0:
                    st.success(f" +{improvement:.1f} points improvement!")
                elif improvement == 0:
                    st.info(" No change from last analysis")
                else:
                    st.warning(f" {improvement:.1f} points decrease")
            
            # Set goals
            st.markdown("**Set Your Goal**")
            target_score = st.slider("Target ATS Score", 60, 100, 85)
            
            current_score = st.session_state.get('current_cv_score', 70)
            remaining = max(0, target_score - current_score)
            
            if remaining > 0:
                st.markdown(f" {remaining} points to reach your goal!")
            else:
                st.success(" Goal achieved!")
    
    def _get_score_color(self, score: float) -> str:
        """Get color for score display"""
        if score >= 85:
            return "#28a745"  # Green
        elif score >= 70:
            return "#ffc107"  # Yellow
        else:
            return "#dc3545"  # Red
    
    def _get_score_grade(self, score: float) -> str:
        """Get letter grade for score"""
        if score >= 90:
            return "A+"
        elif score >= 85:
            return "A"
        elif score >= 80:
            return "A-"
        elif score >= 75:
            return "B+"
        elif score >= 70:
            return "B"
        elif score >= 65:
            return "B-"
        elif score >= 60:
            return "C+"
        else:
            return "C"
    
    def _calculate_score_delta(self, current_score: float) -> str:
        """Calculate score delta from previous analysis"""
        if 'previous_cv_score' in st.session_state:
            delta = current_score - st.session_state.previous_cv_score
            return f"{delta:+.1f}"
        return "New"
    
    def _calculate_structure_score(self, analysis_results: Dict[str, Any]) -> float:
        """Calculate structure score from analysis results"""
        structure = analysis_results.get('structure_analysis', {})
        
        score = 0
        if structure.get('has_contact_info', False):
            score += 20
        if structure.get('has_summary', False):
            score += 15
        if structure.get('has_experience', False):
            score += 25
        if structure.get('has_education', False):
            score += 15
        if structure.get('has_skills', False):
            score += 15
        if structure.get('uses_bullet_points', False):
            score += 10
        
        return min(score, 100)
    
    def _calculate_tech_score(self, analysis_results: Dict[str, Any]) -> float:
        """Calculate technical skills score"""
        matched_tech = len(analysis_results.get('technical_skills_match', []))
        missing_tech = len(analysis_results.get('missing_technical_skills', []))
        
        if matched_tech + missing_tech == 0:
            return 70
        
        return (matched_tech / (matched_tech + missing_tech)) * 100
    
    def _calculate_percentile(self, score: float) -> int:
        """Calculate percentile ranking"""
        if score >= 90:
            return 95
        elif score >= 80:
            return 85
        elif score >= 70:
            return 70
        elif score >= 60:
            return 55
        else:
            return 30
    
    def update_history(self, score: float):
        """Update score history"""
        if 'cv_history' not in st.session_state:
            st.session_state.cv_history = []
        
        st.session_state.cv_history.append({
            'date': datetime.now(),
            'score': score
        })
        
        # Keep only last 10 entries
        if len(st.session_state.cv_history) > 10:
            st.session_state.cv_history = st.session_state.cv_history[-10:]
        
        # Update previous score for delta calculation
        st.session_state.previous_cv_score = st.session_state.get('current_cv_score', score)
        st.session_state.current_cv_score = score
