import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import json
import re
from groq import Groq
from app.auth.auth import Authentication
from app.api.routes import API
from app.services.llm_service import LLMService
from app.config import Config
import os
from dotenv import load_dotenv

load_dotenv()

auth = Authentication()
api = API()
llm = LLMService()

# Get API key from environment variable only - NEVER hardcode
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not found! Please check your .env file.")
    st.info("Make sure you have a .env file in the project root with: GROQ_API_KEY=your_api_key_here")
    st.stop()

st.set_page_config(
    page_title=Config.APP_NAME,
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

def safe_json_parse(content: str):
    """Safely parse JSON even with control characters"""
    try:
        # Remove markdown code blocks if present
        content = re.sub(r'```json\s*', '', content)
        content = re.sub(r'```\s*', '', content)
        
        # Remove invalid control characters (ASCII 0-31 except tab, newline, carriage return)
        content = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', content)
        
        # Clean up any remaining issues
        content = content.strip()
        
        return json.loads(content)
    except json.JSONDecodeError as e:
        # If still failing, try to extract JSON using regex
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass
        raise e

def apply_background():
    """Apply background image and custom styling"""
    st.markdown("""
        <style>
        /* Main app background - full screen */
        .stApp {
            background-image: url("https://i.pinimg.com/1200x/ef/3a/9a/ef3a9a53d8523aba97ed1777e4215029.jpg") !important;
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
                
        }
        
        /* Remove white overlay */
        .stApp::before, .stApp::after {
            display: none !important;
        }
        
        /* Add dark overlay to main content area for readability */
        .stAppViewContainer {
            background-color: rgba(0, 0, 0, 0.3) !important;
        }
        
        /* Header transparent */
        header[data-testid="stHeader"] {
            background-color: transparent !important;
            background: transparent !important;
            box-shadow: none !important;
        }
        
        header[data-testid="stHeader"] > div {
            background-color: transparent !important;
        }
        
        .stApp header {
            background-color: transparent !important;
        }
        
        .st-emotion-cache-12fmjuu {
            background-color: transparent !important;
        }
        
        [class*="header"] {
            background-color: transparent !important;
        }
        
        /* Sidebar - dark semi-transparent */
        [data-testid="stSidebar"] {
            background-color: rgba(0, 0, 0, 0.7) !important;
            backdrop-filter: blur(8px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.2) !important;
        }
        
        /* SIDEBAR TEXT - WHITE ONLY */
        [data-testid="stSidebar"] * {
            color: white !important;
        }
        
        /* MAIN CONTENT TEXT - BLACK/DARK */
        .main * {
            color: #1a1a1a !important;
        }
        
        /* Headers in main content */
        .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
            color: #0a0a0a !important;
        }
        
        /* Paragraphs in main content */
        .main p, .main span, .main div, .stMarkdown p {
            color: #2a2a2a !important;
        }
        
        /* Code blocks */
        .stCodeBlock, .stCodeBlock * {
            background-color: rgba(0, 0, 0, 0.8) !important;
            color: #e0e0e0 !important;
        }
        
        /* ============ UPDATED BUTTON STYLES ============ */
        
        /* Primary buttons (main action buttons) */
        .stButton button[kind="primary"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            font-weight: 600 !important;
            font-size: 16px !important;
            padding: 0.6rem 1.2rem !important;
            border-radius: 10px !important;
            border: none !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
        }
        
        .stButton button[kind="primary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15) !important;
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
        }
        
        /* Regular buttons */
        .stButton button {
            background-color: #4CAF50 !important;
            color: white !important;
            font-weight: 500 !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 0.5rem 1rem !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton button:hover {
            background-color: #45a049 !important;
            transform: scale(1.02) !important;
        }
        
        /* Submit buttons in forms */
        .stForm button[type="submit"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            font-size: 18px !important;
            font-weight: bold !important;
            padding: 0.75rem !important;
            border-radius: 10px !important;
        }
        
        /* Download buttons */
        .stDownloadButton button {
            background-color: #FF9800 !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
        }
        
        .stDownloadButton button:hover {
            background-color: #f57c00 !important;
            transform: scale(1.02) !important;
        }
        
        /* Sidebar buttons */
        [data-testid="stSidebar"] .stButton button {
            background-color: rgba(255, 255, 255, 0.2) !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
        }
        
        [data-testid="stSidebar"] .stButton button:hover {
            background-color: rgba(255, 255, 255, 0.3) !important;
            transform: scale(1.02) !important;
        }
        
        /* Danger/Delete buttons */
        .stButton button[data-testid="baseButton-destructive"] {
            background-color: #dc3545 !important;
            color: white !important;
        }
        
        .stButton button[data-testid="baseButton-destructive"]:hover {
            background-color: #c82333 !important;
        }
        
        /* ============ END BUTTON STYLES ============ */
        
        /* Info boxes - light background with dark text */
        .stAlert, .stInfo, .stSuccess, .stWarning, .stError {
            background-color: rgba(255, 255, 255, 0.95) !important;
            color: #1a1a1a !important;
        }
        
        .stAlert *, .stInfo *, .stSuccess *, .stWarning *, .stError * {
            color: #1a1a1a !important;
        }
        
        /* Input fields */
        .stTextInput input, .stTextArea textarea {
            background-color: rgba(255, 255, 255, 0.95) !important;
            color: #1a1a1a !important;
            border: 1px solid rgba(0, 0, 0, 0.2) !important;
        }
        
        .stTextInput label, .stTextArea label {
            color: #1a1a1a !important;
        }
        
        /* Select boxes */
        .stSelectbox div[data-baseweb="select"] {
            background-color: rgba(255, 255, 255, 0.95) !important;
            color: #1a1a1a !important;
        }
        
        /* Radio buttons in main content */
        .stRadio label {
            color: #1a1a1a !important;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
            justify-content: center;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0.5rem 2rem;
            font-size: 1rem;
            color: #1a1a1a !important;
            background-color: rgba(255, 255, 255, 0.8) !important;
        }
        
        /* Metric cards */
        [data-testid="stMetric"] label, [data-testid="stMetric"] div {
            color: #1a1a1a !important;
        }
        
        /* Expander headers */
        [data-testid="stExpander"] summary p {
            color: #1a1a1a !important;
        }
        
        /* Links */
        a {
            color: #0066cc !important;
        }
        
        /* Better spacing for content containers */
        .stMarkdown {
            margin-bottom: 1rem;
        }
        
        /* Improved radio button alignment */
        .stRadio [role="radiogroup"] {
            display: flex;
            flex-direction: row;
            gap: 2rem;
            flex-wrap: wrap;
        }
        
        /* Consistent card styling */
        .stAlert, .stInfo, .stSuccess {
            border-radius: 10px;
            padding: 1rem;
        }
        
        /* Better expander styling */
        .streamlit-expanderHeader {
            font-weight: 600;
        }
        
        /* Level button styling */
        .level-button {
            padding: 0.5rem 1rem;
            border-radius: 5px;
            text-align: center;
            cursor: pointer;
        }
        </style>
    """, unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'role' not in st.session_state:
        st.session_state.role = None
    if 'page' not in st.session_state:
        st.session_state.page = "login"
    if 'show_register' not in st.session_state:
        st.session_state.show_register = False
    if 'registration_success' not in st.session_state:
        st.session_state.registration_success = False
    if 'current_test' not in st.session_state:
        st.session_state.current_test = None
    if 'quiz_history' not in st.session_state:
        st.session_state.quiz_history = []
    if 'selected_quiz' not in st.session_state:
        st.session_state.selected_quiz = None
    if 'show_quiz' not in st.session_state:
        st.session_state.show_quiz = False
    if 'quiz_active' not in st.session_state:
        st.session_state.quiz_active = False
    if 'active_quiz' not in st.session_state:
        st.session_state.active_quiz = None
    if 'quiz_answers_store' not in st.session_state:
        st.session_state.quiz_answers_store = {}
    if 'test_answers_store' not in st.session_state:
        st.session_state.test_answers_store = {}
    if 'ai_content_generated' not in st.session_state:
        st.session_state.ai_content_generated = False
    if 'ai_quiz_generated' not in st.session_state:
        st.session_state.ai_quiz_generated = False
    if 'ai_mindmap_generated' not in st.session_state:
        st.session_state.ai_mindmap_generated = False

class AILearningSystem:
    """AI-powered learning system using Groq API"""
    
    def __init__(self, api_key: str):
        """Initialize with API key"""
        if not api_key:
            raise ValueError("API key is required")
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
    
    def generate_content_by_level(self, topic: str, level: str) -> dict:
        """Generate detailed content about a topic based on difficulty level"""
        
        level_descriptions = {
            "Beginner": "basic introduction, simple explanations, no prior knowledge assumed",
            "Intermediate": "moderate depth, assumes basic knowledge, includes practical examples",
            "Advanced": "deep technical details, advanced concepts, real-world applications and best practices"
        }
        
        with st.spinner(f"📚 Generating {level} level content about '{topic}'..."):
            prompt = f"""You are an expert educator. Create comprehensive {level} level educational content about "{topic}".

Level Description: {level_descriptions[level]}

Format your response as JSON with EXACTLY this structure:
{{
    "definition": "A clear, 2-3 sentence definition appropriate for {level} level",
    "detailed_overview": "A detailed 4-5 paragraph explanation with {level} level depth and examples",
    "key_concepts": [
        "Key concept 1 with detailed explanation",
        "Key concept 2 with detailed explanation",
        "Key concept 3 with detailed explanation",
        "Key concept 4 with detailed explanation",
        "Key concept 5 with detailed explanation"
    ],
    "practical_examples": [
        "Practical example 1 relevant to {level} level",
        "Practical example 2 relevant to {level} level",
        "Practical example 3 relevant to {level} level"
    ],
    "summary": "A concise 2-3 sentence summary highlighting key takeaways for {level} learners"
}}

Make the content educational, engaging, and appropriate for {level} level learners. Provide approximately 600-1000 words total.
IMPORTANT: Return ONLY valid JSON. No markdown, no extra text, no control characters."""

            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert educator. Always respond with valid JSON only. Do not include any control characters, markdown formatting, or extra text."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=4096
                )
                
                content = response.choices[0].message.content
                # Use safe parsing
                result = safe_json_parse(content)
                return result
                
            except Exception as e:
                st.error(f"Error generating content: {str(e)}")
                return self._fallback_content_by_level(topic, level)
    
    def generate_quiz_by_level(self, topic: str, num_questions: int = 10, level: str = "Intermediate") -> dict:
        """Generate quiz questions about a topic based on difficulty level"""
        
        with st.spinner(f"📝 Generating {num_questions} {level} level quiz questions about '{topic}'..."):
            prompt = f"""Create a {level} level quiz about "{topic}" with exactly {num_questions} questions.

Format your response as JSON with EXACTLY this structure:
{{
    "topic": "{topic}",
    "level": "{level}",
    "questions": [
        {{
            "question": "Question text here appropriate for {level} level",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0,
            "explanation": "Detailed {level} level explanation of why this answer is correct"
        }}
    ]
}}

Requirements:
- Questions must test understanding appropriate for {level} level
- Each question must have exactly 4 options
- "correct" must be the index (0-3) of the correct answer
- Provide clear educational explanations at {level} level

IMPORTANT: Return ONLY valid JSON. No markdown, no extra text, no control characters."""

            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert quiz creator. Always respond with valid JSON only. Do not include any control characters, markdown formatting, or extra text."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.8,
                    max_tokens=4096
                )
                
                content = response.choices[0].message.content
                # Use safe parsing
                result = safe_json_parse(content)
                
                if len(result.get('questions', [])) != num_questions:
                    st.warning(f"Generated {len(result['questions'])} questions (requested {num_questions})")
                
                return result
                
            except Exception as e:
                st.error(f"Error generating quiz: {str(e)}")
                return self._fallback_quiz_by_level(topic, num_questions, level)
    
    def generate_mindmap_by_level(self, topic: str, level: str = "Intermediate") -> dict:
        """Generate a mindmap/learning roadmap based on difficulty level"""
        
        with st.spinner(f"🧠 Creating {level} level learning roadmap for '{topic}'..."):
            prompt = f"""Create a {level} level learning roadmap/mindmap for mastering "{topic}".

Format your response as JSON with EXACTLY this structure:
{{
    "topic": "{topic}",
    "level": "{level}",
    "central_concept": "The main concept of {topic} in one sentence for {level} learners",
    "main_branches": [
        {{
            "name": "Branch name 1",
            "subtopics": ["Subtopic 1", "Subtopic 2", "Subtopic 3", "Subtopic 4"]
        }},
        {{
            "name": "Branch name 2",
            "subtopics": ["Subtopic 1", "Subtopic 2", "Subtopic 3", "Subtopic 4"]
        }}
    ],
    "learning_path": ["Step 1", "Step 2", "Step 3", "Step 4", "Step 5", "Step 6"]
}}

Create 4-6 main branches with 4-6 subtopics each appropriate for {level} level.
IMPORTANT: Return ONLY valid JSON. No markdown, no extra text, no control characters."""

            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert curriculum designer. Always respond with valid JSON only. Do not include any control characters, markdown formatting, or extra text."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=4096
                )
                
                content = response.choices[0].message.content
                # Use safe parsing
                result = safe_json_parse(content)
                return result
                
            except Exception as e:
                st.error(f"Error generating mindmap: {str(e)}")
                return self._fallback_mindmap_by_level(topic, level)
    
    def _fallback_content_by_level(self, topic: str, level: str) -> dict:
        """Fallback content if API fails"""
        return {
            "definition": f"{topic} is an important subject that encompasses key concepts and principles in modern education and technology at {level} level.",
            "detailed_overview": f"{topic} represents a fundamental area of study with numerous real-world applications. Understanding {topic} requires systematic learning and practical implementation. The field continues to evolve with new developments and innovations, making it an exciting area for {level} learners.",
            "key_concepts": [
                f"Concept 1: {topic} requires consistent practice and dedication at {level} level",
                f"Concept 2: Understanding fundamentals is crucial for mastering {topic} at {level} level",
                f"Concept 3: Real-world applications help reinforce {level} level learning",
                f"Concept 4: Regular assessment helps track {level} level progress",
                f"Concept 5: Collaborative learning can accelerate {level} level understanding"
            ],
            "practical_examples": [
                f"Example 1: Practical application of {topic} for {level} learners",
                f"Example 2: Real-world scenario demonstrating {topic} at {level} level",
                f"Example 3: Case study relevant to {level} level understanding"
            ],
            "summary": f"{topic} is a valuable subject that builds foundational skills applicable across multiple domains at {level} level."
        }
    
    def _fallback_quiz_by_level(self, topic: str, num_questions: int, level: str) -> dict:
        """Fallback quiz if API fails"""
        questions = []
        for i in range(min(num_questions, 5)):
            questions.append({
                "question": f"What is an important {level} level concept in {topic}?",
                "options": [
                    f"{level} concept A in {topic}",
                    f"{level} concept B in {topic}",
                    f"{level} concept C in {topic}",
                    f"{level} concept D in {topic}"
                ],
                "correct": 0,
                "explanation": f"This is a fundamental {level} level concept in {topic} that helps build understanding."
            })
        
        return {
            "topic": topic,
            "level": level,
            "questions": questions
        }
    
    def _fallback_mindmap_by_level(self, topic: str, level: str) -> dict:
        """Fallback mindmap if API fails"""
        return {
            "topic": topic,
            "level": level,
            "central_concept": f"Understanding {topic} at {level} level from basics to advanced",
            "main_branches": [
                {"name": f"Fundamentals ({level})", "subtopics": ["Basic Concepts", "Core Principles", "Key Terminology", "Essential Knowledge"]},
                {"name": f"Core Topics ({level})", "subtopics": ["Main Concepts", "Important Theories", "Practical Applications", "Case Studies"]},
                {"name": f"Advanced Concepts ({level})", "subtopics": ["Complex Topics", "Specialized Areas", "Research Directions", "Industry Trends"]},
                {"name": f"Practice & Assessment ({level})", "subtopics": ["Exercises", "Projects", "Quizzes", "Real-world Problems"]}
            ],
            "learning_path": ["Learn fundamentals at " + level + " level", "Practice core concepts", "Explore advanced topics", "Apply knowledge", "Review and assess"]
        }

