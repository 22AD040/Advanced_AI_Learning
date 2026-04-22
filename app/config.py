import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    """Application configuration"""
    SECRET_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyDXyRJAMGDLiSo3M1vwRcz0BuGYnOqaADc')
    APP_NAME = "Smart Academic Assistant Pro"
    DEBUG = os.getenv('DEBUG', False)
    
  
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyDXyRJAMGDLiSo3M1vwRcz0BuGYnOqaADc')
    

    DATA_DIR = "data"
    USERS_FILE = os.path.join(DATA_DIR, "users.json")
    CHATS_FILE = os.path.join(DATA_DIR, "chats.json")
    
  
    ROLES = {
        "school": "School Student",
        "college": "College Student",
        "aspirant": "Exam Aspirant"
    }
    
   
    SCHOOL_SUBJECTS = ["Mathematics", "Science", "English", "Social Studies", "Computer Science"]
    
    
    ASPIRANT_SUBJECTS = ["Quantitative Aptitude", "Logical Reasoning", "English", "General Knowledge", "Technical Subjects"]