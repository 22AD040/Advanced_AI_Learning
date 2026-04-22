import json
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
from app.config import Config
from typing import Dict, List, Any, Optional 

class API:
    """API routes for handling data operations"""
    
    def __init__(self):
        self.chats_file = Config.CHATS_FILE
        self._ensure_chats_file()
        self._ensure_pdf_directory()
        self._init_gemini()  # Initialize Gemini on startup
    
    def _ensure_chats_file(self):
        """Ensure the chats data file exists"""
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        if not os.path.exists(self.chats_file):
            with open(self.chats_file, 'w') as f:
                json.dump([], f)
    
    def _ensure_pdf_directory(self):
        """Ensure PDF directory exists"""
        pdf_dir = os.path.join(Config.DATA_DIR, "pdfs")
        os.makedirs(pdf_dir, exist_ok=True)
        return pdf_dir
    
    def _load_chats(self):
        """Load chats from JSON file"""
        try:
            with open(self.chats_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_chats(self, chats):
        """Save chats to JSON file"""
        with open(self.chats_file, 'w') as f:
            json.dump(chats, f, indent=2)
    
    def save_chat_message(self, username, message, response, role):
        """Save chat interaction"""
        chats = self._load_chats()
        chat_entry = {
            "username": username,
            "role": role,
            "message": message,
            "response": response,
            "timestamp": datetime.now().isoformat()
        }
        chats.append(chat_entry)
        self._save_chats(chats)
    
    def get_user_chats(self, username):
        """Get chat history for a user"""
        chats = self._load_chats()
        return [chat for chat in chats if chat['username'] == username]
    
    def generate_pdf(self, title, content, filename):
        """Generate a real PDF file"""
        pdf_dir = self._ensure_pdf_directory()
        pdf_path = os.path.join(pdf_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Add title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30
        )
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 12))
        
        # Add date
        date_style = ParagraphStyle(
            'DateStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.grey
        )
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", date_style))
        story.append(Spacer(1, 20))
        
        # Add content
        for section in content:
            if isinstance(section, dict):
                story.append(Paragraph(section.get('title', ''), styles['Heading2']))
                story.append(Spacer(1, 10))
                
                for key, value in section.get('items', {}).items():
                    story.append(Paragraph(f"• <b>{key}</b>: {value}", styles['Normal']))
                    story.append(Spacer(1, 6))
            else:
                story.append(Paragraph(section, styles['Normal']))
                story.append(Spacer(1, 10))
        
        doc.build(story)
        return pdf_path
    
    # School Student Resources - COMPLETE STUDY MATERIALS FOR ALL SUBJECTS
    def get_school_study_materials(self, subject):
        """Get study materials for school students with real PDFs for ALL subjects"""
        materials_content = {
            "Mathematics": {
                "Algebra": {
                    "title": "Algebra Study Guide",
                    "content": [
                        {"title": "Chapter 1: Linear Equations", 
                         "items": {
                             "Definition": "Linear equations are equations of the first degree",
                             "Examples": "2x + 3 = 7, 5y - 2 = 13",
                             "Solution Methods": "Isolation method, Substitution method",
                             "Practice Problems": "1) 3x + 5 = 20, 2) 2y - 7 = 11"
                         }},
                        {"title": "Chapter 2: Quadratic Equations",
                         "items": {
                             "Standard Form": "ax² + bx + c = 0",
                             "Quadratic Formula": "x = [-b ± √(b² - 4ac)] / 2a",
                             "Discriminant": "D = b² - 4ac",
                             "Nature of Roots": "If D>0: Real roots, D=0: Equal roots, D<0: No real roots"
                         }},
                        {"title": "Chapter 3: Polynomials",
                         "items": {
                             "Degree": "Highest power of variable",
                             "Types": "Linear, Quadratic, Cubic",
                             "Operations": "Addition, Subtraction, Multiplication"
                         }}
                    ]
                },
                "Geometry": {
                    "title": "Geometry Fundamentals",
                    "content": [
                        {"title": "Basic Shapes",
                         "items": {
                             "Triangle": "Area = ½ × base × height, Sum of angles = 180°",
                             "Circle": "Area = πr², Circumference = 2πr",
                             "Rectangle": "Area = length × width, Perimeter = 2(l+w)",
                             "Square": "Area = side², Perimeter = 4 × side"
                         }},
                        {"title": "Important Theorems",
                         "items": {
                             "Pythagorean Theorem": "a² + b² = c² (for right triangles)",
                             "Angle Sum Property": "Sum of angles in triangle = 180°",
                             "Circle Theorems": "Angle in semicircle = 90°"
                         }}
                    ]
                },
                "Calculus": {
                    "title": "Introduction to Calculus",
                    "content": [
                        {"title": "Differentiation",
                         "items": {
                             "Derivative": "Rate of change of a function",
                             "Basic Rules": "d/dx(x^n) = nx^(n-1)",
                             "Applications": "Finding maxima/minima, velocity, acceleration"
                         }},
                        {"title": "Integration",
                         "items": {
                             "Integral": "Area under a curve",
                             "Basic Rules": "∫x^n dx = x^(n+1)/(n+1) + C",
                             "Applications": "Area, volume, work done"
                         }}
                    ]
                }
            },
            "Science": {
                "Physics": {
                    "title": "Physics Fundamentals",
                    "content": [
                        {"title": "Newton's Laws of Motion",
                         "items": {
                             "First Law": "Law of Inertia - Objects resist change in motion",
                             "Second Law": "F = ma (Force = mass × acceleration)",
                             "Third Law": "Action-Reaction - Every action has equal opposite reaction"
                         }},
                        {"title": "Work, Energy & Power",
                         "items": {
                             "Work": "W = F × d × cosθ",
                             "Kinetic Energy": "KE = ½mv²",
                             "Potential Energy": "PE = mgh",
                             "Power": "P = W/t"
                         }},
                        {"title": "Electricity",
                         "items": {
                             "Ohm's Law": "V = IR",
                             "Resistance": "R = ρL/A",
                             "Power": "P = VI = I²R"
                         }}
                    ]
                },
                "Chemistry": {
                    "title": "Chemistry Basics",
                    "content": [
                        {"title": "Atomic Structure",
                         "items": {
                             "Proton": "Positive charge, in nucleus",
                             "Neutron": "Neutral charge, in nucleus",
                             "Electron": "Negative charge, orbits nucleus"
                         }},
                        {"title": "Chemical Bonding",
                         "items": {
                             "Ionic Bond": "Transfer of electrons",
                             "Covalent Bond": "Sharing of electrons",
                             "Metallic Bond": "Sea of electrons"
                         }},
                        {"title": "Chemical Reactions",
                         "items": {
                             "Combination": "A + B → AB",
                             "Decomposition": "AB → A + B",
                             "Displacement": "A + BC → AC + B"
                         }}
                    ]
                },
                "Biology": {
                    "title": "Biology Essentials",
                    "content": [
                        {"title": "Cell Structure",
                         "items": {
                             "Nucleus": "Control center of cell",
                             "Mitochondria": "Power house of cell",
                             "Ribosomes": "Protein synthesis",
                             "Cell Membrane": "Semi-permeable barrier"
                         }},
                        {"title": "Human Body Systems",
                         "items": {
                             "Digestive System": "Breaks down food",
                             "Respiratory System": "Gas exchange",
                             "Circulatory System": "Transport of nutrients"
                         }}
                    ]
                }
            },
            "English": {
                "Grammar": {
                    "title": "English Grammar Guide",
                    "content": [
                        {"title": "Parts of Speech",
                         "items": {
                             "Noun": "Person, place, or thing",
                             "Verb": "Action or state of being",
                             "Adjective": "Describes noun",
                             "Adverb": "Describes verb"
                         }},
                        {"title": "Tenses",
                         "items": {
                             "Present": "I eat, I am eating, I have eaten",
                             "Past": "I ate, I was eating, I had eaten",
                             "Future": "I will eat, I will be eating, I will have eaten"
                         }}
                    ]
                },
                "Literature": {
                    "title": "Literature Study Guide",
                    "content": [
                        {"title": "Literary Devices",
                         "items": {
                             "Metaphor": "Direct comparison",
                             "Simile": "Comparison using 'like' or 'as'",
                             "Personification": "Giving human qualities to objects"
                         }},
                        {"title": "Writing Skills",
                         "items": {
                             "Essay Writing": "Introduction, Body, Conclusion",
                             "Letter Writing": "Formal and informal letters",
                             "Story Writing": "Plot, characters, setting, theme"
                         }}
                    ]
                }
            },
            "Social Studies": {
                "History": {
                    "title": "World History",
                    "content": [
                        {"title": "Ancient Civilizations",
                         "items": {
                             "Indus Valley": "Advanced urban planning",
                             "Egyptian": "Pyramids and hieroglyphics",
                             "Greek": "Democracy and philosophy"
                         }},
                        {"title": "Modern History",
                         "items": {
                             "Industrial Revolution": "Machines and factories",
                             "World Wars": "Global conflicts",
                             "Independence Movements": "Freedom from colonial rule"
                         }}
                    ]
                },
                "Geography": {
                    "title": "Geography Guide",
                    "content": [
                        {"title": "Physical Geography",
                         "items": {
                             "Mountains": "Fold mountains, volcanic mountains",
                             "Rivers": "Upper, middle, lower course",
                             "Climate": "Tropical, temperate, polar zones"
                         }},
                        {"title": "Human Geography",
                         "items": {
                             "Population": "Distribution and density",
                             "Urbanization": "City growth and planning",
                             "Resources": "Renewable and non-renewable"
                         }}
                    ]
                }
            },
            "Computer Science": {
                "Programming Basics": {
                    "title": "Programming Fundamentals",
                    "content": [
                        {"title": "Programming Concepts",
                         "items": {
                             "Variables": "Store data values",
                             "Data Types": "Integer, float, string, boolean",
                             "Control Structures": "If-else, loops, functions"
                         }},
                        {"title": "Algorithms",
                         "items": {
                             "Sorting": "Bubble sort, Quick sort",
                             "Searching": "Linear search, Binary search",
                             "Complexity": "Time and space complexity"
                         }}
                    ]
                },
                "Web Development": {
                    "title": "Web Development Basics",
                    "content": [
                        {"title": "HTML",
                         "items": {
                             "Tags": "html, head, body, div, p",
                             "Attributes": "class, id, src, href",
                             "Forms": "input, select, textarea"
                         }},
                        {"title": "CSS",
                         "items": {
                             "Selectors": "Element, class, ID selectors",
                             "Properties": "color, margin, padding, display",
                             "Layout": "Flexbox, Grid"
                         }}
                    ]
                }
            }
        }
        
        subject_data = materials_content.get(subject, {})
        if subject_data:
            pdf_files = {}
            for topic, content in subject_data.items():
                filename = f"{subject}_{topic}_{datetime.now().strftime('%Y%m%d')}.pdf"
                pdf_path = self.generate_pdf(content['title'], content['content'], filename)
                with open(pdf_path, 'rb') as f:
                    pdf_files[topic] = f.read()
            return pdf_files
        return {}
    
    def get_exam_time_chart(self):
        """Get exam preparation time chart"""
        return {
            "Daily Study Plan": {
                "Morning (6-8 AM)": "Revision & Practice",
                "Mid-Morning (9-12 PM)": "New Topics",
                "Afternoon (2-4 PM)": "Problem Solving",
                "Evening (5-7 PM)": "Mock Tests",
                "Night (8-10 PM)": "Light Revision"
            },
            "Weekly Schedule": {
                "Monday": "Mathematics",
                "Tuesday": "Science",
                "Wednesday": "English",
                "Thursday": "Social Studies",
                "Friday": "Computer Science",
                "Saturday": "Practice Tests",
                "Sunday": "Revision & Rest"
            }
        }
    
    # College Student Resources
    def get_placement_guides(self):
        """Get placement preparation guides with real PDFs"""
        guides_content = {
            "Resume Building": {
                "title": "Professional Resume Building Guide",
                "content": [
                    {"title": "Resume Sections",
                     "items": {
                         "Contact Info": "Name, phone, email, LinkedIn profile",
                         "Professional Summary": "2-3 sentences highlighting your profile",
                         "Education": "Degrees, institutions, GPA, relevant courses",
                         "Experience": "Internships, projects, work experience",
                         "Technical Skills": "Programming languages, tools, technologies",
                         "Achievements": "Awards, certifications, publications"
                     }},
                    {"title": "Tips for Success",
                     "items": {
                         "Length": "1 page for freshers, 2 pages for experienced",
                         "Format": "PDF format preferred for submission",
                         "Keywords": "Use ATS-friendly keywords from job description",
                         "Action Verbs": "Use strong action verbs (developed, managed, created)",
                         "Quantify": "Use numbers to show impact (increased by 20%)"
                     }}
                ]
            },
            "Aptitude Tests": {
                "title": "Aptitude Test Preparation Guide",
                "content": [
                    {"title": "Quantitative Aptitude",
                     "items": {
                         "Percentages": "Profit/Loss, Discount, Interest",
                         "Ratios": "Proportions, Mixtures, Partnerships",
                         "Averages": "Mean, Median, Mode",
                         "Time & Work": "Work efficiency, Pipes & cisterns",
                         "Time & Distance": "Speed, Distance, Time relationships"
                     }},
                    {"title": "Logical Reasoning",
                     "items": {
                         "Blood Relations": "Family tree problems",
                         "Syllogisms": "Deductive reasoning",
                         "Analogies": "Word and number analogies",
                         "Coding-Decoding": "Pattern recognition",
                         "Series Completion": "Number and letter series"
                     }}
                ]
            },
            "Technical Interviews": {
                "title": "Technical Interview Preparation",
                "content": [
                    {"title": "Data Structures",
                     "items": {
                         "Arrays": "Operations, sorting, searching",
                         "Linked Lists": "Singly, doubly, circular",
                         "Stacks & Queues": "LIFO and FIFO implementations",
                         "Trees": "Binary trees, BST, traversals",
                         "Graphs": "BFS, DFS, shortest path"
                     }},
                    {"title": "Algorithms",
                     "items": {
                         "Sorting": "Bubble, Quick, Merge, Heap sort",
                         "Searching": "Linear, Binary, Interpolation search",
                         "Dynamic Programming": "Memoization, tabulation",
                         "Greedy Algorithms": "Activity selection, Huffman coding"
                     }}
                ]
            },
            "HR Interview Tips": {
                "title": "HR Interview Success Guide",
                "content": [
                    {"title": "Common Questions",
                     "items": {
                         "Tell me about yourself": "30-second elevator pitch focusing on achievements",
                         "Strengths & Weaknesses": "Be honest but strategic with improvement plan",
                         "Why this company": "Show research and alignment with goals",
                         "Where do you see yourself in 5 years": "Show ambition and growth mindset",
                         "Why should we hire you": "Highlight unique value proposition"
                     }},
                    {"title": "Preparation Tips",
                     "items": {
                         "Company Research": "Know their products, culture, values",
                         "Dress Code": "Formal business attire",
                         "Body Language": "Maintain eye contact, sit straight",
                         "Follow-up": "Send thank you email within 24 hours",
                         "Questions to Ask": "Ask about growth, culture, expectations"
                     }}
                ]
            },
            "Group Discussion": {
                "title": "Group Discussion Mastery",
                "content": [
                    {"title": "GD Topics",
                     "items": {
                         "Current Affairs": "Politics, economy, technology trends",
                         "Abstract Topics": "Creative thinking and innovation",
                         "Case Studies": "Business scenarios and problem-solving",
                         "Controversial Topics": "Handle with maturity and facts"
                     }},
                    {"title": "Success Tips",
                     "items": {
                         "Initiate": "Start the discussion if you're confident",
                         "Listen Actively": "Acknowledge others' valid points",
                         "Be Relevant": "Stay on topic, avoid deviation",
                         "Summarize": "Conclude with key points discussed",
                         "Be Polite": "Don't interrupt, respect others"
                     }}
                ]
            }
        }
        
        # Generate PDFs for each guide
        pdf_guides = {}
        for guide_name, content in guides_content.items():
            filename = f"Placement_Guide_{guide_name}_{datetime.now().strftime('%Y%m%d')}.pdf"
            pdf_path = self.generate_pdf(content['title'], content['content'], filename)
            with open(pdf_path, 'rb') as f:
                pdf_guides[guide_name] = f.read()
        return pdf_guides
    
    def get_quizzes(self):
        """Get quizzes with actual questions"""
        return [
            {
                "id": 1,
                "title": "Data Structures Quiz",
                "questions": [
                    {
                        "question": "What is the time complexity of binary search?",
                        "options": ["O(n)", "O(log n)", "O(n²)", "O(1)"],
                        "correct": 1,
                        "explanation": "Binary search has O(log n) time complexity as it divides the search space in half each time."
                    },
                    {
                        "question": "Which data structure uses LIFO (Last In First Out)?",
                        "options": ["Queue", "Stack", "Array", "Linked List"],
                        "correct": 1,
                        "explanation": "Stack follows LIFO principle - last element added is first to be removed."
                    },
                    {
                        "question": "What is a hash table used for?",
                        "options": ["Sorting", "Searching", "Key-value storage", "Graph traversal"],
                        "correct": 2,
                        "explanation": "Hash tables store key-value pairs for efficient lookup with O(1) average time."
                    },
                    {
                        "question": "Which of the following is a linear data structure?",
                        "options": ["Tree", "Graph", "Array", "Hash Table"],
                        "correct": 2,
                        "explanation": "Array is a linear data structure where elements are stored in contiguous memory locations."
                    }
                ]
            },
            {
                "id": 2,
                "title": "Aptitude Test",
                "questions": [
                    {
                        "question": "If a car travels 60 km in 1 hour, how far will it travel in 2.5 hours?",
                        "options": ["120 km", "150 km", "180 km", "200 km"],
                        "correct": 1,
                        "explanation": "Speed = 60 km/h, Distance = Speed × Time = 60 × 2.5 = 150 km"
                    },
                    {
                        "question": "What is 15% of 200?",
                        "options": ["15", "20", "30", "35"],
                        "correct": 2,
                        "explanation": "15% of 200 = (15/100) × 200 = 30"
                    },
                    {
                        "question": "If 5 workers can complete a task in 10 days, how many workers needed to complete it in 5 days?",
                        "options": ["5", "7", "10", "12"],
                        "correct": 2,
                        "explanation": "Work = Workers × Days, so 5 × 10 = 50 worker-days. For 5 days: 50/5 = 10 workers"
                    },
                    {
                        "question": "What is the next number in the sequence: 2, 6, 12, 20, ?",
                        "options": ["28", "30", "32", "34"],
                        "correct": 1,
                        "explanation": "Pattern: 1×2=2, 2×3=6, 3×4=12, 4×5=20, 5×6=30"
                    }
                ]
            },
            {
                "id": 3,
                "title": "Programming Concepts",
                "questions": [
                    {
                        "question": "What does OOP stand for?",
                        "options": ["Object-Oriented Programming", "Order of Operations", "Object Organization Protocol", "Output Optimization Process"],
                        "correct": 0,
                        "explanation": "OOP stands for Object-Oriented Programming, a programming paradigm based on objects."
                    },
                    {
                        "question": "Which of these is NOT an OOP concept?",
                        "options": ["Inheritance", "Polymorphism", "Encapsulation", "Compilation"],
                        "correct": 3,
                        "explanation": "Compilation is a process, not an OOP concept. The main OOP concepts are inheritance, polymorphism, encapsulation, and abstraction."
                    },
                    {
                        "question": "What is a constructor?",
                        "options": ["A function to destroy objects", "A special method to initialize objects", "A type of variable", "A loop structure"],
                        "correct": 1,
                        "explanation": "A constructor is a special method that is automatically called when an object is created to initialize it."
                    }
                ]
            }
        ]
    
    def evaluate_quiz(self, quiz_id, answers):
        """Evaluate quiz answers and return score"""
        quizzes = self.get_quizzes()
        quiz = next((q for q in quizzes if q['id'] == quiz_id), None)
        
        if not quiz:
            return None
        
        score = 0
        results = []
        
        for i, question in enumerate(quiz['questions']):
            is_correct = (answers.get(str(i)) == question['correct'])
            if is_correct:
                score += 1
            results.append({
                'question': question['question'],
                'user_answer': question['options'][answers.get(str(i), 0)],
                'correct_answer': question['options'][question['correct']],
                'is_correct': is_correct,
                'explanation': question['explanation']
            })
        
        return {
            'score': score,
            'total': len(quiz['questions']),
            'percentage': (score / len(quiz['questions'])) * 100,
            'results': results
        }
    
    def get_project_solutions(self):
        """Get real-time project examples"""
        return [
            {
                "title": "E-commerce Website",
                "description": "Full-stack e-commerce solution with payment integration, user authentication, and product management.",
                "technologies": ["React", "Node.js", "MongoDB", "Express", "Stripe"],
                "features": ["User login/signup", "Product search/filter", "Shopping cart", "Payment gateway", "Order tracking", "Admin dashboard"],
                "github_link": "https://github.com/example/ecommerce",
                "demo_link": "https://ecommerce-demo.example.com"
            },
            {
                "title": "Chat Application",
                "description": "Real-time chat app with WebSocket, user rooms, and file sharing capabilities.",
                "technologies": ["Socket.io", "Express", "React", "MongoDB"],
                "features": ["Real-time messaging", "User rooms", "File sharing", "Message history", "Typing indicators", "Online status"],
                "github_link": "https://github.com/example/chatapp",
                "demo_link": "https://chat-demo.example.com"
            },
            {
                "title": "Task Management System",
                "description": "Project management tool with task assignment, deadlines, and progress tracking.",
                "technologies": ["Django", "PostgreSQL", "Bootstrap", "JavaScript", "Chart.js"],
                "features": ["Task creation/assignment", "Deadline tracking", "Progress reports", "Team collaboration", "File attachments", "Email notifications"],
                "github_link": "https://github.com/example/taskmanager",
                "demo_link": "https://tasks-demo.example.com"
            },
            {
                "title": "Weather App",
                "description": "Real-time weather application with location-based forecasts and interactive maps.",
                "technologies": ["React", "OpenWeather API", "Chart.js", "CSS3"],
                "features": ["Current weather", "5-day forecast", "Search by city", "Temperature conversion", "Weather maps", "Responsive design"],
                "github_link": "https://github.com/example/weatherapp",
                "demo_link": "https://youtu.be/sn6GLgaTY0M?si=-CfCb2HtbGcZZTlW"
            }
        ]
    
    # Exam Aspirant Resources - WITH WORKING ASSESSMENT TESTS
    def get_subject_time_charts(self):
        """Get time chart guidance for each subject"""
        return {
            "Quantitative Aptitude": {
                "Topics": ["Number System", "Algebra", "Geometry", "Trigonometry", "Statistics", "Probability"],
                "Time Allocation": "40 hours",
                "Weekly Plan": "8 hours/week for 5 weeks",
                "Daily Schedule": "2 hours daily for Math practice",
                "Important Chapters": ["Percentages", "Ratios", "Averages", "Time & Work", "Time & Distance"]
            },
            "Logical Reasoning": {
                "Topics": ["Analytical Reasoning", "Verbal Reasoning", "Data Sufficiency", "Blood Relations", "Syllogisms", "Coding-Decoding"],
                "Time Allocation": "30 hours",
                "Weekly Plan": "6 hours/week for 5 weeks",
                "Daily Schedule": "1.5 hours daily for Reasoning",
                "Important Chapters": ["Puzzles", "Seating Arrangement", "Direction Sense", "Clock & Calendar"]
            },
            "English": {
                "Topics": ["Vocabulary", "Grammar", "Reading Comprehension", "Sentence Correction", "Para Jumbles", "Cloze Test"],
                "Time Allocation": "25 hours",
                "Weekly Plan": "5 hours/week for 5 weeks",
                "Daily Schedule": "1 hour daily for English",
                "Important Chapters": ["Synonyms/Antonyms", "Idioms & Phrases", "Active/Passive Voice", "Direct/Indirect Speech"]
            },
            "General Knowledge": {
                "Topics": ["Current Affairs", "History", "Geography", "Polity", "Economics", "Science & Technology"],
                "Time Allocation": "35 hours",
                "Weekly Plan": "7 hours/week for 5 weeks",
                "Daily Schedule": "1.5 hours daily for GK",
                "Important Chapters": ["Indian Constitution", "World Organizations", "Awards & Honors", "Sports"]
            }
        }
    
    def get_quick_tips(self):
        """Get quick tips to cover syllabus"""
        return [
            "📅 Create a realistic study schedule and stick to it",
            "📝 Practice previous year question papers regularly",
            "🧠 Focus on understanding concepts, not memorization",
            "⏰ Take regular breaks using Pomodoro technique (25 min study, 5 min break)",
            "👥 Join study groups for collaborative learning",
            "🎯 Use mnemonic devices for memorizing facts",
            "🔄 Review and revise regularly (spaced repetition)",
            "📰 Stay updated with current affairs daily",
            "📊 Take weekly mock tests to track progress",
            "💪 Maintain a healthy lifestyle - exercise, sleep, and diet matter!",
            "📱 Use educational apps for on-the-go learning",
            "🎯 Set daily, weekly, and monthly goals",
            "📹 Watch video tutorials for difficult topics",
            "📚 Make your own notes for quick revision"
        ]
    
    def get_assessment_tests(self):
        """Get assessment tests for aspirants with actual questions"""
        return [
            {
                "id": 1,
                "name": "Quantitative Assessment",
                "questions": [
                    {
                        "question": "If 15% of x = 45, then x = ?",
                        "options": ["200", "250", "300", "350"],
                        "correct": 2,
                        "explanation": "15% of x = 45 → x × 15/100 = 45 → x = 45 × 100/15 = 300"
                    },
                    {
                        "question": "What is the average of first 10 natural numbers?",
                        "options": ["5", "5.5", "6", "6.5"],
                        "correct": 1,
                        "explanation": "Sum of first 10 natural numbers = 55, Average = 55/10 = 5.5"
                    },
                    {
                        "question": "If a : b = 2 : 3 and b : c = 4 : 5, find a : c",
                        "options": ["8:15", "6:15", "8:12", "6:12"],
                        "correct": 0,
                        "explanation": "a:b = 2:3 = 8:12, b:c = 4:5 = 12:15, therefore a:c = 8:15"
                    },
                    {
                        "question": "A train travels 360 km in 4 hours. What is its speed in m/s?",
                        "options": ["20 m/s", "25 m/s", "30 m/s", "35 m/s"],
                        "correct": 1,
                        "explanation": "Speed = 360/4 = 90 km/h = 90 × 5/18 = 25 m/s"
                    },
                    {
                        "question": "If 20 workers can complete a work in 15 days, how many workers needed to complete it in 10 days?",
                        "options": ["25", "30", "35", "40"],
                        "correct": 1,
                        "explanation": "Work = 20 × 15 = 300 worker-days, Workers needed = 300/10 = 30 workers"
                    }
                ],
                "duration": "45 minutes",
                "difficulty": "Medium",
                "topics": ["Arithmetic", "Algebra", "Averages", "Ratio & Proportion"]
            },
            {
                "id": 2,
                "name": "Reasoning Assessment",
                "questions": [
                    {
                        "question": "If 'MAN' is coded as 'NBO', how is 'BOY' coded?",
                        "options": ["CPZ", "CPY", "COZ", "BPZ"],
                        "correct": 0,
                        "explanation": "Each letter is replaced by the next letter: M→N, A→B, N→O, so BOY→CPZ"
                    },
                    {
                        "question": "Find the odd one out: Apple, Mango, Orange, Banana, Potato",
                        "options": ["Apple", "Potato", "Banana", "Orange"],
                        "correct": 1,
                        "explanation": "Potato is a vegetable, all others are fruits"
                    },
                    {
                        "question": "If 3 + 4 = 21, 5 + 6 = 55, then 4 + 5 = ?",
                        "options": ["20", "36", "45", "41"],
                        "correct": 1,
                        "explanation": "Pattern: (3+4)×3 = 21, (5+6)×5 = 55, (4+5)×4 = 36"
                    },
                    {
                        "question": "Complete the series: 2, 6, 12, 20, ?",
                        "options": ["28", "30", "32", "34"],
                        "correct": 1,
                        "explanation": "Pattern: 1×2=2, 2×3=6, 3×4=12, 4×5=20, 5×6=30"
                    }
                ],
                "duration": "30 minutes",
                "difficulty": "Medium",
                "topics": ["Coding-Decoding", "Series", "Odd One Out", "Pattern Recognition"]
            },
            {
                "id": 3,
                "name": "English Proficiency",
                "questions": [
                    {
                        "question": "Choose the correct spelling:",
                        "options": ["Accommodate", "Acommodate", "Accommodate", "Acomodate"],
                        "correct": 0,
                        "explanation": "Accommodate has double 'c' and double 'm'"
                    },
                    {
                        "question": "Select the synonym of 'Happy':",
                        "options": ["Sad", "Joyful", "Angry", "Tired"],
                        "correct": 1,
                        "explanation": "Joyful means feeling happiness"
                    },
                    {
                        "question": "Fill in the blank: She ______ to the store yesterday.",
                        "options": ["go", "goes", "went", "going"],
                        "correct": 2,
                        "explanation": "Past tense of go is went"
                    },
                    {
                        "question": "Identify the antonym of 'Increase':",
                        "options": ["Grow", "Rise", "Decrease", "Expand"],
                        "correct": 2,
                        "explanation": "Decrease is the opposite of increase"
                    }
                ],
                "duration": "40 minutes",
                "difficulty": "Easy",
                "topics": ["Vocabulary", "Grammar", "Spelling", "Synonyms/Antonyms"]
            },
            {
                "id": 4,
                "name": "Full Mock Test",
                "questions": [
                    {
                        "question": "What is the value of sin 90°?",
                        "options": ["0", "1", "-1", "Not defined"],
                        "correct": 1,
                        "explanation": "sin 90° = 1"
                    },
                    {
                        "question": "Who wrote 'Mahabharata'?",
                        "options": ["Valmiki", "Tulsidas", "Ved Vyasa", "Kalidas"],
                        "correct": 2,
                        "explanation": "Mahabharata was written by Maharishi Ved Vyasa"
                    },
                    {
                        "question": "What is the capital of France?",
                        "options": ["London", "Berlin", "Madrid", "Paris"],
                        "correct": 3,
                        "explanation": "Paris is the capital of France"
                    },
                    {
                        "question": "Which of the following is not a programming language?",
                        "options": ["Python", "Java", "HTML", "C++"],
                        "correct": 2,
                        "explanation": "HTML is a markup language, not a programming language"
                    },
                    {
                        "question": "Who invented the light bulb?",
                        "options": ["Newton", "Einstein", "Edison", "Tesla"],
                        "correct": 2,
                        "explanation": "Thomas Edison invented the practical light bulb"
                    }
                ],
                "duration": "180 minutes",
                "difficulty": "Hard",
                "topics": ["All subjects covered - Mathematics, Reasoning, English, GK"]
            }
        ]
    
    def evaluate_assessment_test(self, test_id, answers):
        """Evaluate assessment test and return score"""
        tests = self.get_assessment_tests()
        test = next((t for t in tests if t['id'] == test_id), None)
        
        if not test:
            return None
        
        score = 0
        results = []
        
        for i, question in enumerate(test['questions']):
            user_answer = answers.get(str(i))
            is_correct = (user_answer == question['correct'])
            if is_correct:
                score += 1
            results.append({
                'question': question['question'],
                'user_answer': question['options'][user_answer] if user_answer is not None else "Not answered",
                'correct_answer': question['options'][question['correct']],
                'is_correct': is_correct,
                'explanation': question['explanation']
            })
        
        return {
            'score': score,
            'total': len(test['questions']),
            'percentage': (score / len(test['questions'])) * 100,
            'results': results,
            'test_name': test['name']
        }
    
              # ============ GEMINI AI POWERED METHODS (ENHANCED) ============
    
    def _init_gemini(self):
        """Initialize Gemini AI if available"""
        self.gemini_available = False
        try:
            if Config.GEMINI_API_KEY and Config.GEMINI_API_KEY != "AIzaSyDXyRJAMGDLiSo3M1vwRcz0BuGYnOqaADc":
                import google.generativeai as genai
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
                self.gemini_available = True
                print("Gemini AI initialized successfully with gemini-2.5-flash")
            else:
                print("No valid Gemini API key found")
        except Exception as e:
            print(f"Gemini init error: {e}")
    
    def generate_content_with_gemini(self, topic: str, level: str) -> Dict:
        """Generate creative study content with actual explanations and answers"""
        if not hasattr(self, 'gemini_available'):
            self._init_gemini()
        
        if not self.gemini_available:
            return self._get_fallback_content(topic, level)
        
        try:
            # IMPROVED PROMPT - Now asks for EXPLANATIONS, not questions
            prompt = f"""You are an expert teacher. Create a comprehensive study guide for "{topic}" at {level} level.

IMPORTANT: Return ONLY valid JSON. The "practice_questions" should contain questions WITH their answers/explanation included.

Format exactly like this:
{{
    "overview": "A warm, engaging 2-3 paragraph overview explaining what {topic} is and why it's important to learn. Write in complete sentences with clear explanations.",
    "key_concepts": [
        "<b>Concept 1:</b> Detailed explanation of this concept with examples",
        "<b>Concept 2:</b> Detailed explanation of this concept with real-world applications",
        "<b>Concept 3:</b> Detailed explanation including how it works",
        "<b>Concept 4:</b> Detailed explanation with key points to remember"
    ],
    "detailed_notes": "<h4>📖 Understanding {topic}</h4><p>Write 2-3 detailed paragraphs explaining the fundamentals of {topic}. Include key principles, important facts, and how it works.</p><h4>🔑 Important Details</h4><ul><li>Key point 1 with explanation</li><li>Key point 2 with explanation</li><li>Key point 3 with examples</li></ul><h4>💡 Tips for Mastery</h4><p>Provide practical tips and strategies for learning {topic} effectively.</p>",
    "examples": [
        "<b>Example 1 - Real World:</b> Here's a detailed real-world example of {topic} with step-by-step explanation...",
        "<b>Example 2 - Practical Application:</b> Here's how {topic} is applied in practice with clear explanation...",
        "<b>Example 3 - Problem Solving:</b> Walk through a problem related to {topic} showing the solution process..."
    ],
    "practice_questions": [
        "<b>Question 1:</b> What is [specific aspect of {topic}]?<br><b>Answer:</b> [Provide a complete, detailed answer with explanation]",
        "<b>Question 2:</b> How does [specific concept] work in {topic}?<br><b>Answer:</b> [Provide a thorough explanation with examples]",
        "<b>Question 3:</b> Can you explain [important principle] of {topic}?<br><b>Answer:</b> [Give a comprehensive answer with key points]",
        "<b>Question 4:</b> What are the main applications of {topic}?<br><b>Answer:</b> [List and explain real-world applications]",
        "<b>Question 5:</b> Why is {topic} important to study?<br><b>Answer:</b> [Provide detailed reasoning and benefits]"
    ],
    "summary": "<b>🎯 Key Takeaways:</b><ul><li>Takeaway 1 with brief explanation</li><li>Takeaway 2 with brief explanation</li><li>Takeaway 3 with brief explanation</li><li>Takeaway 4 with brief explanation</li></ul><p><b>Next Steps:</b> Suggestions for further learning about {topic}.</p>"
}}

Make the content educational, accurate, and detailed. Each practice question MUST include the answer with explanation - this is for learning, not testing. Use clear, complete sentences and paragraphs."""
            
            response = self.gemini_model.generate_content(prompt)
            
            import json
            import re
            
            text = response.text.strip()
            
            # Clean markdown code blocks
            if text.startswith('```json'):
                text = text[7:]
            if text.startswith('```'):
                text = text[3:]
            if text.endswith('```'):
                text = text[:-3]
            text = text.strip()
            
            start = text.find('{')
            end = text.rfind('}') + 1
            
            if start != -1 and end > start:
                json_str = text[start:end]
                json_str = re.sub(r',\s*}', '}', json_str)
                json_str = re.sub(r',\s*]', ']', json_str)
                content = json.loads(json_str)
                
                required_keys = ["overview", "key_concepts", "detailed_notes", "examples", "practice_questions", "summary"]
                for key in required_keys:
                    if key not in content:
                        content[key] = [] if key in ["key_concepts", "examples", "practice_questions"] else f"<p>Information about {topic}</p>"
                
                return content
            else:
                return self._get_fallback_content(topic, level)
                
        except Exception as e:
            print(f"Gemini content error: {e}")
            return self._get_fallback_content(topic, level)
    
    def generate_mindmap_with_gemini(self, topic: str) -> Dict:
        """Generate creative mindmap using Gemini AI"""
        if not hasattr(self, 'gemini_available'):
            self._init_gemini()
        
        if not self.gemini_available:
            return self._get_fallback_mindmap(topic)
        
        try:
            prompt = f"""Create a detailed and CREATIVE mindmap for the topic "{topic}".

Return ONLY valid JSON. No markdown.

Format:
{{
    "topic": "{topic}",
    "branches": [
        {{"name": "Main Branch 1 Name", "subtopics": ["subtopic1", "subtopic2", "subtopic3"]}},
        {{"name": "Main Branch 2 Name", "subtopics": ["subtopic1", "subtopic2", "subtopic3"]}},
        {{"name": "Main Branch 3 Name", "subtopics": ["subtopic1", "subtopic2", "subtopic3"]}},
        {{"name": "Main Branch 4 Name", "subtopics": ["subtopic1", "subtopic2"]}}
    ]
}}

Make it comprehensive with 4-6 main branches, each with 2-4 subtopics.
Be creative and educational."""
            
            response = self.gemini_model.generate_content(prompt)
            
            import json
            import re
            
            text = response.text.strip()
            
            if text.startswith('```json'):
                text = text[7:]
            if text.startswith('```'):
                text = text[3:]
            if text.endswith('```'):
                text = text[:-3]
            text = text.strip()
            
            start = text.find('{')
            end = text.rfind('}') + 1
            
            if start != -1 and end > start:
                json_str = text[start:end]
                json_str = re.sub(r',\s*}', '}', json_str)
                json_str = re.sub(r',\s*]', ']', json_str)
                mindmap = json.loads(json_str)
                
                if "branches" not in mindmap:
                    mindmap["branches"] = []
                if len(mindmap["branches"]) < 3:
                    mindmap["branches"].extend(self._get_fallback_mindmap(topic)["branches"])
                
                return mindmap
            
            return self._get_fallback_mindmap(topic)
            
        except Exception as e:
            print(f"Mindmap error: {e}")
            return self._get_fallback_mindmap(topic)
    
    def generate_quiz_with_gemini(self, topic: str, num_questions: int = 10) -> Dict:
        """Generate quiz with 10-15 questions"""
        if not hasattr(self, 'gemini_available'):
            self._init_gemini()
        
        if not self.gemini_available:
            return self._get_fallback_quiz(topic, num_questions)
        
        try:
            prompt = f"""Generate {num_questions} high-quality multiple choice questions about "{topic}".

IMPORTANT: Return ONLY valid JSON array. Make questions varied in difficulty.

Format:
[
    {{
        "question": "Clear, well-phrased question text?",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct": 0,
        "explanation": "Detailed explanation of why this answer is correct"
    }}
]

Requirements:
- Mix of easy (30%), medium (50%), and hard (20%) questions
- Include concept-based, application-based, and analytical questions
- Each explanation should teach something valuable

Generate exactly {num_questions} questions."""
            
            response = self.gemini_model.generate_content(prompt)
            
            import json
            import re
            
            text = response.text.strip()
            
            if text.startswith('```json'):
                text = text[7:]
            if text.startswith('```'):
                text = text[3:]
            if text.endswith('```'):
                text = text[:-3]
            text = text.strip()
            
            start = text.find('[')
            end = text.rfind(']') + 1
            
            if start != -1 and end > start:
                json_str = text[start:end]
                json_str = re.sub(r',\s*}', '}', json_str)
                json_str = re.sub(r',\s*]', ']', json_str)
                questions = json.loads(json_str)
                
                if len(questions) < num_questions:
                    fallback = self._get_fallback_quiz(topic, num_questions - len(questions))
                    questions.extend(fallback["questions"])
                
                return {"topic": topic, "questions": questions[:num_questions]}
            
            return self._get_fallback_quiz(topic, num_questions)
            
        except Exception as e:
            print(f"Quiz error: {e}")
            return self._get_fallback_quiz(topic, num_questions)
    
    def get_ai_chat_response(self, message: str, role: str) -> str:
        """Get AI response for chat using Gemini"""
        if not hasattr(self, 'gemini_available'):
            self._init_gemini()
        
        if not self.gemini_available:
            return "I'm here to help! What would you like to learn about?"
        
        try:
            role_context = {
                "school": "a young school student (ages 12-16). Use simple, fun, encouraging language with examples.",
                "college": "a college student. Provide detailed, practical, career-oriented explanations.",
                "aspirant": "an exam aspirant. Focus on exam strategies, time management, and key concepts."
            }
            
            prompt = f"""You are an AI academic assistant for {role_context.get(role, 'a student')}.

User question: {message}

Provide a helpful, accurate, and concise response. Be supportive, encouraging, and educational.
Use examples where helpful. Keep response to 2-3 paragraphs."""
            
            response = self.gemini_model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"Chat error: {e}")
            return f"I'm here to help with your studies! (Note: AI service temporarily unavailable. Error: {str(e)[:100]})"
    
    def _get_fallback_content(self, topic: str, level: str) -> Dict:
        """Fallback content with actual explanations and answers"""
        return {
            "overview": f"📚 <b>Welcome to your study guide for {topic} at the {level} level!</b><br><br>{topic} is an important subject that helps us understand key concepts in our world. This guide will help you learn the fundamentals and build a strong foundation.",
            "key_concepts": [
                f"<b>Fundamental Understanding:</b> {topic} involves learning core principles that apply to many real-world situations. Understanding these basics is essential for mastery.",
                f"<b>Core Principles:</b> The main principles of {topic} include understanding how components work together, recognizing patterns, and applying logical thinking.",
                f"<b>Practical Applications:</b> {topic} is used in everyday life from technology to nature. Learning these applications helps connect theory to practice.",
                f"<b>Key Terminology:</b> Important terms in {topic} include vocabulary that describes processes, components, and relationships within the subject."
            ],
            "detailed_notes": f"""
<h4>📖 What is {topic}?</h4>
<p><b>{topic}</b> is a fascinating area of study that helps us understand important concepts. At the {level} level, we focus on building a strong foundation of knowledge.</p>

<h4>🔑 Why {topic} Matters</h4>
<ul>
<li><b>Real-world relevance:</b> {topic} appears in many aspects of daily life and professional fields</li>
<li><b>Problem-solving skills:</b> Learning {topic} develops critical thinking and analytical abilities</li>
<li><b>Foundation for advanced topics:</b> Mastering {topic} opens doors to more complex subjects</li>
</ul>

<h4>📝 Key Points to Remember</h4>
<ul>
<li>Start with the basics and build your understanding gradually</li>
<li>Practice applying concepts to real examples</li>
<li>Review and revise regularly to reinforce learning</li>
<li>Connect new information with what you already know</li>
</ul>

<h4>💡 Study Tips for {topic}</h4>
<ul>
<li>Create visual aids like diagrams and mind maps</li>
<li>Explain concepts to someone else to deepen understanding</li>
<li>Use online resources and practice problems</li>
<li>Take breaks and study in focused sessions</li>
</ul>
""",
            "examples": [
                f"<b>Example 1 - Real-World Application:</b> Here's a practical example of how {topic} applies in everyday life.",
                f"<b>Example 2 - Step-by-Step:</b> Let's walk through an example of {topic} step by step.",
                f"<b>Example 3 - Problem Solving:</b> Consider this scenario involving {topic} and how to solve it."
            ],
            "practice_questions": [
                f"<b>Question 1:</b> What are the main concepts of {topic}?<br><br><b>Answer:</b> The main concepts include understanding fundamental principles and applying them to real-world situations.",
                f"<b>Question 2:</b> How does {topic} relate to everyday life?<br><br><b>Answer:</b> {topic} relates to everyday life in many ways, from technology to natural phenomena.",
                f"<b>Question 3:</b> Can you explain {topic} in your own words?<br><br><b>Answer:</b> {topic} is about understanding how different elements work together.",
                f"<b>Question 4:</b> What skills are developed by learning {topic}?<br><br><b>Answer:</b> Learning {topic} develops critical thinking and problem-solving abilities.",
                f"<b>Question 5:</b> How can I improve my understanding of {topic}?<br><br><b>Answer:</b> Practice regularly with varied examples and review consistently."
            ],
            "summary": f"""
<b>🎯 Key Takeaways for {topic}:</b>
<ul>
<li>{topic} is a valuable subject that builds important thinking skills</li>
<li>Understanding core concepts is the foundation for advanced learning</li>
<li>Regular practice and real-world application reinforce knowledge</li>
<li>Keep exploring and asking questions to deepen your knowledge</li>
</ul>
"""
        }
    
    def _get_fallback_mindmap(self, topic: str) -> Dict:
        """Fallback mindmap when AI is unavailable"""
        return {
            "topic": topic,
            "branches": [
                {"name": "📖 Introduction", "subtopics": [f"What is {topic}?", f"History of {topic}", f"Why {topic} matters"]},
                {"name": "🎯 Core Concepts", "subtopics": [f"Key principles of {topic}", f"Important theories", f"Fundamental rules"]},
                {"name": "💡 Applications", "subtopics": [f"Real-world uses of {topic}", f"Examples in daily life", f"Industry applications"]},
                {"name": "📚 Study Resources", "subtopics": ["Recommended books", "Online courses", "Practice materials"]},
                {"name": "⭐ Key Terms", "subtopics": [f"Important vocabulary in {topic}", f"Definitions to remember", f"Common terminology"]}
            ]
        }
    
    def _get_fallback_quiz(self, topic: str, num_questions: int) -> Dict:
        """Fallback quiz when AI is unavailable"""
        questions = []
        for i in range(min(num_questions, 5)):
            questions.append({
                "question": f"What is an important concept in {topic}?",
                "options": [f"Concept A about {topic}", f"Concept B about {topic}", f"Concept C about {topic}", f"All of the above"],
                "correct": 3,
                "explanation": f"All of these concepts are important when studying {topic}. Each contributes to a complete understanding."
            })
        return {"topic": topic, "questions": questions}