def display_ai_content_by_level(content: dict, topic: str, level: str):
    """Display generated content in a nice format with level-based organization"""
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 0.5rem; border-radius: 10px; margin-bottom: 1rem;">
        <h4 style="color: white; text-align: center;">📚 {level} Level Content</h4>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📖 Definition", expanded=True):
        st.info(content.get('definition', 'Definition not available'))
    
    with st.expander("📚 Detailed Overview", expanded=True):
        st.write(content.get('detailed_overview', 'Overview not available'))
    
    with st.expander("🔑 Key Concepts", expanded=True):
        key_concepts = content.get('key_concepts', [])
        if key_concepts:
            cols = st.columns(2)
            for idx, concept in enumerate(key_concepts):
                with cols[idx % 2]:
                    st.markdown(f"**{idx + 1}.** {concept}")
    
    with st.expander("💡 Practical Examples", expanded=True):
        practical_examples = content.get('practical_examples', [])
        for idx, example in enumerate(practical_examples, 1):
            st.markdown(f"**Example {idx}:** {example}")
            st.markdown("---")
    
    with st.expander("📌 Summary", expanded=True):
        st.success(content.get('summary', 'Summary not available'))

def display_ai_quiz_by_level(quiz: dict, topic: str, level: str):
    """Display and evaluate AI-generated quiz by level"""
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 0.5rem; border-radius: 10px; margin-bottom: 1rem;">
        <h4 style="color: white; text-align: center;">📝 {level} Level Quiz: {quiz.get('topic', topic)}</h4>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"**Total Questions:** {len(quiz.get('questions', []))}")
    st.markdown("---")
    
    questions = quiz.get('questions', [])
    answers = {}
    
    # Use a consistent key without timestamp for radio persistence
    quiz_key = f"ai_quiz_{topic}_{level}_{hash(topic + level)}"
    
    # Store answers for this quiz instance
    if quiz_key not in st.session_state:
        st.session_state[quiz_key] = {}
    
    # Create a form to handle all questions together
    with st.form(key=f"quiz_form_{quiz_key}"):
        for i, q in enumerate(questions):
            with st.container():
                st.markdown(f"**Question {i+1}:** {q.get('question', 'Question not available')}")
                
                options = q.get('options', ['A', 'B', 'C', 'D'])
                
                # Get current answer from session state
                current_answer = st.session_state[quiz_key].get(i)
                
                # Use radio with consistent key
                answer = st.radio(
                    f"Select answer for Q{i+1}",
                    options,
                    key=f"{quiz_key}_q_{i}",
                    index=None,
                    horizontal=True,
                    label_visibility="collapsed"
                )
                
                # Store answer temporarily
                if answer is not None:
                    answers[i] = {
                        'selected': answer,
                        'selected_index': options.index(answer),
                        'correct_index': q.get('correct', 0),
                        'correct_answer': options[q.get('correct', 0)],
                        'explanation': q.get('explanation', 'No explanation')
                    }
                elif current_answer is not None and current_answer in range(len(options)):
                    # If there was a previously stored answer, use it
                    answers[i] = {
                        'selected': options[current_answer],
                        'selected_index': current_answer,
                        'correct_index': q.get('correct', 0),
                        'correct_answer': options[q.get('correct', 0)],
                        'explanation': q.get('explanation', 'No explanation')
                    }

                st.markdown("---")
        
        submitted = st.form_submit_button("✅ Submit Quiz", type="primary", use_container_width=True)
        
        if submitted:
            # Store answers in session state
            for i, ans in answers.items():
                st.session_state[quiz_key][i] = ans['selected_index']
            
            if len(answers) == len(questions):
                score = 0
                results = []
                
                for i, q in enumerate(questions):
                    if i in answers:
                        user_answer = answers[i]['selected']
                        correct_answer = answers[i]['correct_answer']
                        is_correct = (answers[i]['selected_index'] == answers[i]['correct_index'])
                        
                        if is_correct:
                            score += 1
                        
                        results.append({
                            'question': q.get('question'),
                            'user_answer': user_answer,
                            'correct_answer': correct_answer,
                            'is_correct': is_correct,
                            'explanation': answers[i]['explanation']
                        })
                
                percentage = (score / len(questions)) * 100
                
                st.markdown("---")
                st.markdown("## 📊 Quiz Results")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("✅ Score", f"{score}/{len(questions)}")
                with col2:
                    st.metric("📈 Percentage", f"{percentage:.1f}%")
                with col3:
                    if percentage >= 70:
                        st.metric("Status", "🎉 Passed!")
                    else:
                        st.metric("Status", "📚 Keep Practicing")
                
                # Store in quiz history
                st.session_state.quiz_history.append({
                    'quiz_title': f"AI Quiz ({level} Level): {topic}",
                    'score': score,
                    'total': len(questions),
                    'percentage': percentage,
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                
                with st.expander("🔍 View Detailed Results & Explanations"):
                    for i, res in enumerate(results):
                        if res['is_correct']:
                            st.markdown(f"✅ **Q{i+1}:** Correct!")
                        else:
                            st.markdown(f"❌ **Q{i+1}:** Incorrect")
                            st.markdown(f"   **Your answer:** {res['user_answer']}")
                            st.markdown(f"   **Correct answer:** {res['correct_answer']}")
                            st.markdown(f"   **📖 Explanation:** {res['explanation']}")
                        st.markdown("---")
                
                if percentage >= 90:
                    st.balloons()
                    st.success("🏆 Outstanding! You're a master of this topic!")
                elif percentage >= 70:
                    st.success("🎉 Great job! You have good understanding!")
                elif percentage >= 50:
                    st.warning("👍 Good effort! Review the material and try again!")
                else:
                    st.error("📚 Keep learning! Focus on understanding the concepts.")
                
            else:
                remaining = len(questions) - len(answers)
                st.warning(f"⚠️ Please answer {remaining} more question(s) before submitting.")

def display_mindmap_by_level(mindmap: dict, topic: str, level: str):
    """Display mindmap/learning roadmap by level with better alignment"""
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 0.5rem; border-radius: 10px; margin-bottom: 1rem;">
        <h4 style="color: white; text-align: center;">🧠 {level} Level Learning Roadmap: {mindmap.get('topic', topic)}</h4>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 🎯 Central Concept")
    st.info(mindmap.get('central_concept', 'No central concept defined'))
    
    st.markdown("#### 📚 Main Topics")
    branches = mindmap.get('main_branches', [])
    
    if branches:
        num_cols = min(4, len(branches))
        cols = st.columns(num_cols)
        
        for idx, branch in enumerate(branches):
            with cols[idx % num_cols]:
                with st.expander(f"**{branch.get('name', 'Branch')}**", expanded=True):
                    for sub in branch.get('subtopics', []):
                        st.markdown(f"• {sub}")
    
    st.markdown("---")
    st.markdown("#### 🗺️ Recommended Learning Path")
    
    learning_path = mindmap.get('learning_path', [])
    for i, step in enumerate(learning_path, 1):
        st.markdown(f"**Step {i}:** {step}")
    
    st.markdown("---")
    st.markdown("💡 **Tip:** Follow this roadmap for systematic learning. Start with fundamentals and gradually move to advanced topics.")

def display_ai_learning():
    """Main AI Learning interface with level-based tabs - Improved layout"""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;">
        <h3 style="color: white;">🤖 AI-Powered Learning Assistant</h3>
        <p style="color: white;">Learn any topic with AI-generated content, test your knowledge with quizzes, and follow structured learning roadmaps!</p>
        <p style="color: white; font-size: 0.9rem;">Powered by Groq API</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check API key
    if not GROQ_API_KEY or GROQ_API_KEY == "":
        st.error("❌ Groq API key not configured! Please add your API key in the .env file.")
        st.info("🔑 Get your API key from: https://console.groq.com")
        return
    
    # Initialize learning system
    if 'ai_learning_system_instance' not in st.session_state:
        try:
            st.session_state.ai_learning_system_instance = AILearningSystem(GROQ_API_KEY)
            st.success("✅ AI Learning System initialized successfully!")
        except Exception as e:
            st.error(f"❌ Failed to initialize AI Learning System: {e}")
            return
    
    # Topic input with unique key
    topic_key = f"ai_learning_topic_{st.session_state.get('username', 'default')}"
    topic = st.text_input(
        "📚 **Enter a topic to learn:**",
        placeholder="e.g., Python Programming, Machine Learning, Artificial Intelligence, Cloud Computing",
        help="Enter any topic you want to learn about",
        key=topic_key
    )
    
    if topic:
        # Level selection
        st.markdown("#### 🎯 Select Learning Level")
        level_cols = st.columns(3)
        
        with level_cols[0]:
            beginner_btn = st.button("🌱 Beginner", key=f"beginner_btn_{topic}", use_container_width=True)
        with level_cols[1]:
            intermediate_btn = st.button("📘 Intermediate", key=f"intermediate_btn_{topic}", use_container_width=True)
        with level_cols[2]:
            advanced_btn = st.button("🚀 Advanced", key=f"advanced_btn_{topic}", use_container_width=True)
        
        # Determine selected level
        selected_level = None
        if beginner_btn:
            selected_level = "Beginner"
            st.session_state.selected_level = selected_level
            # Clear previous data when level changes
            if 'ai_content' in st.session_state:
                del st.session_state.ai_content
            if 'ai_quiz' in st.session_state:
                del st.session_state.ai_quiz
            if 'ai_mindmap' in st.session_state:
                del st.session_state.ai_mindmap
            st.session_state.ai_content_generated = False
            st.session_state.ai_quiz_generated = False
            st.session_state.ai_mindmap_generated = False
        elif intermediate_btn:
            selected_level = "Intermediate"
            st.session_state.selected_level = selected_level
            if 'ai_content' in st.session_state:
                del st.session_state.ai_content
            if 'ai_quiz' in st.session_state:
                del st.session_state.ai_quiz
            if 'ai_mindmap' in st.session_state:
                del st.session_state.ai_mindmap
            st.session_state.ai_content_generated = False
            st.session_state.ai_quiz_generated = False
            st.session_state.ai_mindmap_generated = False
        elif advanced_btn:
            selected_level = "Advanced"
            st.session_state.selected_level = selected_level
            if 'ai_content' in st.session_state:
                del st.session_state.ai_content
            if 'ai_quiz' in st.session_state:
                del st.session_state.ai_quiz
            if 'ai_mindmap' in st.session_state:
                del st.session_state.ai_mindmap
            st.session_state.ai_content_generated = False
            st.session_state.ai_quiz_generated = False
            st.session_state.ai_mindmap_generated = False
        elif 'selected_level' in st.session_state:
            selected_level = st.session_state.selected_level
        
        if selected_level:
            # Create tabs for different features
            tab1, tab2, tab3 = st.tabs(["📚 Study Content", "📝 Quiz", "🧠 Mindmap"])
            
            with tab1:
                # Generate button for content
                if st.button(f"🚀 Generate {selected_level} Level Content", type="primary", use_container_width=True, key=f"gen_content_{topic}_{selected_level}"):
                    with st.spinner(f"📚 Generating {selected_level} level content about '{topic}'..."):
                        content = st.session_state.ai_learning_system_instance.generate_content_by_level(topic, selected_level)
                        st.session_state.ai_content = content
                        st.session_state.ai_current_topic = topic
                        st.session_state.ai_current_level = selected_level
                        st.session_state.ai_content_generated = True
                
                # Display content only if generated and matches current topic/level
                if (st.session_state.get('ai_content_generated', False) and 
                    'ai_content' in st.session_state and 
                    st.session_state.ai_current_topic == topic and 
                    st.session_state.ai_current_level == selected_level):
                    display_ai_content_by_level(st.session_state.ai_content, topic, selected_level)
                elif not st.session_state.get('ai_content_generated', False):
                    st.info(f"👆 Click the button above to generate {selected_level} level study content!")
            
            with tab2:
                # Quiz generation controls
                col_quiz1, col_quiz2 = st.columns([1, 2])
                with col_quiz1:
                    num_questions = st.selectbox("Number of questions:", [5, 10, 15, 20], index=1, key=f"ai_num_questions_{topic}_{selected_level}")
                
                # Generate quiz button
                if st.button(f"🎯 Generate {selected_level} Level Quiz", type="primary", use_container_width=True, key=f"gen_quiz_{topic}_{selected_level}"):
                    with st.spinner(f"📝 Generating {num_questions} {selected_level} level quiz questions..."):
                        quiz = st.session_state.ai_learning_system_instance.generate_quiz_by_level(topic, num_questions, selected_level)
                        st.session_state.ai_quiz = quiz
                        st.session_state.ai_quiz_topic = topic
                        st.session_state.ai_quiz_level = selected_level
                        st.session_state.ai_quiz_generated = True
                        # Clear any previous quiz answers from session state
                        quiz_key = f"ai_quiz_{topic}_{selected_level}_{hash(topic + selected_level)}"
                        if quiz_key in st.session_state:
                            del st.session_state[quiz_key]
                
                # Display quiz only if generated
                if (st.session_state.get('ai_quiz_generated', False) and 
                    'ai_quiz' in st.session_state and 
                    st.session_state.ai_quiz_topic == topic and 
                    st.session_state.ai_quiz_level == selected_level):
                    display_ai_quiz_by_level(st.session_state.ai_quiz, topic, selected_level)
                elif not st.session_state.get('ai_quiz_generated', False):
                    st.info(f"👆 Click the button above to generate a {selected_level} level quiz!")
            
            with tab3:
                if st.button(f"🧠 Generate {selected_level} Level Mindmap", type="primary", use_container_width=True, key=f"gen_mindmap_{topic}_{selected_level}"):
                    with st.spinner(f"🧠 Creating {selected_level} level learning roadmap..."):
                        mindmap = st.session_state.ai_learning_system_instance.generate_mindmap_by_level(topic, selected_level)
                        st.session_state.ai_mindmap = mindmap
                        st.session_state.ai_mindmap_topic = topic
                        st.session_state.ai_mindmap_level = selected_level
                        st.session_state.ai_mindmap_generated = True
                
                if (st.session_state.get('ai_mindmap_generated', False) and 
                    'ai_mindmap' in st.session_state and 
                    st.session_state.ai_mindmap_topic == topic and 
                    st.session_state.ai_mindmap_level == selected_level):
                    display_mindmap_by_level(st.session_state.ai_mindmap, topic, selected_level)
                elif not st.session_state.get('ai_mindmap_generated', False):
                    st.info(f"👆 Click the button above to generate a {selected_level} level learning roadmap!")
    else:
        st.info("💡 **Enter a topic above to start learning!**\n\nExamples: Python, Machine Learning, Web Development, Data Science, Cloud Computing, Artificial Intelligence")

def display_quiz(quiz):
    """Display and evaluate a quiz - WITHOUT ST.RERUN()"""
    st.subheader(f"📝 {quiz['title']}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Questions", len(quiz['questions']))
    with col2:
        st.metric("Time Limit", f"{len(quiz['questions']) * 2} mins")
    with col3:
        st.metric("Passing Score", "60%")
    
    st.markdown("---")
    
    quiz_key = f"quiz_{quiz['id']}"
    
    if quiz_key not in st.session_state.quiz_answers_store:
        st.session_state.quiz_answers_store[quiz_key] = {}
    
    answers = {}
    all_answered = True
    
    for i, q in enumerate(quiz['questions']):
        with st.container():
            st.markdown(f"### Question {i+1}")
            st.markdown(f"**{q['question']}**")
            
            current_answer = st.session_state.quiz_answers_store[quiz_key].get(i)
            
            selected_option = st.radio(
                "Select your answer:",
                q['options'],
                key=f"{quiz_key}_q_{i}",
                index=current_answer if current_answer is not None else None,
                horizontal=True,
                label_visibility="collapsed"
            )
            
            if selected_option is not None:
                answer_index = q['options'].index(selected_option)
                answers[str(i)] = answer_index
                st.session_state.quiz_answers_store[quiz_key][i] = answer_index
            elif current_answer is not None:
                answers[str(i)] = current_answer
            else:
                all_answered = False
            
            st.markdown("---")
    
    submit_key = f"submit_{quiz_key}"
    
    if st.button("📤 Submit Quiz", key=submit_key, use_container_width=True, type="primary"):
        if all_answered and len(answers) == len(quiz['questions']):
            score = 0
            detailed_results = []
            
            for i, q in enumerate(quiz['questions']):
                user_answer_idx = st.session_state.quiz_answers_store[quiz_key].get(i)
                
                if user_answer_idx is not None:
                    is_correct = (user_answer_idx == q.get('correct', 0))
                    if is_correct:
                        score += 1
                    
                    detailed_results.append({
                        'question': q['question'],
                        'user_answer': q['options'][user_answer_idx],
                        'correct_answer': q['options'][q.get('correct', 0)],
                        'is_correct': is_correct,
                        'explanation': q.get('explanation', 'No explanation available')
                    })
            
            percentage = (score / len(quiz['questions'])) * 100
            
            st.session_state.quiz_history.append({
                'quiz_title': quiz['title'],
                'score': score,
                'total': len(quiz['questions']),
                'percentage': percentage,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            
            if quiz_key in st.session_state.quiz_answers_store:
                del st.session_state.quiz_answers_store[quiz_key]
            
            st.markdown("## 📊 Your Results")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=percentage,
                    title={'text': "Score Percentage"},
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "#667eea"},
                        'steps': [
                            {'range': [0, 40], 'color': "red"},
                            {'range': [40, 60], 'color': "orange"},
                            {'range': [60, 80], 'color': "yellow"},
                            {'range': [80, 100], 'color': "green"}
                        ],
                        'threshold': {
                            'line': {'color': "black", 'width': 4},
                            'thickness': 0.75,
                            'value': 60
                        }
                    }
                ))
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown(f"""
                ### Score Details
                - ✅ Correct Answers: **{score}**
                - ❌ Incorrect Answers: **{len(quiz['questions']) - score}**
                - 📊 Percentage: **{percentage:.1f}%**
                """)
            
            with st.expander("🔍 View Detailed Results & Explanations"):
                for i, res in enumerate(detailed_results):
                    if res['is_correct']:
                        st.markdown(f"✅ **Q{i+1}** - Correct!")
                    else:
                        st.markdown(f"❌ **Q{i+1}** - Incorrect")
                        st.markdown(f"Your answer: {res['user_answer']}")
                        st.markdown(f"Correct answer: {res['correct_answer']}")
                        st.markdown(f"📖 **Explanation:** {res['explanation']}")
                    st.markdown("---")
            
            if percentage >= 80:
                st.markdown("🎉 **Excellent!** You're mastering this topic! Keep up the great work!")
            elif percentage >= 60:
                st.markdown("👍 **Good job!** You passed! Review the incorrect answers to improve further.")
            else:
                st.markdown("📚 **Keep practicing!** Focus on understanding the concepts and try again.")
            
            st.session_state.show_quiz_results = True
            st.session_state.quiz_completed = True
            
        else:
            remaining = len(quiz['questions']) - len(answers)
            st.warning(f"⚠️ Please answer {remaining} more question(s) before submitting.")
    
    if st.session_state.get('quiz_completed', False):
        if st.button("← Back to All Quizzes", key=f"back_{quiz_key}", use_container_width=True):
            st.session_state.selected_quiz = None
            st.session_state.quiz_completed = False
            st.session_state.show_quiz_results = False
            if quiz_key in st.session_state.quiz_answers_store:
                del st.session_state.quiz_answers_store[quiz_key]
            st.rerun()

