"""
Translations Catalog for Dianelle AI
Provides EN/FR translations and a helper function t() for UI components.
"""

import streamlit as st

TRANSLATIONS = {
    # Stepper Steps
    "step_upload": {
        "en": "Upload CV",
        "fr": "Charger le CV"
    },
    "step_jd": {
        "en": "Add Job Desc",
        "fr": "Ajouter l'offre"
    },
    "step_analyze": {
        "en": "Analyze",
        "fr": "Analyser"
    },
    "step_enhance": {
        "en": "Enhance",
        "fr": "Optimiser"
    },
    "step_export": {
        "en": "Export",
        "fr": "Exporter"
    },
    
    # Sidebar
    "choose_feature": {
        "en": "Choose a feature:",
        "fr": "Choisir une fonctionnalité :"
    },
    "sys_status": {
        "en": "System Status",
        "fr": "Statut du Système"
    },
    "active_model": {
        "en": "Active Model:",
        "fr": "Modèle Actif :"
    },
    "ollama_online": {
        "en": "Dianelle AI Online",
        "fr": "Dianelle AI en Ligne"
    },
    "ollama_offline": {
        "en": "Ollama Disconnected",
        "fr": "Ollama Déconnecté"
    },
    "ollama_unavailable": {
        "en": "Ollama Not Available",
        "fr": "Ollama Non Disponible"
    },
    "session": {
        "en": "Session",
        "fr": "Session"
    },
    "ats_score": {
        "en": "ATS Score",
        "fr": "Score ATS"
    },
    "enhanced_sections": {
        "en": "Enhanced Sections",
        "fr": "Sections Optimisées"
    },
    "no_session_data": {
        "en": "No active session data. Once you upload and analyze your CV under **CV Analysis**, your ATS score and optimization metrics will appear here.",
        "fr": "Aucune donnée de session active. Une fois votre CV chargé et analysé sous **CV Analysis**, votre score ATS et vos métriques apparaîtront ici."
    },
    
    # Navigation Page Names
    "Home": {
        "en": "Home",
        "fr": "Accueil"
    },
    "CV Analysis": {
        "en": "CV Analysis",
        "fr": "Analyse de CV"
    },
    "CV Rewriter": {
        "en": "CV Rewriter",
        "fr": "Réécriture de CV"
    },
    "Cover Letter": {
        "en": "Cover Letter",
        "fr": "Lettre de Motivation"
    },
    "Export CV": {
        "en": "Export CV",
        "fr": "Exporter le CV"
    },
    "AI Chat Assistant": {
        "en": "AI Chat Assistant",
        "fr": "Assistant Chat IA"
    },
    "Interview Prep": {
        "en": "Interview Prep",
        "fr": "Préparation Entretien"
    },
    "LinkedIn Optimizer": {
        "en": "LinkedIn Optimizer",
        "fr": "Optimiseur LinkedIn"
    },
    "Negotiation & Follow-ups": {
        "en": "Negotiation & Follow-ups",
        "fr": "Négociation & Relances"
    },
    "Analytics Dashboard": {
        "en": "Analytics Dashboard",
        "fr": "Tableau de Bord"
    },
    "Settings": {
        "en": "Settings",
        "fr": "Paramètres"
    },
    
    # Home Page
    "main_subtitle": {
        "en": "Your AI career assistant — Analyze, Enhance, Export, and Land Your Dream Job",
        "fr": "Votre assistant de carrière IA — Analysez, optimisez, exportez et décrochez le job de vos rêves"
    },
    "out_of_100": {
        "en": "out of 100",
        "fr": "sur 100"
    },
    "welcome_title": {
        "en": "Welcome to Dianelle, Your AI Career Assistant",
        "fr": "Bienvenue sur Dianelle, votre Assistant Carrière IA"
    },
    "welcome_subtitle": {
        "en": "Hi! I'm **Dianelle**, your personal AI career assistant. I'll help you transform your CV into an ATS-optimized powerhouse that gets you past automated screening and noticed by recruiters.",
        "fr": "Bonjour ! Je suis **Dianelle**, votre assistante de carrière personnelle. Je vais vous aider à transformer votre CV en un dossier optimisé pour les logiciels de recrutement (ATS) afin de franchir les filtres automatisés et séduire les recruteurs."
    },
    "what_can_do": {
        "en": "What Can I Do For You?",
        "fr": "Ce que je peux faire pour vous"
    },
    "how_it_works": {
        "en": "How It Works",
        "fr": "Comment ça marche"
    },
    "ready_to_start": {
        "en": "**Ready to land your dream job? Start with CV Analysis from the sidebar.**",
        "fr": "**Prêt à décrocher le poste de vos rêves ? Commencez par l'Analyse de CV dans la barre latérale.**"
    },
    "quick_tips": {
        "en": "Quick Tips",
        "fr": "Conseils Rapides"
    },
    "get_started_header": {
        "en": "Get Started",
        "fr": "Démarrer"
    },
    "get_started_desc": {
        "en": "Upload your CV to see your ATS score",
        "fr": "Chargez votre CV pour voir votre score ATS"
    },
    "start_analysis_btn": {
        "en": "Start CV Analysis",
        "fr": "Lancer l'Analyse de CV"
    },
    
    # Home Page Complex Markdown Blocks
    "home_intro_markdown": {
        "en": """
        ## Welcome to Dianelle, Your AI Career Assistant
 
        Hi! I'm **Dianelle**, your personal AI career assistant. I'll help you transform your CV
        into an ATS-optimized powerhouse that gets you past automated screening and noticed by recruiters.
 
        ### What Can I Do For You?
 
        | Feature | Description |
        |---------|-------------|
        | **CV Analysis** | Upload your CV + job description and get a real ATS compatibility score |
        | **CV Rewriter** | AI rewrites your CV sections with ATS-optimized language |
        | **Cover Letter** | Generate personalized cover letters with tone & length options |
        | **Export** | Download your enhanced CV as professional DOCX or PDF |
        | **Interview Prep** | Practice questions, STAR responses, elevator pitches |
        | **LinkedIn** | Optimize your LinkedIn headline, About section, and keywords |
        | **AI Chat** | Chat with Dianelle for career advice anytime |
        | **Analytics** | Track your improvement with detailed dashboards |
 
        ### How It Works
 
        1. **Upload** your current CV (PDF or DOCX)
        2. **Paste** the job description you're targeting
        3. **Analyze** — get your ATS score with detailed breakdown
        4. **Enhance** — Dianelle rewrites weak sections with ATS-optimized language
        5. **Export** — download your enhanced CV in a professional template
        6. **Prepare** — practice interview questions and craft your pitch
 
        **Ready to land your dream job? Start with CV Analysis from the sidebar.**
        """,
        "fr": """
        ## Bienvenue sur Dianelle, votre Assistant Carrière IA
 
        Bonjour ! Je suis **Dianelle**, votre conseillère en carrière dotée d'IA. Je vais vous aider à optimiser votre CV
        pour qu'il franchisse les filtres des logiciels de recrutement (ATS) et capte l'attention des recruteurs.
 
        ### Ce que je peux faire pour vous :
 
        | Fonctionnalité | Description |
        |----------------|-------------|
        | **Analyse de CV** | Chargez votre CV et l'offre d'emploi pour obtenir un score ATS réel |
        | **Réécriture de CV** | L'IA réécrit vos expériences avec un langage optimisé pour les recruteurs |
        | **Lettre de Motivation** | Génère une lettre de motivation ciblée, avec choix de ton et de longueur |
        | **Export** | Téléchargez votre CV optimisé au format professionnel Word ou PDF |
        | **Préparation Entretien** | Entraînez-vous avec des questions, des réponses STAR et votre pitch |
        | **Optimisation LinkedIn** | Optimisez votre titre, résumé 'À propos' et mots-clés |
        | **Chat IA** | Posez vos questions de carrière à Dianelle à tout moment |
        | **Tableau de Bord** | Suivez votre progression grâce à des graphiques détaillés |
 
        ### Comment ça fonctionne ?
 
        1. **Chargez** votre CV actuel (PDF ou Word).
        2. **Collez** la description de l'offre d'emploi visée.
        3. **Analysez** — découvrez votre score de compatibilité ATS avec le détail des points d'amélioration.
        4. **Optimisez** — Dianelle reformule vos expériences selon les meilleures pratiques.
        5. **Exportez** — téléchargez votre nouveau CV avec un modèle professionnel.
        6. **Préparez** — entraînez-vous pour votre futur entretien.
 
        **Prêt à décrocher le poste idéal ? Commencez par l'Analyse de CV dans la barre latérale.**
        """
    },
    "home_tips_markdown": {
        "en": """
        ### Quick Tips
 
        **Do:**
        - Use action verbs (achieved, managed, led)
        - Quantify accomplishments with numbers
        - Include relevant keywords from the JD
        - Keep formatting simple and clean
        - Tailor your CV for each application
 
        **Avoid:**
        - Tables, graphics, or columns
        - Headers/footers
        - Unusual fonts or colors
        """,
        "fr": """
        ### Conseils Rapides
 
        **À faire :**
        - Utiliser des verbes d'action forts (accompli, géré, dirigé)
        - Quantifier vos réussites avec des données chiffrées (%, budgets)
        - Inclure naturellement les mots-clés de la fiche de poste
        - Garder une mise en page claire, propre et aérée
        - Personnaliser le CV pour chaque offre
 
        **À éviter :**
        - Les tableaux complexes, colonnes et graphiques (qui bloquent les parsers ATS)
        - Les en-têtes et pieds de page trop denses
        - Les typographies exotiques ou les surcharges de couleurs
        """
    },
    
    # CV Analysis Page
    "cv_analysis_title": {
        "en": "CV Analysis & Enhancement",
        "fr": "Analyse & Optimisation du CV"
    },
    "upload_cv": {
        "en": "Upload Your CV",
        "fr": "Chargez votre CV"
    },
    "choose_file": {
        "en": "Choose your CV file",
        "fr": "Choisissez votre fichier de CV"
    },
    "file_uploader_help": {
        "en": "Upload your CV in PDF, DOCX, or TXT format",
        "fr": "Format PDF, DOCX, ou TXT accepté"
    },
    "cv_preview": {
        "en": "Extracted CV Text Preview",
        "fr": "Aperçu du texte brut extrait"
    },
    "cv_processed_success": {
        "en": "CV processed successfully ({word_count} words)",
        "fr": "CV analysé avec succès ({word_count} mots)"
    },
    "job_desc_title": {
        "en": "Job Description",
        "fr": "Offre d'Emploi"
    },
    "paste_jd": {
        "en": "Paste the job description here:",
        "fr": "Collez la description de l'offre ici :"
    },
    "jd_placeholder": {
        "en": "Copy and paste the complete job description including requirements, responsibilities, and qualifications...",
        "fr": "Copiez-collez l'intégralité de l'offre (exigences, responsabilités, diplômes)..."
    },
    "analyze_cv_btn": {
        "en": "Analyze CV",
        "fr": "Analyser le CV"
    },
    "running_ats_spinner": {
        "en": "Running ATS simulation... This may take a moment",
        "fr": "Simulation ATS en cours... Cela peut prendre un instant"
    },
    "analysis_complete": {
        "en": "Analysis complete!",
        "fr": "Analyse terminée !"
    },
    "analysis_failed": {
        "en": "Analysis failed: {error}",
        "fr": "Échec de l'analyse : {error}"
    },
    
    # Results Page
    "ats_simulation_results": {
        "en": "ATS Simulation Results",
        "fr": "Résultats de la Simulation ATS"
    },
    "score_excellent": {
        "en": "Excellent!",
        "fr": "Excellent !"
    },
    "score_good": {
        "en": "Good Progress",
        "fr": "Bonne progression"
    },
    "score_improve": {
        "en": "Room for Improvement",
        "fr": "Marge d'amélioration"
    },
    "semantic_match": {
        "en": "Semantic Match",
        "fr": "Match Sémantique"
    },
    "content_relevance_desc": {
        "en": "Content relevance to JD",
        "fr": "Pertinence du contenu"
    },
    "job_fit": {
        "en": "Job Fit",
        "fr": "Adéquation"
    },
    "score_breakdown": {
        "en": "Score Breakdown",
        "fr": "Détail du Score"
    },
    "relevance_label": {
        "en": "Relevance",
        "fr": "Pertinence"
    },
    "keywords_label": {
        "en": "Keywords",
        "fr": "Mots-clés"
    },
    "sections_label": {
        "en": "Sections",
        "fr": "Rubriques"
    },
    "experience_label": {
        "en": "Experience",
        "fr": "Expérience"
    },
    "metrics_label": {
        "en": "Metrics",
        "fr": "Résultats"
    },
    "red_flags_title": {
        "en": "Recruiter Red Flags (10-Second Scan)",
        "fr": "Signaux d'Alarme (Scan de 10 secondes)"
    },
    "no_matched_keywords": {
        "en": "No matched keywords found.",
        "fr": "Aucun mot-clé correspondant trouvé."
    },
    "improvement_areas": {
        "en": "Improvement Areas",
        "fr": "Axes d'Amélioration"
    },
    "requirements_match": {
        "en": "Requirements Match",
        "fr": "Adéquation des Exigences"
    },
    "required": {
        "en": "required",
        "fr": "requis"
    },
    "status_met": {
        "en": "Met",
        "fr": "Satisfait"
    },
    "status_gap": {
        "en": "Gap",
        "fr": "Écart"
    },
    "years_label": {
        "en": "years",
        "fr": "ans"
    },
    "transferable_skill_relates": {
        "en": "- Your **{your_skill}** relates to **{job_needs}**",
        "fr": "- Votre compétence **{your_skill}** correspond à **{job_needs}**"
    },
    "ai_analysis_title": {
        "en": "Dianelle's AI Analysis",
        "fr": "Analyse IA de Dianelle"
    },
    "ollama_warning": {
        "en": "⚠️ **Dianelle AI Analysis Unavailable** : Unable to contact Ollama or the selected model. Verify that your local server is running (`ollama serve`) and the model is pulled.",
        "fr": "⚠️ **Analyse IA Dianelle indisponible** : Impossible de contacter Ollama ou le modèle sélectionné. Vérifiez que le serveur local est actif (`ollama serve`) et que le modèle est installé."
    },
    
    # CV Rewriter Tabs & General
    "rewrite_title": {
        "en": "AI CV Rewriter — Powered by Dianelle",
        "fr": "Dianelle AI CV Rewriter"
    },
    "rewrite_subtitle": {
        "en": "*Transform your CV into an ATS-optimized powerhouse. Dianelle rewrites your sections while keeping everything truthful.*",
        "fr": "*Transformez votre CV en un dossier optimisé pour les logiciels de recrutement (ATS). Dianelle réécrit vos rubriques tout en restant fidèle à votre parcours.*"
    },
    "please_upload_analyze_first_rewrite": {
        "en": "Please upload and analyze your CV first on the **CV Analysis** page!",
        "fr": "Veuillez d'abord charger et analyser votre CV sur la page **Analyse de CV** !"
    },
    "please_run_analysis_first": {
        "en": "Please run the CV analysis first to get personalized rewrites!",
        "fr": "Veuillez d'abord lancer l'analyse de votre CV pour obtenir des réécritures personnalisées !"
    },
    "tab_section_rewriter": {
        "en": "Section Rewriter",
        "fr": "Réécriture par Rubrique"
    },
    "tab_bullet_optimizer": {
        "en": "Bullet Optimizer",
        "fr": "Optimiseur de Puces"
    },
    "tab_summary_generator": {
        "en": "Summary Generator",
        "fr": "Générateur de Résumé"
    },
    "tab_skills_optimizer": {
        "en": "Skills Optimizer",
        "fr": "Optimiseur de Compétences"
    },
    "tab_weak_language_scan": {
        "en": "Weak Language Scan",
        "fr": "Analyse de Langage Passif"
    },
    "tab_quantification_helper": {
        "en": "Quantification Helper",
        "fr": "Aide à la Quantification"
    },
    "tab_double_test": {
        "en": "ATS & Recruiter Double Test",
        "fr": "Double Test ATS & Recruteur"
    },
    "current_ats_score": {
        "en": "Current ATS Score",
        "fr": "Score ATS Actuel"
    },
    "improvement_potential": {
        "en": "Improvement Potential",
        "fr": "Potentiel d'Amélioration"
    },
    "points_available": {
        "en": "{improvement} points available",
        "fr": "{improvement} points disponibles"
    },
    
    # Section Rewriter Tab
    "section_rewriter_title": {
        "en": "Section-by-Section Rewriter",
        "fr": "Réécriture par Rubrique"
    },
    "section_rewriter_desc": {
        "en": "Select sections to rewrite. Dianelle will optimize each one for ATS compatibility.",
        "fr": "Sélectionnez les rubriques à réécrire. Dianelle les optimisera pour les filtres ATS."
    },
    "no_distinct_sections": {
        "en": "No distinct sections detected. Using full CV text instead.",
        "fr": "Aucune rubrique distincte détectée. Utilisation du texte complet du CV."
    },
    "choose_sections_to_rewrite": {
        "en": "Choose sections to rewrite:",
        "fr": "Sélectionnez les rubriques à réécrire :"
    },
    "tone_label": {
        "en": "Tone:",
        "fr": "Ton :"
    },
    "missing_keywords_to_inject": {
        "en": "**Missing keywords to inject:** {keywords}",
        "fr": "**Mots-clés manquants à injecter :** {keywords}"
    },
    "rewrite_selected_btn": {
        "en": "Rewrite Selected Sections",
        "fr": "Réécrire les Rubriques Sélectionnées"
    },
    "please_select_one_section": {
        "en": "Please select at least one section.",
        "fr": "Veuillez sélectionner au moins une rubrique."
    },
    "dianelle_rewriting_spinner": {
        "en": "Dianelle is rewriting your CV sections...",
        "fr": "Dianelle réécrit vos rubriques..."
    },
    "rewrite_results_title": {
        "en": "Rewrite Results",
        "fr": "Résultats de Réécriture"
    },
    "original": {
        "en": "Original",
        "fr": "D'origine"
    },
    "enhanced": {
        "en": "Enhanced",
        "fr": "Optimisé"
    },
    "changes_made": {
        "en": "Changes made:",
        "fr": "Modifications apportées :"
    },
    "keywords_added": {
        "en": "Keywords added: {keywords}",
        "fr": "Mots-clés ajoutés : {keywords}"
    },
    "accept_btn": {
        "en": "Accept",
        "fr": "Accepter"
    },
    "reject_btn": {
        "en": "Reject",
        "fr": "Rejeter"
    },
    "regenerate_btn": {
        "en": "Re-generate",
        "fr": "Régénérer"
    },
    "accepted_success": {
        "en": "Accepted rewrite for {section}!",
        "fr": "Réécriture acceptée pour {section} !"
    },
    "keeping_original": {
        "en": "Keeping original {section}.",
        "fr": "Conservation de la rubrique {section} d'origine."
    },
    "regenerating_info": {
        "en": "Re-generating... Please click 'Rewrite Selected Sections' again.",
        "fr": "Régénération... Veuillez cliquer de nouveau sur 'Réécrire les Rubriques Sélectionnées'."
    },
    "accept_all_rewrites_btn": {
        "en": "Accept All Rewrites",
        "fr": "Accepter toutes les réécritures"
    },
    "all_rewrites_accepted": {
        "en": "All rewrites accepted! Go to **Export** to download your enhanced CV.",
        "fr": "Toutes les réécritures sont acceptées ! Allez sur **Exporter** pour télécharger le nouveau CV."
    },
    
    # Bullet Optimizer Tab
    "bullet_optimizer_title": {
        "en": "Bullet Point Optimizer",
        "fr": "Optimiseur de Puces"
    },
    "bullet_optimizer_desc": {
        "en": "Paste bullet points from your experience section to optimize them individually.",
        "fr": "Collez des puces de votre section Expérience pour les optimiser individuellement."
    },
    "enter_bullets": {
        "en": "Enter your bullet points (one per line):",
        "fr": "Entrez vos puces (une par ligne) :"
    },
    "optimize_bullets_btn": {
        "en": "Optimize Bullets",
        "fr": "Optimiser les Puces"
    },
    "please_enter_bullets": {
        "en": "Please enter some bullet points.",
        "fr": "Veuillez entrer des puces."
    },
    "optimizing_bullets_spinner": {
        "en": "Optimizing bullet points...",
        "fr": "Optimisation des puces en cours..."
    },
    "bullet_original": {
        "en": "*Original:* {text}",
        "fr": "*D'origine :* {text}"
    },
    "bullet_optimized": {
        "en": "*Optimized:* {text}",
        "fr": "*Optimisé :* {text}"
    },
    
    # Summary Tab
    "summary_generator_title": {
        "en": "Professional Summary Generator",
        "fr": "Générateur de Résumé Professionnel"
    },
    "summary_generator_desc": {
        "en": "Generate an ATS-optimized professional summary tailored to the job.",
        "fr": "Génère un résumé professionnel optimisé pour les filtres ATS et ciblé pour ce poste."
    },
    "years_exp": {
        "en": "Years of Experience:",
        "fr": "Années d'Expérience :"
    },
    "summary_info": {
        "en": "A strong summary is one of the most impactful ATS elements.",
        "fr": "Un résumé percutant est l'un des éléments les plus importants pour un ATS."
    },
    "generate_summary_btn": {
        "en": "Generate Summary",
        "fr": "Générer le Résumé"
    },
    "generating_summary_spinner": {
        "en": "Crafting your professional summary...",
        "fr": "Rédaction du résumé professionnel en cours..."
    },
    "generated_summary_title": {
        "en": "**Generated Professional Summary:**",
        "fr": "**Résumé Professionnel Généré :**"
    },
    "edit_summary": {
        "en": "Edit your summary:",
        "fr": "Modifier le résumé :"
    },
    "use_summary_btn": {
        "en": "Use This Summary",
        "fr": "Utiliser ce Résumé"
    },
    "summary_saved": {
        "en": "Summary saved!",
        "fr": "Résumé enregistré !"
    },
    
    # Skills Tab
    "skills_optimizer_title": {
        "en": "Skills Section Optimizer",
        "fr": "Optimiseur de Compétences"
    },
    "skills_optimizer_desc": {
        "en": "Reorganize and optimize your skills to match the job requirements.",
        "fr": "Réorganisez et optimisez vos compétences pour correspondre à l'offre d'emploi."
    },
    "enter_skills": {
        "en": "Enter your current skills:",
        "fr": "Entrez vos compétences actuelles :"
    },
    "missing_tech_skills": {
        "en": "Missing technical skills: {skills}",
        "fr": "Compétences techniques manquantes : {skills}"
    },
    "optimize_skills_btn": {
        "en": "Optimize Skills",
        "fr": "Optimiser les Compétences"
    },
    "please_enter_skills": {
        "en": "Please enter your skills.",
        "fr": "Veuillez entrer vos compétences."
    },
    "optimizing_skills_spinner": {
        "en": "Optimizing skills section...",
        "fr": "Optimisation des compétences en cours..."
    },
    "current_skills_label": {
        "en": "**Current Skills**",
        "fr": "**Compétences Actuelles**"
    },
    "optimized_skills_label": {
        "en": "**Optimized Skills**",
        "fr": "**Compétences Optimisées**"
    },
    "skills_integrated": {
        "en": "Skills integrated: {skills}",
        "fr": "Compétences intégrées : {skills}"
    },
    "accept_skills_btn": {
        "en": "Accept Skills",
        "fr": "Valider les Compétences"
    },
    "skills_saved": {
        "en": "Skills section saved!",
        "fr": "Compétences enregistrées !"
    },
    
    # Weak Language Tab
    "weak_language_title": {
        "en": "Weak Language Scanner",
        "fr": "Analyse du Langage Passif"
    },
    "weak_language_desc": {
        "en": "Find and replace passive, weak language with powerful action-driven alternatives.",
        "fr": "Trouvez et remplacez les tournures passives ou faibles par des verbes d'action percutants."
    },
    "scan_cv_btn": {
        "en": "Scan CV",
        "fr": "Analyser le CV"
    },
    "scanning_cv_spinner": {
        "en": "Scanning CV...",
        "fr": "Analyse du CV en cours..."
    },
    "no_weak_language": {
        "en": "Great job! No weak language patterns detected.",
        "fr": "Excellent ! Aucune tournure passive ou faible détectée."
    },
    "weak_phrases_found": {
        "en": "Found {count} weak phrase(s) to improve:",
        "fr": "{count} tournures passives ou faibles identifiées :"
    },
    
    # Quantification Tab
    "quant_helper_title": {
        "en": "Achievement Quantification Helper",
        "fr": "Aide à la Quantification"
    },
    "quant_helper_desc": {
        "en": "Identify vague statements and get prompts to add impactful metrics.",
        "fr": "Identifiez les affirmations vagues et obtenez des suggestions pour y ajouter des chiffres."
    },
    "find_quant_btn": {
        "en": "Find Quantification Opportunities",
        "fr": "Trouver des Opportunités de Chiffres"
    },
    "scanning_metrics_spinner": {
        "en": "Scanning for metrics...",
        "fr": "Recherche de métriques en cours..."
    },
    "good_quantification": {
        "en": "Your CV already has good quantification!",
        "fr": "Votre CV comporte déjà d'excellents indicateurs chiffrés !"
    },
    "quant_opportunities_found": {
        "en": "Found {count} statements that could be strengthened with numbers:",
        "fr": "{count} affirmations qui pourraient être renforcées avec des chiffres :"
    },
    "add_metric": {
        "en": "Add your metric:",
        "fr": "Ajouter votre chiffre :"
    },
    
    # Double Test Tab
    "double_test_title": {
        "en": "ATS & Recruiter Double Test Scan",
        "fr": "Double Test ATS & Recruteur"
    },
    "double_test_desc": {
        "en": "This scanner analyzes your CV against the job description simultaneously from the perspective of an automated ATS parsing filter and a tired human recruiter reviewing 200 CVs in a row.",
        "fr": "Ce scan teste votre CV simultanément du point de vue d'un filtre robot ATS et d'un recruteur humain fatigué qui lit 200 CV par jour."
    },
    "applying_rewrites_info": {
        "en": "Applying your accepted rewrites to the scanned CV text for an accurate assessment.",
        "fr": "Application de vos modifications acceptées pour une analyse précise."
    },
    "run_double_test_btn": {
        "en": "Run Double Test Scan",
        "fr": "Lancer le Double Test"
    },
    "double_test_spinner": {
        "en": "Pressure testing your CV against ATS and recruiters...",
        "fr": "Test de pression du CV contre les robots et les recruteurs..."
    },
    "ollama_disconnected": {
        "en": "Ollama is disconnected. Unable to run scan.",
        "fr": "Ollama est déconnecté. Impossible de lancer le scan."
    },
    "double_test_results": {
        "en": "#### Double Test Diagnostic Results:",
        "fr": "#### Résultats du Diagnostic Double Test :"
    },
    
    # Cover Letter Page
    "cl_title": {
        "en": "AI Cover Letter Generator",
        "fr": "Générateur de Lettre de Motivation IA"
    },
    "cl_subtitle": {
        "en": "*Dianelle crafts personalized cover letters that complement your CV and speak directly to the hiring manager.*",
        "fr": "*Dianelle rédige des lettres de motivation personnalisées qui complètent votre CV et s'adresse directement aux recruteurs.*"
    },
    "please_upload_first_cl": {
        "en": "Please upload your CV first on the **CV Analysis** page.",
        "fr": "Veuillez d'abord charger votre CV dans l'onglet **Analyse de CV**."
    },
    "cl_settings": {
        "en": "Cover Letter Settings",
        "fr": "Paramètres de la Lettre"
    },
    "use_hadrien_formula": {
        "en": "Use Hadrien's 'Impossible to Reject' 250-word Letter Formula (Recommended)",
        "fr": "Utiliser la formule d'Hadrien 'Impossible à rejeter' de 250 mots (Recommandé)"
    },
    "hadrien_formula_help": {
        "en": "Generates a high-impact, direct 4-paragraph letter addressing company challenges, achievements, and gaps head-on.",
        "fr": "Génère une lettre percutante et directe de 4 paragraphes traitant de front les défis de l'entreprise, vos réalisations et vos écarts."
    },
    "company_name_label": {
        "en": "Company Name:",
        "fr": "Nom de l'Entreprise :"
    },
    "company_name_placeholder": {
        "en": "e.g., Google, Microsoft, Acme Corp",
        "fr": "ex: Google, Microsoft, Acme Corp"
    },
    "hiring_manager_label": {
        "en": "Hiring Manager Name (optional):",
        "fr": "Nom du Recruteur / Manager (optionnel) :"
    },
    "hiring_manager_placeholder": {
        "en": "e.g., Jane Smith",
        "fr": "ex: Jane Smith"
    },
    "role_title_label": {
        "en": "Job Title:",
        "fr": "Intitulé du Poste :"
    },
    "role_title_placeholder": {
        "en": "e.g., Senior Software Engineer",
        "fr": "ex: Développeur Senior, Chef de Projet"
    },
    "hadrien_locked_info": {
        "en": "Hadrien's Formula locks Length to <250 words and Tone to Confident/Direct.",
        "fr": "La formule d'Hadrien verrouille la longueur à moins de 250 mots et le ton à Direct & Confiant."
    },
    "gap_text_label": {
        "en": "CV Gap or Weakness to address head-on (optional):",
        "fr": "Trou ou faiblesse du CV à traiter directement (optionnel) :"
    },
    "gap_text_placeholder": {
        "en": "e.g., career gap in 2023, missing tool/skill, etc.",
        "fr": "ex: transition professionnelle en 2023, compétence manquante, etc."
    },
    "gap_text_help": {
        "en": "Hadrien's guide advises addressing a weakness head-on in the 3rd paragraph to show self-awareness and honesty.",
        "fr": "Le guide d'Hadrien conseille d'aborder une faiblesse directement au 3ème paragraphe pour montrer votre honnêteté et votre recul."
    },
    "num_variations_label": {
        "en": "Number of variations:",
        "fr": "Nombre de variations :"
    },
    "company_research_title": {
        "en": "Company Research Notes (optional but recommended)",
        "fr": "Notes de Recherche sur l'Entreprise (optionnel mais conseillé)"
    },
    "company_notes_label": {
        "en": "Add notes about the company (values, mission, culture, recent news):",
        "fr": "Notes sur l'entreprise (valeurs, culture, actualité, mission) :"
    },
    "company_notes_placeholder": {
        "en": "e.g., The company values innovation and diversity. They recently launched a new AI product line...",
        "fr": "ex: L'entreprise valorise l'innovation et la diversité. Elle vient de lancer un produit IA..."
    },
    "why_company_label": {
        "en": "Why do you want to work at this company?",
        "fr": "Pourquoi voulez-vous rejoindre cette entreprise ?"
    },
    "why_company_placeholder": {
        "en": "e.g., I'm passionate about their mission to democratize AI...",
        "fr": "ex: Je suis passionné par leur mission de démocratiser l'IA..."
    },
    "generate_cl_btn": {
        "en": "Generate Cover Letter",
        "fr": "Générer la Lettre de Motivation"
    },
    "please_add_jd_cl": {
        "en": "Please add a job description on the CV Analysis page first.",
        "fr": "Veuillez d'abord ajouter une offre d'emploi dans l'onglet **Analyse de CV**."
    },
    "generating_cl_spinner": {
        "en": "Dianelle is writing your cover letter...",
        "fr": "Dianelle rédige votre lettre de motivation..."
    },
    "your_cl_title": {
        "en": "Your Cover Letter",
        "fr": "Votre Lettre de Motivation"
    },
    "edit_cl_label": {
        "en": "Edit your cover letter:",
        "fr": "Modifier votre lettre de motivation :"
    },
    "word_count_label": {
        "en": "Word count: {count}",
        "fr": "Nombre de mots : {count}"
    },
    "cl_variations_title": {
        "en": "Cover Letter Variations",
        "fr": "Variations de la Lettre"
    },
    "compare_variations_info": {
        "en": "Compare variations and pick your favorite!",
        "fr": "Comparez les variations et choisissez votre préférée !"
    },
    "version_label": {
        "en": "Version {num}",
        "fr": "Version {num}"
    },
    "use_version_btn": {
        "en": "Use Version {num}",
        "fr": "Utiliser la Version {num}"
    },
    "version_selected": {
        "en": "Version {num} selected!",
        "fr": "Version {num} sélectionnée !"
    },
    "export_cl_title": {
        "en": "Export Cover Letter",
        "fr": "Exporter la Lettre de Motivation"
    },
    "refine_with_dianelle_btn": {
        "en": "Refine with Dianelle",
        "fr": "Optimiser avec Dianelle"
    },
    "refining_spinner": {
        "en": "Refining...",
        "fr": "Optimisation en cours..."
    },
    "download_txt_btn": {
        "en": "Download as TXT",
        "fr": "Télécharger en TXT"
    },
    "download_docx_btn": {
        "en": "Download as DOCX",
        "fr": "Télécharger en DOCX"
    },
    "save_docx_btn": {
        "en": "Save DOCX",
        "fr": "Enregistrer le DOCX"
    },
    
    # Interview Prep Page
    "interview_prep_title": {
        "en": "Interview Preparation",
        "fr": "Préparation aux Entretiens"
    },
    "interview_prep_subtitle": {
        "en": "*Dianelle helps you prepare for interviews by generating likely questions, building STAR responses, and crafting your elevator pitch.*",
        "fr": "*Dianelle vous aide à préparer vos entretiens en prédisant les questions, en bâtissant vos réponses STAR et en rédigeant votre pitch de présentation.*"
    },
    "target_role_details": {
        "en": "Target Role Details",
        "fr": "Détails du Poste Visé"
    },
    "tab_complete_prep": {
        "en": "Complete Prep Pack",
        "fr": "Kit de Préparation Complet"
    },
    "tab_mock_interview": {
        "en": "Interactive Mock Interview",
        "fr": "Entretien Blanc Interactif"
    },
    "tab_star_builder": {
        "en": "STAR Response Builder",
        "fr": "Générateur STAR"
    },
    "tab_behavioral_tech": {
        "en": "Behavioral & Tech Questions",
        "fr": "Questions Comportementales & Tech"
    },
    "tab_elevator_pitch_framing": {
        "en": "Elevator Pitch & Framing",
        "fr": "Pitch & Cadrage des Faiblesses"
    },
    "recruiter_prep_pack": {
        "en": "Recruiter Prep Pack",
        "fr": "Kit de Préparation Recruteur"
    },
    "recruiter_prep_pack_desc": {
        "en": "Generate a complete target company research brief, predicted questions with traps, and questions to ask.",
        "fr": "Génère un briefing de recherche complet sur l'entreprise, 10 questions prédites avec leurs pièges, et des questions pertinentes à leur poser."
    },
    "fill_role_details_info": {
        "en": "Please fill in the Company Name and Job Title at the top to generate a personalized Prep Pack.",
        "fr": "Veuillez saisir le Nom de l'Entreprise et l'Intitulé du Poste en haut pour générer un kit personnalisé."
    },
    "gen_prep_pack_btn": {
        "en": "Generate Prep Pack",
        "fr": "Générer le Kit de Préparation"
    },
    "analyzing_company_spinner": {
        "en": "Analyzing target company and predicting questions...",
        "fr": "Analyse de l'entreprise cible et prédiction des questions..."
    },
    "company_research_brief_title": {
        "en": "#### Company Business & Research Brief",
        "fr": "#### Brief de Recherche & Activité de l'Entreprise"
    },
    "predicted_questions_title": {
        "en": "#### 10 Predicted Questions with Traps & STAR Answers",
        "fr": "#### 10 Questions Prédites avec Pièges & Réponses STAR"
    },
    "why_ask_label": {
        "en": "**Why they ask this:** {reason}",
        "fr": "**Pourquoi ils posent cette question :** {reason}"
    },
    "trap_label": {
        "en": "**The Trap:** {trap}",
        "fr": "**Le Piège :** {trap}"
    },
    "strong_star_answer_label": {
        "en": "**Strong STAR Answer:** {answer}",
        "fr": "**Réponse STAR Forte :** {answer}"
    },
    "questions_to_ask_them_title": {
        "en": "#### 5 Business-Savvy Questions to Ask Them",
        "fr": "#### 5 Questions Stratégiques à leur poser"
    },
    "mock_interview_title": {
        "en": "Interactive Mock Interview Coach",
        "fr": "Simulateur d'Entretien Interactif"
    },
    "mock_interview_desc": {
        "en": "Practice your responses in real-time with Dianelle acting as your interviewer.",
        "fr": "Entraînez-vous en temps réel avec Dianelle jouant le rôle de votre recruteur."
    },
    "mock_fill_details_info": {
        "en": "Please fill in the Company Name and Job Title at the top to start the Mock Interview.",
        "fr": "Veuillez saisir le Nom de l'Entreprise et l'Intitulé du Poste en haut pour démarrer la simulation."
    },
    "start_mock_btn": {
        "en": "Start Mock Interview",
        "fr": "Démarrer l'Entretien Blanc"
    },
    "setting_up_room_spinner": {
        "en": "Setting up the interview room...",
        "fr": "Installation de la salle d'entretien..."
    },
    "mock_chat_placeholder": {
        "en": "Type your response here...",
        "fr": "Écrivez votre réponse ici..."
    },
    "evaluating_mock_spinner": {
        "en": "Evaluating response and generating feedback...",
        "fr": "Évaluation de la réponse et génération du retour..."
    },
    "reset_interview_btn": {
        "en": "Reset Interview",
        "fr": "Réinitialiser l'Entretien"
    },
    "behavioral_questions_title": {
        "en": "Behavioral Questions",
        "fr": "Questions Comportementales"
    },
    "behavioral_questions_desc": {
        "en": "These questions assess your soft skills and past behavior.",
        "fr": "Ces questions évaluent vos compétences douces (soft skills) et vos comportements passés."
    },
    "focus_area_label": {
        "en": "Focus area:",
        "fr": "Axe d'attention :"
    },
    "gen_behavioral_btn": {
        "en": "Generate Behavioral Questions",
        "fr": "Générer les Questions Comportementales"
    },
    "generating_questions_spinner": {
        "en": "Generating questions...",
        "fr": "Génération des questions..."
    },
    "star_method_caption": {
        "en": "Use the STAR method to structure your answer",
        "fr": "Utilisez la méthode STAR pour structurer votre réponse"
    },
    "technical_questions_title": {
        "en": "Technical Questions",
        "fr": "Questions Techniques"
    },
    "technical_questions_desc": {
        "en": "Prepare for technical questions based on the job's required skills.",
        "fr": "Préparez-vous aux questions techniques adaptées aux compétences requises du poste."
    },
    "no_tech_skills_detected": {
        "en": "No specific technical skills detected. Add a job description for targeted questions.",
        "fr": "Aucune compétence technique spécifique détectée. Ajoutez une description de poste pour cibler les questions."
    },
    "focus_skill_label": {
        "en": "Focus on skill:",
        "fr": "Se focaliser sur la compétence :"
    },
    "difficulty_level_label": {
        "en": "Difficulty level:",
        "fr": "Niveau de difficulté :"
    },
    "gen_technical_btn": {
        "en": "Generate Technical Questions",
        "fr": "Générer les Questions Techniques"
    },
    "generating_tech_spinner": {
        "en": "Generating technical questions...",
        "fr": "Génération des questions techniques..."
    },
    "elevator_pitch_title": {
        "en": "Elevator Pitch Generator",
        "fr": "Générateur d'Elevator Pitch"
    },
    "elevator_pitch_desc": {
        "en": "Craft a compelling personal pitch for networking and interviews.",
        "fr": "Rédigez un pitch de présentation percutant pour le réseautage et les entretiens."
    },
    "pitch_length_label": {
        "en": "Pitch length:",
        "fr": "Durée du pitch :"
    },
    "context_label": {
        "en": "Context:",
        "fr": "Contexte :"
    },
    "gen_pitch_btn": {
        "en": "Generate Pitch",
        "fr": "Générer le Pitch"
    },
    "generating_pitch_spinner": {
        "en": "Crafting your elevator pitch...",
        "fr": "Rédaction de votre pitch de présentation..."
    },
    "your_elevator_pitch_title": {
        "en": "#### Your Elevator Pitch:",
        "fr": "#### Votre Elevator Pitch :"
    },
    "download_pitch_btn": {
        "en": "Download Pitch",
        "fr": "Télécharger le Pitch"
    },
    "weakness_framing_title": {
        "en": "Weakness/Strength Framing",
        "fr": "Cadrage Faiblesse/Force"
    },
    "weakness_framing_desc": {
        "en": "Turn CV gaps into compelling growth narratives.",
        "fr": "Transformez les trous de votre CV en récits de croissance convaincants."
    },
    "potential_interview_concerns": {
        "en": "**Potential interview concerns (based on CV gaps):** {gaps}",
        "fr": "**Points d'attention potentiels en entretien (trous du CV) :** {gaps}"
    },
    "enter_weakness_label": {
        "en": "Enter a weakness or gap to frame positively:",
        "fr": "Entrez une faiblesse ou un trou à présenter positivement :"
    },
    "enter_weakness_placeholder": {
        "en": "e.g., No experience with Kubernetes, Career gap in 2023...",
        "fr": "ex: Pas d'expérience avec Kubernetes, Transition de carrière en 2023..."
    },
    "frame_it_btn": {
        "en": "Frame It Positively",
        "fr": "Présenter Positivement"
    },
    "crafting_response_spinner": {
        "en": "Crafting your response...",
        "fr": "Formulation de votre réponse..."
    },
    "positive_framing_title": {
        "en": "#### Positive Framing:",
        "fr": "#### Présentation Positive :"
    },
    
    # LinkedIn Optimizer Page
    "linkedin_optimizer_title": {
        "en": "LinkedIn Profile Optimizer",
        "fr": "Optimiseur de Profil LinkedIn"
    },
    "linkedin_optimizer_subtitle": {
        "en": "*Optimize your LinkedIn profile to complement your CV, align with your target role, and attract recruiters through LinkedIn search.*",
        "fr": "*Optimisez votre profil LinkedIn pour compléter votre CV, cibler le poste recherché et attirer les recruteurs.*"
    },
    "tab_headline_optimizer": {
        "en": "Headline Optimizer",
        "fr": "Optimiseur de Titre"
    },
    "tab_about_section": {
        "en": "About Section",
        "fr": "Section Résumé / À Propos"
    },
    "tab_experience_optimizer": {
        "en": "Experience Optimizer",
        "fr": "Optimiseur d'Expériences"
    },
    "tab_skills_featured": {
        "en": "Skills & Featured",
        "fr": "Compétences & Sélection"
    },
    "tab_consistency_check": {
        "en": "Consistency Check",
        "fr": "Vérification de Cohérence"
    },
    "linkedin_headline_optimizer": {
        "en": "LinkedIn Headline Optimizer",
        "fr": "Optimiseur de Titre LinkedIn"
    },
    "linkedin_headline_desc": {
        "en": "Your headline is the most critical part of your profile for SEO search. LinkedIn allows up to 220 characters. Focus on keywords, target specialty, and results, not just job titles.",
        "fr": "Votre titre est la partie la plus importante pour le référencement (SEO). LinkedIn autorise 220 caractères. Mettez l'accent sur les mots-clés, vos spécialités et vos résultats."
    },
    "current_job_title_label": {
        "en": "Current job title:",
        "fr": "Intitulé de poste actuel :"
    },
    "target_job_title_label": {
        "en": "Target job title:",
        "fr": "Intitulé de poste visé :"
    },
    "generate_headlines_btn": {
        "en": "Generate Headlines",
        "fr": "Générer les Titres"
    },
    "crafting_headlines_spinner": {
        "en": "Crafting headlines...",
        "fr": "Création des titres..."
    },
    "choose_favorite_title": {
        "en": "**Choose your favorite:**",
        "fr": "**Choisissez votre préféré :**"
    },
    "chars_label": {
        "en": "chars",
        "fr": "caractères"
    },
    
    # LinkedIn About
    "about_section_writer": {
        "en": "About Section Writer (Hadrien's Formula)",
        "fr": "Rédacteur de Résumé / À Propos (Formule d'Hadrien)"
    },
    "about_section_desc": {
        "en": "Hadrien's formula dictates a strict 3-paragraph layout: an attention-grabbing hook (no generic openings), a summary of your professional journey with 2-3 metric-driven achievements, and a clear call to action (CTA). No emojis.",
        "fr": "La formule d'Hadrien impose une structure stricte en 3 paragraphes : une accroche percutante (pas d'ouverture générique), un résumé de votre parcours avec 2 ou 3 réussites chiffrées, et un appel à l'action (CTA) clair. Pas d'émojis."
    },
    "generate_about_btn": {
        "en": "Generate About Section",
        "fr": "Générer le Résumé (À Propos)"
    },
    "writing_about_spinner": {
        "en": "Writing your About section...",
        "fr": "Rédaction du résumé en cours..."
    },
    "edit_about_label": {
        "en": "Edit your About section:",
        "fr": "Modifier votre résumé :"
    },
    "character_count_label": {
        "en": "Character count:",
        "fr": "Nombre de caractères :"
    },
    "download_about_btn": {
        "en": "Download About Section",
        "fr": "Télécharger le Résumé"
    },
    
    # LinkedIn Experience
    "experience_optimizer_title_li": {
        "en": "Experience Section Optimizer",
        "fr": "Optimiseur de la Section Expérience"
    },
    "experience_optimizer_desc_li": {
        "en": "Rewrite your experience section to be conversational, results-driven (Google XYZ), and add a 'What I learned' takeaway line at the end of each position.",
        "fr": "Réécrivez vos expériences pour qu'elles soient axées sur les résultats (formule Google XYZ), avec une phrase clé 'Ce que j'ai appris' à la fin de chaque poste."
    },
    "no_parsed_experience_info": {
        "en": "No parsed experience section was auto-detected from your CV. You can paste it below.",
        "fr": "Aucune section d'expérience n'a été extraite automatiquement de votre CV. Vous pouvez la coller ci-dessous."
    },
    "current_experience_label": {
        "en": "Current Experience Section:",
        "fr": "Section Expérience Actuelle :"
    },
    "optimize_experience_btn": {
        "en": "Optimize Experience for LinkedIn",
        "fr": "Optimiser l'Expérience pour LinkedIn"
    },
    "optimizing_experiences_spinner": {
        "en": "Optimizing experiences...",
        "fr": "Optimisation des expériences..."
    },
    "optimized_experience_title_li": {
        "en": "Optimized Experience Section:",
        "fr": "Section Expérience Optimisée :"
    },
    "edit_optimized_experience_label": {
        "en": "Edit optimized experience:",
        "fr": "Modifier l'expérience optimisée :"
    },
    "download_experiences_btn": {
        "en": "Download Experiences",
        "fr": "Télécharger les Expériences"
    },
    
    # LinkedIn Skills & Featured
    "skills_featured_title": {
        "en": "Skills & Featured Section Recommender",
        "fr": "Recommandations de Compétences & Sélection"
    },
    "skills_featured_desc": {
        "en": "Optimize your pinned skills based on recruiter search priorities, and get high-impact recommendations for your LinkedIn 'Featured' section.",
        "fr": "Optimisez vos compétences épinglées en fonction des recherches des recruteurs, et obtenez des recommandations pour votre section 'Sélection'."
    },
    "generate_recommendations_btn": {
        "en": "Generate Recommendations",
        "fr": "Générer les Recommandations"
    },
    "generating_recommendations_spinner": {
        "en": "Generating recommendations...",
        "fr": "Génération des recommandations..."
    },
    
    # LinkedIn Consistency Check
    "consistency_check_title": {
        "en": "CV-LinkedIn Consistency Check",
        "fr": "Cohérence CV-LinkedIn"
    },
    "consistency_check_desc": {
        "en": "Paste your current LinkedIn About section or job details to check for inconsistencies with your CV.",
        "fr": "Collez votre résumé LinkedIn actuel ou vos postes pour identifier des incohérences avec votre CV."
    },
    "paste_linkedin_label": {
        "en": "Paste your current LinkedIn Profile text:",
        "fr": "Collez le texte actuel de votre profil LinkedIn :"
    },
    "check_consistency_btn": {
        "en": "Check Consistency",
        "fr": "Vérifier la Cohérence"
    },
    "checking_consistency_spinner": {
        "en": "Checking consistency...",
        "fr": "Vérification en cours..."
    },
    "linkedin_consistency_success": {
        "en": "Great! Your CV and LinkedIn are consistent.",
        "fr": "Parfait ! Votre CV et votre profil LinkedIn sont bien cohérents."
    },
    "linkedin_inconsistencies_found": {
        "en": "Found {count} potential inconsistency/inconsistencies:",
        "fr": "{count} incohérence(s) potentielle(s) détectée(s) :"
    },
    "inconsistency_title": {
        "en": "Job title \"{title}\" appears in CV but not on LinkedIn",
        "fr": "Le titre de poste \"{title}\" apparaît dans le CV mais pas sur LinkedIn"
    },
    "inconsistency_company": {
        "en": "Company \"{company}\" mentioned in CV but not found on LinkedIn",
        "fr": "L'entreprise \"{company}\" est mentionnée dans le CV mais pas sur LinkedIn"
    },
    "inconsistency_degree": {
        "en": "Degree \"{degree}\" in CV but not mentioned on LinkedIn",
        "fr": "Le diplôme \"{degree}\" est dans le CV mais pas sur LinkedIn"
    },
    "inconsistency_years": {
        "en": "Years {years} appear in CV but not on LinkedIn",
        "fr": "Les années {years} apparaissent dans le CV mais pas sur LinkedIn"
    },
    
    # Export Page
    "export_title": {
        "en": "Export Your Enhanced CV",
        "fr": "Exporter votre CV Optimisé"
    },
    "export_subtitle": {
        "en": "*Download your ATS-optimized CV in professional templates. All templates are tested for ATS compatibility.*",
        "fr": "*Téléchargez votre CV optimisé pour les robots ATS dans un modèle professionnel testé et validé.*"
    },
    "choose_template_title": {
        "en": "### Choose Your Template",
        "fr": "### Choisissez votre Modèle"
    },
    "customization_title": {
        "en": "### Customization",
        "fr": "### Personnalisation"
    },
    "font_size_label": {
        "en": "Font Size",
        "fr": "Taille de Police"
    },
    "accent_color_label": {
        "en": "Accent Color",
        "fr": "Couleur d'Accentuation"
    },
    "sections_to_include_label": {
        "en": "Sections to include:",
        "fr": "Sections à inclure :"
    },
    "contact_info_title": {
        "en": "### Contact Information",
        "fr": "### Coordonnées & Contact"
    },
    "contact_info_desc": {
        "en": "Edit your contact details for the CV header:",
        "fr": "Modifiez vos informations pour l'en-tête du CV :"
    },
    "full_name_label": {
        "en": "Full Name",
        "fr": "Nom Complet"
    },
    "email_label": {
        "en": "Email",
        "fr": "E-mail"
    },
    "phone_label": {
        "en": "Phone",
        "fr": "Téléphone"
    },
    "location_label": {
        "en": "Location",
        "fr": "Ville / Localisation"
    },
    "linkedin_url_label": {
        "en": "LinkedIn URL",
        "fr": "URL de profil LinkedIn"
    },
    "website_label": {
        "en": "Website/Portfolio",
        "fr": "Site Web / Portfolio"
    },
    "download_title": {
        "en": "### Download",
        "fr": "### Téléchargement"
    },
    "including_enhanced_success": {
        "en": "Including {count} enhanced section(s) from the Rewriter.",
        "fr": "Intégration de {count} section(s) optimisée(s) depuis l'outil de réécriture."
    },
    "rewriter_tip_info": {
        "en": "Tip: Use the **CV Rewriter** page first to enhance your sections before exporting.",
        "fr": "Conseil : Utilisez d'abord l'onglet **CV Rewriter** pour réécrire vos rubriques avant d'exporter."
    },
    "generate_docx_btn": {
        "en": "Generate DOCX",
        "fr": "Générer le DOCX"
    },
    "generating_docx_spinner": {
        "en": "Generating DOCX...",
        "fr": "Génération du DOCX en cours..."
    },
    "docx_generated_success": {
        "en": "DOCX generated!",
        "fr": "Fichier DOCX généré !"
    },
    "generate_pdf_btn": {
        "en": "Generate PDF",
        "fr": "Générer le PDF"
    },
    "generating_pdf_spinner": {
        "en": "Generating PDF...",
        "fr": "Génération du PDF en cours..."
    },
    "pdf_generated_success": {
        "en": "PDF generated!",
        "fr": "Fichier PDF généré !"
    },
    "pdf_fpdf_warning": {
        "en": "PDF generation requires `fpdf2`. Install with: `pip install fpdf2`",
        "fr": "La génération PDF nécessite `fpdf2`. Installez-le avec : `pip install fpdf2`"
    },
    "ats_safety_title": {
        "en": "**ATS Safety**",
        "fr": "**Sécurité ATS**"
    },
    "ats_safe_templates": {
        "en": "ATS-Safe Templates",
        "fr": "Modèles ATS-Safe"
    },
    "ats_safe_desc": {
        "en": "No tables, no graphics, no text boxes",
        "fr": "Pas de tableaux, pas de graphiques, pas de zones de texte"
    },
    "download_docx_btn": {
        "en": "Download DOCX",
        "fr": "Télécharger le DOCX"
    },
    "download_pdf_btn": {
        "en": "Download PDF",
        "fr": "Télécharger le PDF"
    },
    "detected_sections_title": {
        "en": "**Detected Sections:**",
        "fr": "**Sections Détectées :**"
    },
    "total_sections_metric": {
        "en": "Total Sections",
        "fr": "Sections Totales"
    },
    "enhanced_sections_metric": {
        "en": "Enhanced Sections",
        "fr": "Sections Optimisées"
    },
    
    # Negotiation and Follow-ups
    "neg_follow_title": {
        "en": "Negotiation & Follow-up Engine",
        "fr": "Moteur de Négociation & Relances"
    },
    "neg_follow_subtitle": {
        "en": "*Maximize your landing success. Dianelle writes market-backed salary negotiation scripts and writes high-impact follow-up emails for every stage of the process.*",
        "fr": "*Maximisez vos chances de succès. Dianelle rédige des scripts de négociation salariale basés sur le marché et des e-mails de relance percutants pour chaque étape du processus.*"
    },
    "tab_salary_negotiation": {
        "en": "Salary Negotiation Script",
        "fr": "Script de Négociation Salariale"
    },
    "tab_followup_emails": {
        "en": "Follow-up Email Templates",
        "fr": "Modèles d'E-mails de Relance"
    },
    "salary_neg_title": {
        "en": "Salary Negotiation Strategy (Hadrien's Formula)",
        "fr": "Stratégie de Négociation Salariale (Formule d'Hadrien)"
    },
    "salary_neg_desc": {
        "en": "Almost all job offers have negotiation room. Recruiters expect you to negotiate. Enter details of the offer you received below to generate custom negotiation scripts.",
        "fr": "Presque toutes les offres d'emploi disposent d'une marge de négociation. Les recruteurs s'attendent à ce que vous négociiez. Saisissez les détails de l'offre ci-dessous pour générer vos scripts de négociation personnalisés."
    },
    "base_salary_label": {
        "en": "Base Salary Offered:",
        "fr": "Salaire de Base Offert :"
    },
    "bonus_label": {
        "en": "Annual Bonus Structure (optional):",
        "fr": "Structure de Bonus Annuel (optionnel) :"
    },
    "equity_label": {
        "en": "Equity / RSU / Options (optional):",
        "fr": "Equity / Actions / Options (optionnel) :"
    },
    "benefits_label": {
        "en": "Other Benefits (optional):",
        "fr": "Autres Avantages (optionnel) :"
    },
    "gen_negotiation_btn": {
        "en": "Generate Negotiation Pack",
        "fr": "Générer le Kit de Négociation"
    },
    "fill_role_company_warning": {
        "en": "Please fill in Job Title and Company Name.",
        "fr": "Veuillez saisir l'Intitulé du Poste et le Nom de l'Entreprise."
    },
    "analyzing_offer_spinner": {
        "en": "Analyzing offer and drafting scripts...",
        "fr": "Analyse de l'offre et rédaction des scripts..."
    },
    "custom_neg_plan_title": {
        "en": "### Your Custom Negotiation Plan",
        "fr": "### Votre Plan de Négociation Personnalisé"
    },
    "neg_pack_details_label": {
        "en": "Negotiation Pack Details:",
        "fr": "Détails du kit de négociation :"
    },
    "download_neg_script_btn": {
        "en": "Download Negotiation Script",
        "fr": "Télécharger le Script de Négociation"
    },
    "followup_emails_title": {
        "en": "Follow-up Email Templates",
        "fr": "Modèles d'E-mails de Relance"
    },
    "followup_emails_desc": {
        "en": "Relancing keeps you top of mind. Generating 3 templates: post-application (3 days, <60 words), thank-you email (24h, <100 words), and check-in relance (7 days, <80 words). No emojis.",
        "fr": "La relance vous maintient dans l'esprit du recruteur. Génère 3 modèles : après candidature (3 jours, <60 mots), e-mail de remerciement (24h, <100 mots), et e-mail de relance/suivi (7 jours, <80 mots). Pas d'émojis."
    },
    "interviewer_name_label": {
        "en": "Interviewer Name (optional):",
        "fr": "Nom du Recruteur / Interlocuteur (optionnel) :"
    },
    "gen_followup_btn": {
        "en": "Generate Follow-up Emails",
        "fr": "Générer les E-mails de Relance"
    },
    "drafting_followup_spinner": {
        "en": "Drafting follow-ups...",
        "fr": "Rédaction des relances en cours..."
    },
    "gen_email_templates_title": {
        "en": "### Generated Email Templates",
        "fr": "### Modèles d'E-mails Générés"
    },
    "email_templates_details_label": {
        "en": "Email Templates Details:",
        "fr": "Détails des modèles d'e-mails :"
    },
    "download_emails_btn": {
        "en": "Download Emails",
        "fr": "Télécharger les E-mails"
    },
    
    # Chat Page
    "chat_title": {
        "en": "Chat with Dianelle — Your AI Career Assistant",
        "fr": "Chattez avec Dianelle — Votre Assistante de Carrière IA"
    },
    "please_upload_analyze_first": {
        "en": "Please upload and analyze your CV first to get personalized advice.",
        "fr": "Veuillez d'abord charger et analyser votre CV pour obtenir des conseils personnalisés."
    },
    "chat_input_placeholder": {
        "en": "Ask Dianelle anything about your CV or career...",
        "fr": "Posez toutes vos questions sur votre CV ou carrière à Dianelle..."
    },
    "thinking_spinner": {
        "en": "Thinking...",
        "fr": "Réflexion en cours..."
    },
    "chat_error": {
        "en": "Sorry, I encountered an error: {error}",
        "fr": "Désolée, j'ai rencontré une erreur : {error}"
    },
    
    # Settings Page
    "ai_model_settings": {
        "en": "AI Model Settings",
        "fr": "Paramètres du Modèle IA"
    },
    "choose_ai_model": {
        "en": "Choose AI Model:",
        "fr": "Choisir le Modèle IA :"
    },
    "response_creativity": {
        "en": "Response Creativity",
        "fr": "Créativité des Réponses"
    },
    "creativity_help": {
        "en": "Higher values make responses more creative but less focused",
        "fr": "Des valeurs plus élevées rendent les réponses plus créatives mais moins ciblées"
    },
    "interface_settings": {
        "en": "Interface Settings",
        "fr": "Paramètres d'Interface"
    },
    "theme_info": {
        "en": "The interface automatically adapts to your Streamlit theme settings.",
        "fr": "L'interface s'adapte automatiquement aux thèmes de votre navigateur."
    },
    "show_advanced": {
        "en": "Show Advanced Features",
        "fr": "Afficher les Fonctionnalités Avancées"
    },
    "advanced_help": {
        "en": "Enable advanced CV analysis features",
        "fr": "Activer les fonctions avancées d'analyse de CV"
    },
    "data_management": {
        "en": "Data Management",
        "fr": "Gestion des Données"
    },
    "export_analysis_btn": {
        "en": "Export Analysis",
        "fr": "Exporter l'Analyse"
    },
    "download_json_btn": {
        "en": "Download JSON",
        "fr": "Télécharger le JSON"
    },
    "no_analysis_export": {
        "en": "No analysis to export yet.",
        "fr": "Aucune analyse à exporter pour le moment."
    },
    "clear_session_btn": {
        "en": "Clear Session",
        "fr": "Effacer la Session"
    },
    "session_cleared": {
        "en": "Session cleared!",
        "fr": "Session effacée !"
    },
    "help_support_btn": {
        "en": "Help & Support",
        "fr": "Aide & Support"
    },
    "contact_support_desc": {
        "en": "Contact support: nguefackuriel@gmail.com",
        "fr": "Contacter le support : nguefackuriel@gmail.com"
    },
    
    # Fit Levels
    "fit_level_excellent_fit": {
        "en": "Excellent Fit",
        "fr": "Adéquation Excellente"
    },
    "fit_level_strong_fit": {
        "en": "Strong Fit",
        "fr": "Adéquation Forte"
    },
    "fit_level_moderate_fit": {
        "en": "Moderate Fit",
        "fr": "Adéquation Modérée"
    },
    "fit_level_partial_fit": {
        "en": "Partial Fit",
        "fr": "Adéquation Partielle"
    },
    "fit_level_low_fit": {
        "en": "Low Fit",
        "fr": "Adéquation Faible"
    },
    
    # General / Buttons
    "next_step_rewriter": {
        "en": "**Next step:** Go to **CV Rewriter** to automatically enhance your CV sections.",
        "fr": "**Étape suivante :** Allez dans **CV Rewriter** pour réécrire et optimiser vos rubriques."
    },
    "error_processing_cv": {
        "en": "Error processing CV: {error}",
        "fr": "Erreur lors du traitement du CV : {error}"
    },
    "please_upload_first": {
        "en": "Please upload your CV first on the **CV Analysis** page.",
        "fr": "Veuillez d'abord importer votre CV dans l'onglet **Analyse de CV**."
    },
    "please_add_jd_first": {
        "en": "Please add a job description on the **CV Analysis** page first.",
        "fr": "Veuillez d'abord ajouter une offre d'emploi dans l'onglet **Analyse de CV**."
    }
}

def t(key: str, **kwargs) -> str:
    """
    Get translated string for key in active language.
    Defaults to English if key or language translation is not found.
    """
    # Default to French for Kinshasa workshop, otherwise use st.session_state['language']
    lang_full = st.session_state.get('language', 'Français')
    lang = 'fr' if lang_full == 'Français' else 'en'
    
    entry = TRANSLATIONS.get(key)
    if not entry:
        return key
    
    val = entry.get(lang, entry.get('en', key))
    if kwargs:
        return val.format(**kwargs)
    return val
