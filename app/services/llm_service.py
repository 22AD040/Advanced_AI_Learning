"""
LLM Service for Smart Academic Assistant Pro
Enhanced version with ADVANCED content generation
"""

from typing import Dict, List, Optional
import json
import re
from datetime import datetime

class LLMService:
    """Service for handling LLM interactions with PROVEN prompt engineering"""

    def __init__(self):
        """Initialize LLM service with Gemini AI"""
        self.gemini_available = False
        self.gemini_model = None
        
        # Initialize Gemini AI
        try:
            import google.generativeai as genai
            from app.config import Config
            
            # FIXED: Use correct model name 'gemini-1.5-flash' (not gemini-2.5-flash)
            if Config.GEMINI_API_KEY and Config.GEMINI_API_KEY != "AIzaSyCQHhodobMCacO3sIH37tpdvdC8CTprPVk ":
                genai.configure(api_key=Config.GEMINI_API_KEY.strip())  # Added .strip() to remove spaces
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')  # FIXED model name
                self.gemini_available = True
                print(f"✅ Gemini AI initialized with model: gemini-1.5-flash")
            else:
                print("⚠️ No valid Gemini API key found - using ENHANCED fallback content")
        except Exception as e:
            print(f"⚠️ Gemini initialization error: {e} - using ENHANCED fallback content")
    
    def generate_study_content_with_ai(self, topic: str, level: str) -> Dict:
        """Generate COMPREHENSIVE study content with DETAILED abbreviations"""
        
        if not self.gemini_available:
            return self._get_advanced_fallback_content(topic, level)
        
        try:
            print(f"🚀 Generating content for: {topic} at {level} level")
            
            # IMPROVED PROMPT - Focuses heavily on abbreviations and detailed content
            prompt = f"""You are an EXPERT EDUCATOR. Create a COMPREHENSIVE study guide about "{topic}" for {level} level students.

CRITICAL REQUIREMENTS:
1. Provide EXTREMELY DETAILED explanations (minimum 1500 words total)
2. Include ALL abbreviations with their FULL FORMS, MEANINGS, PURPOSES, and EXAMPLES
3. Use REAL-WORLD examples with specific company names, metrics, and results
4. Write in a professional, educational tone

Return ONLY valid JSON with this exact structure:

{{
    "overview": "A detailed 300-400 word overview explaining what {topic} is, why it's important, historical context, and real-world relevance. Include specific statistics and examples.",

    "abbreviations": "Create a DETAILED glossary of 10-12 key terms related to {topic}. For EACH term use this EXACT format:\\n\\n**TERM** - FULL FORM\\n📖 MEANING: (2-3 detailed sentences explaining the concept)\\n🎯 PURPOSE: (2-3 sentences explaining why this concept is used)\\n💡 EXAMPLE: (Specific real-world application with details)\\n🔗 RELATED: Related terms\\n\\nExample:\\n**AI** - Artificial Intelligence\\n📖 MEANING: The simulation of human intelligence processes by machines, especially computer systems. Includes learning, reasoning, and self-correction.\\n🎯 PURPOSE: To create systems that can perform tasks requiring human intelligence, reducing human effort and improving accuracy.\\n💡 EXAMPLE: Self-driving cars use AI to perceive their environment, detect obstacles, and make driving decisions in real-time.\\n🔗 RELATED: Machine Learning, Deep Learning, Neural Networks",

    "key_concepts": [
        "CONCEPT 1 NAME: Write 100-120 words explaining this concept in detail. Include definition, importance, real-world application, and how it relates to {topic}.",
        "CONCEPT 2 NAME: Write 100-120 words with technical depth, practical examples, and connections to other concepts.",
        "CONCEPT 3 NAME: Write 100-120 words including sub-concepts, challenges, and solutions.",
        "CONCEPT 4 NAME: Write 100-120 words with case studies or research findings.",
        "CONCEPT 5 NAME: Write 100-120 words about future trends and innovations.",
        "CONCEPT 6 NAME: Write 100-120 words comparing different approaches or methodologies."
    ],

    "detailed_notes": "Write 800-1000 words organized into these EXACT sections:\\n\\n## 1. FOUNDATION & CORE PRINCIPLES (200 words)\\nExplain fundamental theories, historical development, and key principles with examples.\\n\\n## 2. HOW IT WORKS - TECHNICAL DEEP DIVE (250 words)\\nBreak down the mechanism step-by-step. Include algorithms, formulas, or architectures with clear explanations.\\n\\n## 3. REAL-WORLD APPLICATIONS & CASE STUDIES (200 words)\\nProvide 3-4 specific examples with company names, metrics, and results. Include quantitative data.\\n\\n## 4. BENEFITS vs. LIMITATIONS (150 words)\\nBalanced analysis with specific trade-offs, challenges, and solutions.\\n\\n## 5. FUTURE TRENDS & INNOVATIONS (100 words)\\nEmerging research directions, predictions for next 3-5 years, and potential breakthroughs.",

    "examples": [
        "EXAMPLE 1: [Real Company Name] - Detailed case study with specific metrics",
        "EXAMPLE 2: [Different Industry] - Implementation details and outcomes",
        "EXAMPLE 3: [Research/Academic] - Breakthrough findings and implications",
        "EXAMPLE 4: [Personal/Professional] - Practical application guidance"
    ],

    "practice_questions": [
        "QUESTION 1: (Application-based scenario)\\n\\nANSWER FRAMEWORK: • Key consideration 1 • Key consideration 2 • Expected outcome",
        "QUESTION 2: (Analysis and evaluation question)\\n\\nANSWER FRAMEWORK: • Analytical approach • Evidence to consider • Conclusion structure",
        "QUESTION 3: (Problem-solving question)\\n\\nANSWER FRAMEWORK: • Step-by-step solution • Tools/methods • Validation approach",
        "QUESTION 4: (Comparison question)\\n\\nANSWER FRAMEWORK: • Comparison criteria • Pros/cons analysis • Recommendation",
        "QUESTION 5: (Synthesis/Creative question)\\n\\nANSWER FRAMEWORK: • Design principles • Implementation • Success metrics"
    ],

    "summary": "## 🎯 KEY TAKEAWAYS (8-10 bullet points with specific insights)\\n• First major takeaway with practical implication\\n• Second major takeaway with real-world relevance\\n\\n## 📝 QUICK REFERENCE GUIDE\\n### Essential Terminology Recap:\\n• Term 1: Brief definition\\n• Term 2: Brief definition\\n\\n### Critical Formulas/Concepts:\\n• Concept 1: When and how to apply\\n\\n## 🚀 ACTION ITEMS FOR MASTERY\\n1. Specific action for today\\n2. Specific action for this week\\n3. Long-term mastery strategy\\n\\n## 📚 NEXT STEPS\\n• What to learn after {topic}\\n• Recommended resources and projects"
}}

Make the content SPECIFIC, DETAILED, and PRACTICAL. Include REAL numbers, dates, and company names. Write for {level} level students but add substantial depth.

Generate the JSON now:"""

            response = self.gemini_model.generate_content(prompt)
            print(f"📝 Received response from Gemini ({len(response.text)} chars)")
            
            # Parse the response
            content = self._extract_json(response.text)
            
            if content and self._has_substance(content):
                print(f"✅ Successfully generated detailed content for {topic}")
                # Add a flag to indicate this is AI-generated
                content['_source'] = 'gemini_ai'
                return content
            else:
                print("⚠️ Generated content lacked substance, using enhanced fallback")
                return self._get_advanced_fallback_content(topic, level)
                
        except Exception as e:
            print(f"❌ Content generation error: {e}")
            return self._get_advanced_fallback_content(topic, level)
    
    def generate_quiz_with_ai(self, topic: str, num_questions: int = 10) -> Dict:
        """Generate detailed quiz with comprehensive explanations"""
        
        if not self.gemini_available:
            return self._get_advanced_fallback_quiz(topic, num_questions)
        
        try:
            prompt = f"""Create a CHALLENGING, EDUCATIONAL quiz on "{topic}" with {num_questions} questions.

REQUIREMENTS:
- Questions must require DEEP UNDERSTANDING, not just recall
- Include REAL-WORLD scenarios in at least 50% of questions
- Explanations must be 75+ words each with WHY correct/incorrect
- Distractors should address common misconceptions

Return ONLY valid JSON:
{{
    "topic": "{topic}",
    "questions": [
        {{
            "question": "Detailed, scenario-based question requiring analysis",
            "options": [
                "Option A: Plausible but incorrect (addresses a common misconception)",
                "Option B: CORRECT answer with accuracy and detail",
                "Option C: Another plausible incorrect (tests attention to detail)",
                "Option D: Distractor requiring deeper thinking to eliminate"
            ],
            "correct": 1,
            "explanation": "WHY correct answer is right: (2-3 sentences)\\nWHY other answers are wrong: (2-3 sentences)\\nKEY CONCEPT being tested: (1 sentence)\\nREAL-WORLD APPLICATION: (1-2 sentences)\\nPRO TIP for future reference: (1 sentence)"
        }}
    ]
}}

Make each question TEACH something valuable even if answered incorrectly!"""

            response = self.gemini_model.generate_content(prompt)
            quiz_data = self._extract_json(response.text)
            
            if quiz_data and 'questions' in quiz_data:
                return quiz_data
            else:
                return self._get_advanced_fallback_quiz(topic, num_questions)
                
        except Exception as e:
            print(f"Quiz generation error: {e}")
            return self._get_advanced_fallback_quiz(topic, num_questions)
    
    def generate_mindmap_with_ai(self, topic: str) -> Dict:
        """Generate detailed, structured mindmap"""
        
        if not self.gemini_available:
            return self._get_advanced_fallback_mindmap(topic)
        
        try:
            prompt = f"""Create a COMPREHENSIVE learning roadmap/mindmap for "{topic}".

Requirements:
- 6-8 main branches covering all aspects
- 4-6 subtopics per branch with brief explanations (15-25 words each)
- Include learning path, resources, and practical applications
- Make it practical and actionable

Return ONLY valid JSON:
{{
    "topic": "{topic}",
    "branches": [
        {{"name": "Foundation & Core Concepts", "subtopics": [
            "Definition and scope: Clear explanation of what {topic} encompasses",
            "Historical development: Key milestones and breakthroughs",
            "Key principles: Fundamental theories and frameworks",
            "Essential terminology: Critical vocabulary for understanding"
        ]}},
        {{"name": "How It Works - Technical Deep Dive", "subtopics": [
            "Core mechanisms: Step-by-step explanation of processes",
            "Data flow: How information moves through the system",
            "Key components: Major building blocks and their roles",
            "Performance metrics: How success is measured"
        ]}},
        {{"name": "Practical Applications", "subtopics": [
            "Industry use cases: Real-world implementations with company examples",
            "Research applications: Academic and scientific uses",
            "Personal projects: Hands-on learning opportunities",
            "Integration patterns: How to combine with other technologies"
        ]}},
        {{"name": "Tools & Resources", "subtopics": [
            "Essential tools: Software and platforms for implementation",
            "Learning platforms: Courses, tutorials, and documentation",
            "Community resources: Forums, groups, and events",
            "Practice exercises: Hands-on challenges and projects"
        ]}},
        {{"name": "Challenges & Solutions", "subtopics": [
            "Common obstacles: Typical problems learners face",
            "Technical limitations: Current constraints of the technology",
            "Ethical considerations: Important moral and legal aspects",
            "Mitigation strategies: Proven solutions and workarounds"
        ]}},
        {{"name": "Mastery Path & Career", "subtopics": [
            "Learning progression: Beginner → Intermediate → Advanced roadmap",
            "Certification options: Validated credentials and exams",
            "Portfolio projects: Demonstrable work to showcase skills",
            "Career opportunities: Job roles and industry demand"
        ]}}
    ],
    "learning_path": {{
        "weeks_1_2": ["Complete foundational courses", "Master basic terminology", "Build first simple project"],
        "weeks_3_4": ["Deep dive into core concepts", "Complete intermediate tutorials", "Start medium-complexity project"],
        "weeks_5_6": ["Advanced topics exploration", "Build portfolio project", "Participate in community"],
        "weeks_7_8": ["Mastery challenges", "Contribute to open source", "Prepare for certification/interviews"]
    }},
    "resources": {{
        "beginner": ["Recommended introductory courses", "Beginner-friendly documentation", "Practice platforms for basics"],
        "intermediate": ["Advanced courses and workshops", "Technical blogs and research papers", "Project-based learning resources"],
        "advanced": ["Specialized training programs", "Conference talks and proceedings", "Expert communities and mentorship"]
    }}
}}

Make it comprehensive and actionable for learners!"""

            response = self.gemini_model.generate_content(prompt)
            mindmap = self._extract_json(response.text)
            
            if mindmap:
                return mindmap
            else:
                return self._get_advanced_fallback_mindmap(topic)
                
        except Exception as e:
            print(f"Mindmap generation error: {e}")
            return self._get_advanced_fallback_mindmap(topic)
    
    def _extract_json(self, text: str) -> Optional[Dict]:
        """Extract JSON from response text"""
        try:
            # Remove markdown code blocks
            text = re.sub(r'```json\s*', '', text)
            text = re.sub(r'```\s*', '', text)
            text = text.strip()
            
            # Find JSON object
            start = text.find('{')
            end = text.rfind('}') + 1
            
            if start != -1 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
            else:
                print(f"No JSON found in response. First 200 chars: {text[:200]}")
                return None
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Problematic text: {text[:500]}")
            return None
        except Exception as e:
            print(f"JSON extraction error: {e}")
            return None
    
    def _has_substance(self, content: Dict) -> bool:
        """Check if content has real substance"""
        if not content:
            return False
        if len(content.get('detailed_notes', '')) < 300:
            print(f"Content too short: {len(content.get('detailed_notes', ''))} chars")
            return False
        if len(content.get('key_concepts', [])) < 4:
            print(f"Not enough key concepts: {len(content.get('key_concepts', []))}")
            return False
        if len(content.get('abbreviations', '')) < 200:
            print(f"Abbreviations too short: {len(content.get('abbreviations', ''))} chars")
            return False
        return True
    
    # ============ FALLBACK CONTENT METHODS (keep all your existing fallback methods) ============
    # ... (keep all your _get_advanced_fallback_content, _get_genai_fallback, etc. methods here)
    
    def _get_advanced_fallback_content(self, topic: str, level: str) -> Dict:
        """Generate ADVANCED fallback content"""
        topic_lower = topic.lower()
        
        if "generative ai" in topic_lower or "gen ai" in topic_lower:
            return self._get_genai_fallback(topic, level)
        elif "python" in topic_lower:
            return self._get_python_fallback(topic, level)
        elif "machine learning" in topic_lower:
            return self._get_ml_fallback(topic, level)
        else:
            return self._get_generic_fallback(topic, level)
    
    def _get_genai_fallback(self, topic: str, level: str) -> Dict:
        """Generative AI specific fallback content with detailed abbreviations"""
        return {
            "overview": f"""## What is {topic}? A Complete Technical Overview

{topic} represents one of the most significant technological breakthroughs of the 21st century. Unlike traditional AI that analyzes existing data, Generative AI creates entirely NEW content - text, images, music, code, and videos - that mirrors human-created work.

### The Technical Revolution

At its core, {topic} leverages transformer architecture (introduced in Google's 2017 paper "Attention Is All You Need") to understand patterns in training data and generate novel outputs. The self-attention mechanism allows models to understand context by weighing the importance of different elements in a sequence.

### Why {topic} Matters Today

- **ChatGPT** reached 100 million users in just 2 months - fastest adoption in history
- **Market Size**: Projected $1.3 trillion by 2032 (42% CAGR)
- **Productivity**: GitHub Copilot makes developers 55% faster
- **Scientific Impact**: Drug discovery timeline reduced from 5+ years to 18 months

For {level} learners, mastering {topic} requires understanding transformers, attention mechanisms, and practical applications like RAG and fine-tuning.""",

            "abbreviations": """
**LLM** - Large Language Model
📖 MEANING: A neural network trained on massive text data (billions of parameters) to understand, generate, and manipulate human language.
🎯 PURPOSE: Enable natural language understanding, generation, translation, summarization, and reasoning capabilities without task-specific training.
💡 EXAMPLE: GPT-4 can write essays, debug code, pass professional exams (bar exam, medical licensing), and engage in complex reasoning.
🔗 RELATED: Transformer, Foundation Model, Pre-training

**GAN** - Generative Adversarial Network
📖 MEANING: Two competing neural networks - a Generator that creates fake data and a Discriminator that tries to detect fakes - improving through competition.
🎯 PURPOSE: Generate highly realistic synthetic data including images, videos, and audio that can be indistinguishable from real data.
💡 EXAMPLE: Creating photorealistic human faces at ThisPersonDoesNotExist.com where no real person exists.
🔗 RELATED: Generator, Discriminator, Nash Equilibrium, Deepfake

**VAE** - Variational Autoencoder
📖 MEANING: A generative model that learns to encode input data into a compressed latent space representation and decode it back to reconstruct the original.
🎯 PURPOSE: Generate new data samples similar to training data with controlled variations and smooth interpolation between examples.
💡 EXAMPLE: Generating novel molecule structures for drug discovery by exploring the latent space of known effective drugs.
🔗 RELATED: Encoder, Decoder, Latent Space, KL Divergence

**Transformer** - Neural Network Architecture
📖 MEANING: Deep learning model using self-attention mechanisms to process sequential data in parallel (not sequentially like RNNs). 
🎯 PURPOSE: Handle long-range dependencies in data more effectively, enabling better understanding of context in sequences of any length.
💡 EXAMPLE: BERT for understanding search queries, GPT for text generation, ViT for image recognition, AlphaFold for protein folding.
🔗 RELATED: Self-Attention, Multi-Head Attention, Positional Encoding

**RLHF** - Reinforcement Learning from Human Feedback
📖 MEANING: Training technique where human preference comparisons create a reward model that guides AI behavior toward desired outcomes.
🎯 PURPOSE: Align AI models with human values, making them helpful, harmless, and honest while reducing harmful or undesirable outputs.
💡 EXAMPLE: ChatGPT's training used RLHF to make responses more helpful, less biased, and appropriate - refusing harmful queries while being useful.
🔗 RELATED: Alignment, Reward Modeling, PPO (Proximal Policy Optimization)

**RAG** - Retrieval-Augmented Generation
📖 MEANING: Technique combining information retrieval with text generation - looking up relevant information from external knowledge bases during generation.
🎯 PURPOSE: Reduce hallucinations, provide up-to-date information, enable domain-specific knowledge, and cite sources without retraining models.
💡 EXAMPLE: Customer support chatbot that retrieves your purchase history and account details before answering questions about your specific order.
🔗 RELATED: Vector Database, Embeddings, Semantic Search, Knowledge Base

**Fine-tuning** - Model Adaptation
📖 MEANING: Taking a pre-trained model and continuing training on a smaller, domain-specific dataset to specialize its capabilities.
🎯 PURPOSE: Adapt general-purpose models to specific tasks, industries, or domains with limited data (hundreds to thousands of examples).
💡 EXAMPLE: Fine-tuning GPT-3 on medical literature to create Med-PaLM 2, a medical consultation chatbot that passes medical licensing exams.
🔗 RELATED: Transfer Learning, Parameter-Efficient Fine-Tuning (PEFT), LoRA

**Diffusion Model** - Denoising Framework
📖 MEANING: Model that generates data by starting with random noise and iteratively denoising it over hundreds of steps, learning to reverse a gradual noising process.
🎯 PURPOSE: Create high-quality, diverse outputs with fine-grained control over generation, often outperforming GANs in image quality.
💡 EXAMPLE: Stable Diffusion generates detailed images from text prompts; DALL-E 2 and 3 use diffusion for photorealistic outputs.
🔗 RELATED: Forward Process, Reverse Process, Noise Schedule

**Prompt Engineering** - Input Optimization
📖 MEANING: The practice of designing and refining input prompts to elicit desired responses from language models without changing model weights.
🎯 PURPOSE: Improve output quality, consistency, and task-specific performance while reducing costs and need for fine-tuning.
💡 EXAMPLE: Using chain-of-thought prompting ("Let's think step by step") improves mathematical reasoning by forcing explicit reasoning steps.
🔗 RELATED: Few-shot Learning, Zero-shot Learning, Chain-of-Thought, In-Context Learning

**Hallucination** - Model Error
📖 MEANING: When an AI model confidently generates factually incorrect or nonsensical information not grounded in training data or provided context.
🎯 PURPOSE: Understanding this critical limitation is essential for safe deployment in high-stakes applications like medicine, law, or finance.
💡 EXAMPLE: Legal chatbot inventing non-existent court cases or citations that sound plausible but don't exist in any legal database.
🔗 RELATED: Grounding, Calibration, Uncertainty Estimation, Factual Consistency
""",

            "key_concepts": [
                "**Self-Attention Mechanism**: The revolutionary innovation that enables models to understand context dynamically. For each word, self-attention computes scores to every other word, determining how much focus to put on each. Example: In 'The bank of the river', 'bank' attends strongly to 'river' for meaning; in 'The bank approved my loan', 'bank' attends to 'approved' and 'loan'. This context-awareness is why modern AI understands nuance.",
                
                "**Tokenization and Embeddings**: Before processing, text breaks into tokens (subwords) and converts to numerical vectors (embeddings) that capture semantic meaning. Similar words have similar vectors - famously, 'king' - 'man' + 'woman' ≈ 'queen' in embedding space. This mathematical representation enables analogical reasoning and semantic understanding.",
                
                "**Scaling Laws**: Research shows predictable improvements: model performance follows power laws with compute, dataset size, and parameters. GPT-3 (175B parameters) showed emergent abilities - few-shot learning, translation, coding - that weren't present in smaller models. These capabilities emerge naturally at scale, not through explicit programming.",
                
                "**Temperature and Sampling**: During generation, models output probability distributions over next tokens. Temperature controls randomness - low (0.1-0.3) gives focused, deterministic outputs; high (0.8-1.5) increases creativity. Top-k sampling limits to k most probable tokens; Top-p (nucleus) selects from tokens whose cumulative probability reaches p (e.g., 0.9). These balance quality vs. creativity.",
                
                "**Alignment and Safety**: RLHF aligns models with human values through three stages: (1) collect human preference comparisons, (2) train reward model to predict preferences, (3) optimize policy with PPO while maintaining capabilities. Constitutional AI adds explicit rules via self-critique. Despite progress, challenges remain with bias, hallucination, and misuse.",
                
                "**Multimodal Architectures**: Cutting-edge models process multiple modalities simultaneously. CLIP learns shared embeddings for text and images. Flamingo and GPT-4 Vision handle interleaved images and text. Gemini processes text, images, audio, and video. These enable image captioning, visual QA, video understanding, and robotics - moving beyond text-only."
            ],
            
            "detailed_notes": f"""
## Complete Study Notes: {topic} Advanced Concepts

### 1. FOUNDATION & CORE PRINCIPLES

{topic} represents a fundamental shift from discriminative to generative modeling. Generative models learn the joint probability distribution P(X,Y) or P(X), while discriminative models learn P(Y|X). This allows generative models to sample new instances, not just predict labels.

**Maximum Likelihood Estimation**: Training maximizes likelihood of training data: θ* = argmax_θ Π P(x_i; θ). For language models, this minimizes cross-entropy loss: L = -Σ log P(word_t | context).

**Historical Evolution**:
- 2014: Ian Goodfellow invents GANs at University of Montreal
- 2017: Vaswani et al. publish "Attention Is All You Need" - Transformer architecture
- 2018: BERT and GPT-1 show pre-training effectiveness
- 2020: GPT-3 (175B parameters) demonstrates emergent few-shot learning
- 2021: DALL-E and Stable Diffusion bring text-to-image to mainstream
- 2022: ChatGPT reaches 100M users in 2 months - fastest adoption ever
- 2023: GPT-4, Gemini, Claude 2 - multimodal and longer contexts
- 2024-2025: Agent-based systems, on-device AI, regulatory frameworks

### 2. HOW IT WORKS - STEP BY STEP

**Step 1: Data Collection** - Massive datasets: Common Crawl (billions of web pages), Wikipedia, books (Project Gutenberg), academic papers (arXiv), code repositories (GitHub). Typically 1-10 trillion tokens.

**Step 2: Tokenization** - Convert text to tokens using subword tokenizers (Byte-Pair Encoding, SentencePiece, Unigram). Vocabulary size typically 50k-100k tokens. Handles out-of-vocabulary words via subword splitting.

**Step 3: Architecture Design** - Transformer with L layers, H attention heads, d_model dimensions. GPT-3: 96 layers, 96 heads, 12,288 dimensions, 175B parameters. Each layer: Multi-head attention → LayerNorm → Feed-forward → LayerNorm with residuals.

**Step 4: Pre-training** - Self-supervised learning predicting next token (causal LM) or masked tokens (masked LM). Compute cost: GPT-3 ~$4.6M, GPT-4 estimated $100M+. Training time: months on thousands of GPUs/TPUs.

**Step 5: Fine-tuning** - Supervised fine-tuning (SFT) on instruction-following datasets: (instruction, input, output) triples. Example: "Explain quantum computing" → detailed explanation. Typically 1-10 epochs on 10k-100k examples.

**Step 6: Alignment (RLHF)** - Three stages: (1) collect human preferences (comparisons between outputs), (2) train reward model to predict preferences, (3) optimize policy using PPO with KL penalty to maintain capabilities.

**Step 7: Inference** - Autoregressive generation: tokenized prompt → model → logits → softmax → probability distribution → sample next token → repeat. Sampling strategies: greedy, temperature, top-k, top-p control quality vs. diversity.

### 3. REAL-WORLD APPLICATIONS

**GitHub Copilot**: AI pair programmer from Microsoft + OpenAI. Fine-tuned Codex on 54M public repositories. Results: 55% faster coding (Microsoft research), 40% of code in popular files written by Copilot, billions of daily suggestions.

**Midjourney**: Text-to-image generation via Discord bot. $200M+ annual revenue, subscription model ($10-120/month). Generated winning art at Colorado State Fair (2022), sparking copyright debates. Diffusion model trained on millions of images.

**AlphaFold 2**: DeepMind's protein folding breakthrough. Solved 50-year biology grand challenge (CASP14). Predicted 200M+ protein structures - essentially all known proteins. Accelerating drug discovery, disease understanding, and bioengineering.

**Character.AI**: Personalized AI characters with consistent personalities. 20M+ monthly active users, billions of messages. Founders ex-Google AI researchers. Fine-tuned LLMs for memory, personality, and character consistency. User-created characters with customizable traits.

### 4. BENEFITS & LIMITATIONS

**Benefits**: Democratized creativity (anyone can create professional content), massive productivity gains ($2.6-4.4T economic impact, McKinsey), personalization at scale, bridging skill gaps, accelerating research (80% faster drug discovery), 24/7 availability, multilingual capabilities.

**Challenges**: Hallucination (confidently false info - 88% invented cases in legal study), bias from training data (gender/racial bias in hiring, housing), copyright uncertainty (lawsuits from NY Times, authors, Getty Images), environmental cost (GPT-3: 500 tons CO2), security risks (deepfakes, disinformation, phishing), black box problem (limited interpretability).

### 5. FUTURE TRENDS

**Agent Systems (2025-2026)**: Models that take actions - browse web, use software, execute code, make API calls. AutoGPT and BabyAGI are precursors. Will enable autonomous research, personal assistants, automated workflows, and complex task completion.

**On-Device AI (2024-2025)**: Models running locally on phones/laptops. Qualcomm, Apple, Google adding AI accelerators. Benefits: privacy (no cloud), offline capability, lower latency (<10ms). Gemini Nano already on Pixel 8 Pro.

**Longer Context Windows**: Gemini 1.5 Pro handles 1M tokens (entire Lord of the Rings trilogy, 3 hours of video, 700,000 words). Will enable analysis of entire codebases, books, meeting histories, and personal data.

**Smaller, Efficient Models**: LLaMA (Meta), Mistral, Phi (Microsoft) show high-quality models at 7B-13B parameters (vs GPT-4's ~1.8T). Democratizes AI - run powerful models on consumer hardware. Techniques: Mixture-of-Experts, quantization, pruning, knowledge distillation.

**Regulation (2024-2026)**: EU AI Act (effective 2024, full enforcement 2026) - risk-based classification, transparency requirements, conformity assessments. US Executive Order on AI - safety testing, watermarking, privacy guidelines. China's generative AI regulations - content control, security reviews.
""",
            
            "examples": [
                "**EXAMPLE 1: Customer Service Transformation** - Zendesk fine-tuned GPT-4 on 500,000 historical support tickets. Results: 45% faster response (8 hours → 4.4 hours), 35% lower agent workload, 92% customer satisfaction, $4.2M annual savings for enterprise customer. Key insight: AI augments rather than replaces humans.",
                
                "**EXAMPLE 2: Drug Discovery Breakthrough** - Insilico Medicine used GANs and VAEs for novel molecule design. Discovered INS018_055 (fibrosis treatment) in 18 months vs 4-5 years traditional. Entered clinical trials November 2023 - first AI-discovered drug to reach humans. 80% faster discovery, 3x higher success rate.",
                
                "**EXAMPLE 3: AI Tutoring at Scale** - Khan Academy's Khanmigo provides Socratic tutoring (never gives direct answers). Fine-tuned GPT-4 on tutoring dialogues, added cheating safeguards. Results with 50,000+ students: 62% better understanding, 2x engagement, teachers saved 5+ hours/week, improved equity for low-income schools.",
                
                "**EXAMPLE 4: Game Development Efficiency** - Ubisoft's Ghostwriter generates NPC dialogue and barks. Fine-tuned Mistral 7B on proprietary game scripts. Results: 70% reduction in dialogue writing time, 500+ unique barks per NPC (vs 20 before), 10,000+ human hours saved, writers focus on main story and quality."
            ],
            
            "practice_questions": [
                "**Q1: Generative vs Discriminative Models** - Explain the difference between generative and discriminative AI models with concrete examples of each. When would you choose one over the other?\n\n**Answer Framework**: Definition of each (generative learns P(X,Y) vs discriminative learns P(Y|X)), examples (GPT-4 vs spam classifier), use cases (content creation vs classification), trade-offs (flexibility vs efficiency).",
                
                "**Q2: Hallucination Mitigation** - What causes hallucination in LLMs and why is it difficult to eliminate? Describe three current approaches to mitigation and their limitations.\n\n**Answer Framework**: Definition (confidently false info), causes (next-token prediction, no truth concept), difficulty (trade-off with creativity, no verification mechanism), approaches (RAG reduces from 20% to 5%, RLHF effective but expensive, CoT adds reasoning), limitations (no perfect solution, human verification needed).",
                
                "**Q3: Production AI System Design** - You're implementing an AI system for a hospital to answer patient questions. Describe technical architecture, safety measures, and ethical guidelines.\n\n**Answer Framework**: RAG with verified knowledge base (only hospital's approved materials), confidence scoring with escalation, human-in-the-loop for critical decisions, transparency disclosure ('AI-generated, not medical advice'), privacy protections, emergency keyword detection, regular auditing for bias and accuracy. Key principle: AI augments, doesn't replace medical expertise.",
                
                "**Q4: Future Trends Analysis** - What three emerging trends in generative AI will have the biggest impact in the next 3 years? Justify each with technical and business reasoning.\n\n**Answer Framework**: Agent systems (autonomous task completion - AutoGPT precursors), on-device AI (privacy, offline, low latency - Gemini Nano), multimodal models (unified text/image/audio/video - GPT-4V, Gemini). Each with technical explanation and business impact (automated workflows, privacy-preserving apps, video generation).",
                
                "**Q5: Educational AI Ethics** - Propose an ethical framework for deploying generative AI in K-12 schools. What specific rules would you implement and why?\n\n**Answer Framework**: Core principles (learning augmentation not bypass, age-appropriate safeguards, transparency, teacher oversight, bias monitoring), specific rules (no direct answers to homework - Socratic questioning only, citation required, content filtering, privacy protections, opt-out rights), implementation (fine-tuned guardrails, teacher dashboard, incident reporting, ethics training)."
            ],
            
            "summary": """
## 🎯 KEY TAKEAWAYS

• **Generative AI creates new content** - text, images, code, music - rather than analyzing existing data. This represents a paradigm shift in human-computer interaction.

• **Transformer architecture with self-attention** is the foundation of modern generative AI. The 2017 "Attention Is All You Need" paper revolutionized the field.

• **Large Language Models (LLMs) demonstrate emergent abilities** - few-shot learning, reasoning, and tool use that weren't explicitly programmed but emerged at scale (GPT-3, 175B parameters).

• **Hallucination remains a critical challenge** - models confidently generate false information. RAG (retrieval-augmented generation) and RLHF help but don't eliminate the problem.

• **Real-world impact is already massive** - GitHub Copilot (55% faster coding), drug discovery (80% faster), customer service (45% reduced response time), $1.3T projected market by 2032.

• **Ethical concerns are serious** - bias, copyright issues, deepfakes, environmental cost (500 tons CO2 for GPT-3), and job displacement require active management and regulation.

• **The future is multimodal and agentic** - models handling video, audio, 3D, and taking autonomous actions. On-device AI will enable privacy-preserving applications.

• **Best practice is AI + human collaboration** - AI handles volume and speed; humans provide judgment, creativity, and ethical oversight. Never deploy in high-stakes domains without human verification.

## 📝 QUICK REFERENCE GUIDE

**Essential Terminology**:
- **GenAI**: Generative Artificial Intelligence (creates new content)
- **LLM**: Large Language Model (text-focused generative AI)
- **Transformer**: The architecture powering modern GenAI
- **GAN**: Generative Adversarial Network (two networks competing)
- **Diffusion Model**: Gradual denoising to generate images
- **Fine-tuning**: Adapting pre-trained models to specific domains
- **RAG**: Retrieval-Augmented Generation (fact lookup during generation)
- **RLHF**: Reinforcement Learning from Human Feedback (alignment technique)

**Critical Metrics**:
- GPT-3 training cost: ~$4.6M
- ChatGPT users in 2 months: 100 million
- GitHub Copilot productivity gain: 55%
- Global GenAI market by 2032: $1.3 trillion
- Drug discovery time reduction: 80%

**When to Use GenAI**:
✅ **Good for**: Drafting, brainstorming, summarizing, code assistance, translation, personalization, data augmentation
❌ **Bad for**: Medical diagnosis, legal advice, financial decisions, identity verification, safety-critical systems (without human verification)

## 🚀 ACTION ITEMS FOR MASTERY

**Today**:
1. Open ChatGPT or Claude and explore for 30 minutes
2. Try different prompt styles: detailed, step-by-step, role-playing
3. Note what works well and what fails (hallucinations, misunderstandings)

**This Week**:
1. Complete "ChatGPT Prompt Engineering for Developers" (DeepLearning.ai - free)
2. Build a simple RAG chatbot using your documents
3. Experiment with different models (GPT, Claude, Gemini, Llama via API)

**This Month**:
1. Learn RAG in depth - vector databases, embeddings, semantic search
2. Fine-tune a small model (e.g., Llama 7B or Mistral) on custom data
3. Implement an AI agent with function calling/tool use
4. Build a portfolio project - chatbot, image generator, or code assistant

**Long-term Mastery**:
1. Study deep learning fundamentals (CS224n, Fast.ai, DeepLearning Specialization)
2. Read research papers weekly (arXiv cs.CL, cs.LG, AI newsletters)
3. Build production-grade applications with monitoring, logging, safety controls
4. Specialize: Multimodal models, agents, efficiency optimization, or AI ethics

## 📚 NEXT STEPS AFTER GENERATIVE AI

**Related Topics to Explore**:
• Reinforcement Learning (how AI learns from feedback and rewards)
• Computer Vision (image understanding, generation, and analysis)
• Natural Language Processing (text understanding fundamentals)
• MLOps (deploying and maintaining AI systems in production)
• AI Ethics and Governance (regulation, safety, responsible AI)

**Recommended Projects**:
• Build a RAG chatbot for your personal notes or documentation
• Create an AI-powered study assistant for a subject you know well
• Fine-tune a model for a specific domain (healthcare, law, finance, coding)
• Develop an AI agent that uses APIs to accomplish multi-step tasks
• Build a multimodal app combining text, image, and audio understanding

**Recommended Resources**:
• **Courses**: DeepLearning.ai, Fast.ai, CS224n (Stanford)
• **Books**: "Deep Learning" by Goodfellow, "The Alignment Problem"
• **News**: The Batch (DeepLearning.ai), Import AI (Jack Clark), Last Week in AI
• **Communities**: r/LocalLLaMA, EleutherAI Discord, Hugging Face forums, r/StableDiffusion
• **Practice**: Kaggle competitions, Hugging Face challenges, open-source contributions
"""
        }
    
    # Keep your existing fallback methods...
    def _get_python_fallback(self, topic: str, level: str) -> Dict:
        """Python specific fallback content"""
        return {
            "overview": f"Python is a high-level, interpreted programming language created by Guido van Rossum in 1991. It emphasizes code readability through significant whitespace and clean syntax. Python is the #1 language for data science, AI, web development, and automation, with applications at Google, Netflix, NASA, and Instagram.",
            "abbreviations": """
**OOP** - Object-Oriented Programming: Organizes code into reusable objects with data and methods.
**IDE** - Integrated Development Environment: PyCharm, VS Code, Jupyter for Python development.
**PEP** - Python Enhancement Proposal: PEP 8 is the style guide for Python code formatting.
**pip** - Package installer for Python: `pip install numpy` installs packages from PyPI.
**PyPI** - Python Package Index: 400,000+ packages available for Python.
**REPL** - Read-Eval-Print Loop: Interactive Python shell where `>>> 2+2` shows `4`.
**GIL** - Global Interpreter Lock: Limits CPU-bound multi-threading in CPython.
""",
            "key_concepts": [
                "**Dynamic Typing**: Variables have types determined at runtime, not compile time. Write `x = 5` then `x = 'hello'` without declarations.",
                "**Indentation as Syntax**: Uses indentation levels (4 spaces recommended) for code blocks instead of braces {}.",
                "**Everything is an Object**: Functions, classes, and modules are objects enabling powerful metaprogramming.",
                "**List Comprehensions**: Concise syntax: `[x**2 for x in range(10) if x % 2 == 0]` - more readable and faster than loops.",
                "**Duck Typing**: 'If it walks like a duck...' - checks capabilities, not explicit types.",
                "**Decorators**: Functions that modify other functions: `@timer def slow_function():` for logging, timing, access control."
            ],
            "detailed_notes": f"""
## Python Study Notes

### Core Features
- **Readable Syntax**: Clean, English-like code that's easy to learn and maintain
- **Interpreted**: No compilation step, run code directly
- **Dynamically Typed**: Flexible but requires testing to catch type errors
- **Memory Managed**: Automatic garbage collection with reference counting

### Popular Libraries
- **Data Science**: NumPy, Pandas, Matplotlib, Scikit-learn
- **Web Development**: Django, Flask, FastAPI
- **AI/ML**: TensorFlow, PyTorch, Transformers
- **Automation**: Requests, Selenium, BeautifulSoup

### Best Practices
- Follow PEP 8 style guide
- Write docstrings for functions and classes
- Use virtual environments for project isolation
- Write unit tests with pytest or unittest
- Use type hints (Python 3.6+) for better code clarity
""",
            "examples": [
                "**Data Analysis**: Pandas DataFrame operations on CSV files",
                "**Web API**: FastAPI endpoint returning JSON responses", 
                "**Automation**: Selenium script for web scraping",
                "**Machine Learning**: Scikit-learn model training pipeline"
            ],
            "practice_questions": [
                "Write a function that returns Fibonacci sequence up to n terms",
                "Create a class for a Bank Account with deposit/withdraw methods",
                "Use list comprehension to filter even numbers from a list"
            ],
            "summary": "Python combines readability with power. Master dynamic typing, indentation, object model, comprehensions, and decorators. Practice with projects - automation, data analysis, or web apps."
        }
    
    def _get_ml_fallback(self, topic: str, level: str) -> Dict:
        """Machine Learning specific fallback content"""
        return {
            "overview": f"Machine Learning enables systems to learn from data without explicit programming. ML algorithms identify patterns and make predictions, transforming industries from healthcare to finance. Key types: supervised (labeled data), unsupervised (unlabeled data), and reinforcement learning (trial and error).",
            "abbreviations": """
**ML** - Machine Learning: Algorithms improving through experience/data.
**Supervised Learning**: Learn from labeled examples (inputs with correct outputs).
**Unsupervised Learning**: Find patterns in unlabeled data (clustering, dimensionality reduction).
**Reinforcement Learning**: Learn through rewards/penalties (game playing, robotics).
**CNN** - Convolutional Neural Network: For image data - detects spatial patterns.
**RNN** - Recurrent Neural Network: For sequential data with memory (speech, time series).
**NLP** - Natural Language Processing: Understanding and generating human language.
""",
            "key_concepts": [
                "**Supervised Learning**: Regression (predict numbers) and classification (predict categories). Requires labeled data but achieves high accuracy.",
                "**Unsupervised Learning**: Clustering (group customers), dimensionality reduction (visualize high-D data), anomaly detection (find fraud).",
                "**Training/Testing Split**: 80/20 split to detect overfitting. Cross-validation provides robust estimates.",
                "**Bias-Variance Tradeoff**: Underfitting (high bias) vs overfitting (high variance). Find sweet spot with regularization.",
                "**Feature Engineering**: Transforming raw data into informative features - scaling, encoding, creating interactions."
            ],
            "detailed_notes": f"""
## Machine Learning Study Notes

### The ML Pipeline
1. **Data Collection**: Gather relevant, representative data
2. **Data Preparation**: Clean, normalize, handle missing values
3. **Feature Engineering**: Create informative features
4. **Model Selection**: Choose algorithm based on problem type
5. **Training**: Learn parameters from training data
6. **Evaluation**: Test on unseen data - accuracy, precision, recall, F1
7. **Deployment**: Integrate model into production system
8. **Monitoring**: Track performance, detect drift, retrain

### Common Algorithms
- **Linear/Logistic Regression**: Baseline models for regression/classification
- **Decision Trees/Random Forest**: Interpretable, handles non-linear relationships
- **SVM**: Effective for high-dimensional spaces
- **Neural Networks**: Deep learning for complex patterns
- **K-Means**: Simple clustering algorithm
- **PCA**: Dimensionality reduction

### Evaluation Metrics
- **Classification**: Accuracy, Precision, Recall, F1-Score, ROC-AUC
- **Regression**: MSE, MAE, R-squared, RMSE
- **Clustering**: Silhouette score, inertia
""",
            "examples": [
                "**Recommendation Systems**: Netflix suggesting movies based on viewing history",
                "**Fraud Detection**: Credit card transactions flagged as suspicious",
                "**Medical Diagnosis**: Identifying tumors in medical scans",
                "**Autonomous Vehicles**: Self-driving cars perceiving environment"
            ],
            "practice_questions": [
                "Explain the bias-variance tradeoff with examples",
                "When would you use random forest vs logistic regression?",
                "How do you handle imbalanced datasets in classification?"
            ],
            "summary": "Machine Learning transforms data into predictions. Master supervised/unsupervised learning, train/test splits, cross-validation, bias-variance tradeoff, and feature engineering. Start with scikit-learn, progress to deep learning with TensorFlow/PyTorch."
        }
    
    def _get_generic_fallback(self, topic: str, level: str) -> Dict:
        """Generic fallback for any topic"""
        return {
            "overview": f"## {topic}\n\n{topic} is a fundamental area of study combining theoretical knowledge with practical applications. This comprehensive guide covers foundations, core concepts, applications, and mastery strategies.\n\n### Why {topic} Matters\n\nMastering {topic} develops critical thinking, analytical skills, and problem-solving abilities that transfer across domains. Whether you're beginning your journey or seeking expertise, this foundation opens doors to numerous opportunities.",
            
            "abbreviations": f"""
**Core Terms for {topic}**:
- **Fundamental Concepts**: Essential vocabulary and building blocks
- **Applied Methods**: How theories translate to practice  
- **Advanced Terminology**: Specialized vocabulary for experts
""",
            
            "key_concepts": [
                f"**Foundational Principles of {topic}**: Understanding core theories establishes the basis for advanced study.",
                f"**Practical Applications**: How {topic} applies to real-world problems across industries.",
                f"**Methodologies**: Different approaches to analyze and solve problems in {topic}.",
                f"**Tools and Techniques**: Essential resources and methods for working with {topic}.",
                f"**Quality Metrics**: How to measure success and improve performance.",
                f"**Advanced Topics**: Specialized areas for deeper expertise."
            ],
            
            "detailed_notes": f"""
## Study Notes for {topic}

### Section 1: Foundations

Understanding {topic} begins with core principles that govern its operation. These foundations apply across all applications and expertise levels.

**Historical Context**: The development of {topic} has been shaped by key discoveries, technological advances, and changing needs.

**Core Definitions**: Precise terminology enables clear communication and deep understanding.

### Section 2: How It Works

The mechanisms behind {topic} involve interconnected processes:
1. Assessment: Understanding requirements and constraints
2. Planning: Developing systematic approach
3. Implementation: Executing planned activities
4. Evaluation: Measuring outcomes against objectives
5. Iteration: Refining based on feedback

### Section 3: Best Practices

- Start with fundamentals before advancing
- Practice regularly with varied examples
- Seek feedback and learn from mistakes
- Connect new knowledge to existing understanding
- Apply learning to real problems
- Collaborate and discuss with peers
""",
            
            "examples": [
                f"**Academic Application**: Student learning {topic} applies concepts to assignments and prepares for examinations.",
                f"**Professional Scenario**: Professional uses {topic} knowledge to solve workplace challenges.",
                f"**Research Context**: Researchers apply {topic} to discover new insights.",
                f"**Personal Development**: Individual uses {topic} for self-improvement."
            ],
            
            "practice_questions": [
                f"Explain the core principles of {topic} and why they matter.",
                f"Describe a real-world situation where {topic} knowledge would be essential.",
                f"Compare different approaches to mastering {topic}.",
                f"How would you apply {topic} to solve a complex problem?",
                f"Where is {topic} heading in the next 5-10 years?"
            ],
            
            "summary": f"""
## Key Takeaways for {topic}

### Essential Points:
- {topic} requires both theory and practice
- Consistent deliberate practice leads to mastery
- Real-world connection reinforces learning
- Continuous learning is essential

### Action Steps:
1. Review core concepts daily
2. Practice with real problems
3. Seek feedback on understanding
4. Apply knowledge to personal projects

### Success Indicators:
- Ability to explain concepts clearly
- Confidence in applying knowledge
- Problem-solving speed and accuracy
- Recognition from peers and mentors
"""
        }
    
    def _get_advanced_fallback_quiz(self, topic: str, num_questions: int) -> Dict:
        """Advanced fallback quiz"""
        return {
            "topic": topic,
            "questions": [
                {
                    "question": f"What are the three most important foundational concepts in {topic} that beginners should master first? Explain why each matters.",
                    "options": [
                        "Memorization, repetition, and testing",
                        f"Core principles, practical applications, and problem-solving frameworks specific to {topic}",
                        "Speed, quantity, and competition",
                        "Theory only, without practice"
                    ],
                    "correct": 1,
                    "explanation": f"Mastering {topic} requires understanding core principles (the 'what' and 'why'), practical applications (the 'how' and 'where'), and problem-solving frameworks (the structured approach to challenges). These three pillars support all advanced learning and real-world application."
                },
                {
                    "question": f"Why is consistent practice essential for mastering {topic}?",
                    "options": [
                        "It doesn't matter—talent is most important",
                        "Practice builds muscle memory, reinforces neural pathways, and reveals gaps in understanding that passive learning misses",
                        "Only reading is sufficient",
                        "Practice is only for beginners"
                    ],
                    "correct": 1,
                    "explanation": f"Neuroscience research shows that consistent practice strengthens neural connections (myelination), making recall and application faster and more automatic. Practice also reveals what you don't know—passive reading creates illusion of competence while practice exposes gaps. The '10,000 hour rule' (popularized by Gladwell, based on Ericsson's research) emphasizes deliberate practice, not just repetition."
                },
                {
                    "question": f"How does real-world application enhance learning of {topic}?",
                    "options": [
                        "It doesn't—abstract learning is better",
                        "Application provides context, motivation, and feedback loops that accelerate understanding and retention",
                        "Only theoretical knowledge matters",
                        "Application is only for professionals"
                    ],
                    "correct": 1,
                    "explanation": f"Real-world application activates multiple learning pathways: contextual learning (understanding why something matters), motivated learning (solving actual problems is engaging), and feedback loops (results tell you if you're right). Research shows retention rates: lecture 5%, reading 10%, demonstration 30%, discussion 50%, practice by doing 75%, teaching others 90%."
                }
            ][:num_questions]
        }
    
    def _get_advanced_fallback_mindmap(self, topic: str) -> Dict:
        """Advanced fallback mindmap"""
        return {
            "topic": topic,
            "branches": [
                {"name": "Foundations", "subtopics": ["Core definitions", "Historical context", "Key principles", "Essential terminology"]},
                {"name": "How It Works", "subtopics": ["Step-by-step process", "Key components", "Common patterns", "Success metrics"]},
                {"name": "Applications", "subtopics": ["Real-world use cases", "Industry examples", "Research applications", "Personal projects"]},
                {"name": "Tools & Resources", "subtopics": ["Essential tools", "Learning platforms", "Practice exercises", "Community support"]},
                {"name": "Mastery Path", "subtopics": ["Beginner steps", "Intermediate goals", "Advanced topics", "Expert resources"]}
            ]
        }
    
    # ============ ORIGINAL METHODS FOR COMPATIBILITY ============
    
    def generate_response(self, query: str, role: str, context: Dict = None) -> str:
        """Generate response based on user role"""
        if self.gemini_available:
            try:
                role_context = {
                    "school": "school student (ages 12-16). Use simple language, examples, and encouraging tone.",
                    "college": "college student. Provide detailed, practical, career-oriented explanations.",
                    "aspirant": "exam aspirant. Focus on exam strategies, time management, and high-yield content."
                }
                prompt = f"You are an expert academic assistant for a {role_context.get(role, 'student')}\n\nQuestion: {query}\n\nProvide a helpful, detailed response."
                response = self.gemini_model.generate_content(prompt)
                return response.text
            except:
                pass
        
        responses = {
            "school": "I'm here to help you learn! What subject would you like to explore? 📚",
            "college": "Great question! Let me provide you with detailed information to support your studies. 🎓",
            "aspirant": "Excellent focus on exam preparation! Let me help you optimize your study strategy. 🎯"
        }
        return responses.get(role, "How can I assist with your learning today?")
    
    def get_study_recommendations(self, role: str, performance: Dict = None) -> List[str]:
        """Get personalized study recommendations"""
        base_recommendations = {
            "school": [
                "Create a daily study schedule (2-3 hours)",
                "Take notes during class and review them same day",
                "Practice problems daily - start with 10 problems",
                "Read actively: highlight, question, summarize",
                "Form study groups to discuss concepts",
                "Set weekly goals and track progress",
                "Use the Pomodoro Technique: 25 min study, 5 min break"
            ],
            "college": [
                "Build a portfolio of 3-5 substantial projects",
                "Practice technical interviews weekly",
                "Network on LinkedIn and attend career fairs",
                "Write blog posts explaining concepts you learn",
                "Contribute to open source projects",
                "Earn relevant certifications in your field",
                "Participate in hackathons and competitions"
            ],
            "aspirant": [
                "Create a 6-month study calendar with weekly targets",
                "Take weekly mock tests under timed conditions",
                "Analyze mistakes and maintain an error log",
                "Focus 80% time on weak areas, 20% on strengths",
                "Practice time management daily",
                "Review using spaced repetition",
                "Maintain health: sleep 7-8 hours, exercise, eat well"
            ]
        }
        return base_recommendations.get(role, base_recommendations["college"])
 