def display_assessment_test(test):
    """Display and evaluate assessment test - SIMPLE WORKING VERSION"""
    st.subheader(f"📝 {test['name']}")
    st.info(f"⏱️ Duration: {test['duration']} | 🎯 Difficulty: {test['difficulty']}")
    st.markdown(f"**Topics Covered:** {', '.join(test['topics'])}")
    st.markdown("---")
    
    answers = {}
    
    for i, q in enumerate(test['questions']):
        st.markdown(f"**Q{i+1}. {q['question']}**")
        
        answer = st.radio(
            "Select your answer:",
            q['options'],
            key=f"test_{test['id']}_q_{i}",
            index=None,
            horizontal=True
        )
        if answer:
            answers[str(i)] = q['options'].index(answer)
        st.markdown("---")
    
    if st.button("Submit Assessment Test", key=f"submit_test_{test['id']}", use_container_width=True):
        if len(answers) == len(test['questions']):
            result = api.evaluate_assessment_test(test['id'], answers)
            
            if result:
                st.success(f"🎯 Your Score: {result['score']}/{result['total']} ({result['percentage']:.1f}%)")
                
                if result['percentage'] >= 80:
                    st.markdown("🎉 Excellent performance! You're well prepared!")
                elif result['percentage'] >= 60:
                    st.markdown("👍 Good effort! Review the incorrect answers to improve.")
                elif result['percentage'] >= 40:
                    st.markdown("📚 Need more practice. Focus on weak areas and try again.")
                else:
                    st.markdown("💪 Keep working hard! Review all topics thoroughly.")
                
                with st.expander("🔍 View Detailed Results & Explanations"):
                    for i, res in enumerate(result['results']):
                        if res['is_correct']:
                            st.markdown(f"✅ **Q{i+1}** - Correct!")
                        else:
                            st.markdown(f"❌ **Q{i+1}** - Incorrect")
                            st.markdown(f"Your answer: {res['user_answer']}")
                            st.markdown(f"Correct answer: {res['correct_answer']}")
                            st.markdown(f"📖 **Explanation:** {res['explanation']}")
                        st.markdown("---")
                
                st.subheader("📚 Study Recommendations")
                if result['percentage'] < 60:
                    st.markdown("""
                    - Review the topics where you made mistakes
                    - Practice more questions on weak areas
                    - Take topic-wise tests before attempting full tests
                    - Watch video tutorials for difficult concepts
                    """)
                else:
                    st.markdown("""
                    - Keep practicing to maintain your performance
                    - Focus on time management
                    - Attempt more mock tests for better preparation
                    - Revise regularly to retain concepts
                    """)
                
                if st.button("← Back to Tests", use_container_width=True):
                    st.session_state.current_test = None
                    st.rerun()
        else:
            st.warning(f"⚠️ Please answer all {len(test['questions'])} questions before submitting.")

