from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import os
import json
import uvicorn
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv


load_dotenv()


app = FastAPI(
    title="Smart Academic Assistant API",
    description="AI-Powered Learning Platform API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please check your .env file.")


client = Groq(api_key=GROQ_API_KEY)
model = "llama-3.3-70b-versatile"

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    topic: Optional[str] = None
    level: Optional[str] = "Intermediate"

class QuizRequest(BaseModel):
    topic: str
    num_questions: int = 10
    level: str = "Intermediate"

class ContentRequest(BaseModel):
    topic: str
    level: str = "Intermediate"

class MindmapRequest(BaseModel):
    topic: str
    level: str = "Intermediate"

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str
    role: str

@app.get("/")
async def root():
    return {
        "message": "🎓 Smart Academic Assistant API is running!",
        "status": "active",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "health": "/health",
            "generate_content": "/generate/content (POST)",
            "generate_quiz": "/generate/quiz (POST)",
            "generate_mindmap": "/generate/mindmap (POST)",
            "chat": "/chat (POST)",
            "auth_login": "/auth/login (POST)",
            "auth_register": "/auth/register (POST)"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "groq_api_configured": bool(GROQ_API_KEY)
    }

@app.post("/generate/content")
async def generate_content(request: ContentRequest):
    """Generate educational content based on topic and level"""
    try:
        level_descriptions = {
            "Beginner": "basic introduction, simple explanations, no prior knowledge assumed",
            "Intermediate": "moderate depth, assumes basic knowledge, includes practical examples",
            "Advanced": "deep technical details, advanced concepts, real-world applications and best practices"
        }
        
        prompt = f"""You are an expert educator. Create comprehensive {request.level} level educational content about "{request.topic}".

Level Description: {level_descriptions.get(request.level, level_descriptions['Intermediate'])}

Format your response as JSON with EXACTLY this structure:
{{
    "definition": "A clear, 2-3 sentence definition appropriate for {request.level} level",
    "detailed_overview": "A detailed 4-5 paragraph explanation with {request.level} level depth and examples",
    "key_concepts": [
        "Key concept 1 with detailed explanation",
        "Key concept 2 with detailed explanation",
        "Key concept 3 with detailed explanation",
        "Key concept 4 with detailed explanation",
        "Key concept 5 with detailed explanation"
    ],
    "practical_examples": [
        "Practical example 1 relevant to {request.level} level",
        "Practical example 2 relevant to {request.level} level",
        "Practical example 3 relevant to {request.level} level"
    ],
    "summary": "A concise 2-3 sentence summary highlighting key takeaways for {request.level} learners"
}}

Make the content educational, engaging, and appropriate for {request.level} level learners."""

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert educator. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4096
        )
        
        content = response.choices[0].message.content
        content = content.replace('```json', '').replace('```', '').strip()
        result = json.loads(content)
        
        return {"success": True, "data": result, "topic": request.topic, "level": request.level}
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.post("/generate/quiz")
async def generate_quiz(request: QuizRequest):
    """Generate quiz questions based on topic and level"""
    try:
        prompt = f"""Create a {request.level} level quiz about "{request.topic}" with exactly {request.num_questions} questions.

Format your response as JSON with EXACTLY this structure:
{{
    "topic": "{request.topic}",
    "level": "{request.level}",
    "questions": [
        {{
            "question": "Question text here",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0,
            "explanation": "Detailed explanation"
        }}
    ]
}}

Each question must have exactly 4 options. 'correct' must be the index (0-3) of the correct answer.
Provide ONLY valid JSON in your response."""

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert quiz creator. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=4096
        )
        
        content = response.choices[0].message.content
        content = content.replace('```json', '').replace('```', '').strip()
        result = json.loads(content)
        
        return {"success": True, "data": result}
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.post("/generate/mindmap")
async def generate_mindmap(request: MindmapRequest):
    """Generate learning roadmap/mindmap based on topic and level"""
    try:
        prompt = f"""Create a {request.level} level learning roadmap/mindmap for mastering "{request.topic}".

Format your response as JSON with EXACTLY this structure:
{{
    "topic": "{request.topic}",
    "level": "{request.level}",
    "central_concept": "The main concept in one sentence",
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

Create 4-6 main branches with 4-6 subtopics each.
Provide ONLY valid JSON in your response."""

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert curriculum designer. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4096
        )
        
        content = response.choices[0].message.content
        content = content.replace('```json', '').replace('```', '').strip()
        result = json.loads(content)
        
        return {"success": True, "data": result}
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.post("/chat")
async def chat(request: ChatRequest):
    """Interactive chat with AI assistant"""
    try:
        system_prompt = """You are a helpful educational assistant. Help students with their academic questions, 
        provide explanations, study tips, and guidance. Be supportive and educational."""
        
        messages = [{"role": "system", "content": system_prompt}]
        for msg in request.messages:
            messages.append({"role": msg.role, "content": msg.content})
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )
        
        return {
            "success": True,
            "response": response.choices[0].message.content,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


users_db = {}

@app.post("/auth/register")
async def register(request: RegisterRequest):
    """Register a new user"""
    try:
        if request.username in users_db:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Username already exists"}
            )
        
        users_db[request.username] = {
            "username": request.username,
            "password": request.password,
            "email": request.email,
            "role": request.role,
            "created_at": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "message": "Registration successful",
            "user": {"username": request.username, "role": request.role}
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": str(e)}
        )

