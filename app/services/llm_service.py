from typing import Dict, List
import random
import json

class LLMService:
    """Service for handling LLM interactions and responses"""
    
    def __init__(self):
        self.context = {}
       
        try:
            import google.generativeai as genai
            from app.config import Config
            
        
            if Config.GEMINI_API_KEY and Config.GEMINI_API_KEY != "AIzaSyDXyRJAMGDLiSo3M1vwRcz0BuGYnOqaADc":
                genai.configure(api_key=Config.GEMINI_API_KEY)
               
                self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')  # or 'gemini-2.5-flash'
                self.gemini_available = True
                print(f"Gemini AI available in LLMService with model: gemini-2.5-flash")
            else:
                self.gemini_available = False
                print("No valid Gemini API key found")
        except Exception as e:
            print(f"Gemini not available in LLMService: {e}")
            self.gemini_available = False
    
    def generate_response(self, query: str, role: str, context: Dict = None) -> str:
        """Generate response based on user role and query - Enhanced with Gemini"""
        
     
        if self.gemini_available:
            try:
                role_context = {
                    "school": "school student (ages 12-16). Use simple language and encouraging tone. Keep explanations clear and fun.",
                    "college": "college student. Provide detailed, practical, and career-oriented explanations.",
                    "aspirant": "exam aspirant. Focus on exam-relevant tips, strategies, and time management."
                }
                
                prompt = f"""You are an AI academic assistant for a {role_context.get(role, 'student')}
                
                User question: {query}
                
                Provide a helpful, accurate response. Include examples if relevant.
                Be concise but thorough. Keep the tone supportive and educational.
                If the question is about studying, exams, or academics, give practical advice."""
                
                response = self.gemini_model.generate_content(prompt)
                return response.text
            except Exception as e:
                print(f"Gemini error, falling back: {e}")
              
        
        if role == "school":
            return self._school_response(query)
        elif role == "college":
            return self._college_response(query)
        elif role == "aspirant":
            return self._aspirant_response(query)
        else:
            return "I'm here to help with your academic needs. How can I assist you today?"
    
    def generate_study_content_with_ai(self, topic: str, level: str) -> Dict:
        """Generate study content using Gemini AI"""
        if not self.gemini_available:
            return self._get_fallback_content(topic, level)
        
        try:
            prompt = f"""Generate study content for "{topic}" at {level} level.
            
            Return in this exact JSON format (no markdown, just JSON):
            {{
                "overview": "brief overview of the topic",
                "key_concepts": ["concept1", "concept2", "concept3"],
                "detailed_notes": "detailed explanation of the topic",
                "examples": ["example1", "example2"],
                "practice_questions": ["question1", "question2", "question3"],
                "summary": "key takeaways summary"
            }}
            
            Make it educational and age-appropriate for {level} level."""
            
            response = self.gemini_model.generate_content(prompt)
            response_text = response.text
            
          
            response_text = response_text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(response_text[start:end])
            else:
                return self._get_fallback_content(topic, level)
        except Exception as e:
            print(f"Content generation error: {e}")
            return self._get_fallback_content(topic, level)
    
    def generate_quiz_with_ai(self, topic: str, num_questions: int) -> Dict:
        """Generate quiz using Gemini AI"""
        if not self.gemini_available:
            return self._get_fallback_quiz(topic, num_questions)
        
        try:
            prompt = f"""Generate a quiz on "{topic}" with exactly {num_questions} questions.
            
            Return in this exact JSON format:
            {{
                "topic": "{topic}",
                "questions": [
                    {{
                        "question": "question text",
                        "options": ["option1", "option2", "option3", "option4"],
                        "correct": 0,
                        "explanation": "explanation of the correct answer"
                    }}
                ]
            }}
            
            Make questions educational and appropriate difficulty. Return ONLY valid JSON."""
            
            response = self.gemini_model.generate_content(prompt)
            response_text = response.text
            

            response_text = response_text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(response_text[start:end])
            else:
                return self._get_fallback_quiz(topic, num_questions)
        except Exception as e:
            print(f"Quiz generation error: {e}")
            return self._get_fallback_quiz(topic, num_questions)
    
    def generate_mindmap_with_ai(self, topic: str) -> Dict:
        """Generate mindmap using Gemini AI"""
        if not self.gemini_available:
            return self._get_fallback_mindmap(topic)
        
        try:
            prompt = f"""Create a mindmap for the topic "{topic}".
            
            Return in JSON format:
            {{
                "topic": "{topic}",
                "branches": [
                    {{
                        "name": "branch name",
                        "subtopics": ["subtopic1", "subtopic2", "subtopic3"]
                    }}
                ]
            }}
            
            Include 3-5 main branches, each with 2-4 subtopics."""
            
            response = self.gemini_model.generate_content(prompt)
            response_text = response.text
            
            
            response_text = response_text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(response_text[start:end])
            else:
                return self._get_fallback_mindmap(topic)
        except Exception as e:
            print(f"Mindmap generation error: {e}")
            return self._get_fallback_mindmap(topic)
    
    def _get_fallback_content(self, topic: str, level: str) -> Dict:
        """Fallback content generation"""
        return {
            "overview": f"Study guide for {topic} at {level} level.",
            "key_concepts": [f"Concept 1 of {topic}", f"Concept 2 of {topic}", f"Concept 3 of {topic}"],
            "detailed_notes": f"Detailed notes for {topic} would appear here. Focus on understanding the fundamentals first.",
            "examples": [f"Example 1 for {topic}", f"Example 2 for {topic}"],
            "practice_questions": [f"Practice question 1 for {topic}", f"Practice question 2 for {topic}", f"Practice question 3 for {topic}"],
            "summary": f"Summary of key points from {topic}"
        }
    
    def _get_fallback_quiz(self, topic: str, num_questions: int) -> Dict:
        """Fallback quiz generation"""
        questions = []
        for i in range(num_questions):
            questions.append({
                "question": f"Sample question {i+1} about {topic}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct": 0,
                "explanation": f"This is a sample explanation for question {i+1}."
            })
        return {
            "topic": topic,
            "questions": questions
        }
    
    def _get_fallback_mindmap(self, topic: str) -> Dict:
        """Fallback mindmap generation"""
        return {
            "topic": topic,
            "branches": [
                {"name": "Introduction", "subtopics": ["Basic concepts", "History", "Importance"]},
                {"name": "Core Concepts", "subtopics": ["Key principles", "Important theories", "Applications"]},
                {"name": "Advanced Topics", "subtopics": ["Complex ideas", "Research areas", "Future scope"]},
                {"name": "Resources", "subtopics": ["Books", "Online courses", "Practice materials"]}
            ]
        }
    
    # ============ YOUR ORIGINAL METHODS (COMPLETELY UNCHANGED) ============
    
    def _school_response(self, query: str) -> str:
        """Generate responses for school students"""
        responses = {
            "homework": "I can help you with your homework! What subject are you working on?",
            "study": "Creating a study schedule is important. Would you like me to help you plan your study time?",
            "exam": "Exam preparation is key. Focus on understanding concepts rather than memorizing.",
            "default": "That's a great question! Let me help you understand this better."
        }
        
        for key in responses:
            if key in query.lower():
                return responses[key]
        return responses["default"]
    
    def _college_response(self, query: str) -> str:
        """Generate responses for college students"""
        responses = {
            "placement": "Placement preparation requires consistent effort. Have you checked our placement guides?",
            "project": "Real-time projects are excellent for learning. Check out our project examples section!",
            "interview": "Interview preparation involves both technical and soft skills. Practice regularly!",
            "default": "Great query! Let me provide you with resources to help with your college studies."
        }
        
        for key in responses:
            if key in query.lower():
                return responses[key]
        return responses["default"]
    
    def _aspirant_response(self, query: str) -> str:
        """Generate responses for exam aspirants"""
        responses = {
            "time": "Time management is crucial. Follow our subject-wise time charts for better preparation.",
            "syllabus": "Cover the syllabus systematically. Start with high-weightage topics first.",
            "mock": "Taking mock tests regularly will improve your performance. Try our assessment tests!",
            "default": "Your dedication to exam preparation is commendable. Let me help you optimize your study plan."
        }
        
        for key in responses:
            if key in query.lower():
                return responses[key]
        return responses["default"]
    
    def get_study_recommendations(self, role: str, performance: Dict = None) -> List[str]:
        """Get study recommendations based on role and performance"""
        if role == "school":
            return [
                "Complete your daily homework on time",
                "Review class notes every day",
                "Practice math problems regularly",
                "Read English newspapers to improve vocabulary"
            ]
        elif role == "college":
            return [
                "Build a strong GitHub portfolio with projects",
                "Practice coding on platforms like LeetCode",
                "Network with alumni for placement tips",
                "Work on real-time projects"
            ]
        else:
            return [
                "Create a 6-month study plan",
                "Take weekly mock tests",
                "Analyze your weak areas and focus on them",
                "Join online test series for practice"
            ]