def login_page():
    """Display login page"""
    st.markdown("""
    <div class="login-header">
        <h1 style="text-align: center; margin: 0;">🎓 Smart Academic Assistant Pro</h1>
        <p style="text-align: center; margin: 10px 0 0 0;">Your Intelligent Learning Companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if not st.session_state.show_register:
            st.subheader("🔐 Login")
            
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login", use_container_width=True)
                
                if submit:
                    result = auth.login_user(username, password)
                    if result['success']:
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.session_state.role = result['user']['role']
                        st.success(result['message'])
                        st.rerun()
                    else:
                        st.error(result['message'])
            
            st.markdown("---")
            st.markdown("### New User?")
            if st.button("Register Here", use_container_width=True):
                st.session_state.show_register = True
                st.rerun()
        
        else:
            st.subheader("📝 Registration")
            
            with st.form("register_form"):
                username = st.text_input("Username")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                role = st.selectbox("Select Your Role", 
                                   ["School Student", "College Student", "Exam Aspirant"])
                
                submit = st.form_submit_button("Register", use_container_width=True)
                
                if submit:
                    if password != confirm_password:
                        st.error("Passwords do not match!")
                    elif not username or not email or not password:
                        st.error("Please fill all fields!")
                    else:
                        role_key = {
                            "School Student": "school",
                            "College Student": "college",
                            "Exam Aspirant": "aspirant"
                        }[role]
                        
                        result = auth.register_user(username, password, email, role_key)
                        if result['success']:
                            st.success(result['message'])
                            st.session_state.show_register = False
                            st.session_state.registration_success = True
                            st.rerun()
                        else:
                            st.error(result['message'])
            
            if st.button("← Back to Login", use_container_width=True):
                st.session_state.show_register = False
                st.rerun()

def add_ai_logo_to_sidebar():
    """Add AI logo to the top of sidebar"""
    st.sidebar.markdown("""
    <div class="ai-logo">
        <div class="ai-logo-text">
            🤖 AI <span style="font-size: 18px;">Smart Assistant</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("---")

def get_comprehensive_college_quizzes():
    """Return comprehensive college quizzes with complete answers"""
    return [
        {
            "id": 1,
            "title": "Database Management Systems",
            "questions": [
                {"question": "What does SQL stand for?", "options": ["Structured Query Language", "Simple Query Language", "System Query Language", "Standard Query Language"], "correct": 0, "explanation": "SQL stands for Structured Query Language, used to communicate with databases."},
                {"question": "What is a primary key?", "options": ["Unique identifier for each record", "Foreign key reference", "Index for faster queries", "Constraint for null values"], "correct": 0, "explanation": "A primary key uniquely identifies each record in a database table."},
                {"question": "What is normalization?", "options": ["Organizing data to reduce redundancy", "Adding duplicate data", "Deleting data", "Backing up data"], "correct": 0, "explanation": "Normalization reduces data redundancy and improves data integrity."},
                {"question": "What is a foreign key?", "options": ["References primary key in another table", "Always unique", "Can be null", "Used for indexing"], "correct": 0, "explanation": "A foreign key establishes a link between two tables."},
                {"question": "What is ACID?", "options": ["Atomicity, Consistency, Isolation, Durability", "Atomic, Consistent, Isolated, Durable", "Access, Control, Integrity, Data", "All Commands In Database"], "correct": 0, "explanation": "ACID ensures reliable processing of database transactions."}
            ]
        },
        {
            "id": 2,
            "title": "Operating Systems",
            "questions": [
                {"question": "What is a process?", "options": ["Program in execution", "Program on disk", "Memory location", "CPU register"], "correct": 0, "explanation": "A process is a program that is currently being executed."},
                {"question": "What is deadlock?", "options": ["Processes waiting indefinitely", "Process completed", "Memory full", "CPU overload"], "correct": 0, "explanation": "Deadlock occurs when processes wait for resources held by each other."},
                {"question": "What is paging?", "options": ["Memory management scheme", "Page replacement", "Process scheduling", "File system"], "correct": 0, "explanation": "Paging divides memory into fixed-size blocks."},
                {"question": "What is a semaphore?", "options": ["Synchronization tool", "Variable type", "Memory unit", "File descriptor"], "correct": 0, "explanation": "Semaphores control access to shared resources."},
                {"question": "What is thrashing?", "options": ["Excessive paging", "Process termination", "Memory failure", "CPU error"], "correct": 0, "explanation": "Thrashing occurs when system spends more time paging than executing."}
            ]
        },
        {
            "id": 3,
            "title": "Computer Networks",
            "questions": [
                {"question": "What does TCP/IP stand for?", "options": ["Transmission Control Protocol/Internet Protocol", "Transfer Control Protocol", "Transmission Communication Protocol", "Transfer Communication Protocol"], "correct": 0, "explanation": "TCP/IP is the fundamental protocol suite for the Internet."},
                {"question": "What is an IP address?", "options": ["Unique identifier for network devices", "Web address", "Email identifier", "Domain name"], "correct": 0, "explanation": "IP address uniquely identifies devices on a network."},
                {"question": "What is DNS?", "options": ["Domain Name System", "Data Network Service", "Digital Name Server", "Domain Naming Service"], "correct": 0, "explanation": "DNS translates domain names to IP addresses."},
                {"question": "What is HTTP?", "options": ["HyperText Transfer Protocol", "High Transfer Text Protocol", "Hyper Transfer Text Protocol", "High Text Transfer Protocol"], "correct": 0, "explanation": "HTTP is used for transmitting web pages."},
                {"question": "What is a firewall?", "options": ["Network security system", "Virus scanner", "Web browser", "Email client"], "correct": 0, "explanation": "Firewall monitors and controls network traffic."}
            ]
        },
        {
            "id": 4,
            "title": "Web Development",
            "questions": [
                {"question": "What does HTML stand for?", "options": ["HyperText Markup Language", "High Tech Modern Language", "Hyper Transfer Markup Language", "Home Tool Markup Language"], "correct": 0, "explanation": "HTML is the standard markup language for web pages."},
                {"question": "What is CSS used for?", "options": ["Styling web pages", "Database queries", "Server-side scripting", "Network protocols"], "correct": 0, "explanation": "CSS controls the presentation of HTML elements."},
                {"question": "What is JavaScript?", "options": ["Programming language for web", "Database system", "Server software", "Markup language"], "correct": 0, "explanation": "JavaScript adds interactivity to web pages."},
                {"question": "What is React?", "options": ["JavaScript library for UIs", "Database system", "Backend framework", "CSS framework"], "correct": 0, "explanation": "React builds component-based user interfaces."},
                {"question": "What is REST API?", "options": ["Architectural style for web services", "Database protocol", "Programming language", "Web server"], "correct": 0, "explanation": "REST API enables client-server communication using HTTP."}
            ]
        },
        {
            "id": 5,
            "title": "Software Engineering",
            "questions": [
                {"question": "What is Agile?", "options": ["Iterative development approach", "Waterfall model", "Spiral model", "V-model"], "correct": 0, "explanation": "Agile focuses on iterative development with collaboration."},
                {"question": "What is a sprint?", "options": ["Time-boxed development cycle", "Code compilation", "Testing phase", "Deployment phase"], "correct": 0, "explanation": "A sprint is a fixed time period for completing work."},
                {"question": "What is unit testing?", "options": ["Testing individual components", "Testing entire system", "User testing", "Performance testing"], "correct": 0, "explanation": "Unit testing verifies individual code units."},
                {"question": "What is version control?", "options": ["System tracking code changes", "Database management", "Testing framework", "Deployment tool"], "correct": 0, "explanation": "Version control manages changes to source code."},
                {"question": "What is CI/CD?", "options": ["Continuous Integration/Deployment", "Code Integration/Deployment", "Continuous Implementation/Delivery", "Code Implementation/Delivery"], "correct": 0, "explanation": "CI/CD automates building, testing, and deployment."}
            ]
        }
    ]

def school_student_dashboard():
    """Dashboard for school students"""
    add_ai_logo_to_sidebar()
    
    st.markdown(f'<div class="main-header"><h1>📚 Welcome, {st.session_state.username}!</h1><p>School Student Dashboard</p></div>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown(f"### 👨‍🎓 {st.session_state.username}")
        st.markdown("---")
        
        menu = st.radio("Navigation", 
                       ["📖 Study Materials", "⏰ Exam Time Chart", "📊 Progress", "🤖 AI Learning"])
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            for key in ['authenticated', 'username', 'role', 'show_register', 'registration_success']:
                if key in st.session_state:
                    st.session_state[key] = None if key != 'show_register' else False
            st.rerun()
    
    if menu == "📖 Study Materials":
        st.header("📖 Download Study Materials")
        subject = st.selectbox("Select Subject", Config.SCHOOL_SUBJECTS)
        materials = api.get_school_study_materials(subject)
        
        if materials:
            for topic, pdf_data in materials.items():
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{topic}**")
                    with col2:
                        st.download_button(
                            label="📥 Download PDF",
                            data=pdf_data,
                            file_name=f"{topic}.pdf",
                            mime="application/pdf",
                            key=f"download_{topic}"
                        )
        else:
            st.info("Materials coming soon for this subject!")
    
    elif menu == "⏰ Exam Time Chart":
        st.header("📅 Exam Preparation Schedule")
        
        tab1, tab2, tab3, tab4 = st.tabs(["📅 Daily Schedule", "📊 Weekly Plan", "🎯 Study Goals", "📈 Progress Tracking"])
        
        with tab1:
            st.markdown("### ⏰ Daily Study Schedule")
            
            daily_schedule = [
                {"time": "6:00 AM - 7:00 AM", "activity": "🌅 Morning Revision", "details": "Review yesterday's topics"},
                {"time": "7:00 AM - 8:00 AM", "activity": "🍳 Breakfast & Break", "details": "Refresh your mind"},
                {"time": "8:00 AM - 10:00 AM", "activity": "📖 Core Subject Study", "details": "Focus on difficult topics"},
                {"time": "10:00 AM - 10:30 AM", "activity": "☕ Short Break", "details": "Rest and recharge"},
                {"time": "10:30 AM - 12:30 PM", "activity": "✍️ Practice Problems", "details": "Solve worksheets"},
                {"time": "12:30 PM - 2:00 PM", "activity": "🍽️ Lunch Break", "details": "Healthy meal & rest"},
                {"time": "2:00 PM - 4:00 PM", "activity": "🎯 Subject Practice", "details": "Apply concepts"},
                {"time": "4:00 PM - 4:30 PM", "activity": "🧘 Evening Break", "details": "Stretch & refresh"},
                {"time": "4:30 PM - 6:30 PM", "activity": "📚 Revision & Notes", "details": "Make summary notes"},
                {"time": "6:30 PM - 8:00 PM", "activity": "🏃 Free Time", "details": "Hobbies & relaxation"},
                {"time": "8:00 PM - 10:00 PM", "activity": "🎯 Mock Tests", "details": "Practice under time limit"},
                {"time": "10:00 PM", "activity": "😴 Bed Time", "details": "Get 8 hours of sleep"}
            ]
            
            for slot in daily_schedule:
                with st.container():
                    col1, col2, col3 = st.columns([1, 2, 2])
                    with col1:
                        st.markdown(f"<div class='time-slot'>{slot['time']}</div>", unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"**{slot['activity']}**")
                    with col3:
                        st.markdown(f"<small>{slot['details']}</small>", unsafe_allow_html=True)
                    st.markdown("---")
        
        with tab2:
            st.markdown("### 📊 Weekly Study Plan")
            
            weeks = ["Week 1", "Week 2", "Week 3", "Week 4"]
            subjects = ["Mathematics", "Science", "English", "Social Studies", "Computer Science"]
            
            study_data = pd.DataFrame({
                'Subject': subjects,
                'Week 1': [4, 3, 2, 2, 1],
                'Week 2': [4, 3, 2, 2, 2],
                'Week 3': [5, 4, 3, 3, 2],
                'Week 4': [5, 4, 3, 3, 3]
            })
            
            fig = px.imshow(
                study_data[weeks].T,
                x=subjects,
                y=weeks,
                labels=dict(x="Subjects", y="Week", color="Study Hours"),
                title="Weekly Study Intensity (Hours per day)",
                color_continuous_scale="Viridis"
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("#### 📅 Detailed Weekly Schedule")
            
            weekly_schedule = {
                "Monday": ["Mathematics", "Science", "Practice", "Revision"],
                "Tuesday": ["English", "Social Studies", "Computer Science", "Practice"],
                "Wednesday": ["Mathematics", "Science", "English", "Mock Test"],
                "Thursday": ["Social Studies", "Computer Science", "Mathematics", "Revision"],
                "Friday": ["Science", "English", "Practice", "Doubt Clearing"],
                "Saturday": ["Full Syllabus Revision", "Mock Test", "Error Analysis", "Weak Topic Focus"],
                "Sunday": ["Light Revision", "Rest & Recreation", "Plan Next Week", "Goal Setting"]
            }
            
            for day, topics in weekly_schedule.items():
                with st.expander(f"📌 {day}"):
                    cols = st.columns(4)
                    for i, topic in enumerate(topics):
                        with cols[i]:
                            st.markdown(f"**{topic}**")
                            st.markdown(f"🕒 {2 + i} hours")
            
            st.markdown("#### 💪 Weekly Motivation")
            st.info("""
            🎯 **Week 1-2:** Focus on understanding concepts
            📈 **Week 3:** Increase practice and problem-solving
            🏆 **Week 4:** Take full-length mock tests and analyze performance
            """)
        
        with tab3:
            st.markdown("### 🎯 Study Goals & Milestones")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Short-term Goals (Daily)")
                daily_goals = [
                    "Complete 2 chapters",
                    "Solve 20 practice problems",
                    "Revise 1 previous topic",
                    "Take 1 mini test"
                ]
                for goal in daily_goals:
                    st.checkbox(goal, key=f"daily_{goal}")
            
            with col2:
                st.markdown("#### Long-term Goals (Weekly)")
                weekly_goals = [
                    "Complete 3 subjects",
                    "Score 80% in mock test",
                    "Finish all assignments",
                    "Create revision notes"
                ]
                for goal in weekly_goals:
                    st.checkbox(goal, key=f"weekly_{goal}")
            
            st.markdown("### 📊 Goal Progress Tracker")
            
            goal_progress = {
                "Chapters Completed": 15,
                "Practice Problems": 245,
                "Mock Tests Taken": 8,
                "Revision Hours": 32
            }
            
            for goal, value in goal_progress.items():
                st.markdown(f"**{goal}:** {value}")
                st.progress(min(value/100, 1.0))
        
        with tab4:
            st.markdown("### 📈 Progress Tracking Dashboard")
            
            progress_data = pd.DataFrame({
                'Subject': Config.SCHOOL_SUBJECTS,
                'Progress': [75, 60, 85, 40, 50],
                'Target': [100, 100, 100, 100, 100]
            })
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Current Progress', x=progress_data['Subject'], y=progress_data['Progress'], marker_color='#667eea'))
            fig.add_trace(go.Bar(name='Target', x=progress_data['Subject'], y=progress_data['Target'], marker_color='#e0e0e0'))
            fig.update_layout(title="Subject-wise Progress", barmode='group', height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("#### ⏰ Weekly Study Hours")
            hours_data = pd.DataFrame({
                'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                'Hours': [4, 5, 3, 6, 4, 7, 2]
            })
            
            fig = px.line(hours_data, x='Day', y='Hours', title="Study Hours Tracker", markers=True)
            fig.update_traces(line_color='#667eea', line_width=3)
            st.plotly_chart(fig, use_container_width=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📚 Topics Completed", "24/40", "60%")
            with col2:
                st.metric("⏰ Total Study Hours", "128 hrs", "+12 this week")
            with col3:
                st.metric("📝 Tests Taken", "12", "+3 this week")
            with col4:
                st.metric("📈 Average Score", "75%", "+5%")
    
    elif menu == "📊 Progress":
        st.header("📊 Your Progress")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📚 Subjects Completed", "3/5")
        with col2:
            st.metric("⏰ Study Hours", "45 hrs")
        with col3:
            st.metric("📝 Tests Taken", "12")
        
        progress_data = pd.DataFrame({
            'Subject': Config.SCHOOL_SUBJECTS,
            'Progress': [75, 60, 85, 40, 50]
        })
        fig = px.bar(progress_data, x='Subject', y='Progress', 
                    title="Subject-wise Progress", color='Progress')
        st.plotly_chart(fig, use_container_width=True)
    
    elif menu == "🤖 AI Learning":
        display_ai_learning()

def college_student_dashboard():
    """Dashboard for college students"""
    add_ai_logo_to_sidebar()
    
    st.markdown(f'<div class="main-header"><h1>🎓 Welcome, {st.session_state.username}!</h1><p>College Student Dashboard</p></div>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown(f"### 👨‍🎓 {st.session_state.username}")
        st.markdown("---")
        
        menu = st.radio("Navigation", 
                       ["💼 Placement Guides", "📝 Quizzes", "💻 Project Solutions", "📊 Progress", "🤖 AI Learning"])
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            for key in ['authenticated', 'username', 'role', 'show_register', 'registration_success']:
                if key in st.session_state:
                    st.session_state[key] = None if key != 'show_register' else False
            st.rerun()
    
    if menu == "💼 Placement Guides":
        st.header("💼 Placement Preparation Guides")
        guides = api.get_placement_guides()
        for guide_name, pdf_data in guides.items():
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{guide_name}**")
                with col2:
                    st.download_button(
                        label="📥 Download PDF",
                        data=pdf_data,
                        file_name=f"{guide_name.replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        key=f"guide_{guide_name}"
                    )
    
    elif menu == "📝 Quizzes":
        st.header("📝 Practice Quizzes")
        
        if 'quiz_completed' not in st.session_state:
            st.session_state.quiz_completed = False
        
        if st.session_state.selected_quiz and not st.session_state.get('quiz_completed', False):
            col1, col2 = st.columns([5, 1])
            with col2:
                if st.button("← Back", key="back_from_quiz", use_container_width=True):
                    quiz_key = f"quiz_{st.session_state.selected_quiz['id']}"
                    if quiz_key in st.session_state.quiz_answers_store:
                        del st.session_state.quiz_answers_store[quiz_key]
                    st.session_state.selected_quiz = None
                    st.session_state.quiz_completed = False
                    st.rerun()
            
            st.markdown("---")
            display_quiz(st.session_state.selected_quiz)
        
        elif st.session_state.selected_quiz and st.session_state.get('quiz_completed', False):
            if st.button("← Back to All Quizzes", key="back_after_quiz", use_container_width=True):
                st.session_state.selected_quiz = None
                st.session_state.quiz_completed = False
                st.rerun()
        
        else:
            all_quizzes = get_comprehensive_college_quizzes()
            
            if st.session_state.quiz_history:
                with st.expander("📜 Your Quiz History"):
                    history_df = pd.DataFrame(st.session_state.quiz_history[-10:])
                    st.dataframe(history_df, use_container_width=True)
            
            for i, quiz in enumerate(all_quizzes):
                if i % 2 == 0:
                    col1, col2 = st.columns(2)
                    with col1:
                        with st.container():
                            st.markdown(f"### {quiz['title']}")
                            st.markdown(f"📊 {len(quiz['questions'])} Questions | ⏱️ {len(quiz['questions']) * 2} minutes")
                            if st.button(f"Start {quiz['title']}", key=f"start_quiz_{quiz['id']}"):
                                quiz_key = f"quiz_{quiz['id']}"
                                if quiz_key in st.session_state.quiz_answers_store:
                                    del st.session_state.quiz_answers_store[quiz_key]
                                st.session_state.selected_quiz = quiz
                                st.session_state.quiz_completed = False
                                st.rerun()
                            st.markdown("---")
                    if i + 1 < len(all_quizzes):
                        next_quiz = all_quizzes[i + 1]
                        with col2:
                            with st.container():
                                st.markdown(f"### {next_quiz['title']}")
                                st.markdown(f"📊 {len(next_quiz['questions'])} Questions | ⏱️ {len(next_quiz['questions']) * 2} minutes")
                                if st.button(f"Start {next_quiz['title']}", key=f"start_quiz_{next_quiz['id']}"):
                                    quiz_key = f"quiz_{next_quiz['id']}"
                                    if quiz_key in st.session_state.quiz_answers_store:
                                        del st.session_state.quiz_answers_store[quiz_key]
                                    st.session_state.selected_quiz = next_quiz
                                    st.session_state.quiz_completed = False
                                    st.rerun()
                                st.markdown("---")
    
    elif menu == "💻 Project Solutions":
        st.header("💻 Real-time Project Examples")
        projects = api.get_project_solutions()
        for project in projects:
            with st.expander(f"📁 {project['title']}"):
                st.markdown(f"**Description:** {project['description']}")
                st.markdown(f"**Technologies:** {', '.join(project['technologies'])}")
                st.markdown(f"**Features:**")
                for feature in project['features']:
                    st.markdown(f"  • {feature}")
    
    elif menu == "📊 Progress":
        st.header("📊 Your Progress")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📚 Projects Completed", "4/8")
        with col2:
            st.metric("📝 Quizzes Taken", len(st.session_state.quiz_history))
        with col3:
            st.metric("💼 Applications Sent", "15")
        
        if st.session_state.quiz_history:
            st.subheader("Quiz Performance Trend")
            quiz_df = pd.DataFrame(st.session_state.quiz_history)
            fig = px.line(quiz_df, x='date', y='percentage', title="Quiz Scores Over Time")
            st.plotly_chart(fig, use_container_width=True)
    
    elif menu == "🤖 AI Learning":
        display_ai_learning()

def exam_aspirant_dashboard():
    """Dashboard for exam aspirants"""
    add_ai_logo_to_sidebar()
    
    st.markdown(f'<div class="main-header"><h1>🎯 Welcome, {st.session_state.username}!</h1><p>Exam Aspirant Dashboard</p></div>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown(f"### 👨‍🎓 {st.session_state.username}")
        st.markdown("---")
        
        menu = st.radio("Navigation", 
                       ["⏰ Time Charts", "💡 Quick Tips", "📝 Assessment Tests", "📊 Progress", "🤖 AI Learning"])
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            for key in ['authenticated', 'username', 'role', 'show_register', 'registration_success']:
                if key in st.session_state:
                    st.session_state[key] = None if key != 'show_register' else False
            st.rerun()
    
    if menu == "⏰ Time Charts":
        st.header("⏰ Detailed Exam Preparation Time Charts")
        
        tab1, tab2, tab3 = st.tabs(["📊 Subject-wise Plan", "📅 Monthly Schedule", "🎯 Weekly Targets"])
        
        with tab1:
            st.markdown("### 📊 Comprehensive Subject-wise Study Plan")
            
            time_charts = api.get_subject_time_charts()
            
            for subject, details in time_charts.items():
                with st.expander(f"📚 {subject} - Detailed Plan", expanded=True):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### 📖 Topics to Cover")
                        for topic in details.get('Topics', []):
                            st.markdown(f"• {topic}")
                    
                    with col2:
                        st.markdown("#### ⏰ Time Allocation")
                        st.info(f"**Total:** {details.get('Time Allocation', 'N/A')}")
                        st.info(f"**Weekly:** {details.get('Weekly Plan', 'N/A')}")
                        st.info(f"**Daily:** {details.get('Daily Schedule', 'N/A')}")
        
        with tab2:
            st.markdown("### 📅 Monthly Study Calendar")
            
            months = ['January', 'February', 'March', 'April', 'May', 'June']
            subjects = ['Quantitative Aptitude', 'Logical Reasoning', 'English', 'General Knowledge']
            
            intensity_data = pd.DataFrame([
                [3, 4, 5, 4, 3, 2],
                [2, 3, 4, 4, 3, 2],
                [2, 2, 3, 3, 4, 3],
                [1, 2, 3, 4, 5, 5]
            ], index=subjects, columns=months)
            
            fig = px.imshow(intensity_data, 
                           labels=dict(x="Month", y="Subject", color="Study Hours"),
                           title="Monthly Study Intensity (Hours per day)",
                           color_continuous_scale="Viridis")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("#### 📌 Important Milestones")
            milestones = {
                "Month 1-2": "Complete 50% syllabus",
                "Month 3-4": "Complete 80% syllabus + Start mock tests",
                "Month 5": "Revision + Intensive practice",
                "Month 6": "Full-length mock tests + Final revision"
            }
            
            for period, milestone in milestones.items():
                st.markdown(f"**{period}:** {milestone}")
        
        with tab3:
            st.markdown("### 🎯 Weekly Study Targets")
            
            weeks_data = []
            for week in range(1, 13):
                weeks_data.append({
                    'Week': f'Week {week}',
                    'Quantitative': min(25, week * 2),
                    'Reasoning': min(25, week * 2),
                    'English': min(25, week * 1.5),
                    'GK': min(25, week * 2)
                })
            
            weekly_df = pd.DataFrame(weeks_data)
            
            fig = px.line(weekly_df, x='Week', y=['Quantitative', 'Reasoning', 'English', 'GK'],
                         title="12-Week Study Plan Progress Tracker",
                         markers=True)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("#### 📋 This Week's Study Plan")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Morning Session (6 AM - 12 PM)**")
                st.markdown("""
                - Monday: Quantitative Aptitude (Number System)
                - Tuesday: Logical Reasoning (Analytical)
                - Wednesday: Quantitative Aptitude (Algebra)
                - Thursday: English (Grammar)
                - Friday: Quantitative Aptitude (Geometry)
                - Saturday: General Knowledge (Current Affairs)
                - Sunday: Revision + Mock Test
                """)
            
            with col2:
                st.markdown("**Evening Session (2 PM - 8 PM)**")
                st.markdown("""
                - Monday: Logical Reasoning (Puzzles)
                - Tuesday: English (Vocabulary)
                - Wednesday: General Knowledge (History)
                - Thursday: Quantitative Aptitude (Statistics)
                - Friday: Logical Reasoning (Data Sufficiency)
                - Saturday: Practice Questions
                - Sunday: Error Analysis + Planning
                """)
            
            st.markdown("#### ✅ Weekly Checklist")
            checklist_items = [
                "Complete weekly targets for all subjects",
                "Take 2 full-length mock tests",
                "Analyze mistakes and note weak areas",
                "Revise previous week's topics",
                "Practice 50 questions per subject"
            ]
            
            for item in checklist_items:
                st.checkbox(item)
    
    elif menu == "💡 Quick Tips":
        st.header("💡 Comprehensive Exam Preparation Tips")
        
        tip_categories = {
            "📚 Study Strategies": [
                "Create a realistic study schedule and stick to it consistently",
                "Use the Pomodoro Technique: 25 minutes study, 5 minutes break",
                "Practice active recall instead of passive reading",
                "Make concise notes for quick revision before exams",
                "Use spaced repetition for better long-term retention"
            ],
            "⏰ Time Management": [
                "Prioritize topics based on weightage and difficulty",
                "Allocate more time to weak areas while maintaining strong ones",
                "Take regular breaks to avoid burnout (5 min every hour)",
                "Set daily, weekly, and monthly goals",
                "Use time-blocking technique for different subjects"
            ],
            "📝 Practice Techniques": [
                "Solve previous year question papers (last 5 years)",
                "Take weekly mock tests under exam conditions",
                "Analyze mistakes and maintain an error log",
                "Focus on accuracy before speed",
                "Practice time-bound question solving"
            ],
            "🧠 Memory Enhancement": [
                "Use mnemonics and visualization techniques",
                "Create mind maps for complex topics",
                "Teach concepts to others to reinforce learning",
                "Use flashcards for formulas and facts",
                "Connect new information with known concepts"
            ],
            "💪 Health & Wellness": [
                "Get 7-8 hours of quality sleep daily",
                "Stay hydrated and eat brain-healthy foods",
                "Exercise or meditate for 30 minutes daily",
                "Take short walks during study breaks",
                "Avoid caffeine and heavy meals before study sessions"
            ],
            "🎯 Exam Strategy": [
                "Read all questions before starting the exam",
                "Attempt easy questions first, then difficult ones",
                "Manage time by allocating minutes per question",
                "Don't spend too much time on one question",
                "Review answers if time permits"
            ]
        }
        
        for category, tips in tip_categories.items():
            st.markdown(f"## {category}")
            for tip in tips:
                st.markdown(f"💡 {tip}")
            st.markdown("---")
        
        import random
        motivational_quotes = [
            "Success is the sum of small efforts, repeated day in and day out.",
            "The expert in anything was once a beginner.",
            "Don't study until you get it right, study until you can't get it wrong.",
            "Your future self will thank you for the hard work you do today.",
            "Consistency is more important than intensity."
        ]
        quote = random.choice(motivational_quotes)
        st.info(f"✨ **Quote of the Day:** {quote}")
    
    elif menu == "📝 Assessment Tests":
        st.header("📝 Assessment Tests")
        tests = api.get_assessment_tests()
        
        if st.session_state.current_test:
            st.markdown("---")
            display_assessment_test(st.session_state.current_test)
            if st.button("← Back to Tests", use_container_width=True):
                for key in list(st.session_state.test_answers_store.keys()):
                    if key.startswith("test_"):
                        del st.session_state.test_answers_store[key]
                st.session_state.current_test = None
                st.rerun()
        else:
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Quantitative", "🧠 Reasoning", "📖 English", "🎯 Full Mock"])
            
            with tab1:
                test = tests[0]
                with st.expander(f"📋 {test['name']}", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Questions", len(test['questions']))
                    with col2:
                        st.metric("Duration", test['duration'])
                    with col3:
                        st.metric("Difficulty", test['difficulty'])
                    
                    if st.button(f"Start {test['name']}", key="start_quant", use_container_width=True):
                        st.session_state.current_test = test
                        st.rerun()
            
            with tab2:
                test = tests[1]
                with st.expander(f"📋 {test['name']}", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Questions", len(test['questions']))
                    with col2:
                        st.metric("Duration", test['duration'])
                    with col3:
                        st.metric("Difficulty", test['difficulty'])
                    
                    if st.button(f"Start {test['name']}", key="start_reasoning", use_container_width=True):
                        st.session_state.current_test = test
                        st.rerun()
            
            with tab3:
                test = tests[2]
                with st.expander(f"📋 {test['name']}", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Questions", len(test['questions']))
                    with col2:
                        st.metric("Duration", test['duration'])
                    with col3:
                        st.metric("Difficulty", test['difficulty'])
                    
                    if st.button(f"Start {test['name']}", key="start_english", use_container_width=True):
                        st.session_state.current_test = test
                        st.rerun()
            
            with tab4:
                test = tests[3]
                with st.expander(f"📋 {test['name']}", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Questions", len(test['questions']))
                    with col2:
                        st.metric("Duration", test['duration'])
                    with col3:
                        st.metric("Difficulty", test['difficulty'])
                    
                    if st.button(f"Start {test['name']}", key="start_mock", use_container_width=True):
                        st.session_state.current_test = test
                        st.rerun()
    
    elif menu == "📊 Progress":
        st.header("📊 Your Preparation Progress")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📚 Topics Covered", "45/120")
        with col2:
            st.metric("📝 Tests Taken", "8")
        with col3:
            st.metric("⏰ Study Hours", "120 hrs")
        
        subjects = list(api.get_subject_time_charts().keys())
        progress = [65, 45, 70, 50]
        
        progress_df = pd.DataFrame({
            'Subject': subjects,
            'Progress': progress
        })
        
        fig = px.bar(progress_df, x='Subject', y='Progress', 
                    title="Subject-wise Preparation Progress",
                    color='Progress',
                    color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)
    
    elif menu == "🤖 AI Learning":
        display_ai_learning()

def main_app():
    """Main application router"""
    apply_background()  
    init_session_state()
    
    if not st.session_state.authenticated:
        login_page()
    else:
        if st.session_state.role == "school":
            school_student_dashboard()
        elif st.session_state.role == "college":
            college_student_dashboard()
        elif st.session_state.role == "aspirant":
            exam_aspirant_dashboard()
        else:
            st.error("Invalid role detected!")
            if st.button("Logout"):
                for key in ['authenticated', 'username', 'role']:
                    st.session_state[key] = None
                st.rerun()

if __name__ == "__main__":
    main_app()