@app.post("/auth/login")
async def login(request: LoginRequest):
    """Login user"""
    try:
        user = users_db.get(request.username)
        
        if not user or user["password"] != request.password:
            return JSONResponse(
                status_code=401,
                content={"success": False, "message": "Invalid credentials"}
            )
        
        return {
            "success": True,
            "message": "Login successful",
            "user": {"username": request.username, "role": user["role"]}
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": str(e)}
        )

@app.get("/materials/school/{subject}")
async def get_school_materials(subject: str):
    """Get school study materials by subject"""
    materials = {
        "Mathematics": {
            "Algebra": "Comprehensive Algebra guide",
            "Geometry": "Geometry concepts",
            "Calculus": "Calculus fundamentals"
        },
        "Science": {
            "Physics": "Physics fundamentals",
            "Chemistry": "Chemical reactions",
            "Biology": "Living organisms"
        },
        "English": {
            "Grammar": "Grammar rules",
            "Literature": "Literary analysis"
        },
        "Social Studies": {
            "History": "Historical events",
            "Geography": "Physical geography"
        },
        "Computer Science": {
            "Programming": "Programming basics",
            "Web Development": "Web technologies"
        }
    }
    
    return {
        "success": True,
        "subject": subject,
        "materials": materials.get(subject, {})
    }

@app.get("/materials/placement")
async def get_placement_guides():
    """Get placement preparation guides"""
    guides = {
        "Aptitude Test Guide": "Complete aptitude preparation",
        "Technical Interview Guide": "Technical questions",
        "HR Interview Guide": "HR interview tips",
        "Resume Building Guide": "Resume creation guide"
    }
    
    return {"success": True, "guides": guides}

@app.get("/projects")
async def get_projects():
    """Get project examples"""
    projects = [
        {
            "id": 1,
            "title": "E-commerce Website",
            "description": "Full-stack e-commerce platform",
            "technologies": ["React", "Node.js", "MongoDB"],
            "features": ["Authentication", "Products", "Cart", "Payment"]
        },
        {
            "id": 2,
            "title": "Task Management App",
            "description": "Project management tool",
            "technologies": ["Vue.js", "Express", "PostgreSQL"],
            "features": ["Tasks", "Real-time", "Collaboration"]
        }
    ]
    
    return {"success": True, "projects": projects}

@app.get("/tests/assessment")
async def get_assessment_tests():
    """Get assessment tests"""
    tests = [
        {
            "id": 1,
            "name": "Quantitative Aptitude Test",
            "duration": "45 minutes",
            "difficulty": "Medium",
            "topics": ["Number System", "Algebra", "Geometry"]
        },
        {
            "id": 2,
            "name": "Logical Reasoning Test",
            "duration": "35 minutes",
            "difficulty": "Medium",
            "topics": ["Analytical", "Puzzles"]
        }
    ]
    
    return {"success": True, "tests": tests}

@app.get("/time-charts")
async def get_time_charts():
    """Get time allocation charts"""
    charts = {
        "Quantitative Aptitude": {
            "Time Allocation": "60 hours",
            "Weekly Plan": "12 hours per week"
        },
        "Logical Reasoning": {
            "Time Allocation": "50 hours",
            "Weekly Plan": "10 hours per week"
        }
    }
    
    return {"success": True, "charts": charts}

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """HTML dashboard"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Smart Academic Assistant API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                text-align: center;
            }
            .card {
                background: rgba(255,255,255,0.95);
                color: #333;
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
            }
            .docs-link {
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                margin: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎓 Smart Academic Assistant API</h1>
            <p>AI-Powered Learning Platform</p>
            <div class="card">
                <h2>📚 API Documentation</h2>
                <a href="/docs" class="docs-link">📖 Interactive API Docs</a>
                <a href="/redoc" class="docs-link">📕 ReDoc Documentation</a>
            </div>
            <div class="card">
                <h2>🚀 Ready to Use</h2>
                <p>API is running successfully!</p>
                <p>Visit <strong>/docs</strong> for interactive documentation</p>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    print("🚀 Starting Smart Academic Assistant API Server...")
    print("📍 Server will run at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔧 Press CTRL+C to stop the server")
    print("-" * 50)
    
    uvicorn.run(
        app, 
        host="127.0.0.1",  
        port=8000,
        log_level="info",
        reload=False  
    )