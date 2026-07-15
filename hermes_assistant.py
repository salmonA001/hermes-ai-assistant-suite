#!/usr/bin/env python3
"""
Hermes Assistant - An Advanced, User-Friendly AI Chatbot for Terminal
Features: Natural Language Processing, Knowledge Base, Calculations, File Operations, Data Analysis, System Utilities
"""

import os
import sys
import json
import math
import random
import datetime
import subprocess
import platform
from typing import Dict, List, Any, Optional, Tuple

# ==================== CONFIGURATION ====================

CONFIG = {
    "name": "Hermes Assistant",
    "version": "3.0.0",
    "creator": "Nous Research (Hermes Framework)",
    "max_history": 50,
    "file_size_limit": 1024 * 1024,  # 1MB
    "display_limit": 1500,
}

# ==================== MAIN ASSISTANT CLASS ====================

class HermesAssistant:
    """Advanced AI Assistant with multiple capabilities"""
    
    def __init__(self):
        self.name = CONFIG["name"]
        self.version = CONFIG["version"]
        self.creator = CONFIG["creator"]
        self.conversation_history = []
        self.user_name = None
        self.session_start = datetime.datetime.now()
        self.knowledge_base = self._load_knowledge_base()
        self.sample_datasets = self._create_sample_datasets()
        
        # Response templates
        self.greetings = [
            f"Hello! I'm {self.name} v{self.version}, your AI assistant. How can I help you today?",
            f"Hi there! Ready to assist with questions, calculations, or just chat. What's on your mind?",
            f"Greetings! I'm here to help with information, problem-solving, or friendly conversation.",
            f"Hey! I'm {self.name}. I can answer questions, help with calculations, analyze data, and more."
        ]
        
        self.farewells = [
            "Goodbye! It was nice chatting with you. Have a great day!",
            "See you later! Remember I'm here whenever you need assistance.",
            "Farewell! Thanks for the conversation. Come back anytime!",
            "Bye for now! I'll be here when you need me again."
        ]
        
        self.jokes = [
            "Why don't scientists trust atoms anymore? Because they make up everything!",
            "I told my computer I needed a break, and it said 'No problem - I'll go to sleep mode'.",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "There are 10 types of people in the world: those who understand binary, and those who don't.",
            "Debugging: Removing the needles from the haystack.",
            "Why was the math book sad? Because it had too many problems.",
            "I would tell you a UDP joke, but you might not get it.",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
            "Why do Java developers wear glasses? Because they don't see sharp!",
            "What do you call a bear with no teeth? A gummy bear!"
        ]
        
        self.quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Innovation distinguishes between a leader and a follower. - Steve Jobs",
            "Life is what happens when you're busy making other plans. - John Lennon",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "It is during our darkest moments that we must focus to see the light. - Aristotle",
            "The only limit to our realization of tomorrow is our doubts today. - Franklin D. Roosevelt",
            "In the middle of difficulty lies opportunity. - Albert Einstein",
            "Whether you think you can or you think you can't, you're right. - Henry Ford",
            "The journey of a thousand miles begins with one step. - Lao Tzu",
            "Believe you can and you're halfway there. - Theodore Roosevelt",
            "Strive not to be a success, but rather to be of value. - Albert Einstein",
            "Two roads diverged in a wood, and I—I took the one less traveled by. - Robert Frost"
        ]
    
    def _load_knowledge_base(self) -> Dict[str, str]:
        """Load the AI's knowledge base"""
        return {
            # AI & Technology
            "ai_definition": "Artificial Intelligence (AI) is the simulation of human intelligence in machines that are programmed to think like humans and mimic their actions.",
            "machine_learning": "Machine Learning is a subset of AI that provides systems the ability to automatically learn and improve from experience without being explicitly programmed.",
            "deep_learning": "Deep Learning is a subset of machine learning that uses neural networks with many layers to analyze various factors of data.",
            "nlp": "Natural Language Processing (NLP) is a branch of AI that helps computers understand, interpret and manipulate human language.",
            "computer_vision": "Computer Vision is a field of AI that trains computers to interpret and understand the visual world.",
            "robotics": "Robotics is an interdisciplinary field that integrates computer science and engineering to design, construct, operate, and use robots.",
            "data_science": "Data Science is an interdisciplinary field that uses scientific methods, processes, algorithms and systems to extract knowledge from data.",
            "big_data": "Big data refers to extremely large datasets that may be analyzed computationally to reveal patterns, trends, and associations.",
            "cloud_computing": "Cloud computing is the delivery of computing services—including servers, storage, databases, networking, software—over the internet.",
            "blockchain": "Blockchain is a system of recording information in a way that makes it difficult or impossible to change, hack, or cheat the system.",
            "cybersecurity": "Cybersecurity is the practice of defending computers, servers, mobile devices, electronic systems, networks, and data from malicious attacks.",
            "neural_network": "A neural network is a series of algorithms that endeavors to recognize underlying relationships in a set of data through a process that mimics the way the human brain operates.",
            "algorithm": "An algorithm is a finite sequence of well-defined instructions, typically to solve a class of problems or to perform a computation.",
            "data_structure": "A data structure is a particular way of organizing data in a computer so that it can be used efficiently.",
            
            # Programming & Tools
            "python": "Python is a high-level, interpreted programming language known for its simplicity and readability. It's widely used in AI, data science, web development, and automation.",
            "javascript": "JavaScript is a programming language that enables interactive web pages. It's an essential part of web applications.",
            "git": "Git is a distributed version control system for tracking changes in source code during software development.",
            "docker": "Docker is a platform for developing, shipping, and running applications in containers.",
            "sql": "SQL (Structured Query Language) is a domain-specific language used in programming and designed for managing data held in a relational database management system.",
            "html": "HTML (HyperText Markup Language) is the standard markup language for documents designed to be displayed in a web browser.",
            "css": "CSS (Cascading Style Sheets) is a style sheet language used for describing the presentation of a document written in HTML or XML.",
            "react": "React is a JavaScript library for building user interfaces, particularly single-page applications.",
            "api": "An API (Application Programming Interface) is a set of rules that allows different software entities to communicate with each other.",
            "framework": "A software framework is an abstraction in which software providing generic functionality can be selectively changed by additional user-written code.",
            
            # Science & Math
            "quantum_computing": "Quantum computing is a type of computation that harnesses the collective properties of quantum states, such as superposition and entanglement, to perform calculations.",
            "relativity": "The theory of relativity, developed by Albert Einstein, describes the relationship between space, time, and gravity.",
            "evolution": "Evolution is the change in the heritable characteristics of biological populations over successive generations.",
            "photosynthesis": "Photosynthesis is the process used by plants, algae and certain bacteria to harness energy from sunlight and turn it into chemical energy.",
            "dna": "DNA (Deoxyribonucleic acid) is a molecule composed of two polynucleotide chains that coil around each other to form a double helix carrying genetic instructions.",
            "statistics": "Statistics is the discipline that concerns the collection, organization, analysis, interpretation, and presentation of data.",
            "probability": "Probability is the branch of mathematics concerning numerical descriptions of how likely an event is to occur.",
            "calculus": "Calculus is the mathematical study of continuous change, in the same way that geometry is the study of shape and algebra is the study of operations.",
            "linear_algebra": "Linear algebra is the branch of mathematics concerning linear equations, linear maps, and their representations in vector spaces and through matrices.",
            "physics": "Physics is the natural science that studies matter, its motion and behavior through space and time, and the related entities of energy and force.",
            "chemistry": "Chemistry is the scientific study of the properties and behavior of matter.",
            "biology": "Biology is the natural science that studies life and living organisms, including their physical structure, chemical processes, molecular interactions, physiological mechanisms, development and evolution.",
            
            # General Knowledge
            "universe": "The universe is all of space and time and their contents, including planets, stars, galaxies, and all other forms of matter and energy.",
            "climate_change": "Climate change refers to long-term shifts in temperatures and weather patterns, primarily caused by human activities since the 1800s.",
            "renewable_energy": "Renewable energy is energy from sources that are naturally replenishing but flow-limited, such as solar, wind, rain, tides, waves, and geothermal heat.",
            "artificial_intelligence_ethics": "AI ethics is a branch of ethics that focuses on the ethical issues surrounding the development and use of artificial intelligence technologies.",
            "democracy": "Democracy is a system of government where the citizens exercise power by voting.",
            "capitalism": "Capitalism is an economic system based on the private ownership of the means of production and their operation for profit.",
            "globalization": "Globalization is the process of interaction and integration among people, companies, and governments worldwide.",
            "internet": "The Internet is a global network of interconnected computers that use the standard Internet protocol suite to communicate between networks and devices.",
            "psychology": "Psychology is the science of mind and behavior.",
            "philosophy": "Philosophy is the study of general and fundamental questions about existence, knowledge, values, reason, mind, and language.",
            
            # About Hermes
            "hermes_origin": "Hermes is an AI agent framework created by Nous Research, designed to be extensible, self-improving, and capable of tool use.",
            "hermes_capabilities": "Hermes Assistant can understand natural language, perform data analysis, execute mathematical calculations, access knowledge bases, assist with file operations, provide system information, and help with various tasks through conversation.",
            "hermes_version": f"This is {self.name} version {self.version}.",
        }
    
    def _create_sample_datasets(self) -> Dict[str, List[Dict]]:
        """Create sample datasets for demonstration"""
        return {
            "employees": [
                {"id": 1, "name": "Alice Smith", "age": 29, "department": "Engineering", "salary": 75000, "years_exp": 5, "city": "New York"},
                {"id": 2, "name": "Bob Johnson", "age": 35, "department": "Marketing", "salary": 65000, "years_exp": 8, "city": "San Francisco"},
                {"id": 3, "name": "Carol Davis", "age": 42, "department": "Sales", "salary": 80000, "years_exp": 12, "city": "Chicago"},
                {"id": 4, "name": "David Wilson", "age": 31, "department": "Engineering", "salary": 72000, "years_exp": 6, "city": "Seattle"},
                {"id": 5, "name": "Eva Brown", "age": 28, "department": "HR", "salary": 58000, "years_exp": 4, "city": "Austin"},
                {"id": 6, "name": "Frank Miller", "age": 45, "department": "Finance", "salary": 90000, "years_exp": 15, "city": "Boston"},
                {"id": 7, "name": "Grace Lee", "age": 33, "department": "Engineering", "salary": 78000, "years_exp": 7, "city": "Denver"},
                {"id": 8, "name": "Henry Garcia", "age": 38, "department": "Sales", "salary": 82000, "years_exp": 10, "city": "Miami"}
            ],
            "sales": [
                {"month": "Jan", "region": "North", "sales": 15000, "target": 12000, "rep": "Alice"},
                {"month": "Feb", "region": "North", "sales": 18000, "target": 13000, "rep": "Alice"},
                {"month": "Mar", "region": "North", "sales": 16500, "target": 14000, "rep": "Alice"},
                {"month": "Apr", "region": "North", "sales": 17000, "target": 15000, "rep": "Alice"},
                {"month": "Jan", "region": "South", "sales": 12000, "target": 10000, "rep": "Bob"},
                {"month": "Feb", "region": "South", "sales": 14000, "target": 11000, "rep": "Bob"},
                {"month": "Mar", "region": "South", "sales": 13000, "target": 12000, "rep": "Bob"},
                {"month": "Apr", "region": "South", "sales": 15000, "target": 13000, "rep": "Bob"},
                {"month": "Jan", "region": "East", "sales": 18000, "target": 15000, "rep": "Carol"},
                {"month": "Feb", "region": "East", "sales": 20000, "target": 16000, "rep": "Carol"},
                {"month": "Mar", "region": "East", "sales": 19000, "target": 17000, "rep": "Carol"},
                {"month": "Apr", "region": "East", "sales": 21000, "target": 18000, "rep": "Carol"}
            ],
            "products": [
                {"id": 1, "name": "Laptop Pro", "category": "Electronics", "price": 1299.99, "stock": 45, "rating": 4.5},
                {"id": 2, "name": "Smartphone X", "category": "Electronics", "price": 899.99, "stock": 120, "rating": 4.7},
                {"id": 3, "name": "Wireless Earbuds", "category": "Electronics", "price": 149.99, "stock": 89, "rating": 4.3},
                {"id": 4, "name": "Office Chair", "category": "Furniture", "price": 299.99, "stock": 22, "rating": 4.1},
                {"id": 5, "name": "Desk Lamp", "category": "Home", "price": 29.99, "stock": 156, "rating": 4.0},
                {"id": 6, "name": "Coffee Maker", "category": "Appliances", "price": 79.99, "stock": 67, "rating": 4.4},
                {"id": 7, "name": "Blender", "category": "Appliances", "price": 49.99, "stock": 34, "rating": 4.2},
                {"id": 8, "name": "Monitor 27\"", "category": "Electronics", "price": 349.99, "stock": 28, "rating": 4.6}
            ]
        }
    
    # ==================== CORE FUNCTIONALITY ====================
    
    def _get_current_time(self) -> str:
        """Get current date and time"""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _get_current_date(self) -> str:
        """Get current date"""
        return datetime.datetime.now().strftime("%Y-%m-%d")
    
    def _get_system_info(self) -> str:
        """Get system information"""
        try:
            uname = platform.uname()
            return f"""💻 **System Information**
OS: {uname.system} {uname.release} ({uname.version})
Architecture: {uname.machine}
Processor: {uname.processor}
Python: {platform.python_version()}
Hostname: {uname.node}"""
        except:
            return f"""💻 **System Information**
OS: {platform.system()} {platform.release()}
Python: {platform.python_version()}
Architecture: {platform.machine()}"""
    
    def _calculate_expression(self, expression: str) -> str:
        """Safely evaluate a mathematical expression"""
        try:
            # Remove any non-math characters for safety (basic sanitization)
            allowed_chars = set('0123456789+-*/().%^ ')
            cleaned = ''.join(c for c in expression if c in allowed_chars)
            
            # Replace ^ with ** for exponentiation
            cleaned = cleaned.replace('^', '**')
            
            # Add math functions safely
            allowed_names = {
                "abs": abs, "round": round, "min": min, "max": max, "sum": sum,
                "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "log": math.log, "log10": math.log10, "exp": math.exp,
                "pi": math.pi, "e": math.e
            }
            
            # Evaluate the expression
            result = eval(cleaned, {"__builtins__": {}}, allowed_names)
            
            # Format the result nicely
            if isinstance(result, float):
                if result.is_integer():
                    return str(int(result))
                else:
                    return f"{result:.6f}".rstrip('0').rstrip('.')
            else:
                return str(result)
                
        except Exception as e:
            return f"Sorry, I couldn't calculate that. Error: {str(e)}"
    
    def _get_knowledge(self, query: str) -> Optional[str]:
        """Retrieve information from knowledge base"""
        query_lower = query.lower().strip()
        
        # Direct lookup
        for key, value in self.knowledge_base.items():
            if key in query_lower or query_lower in key:
                return value
        
        # Pattern matching for common questions
        if any(word in query_lower for word in ['what is', 'what are', 'define', 'definition', 'explain']):
            # Extract the concept being asked about
            for key, value in self.knowledge_base.items():
                if key.replace('_', ' ') in query_lower:
                    return value
        
        return None
    
    def _analyze_dataset(self, dataset_name: str) -> str:
        """Provide analysis of a sample dataset"""
        if dataset_name not in self.sample_datasets:
            available = ", ".join(self.sample_datasets.keys())
            return f"I don't have a dataset named '{dataset_name}'. Available datasets: {available}"
        
        data = self.sample_datasets[dataset_name]
        if not data:
            return f"The dataset '{dataset_name}' is empty."
        
        # Basic info
        result = f"📊 **Dataset Analysis: {dataset_name.title()}**\n"
        result += f"   Records: {len(data)}\n"
        result += f"   Fields: {', '.join(data[0].keys())}\n\n"
        
        # Analyze numeric fields
        numeric_fields = {}
        for record in data:
            for key, value in record.items():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    if key not in numeric_fields:
                        numeric_fields[key] = []
                    numeric_fields[key].append(value)
        
        if numeric_fields:
            result += "📈 **Numeric Fields Summary:**\n"
            for field, values in numeric_fields.items():
                if len(values) >= 2:
                    mean_val = sum(values) / len(values)
                    median_val = sorted(values)[len(values)//2]
                    min_val = min(values)
                    max_val = max(values)
                    std_dev = (sum((x - mean_val) ** 2 for x in values) / len(values)) ** 0.5
                    result += f"   • {field}: Mean={mean_val:.2f}, Median={median_val:.2f}, StdDev={std_dev:.2f}, Range=[{min_val}-{max_val}]\n"
                else:
                    result += f"   • {field}: {values[0]} (single value)\n"
            result += "\n"
        
        # Analyze categorical fields
        categorical_fields = {}
        for record in data:
            for key, value in record.items():
                if not isinstance(value, (int, float)) or isinstance(value, bool):
                    if key not in categorical_fields:
                        categorical_fields[key] = []
                    if value not in categorical_fields[key]:
                        categorical_fields[key].append(value)
        
        if categorical_fields:
            result += "🏷️  **Categorical Fields:**\n"
            for field, values in categorical_fields.items():
                if len(values) <= 5:  # Show all if few options
                    values_str = ', '.join(str(v) for v in values)
                    result += f"   • {field}: {values_str}\n"
                else:
                    first_three = [str(v) for v in values[:3]]
                    values_str = ', '.join(first_three)
                    result += f"   • {field}: {len(values)} unique values (e.g., {values_str}...)\n"
        
        return result
    
    def _list_files(self, directory: str = ".") -> str:
        """List files in a directory"""
        try:
            items = os.listdir(directory)
            files = [f for f in items if os.path.isfile(os.path.join(directory, f))]
            dirs = [d for d in items if os.path.isdir(os.path.join(directory, d))]
            
            result = f"📁 **Contents of '{directory}':**\n"
            if dirs:
                result += "📂 **Directories:**\n"
                for d in sorted(dirs):
                    result += f"   • {d}/\n"
            if files:
                result += "📄 **Files:**\n"
                for f in sorted(files):
                    # Get file size
                    try:
                        size = os.path.getsize(os.path.join(directory, f))
                        if size < 1024:
                            size_str = f"{size} B"
                        elif size < 1024*1024:
                            size_str = f"{size/1024:.1f} KB"
                        else:
                            size_str = f"{size/(1024*1024):.1f} MB"
                        result += f"   • {f} ({size_str})\n"
                    except:
                        result += f"   • {f}\n"
            else:
                result += "   (No files found)\n"
            
            return result
        except Exception as e:
            return f"Error listing directory: {str(e)}"
    
    def _read_file(self, filename: str) -> str:
        """Read and display contents of a text file"""
        try:
            if not os.path.exists(filename):
                return f"File '{filename}' not found."
            
            # Check if it's likely a text file
            if os.path.getsize(filename) > CONFIG["file_size_limit"]:  # 1MB limit
                return f"File '{filename}' is too large to display (>1MB)."
            
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Limit display size
            if len(content) > CONFIG["display_limit"]:
                content = content[:CONFIG["display_limit"]] + "\n\n... (file truncated, showing first " + str(CONFIG["display_limit"]) + " characters)"
            
            return f"📄 **Contents of '{filename}':**\n{'-'*50}\n{content}\n{'-'*50}"
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def _run_system_command(self, command: str) -> str:
        """Run a system command safely"""
        # Security: Only allow certain safe commands
        safe_commands = ['ls', 'dir', 'pwd', 'whoami', 'date', 'time', 'echo', 'hostname']
        cmd_parts = command.strip().split()
        if not cmd_parts or cmd_parts[0] not in safe_commands:
            return "Sorry, I can only run safe system commands for security reasons."
        
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                output = result.stdout.strip()
                if not output:
                    return "Command executed successfully (no output)."
                return f"💻 **Command Output:**\n{output}"
            else:
                return f"❌ Command failed with error:\n{result.stderr.strip()}"
        except subprocess.TimeoutExpired:
            return "⏰ Command timed out (10 second limit)."
        except Exception as e:
            return f"Error executing command: {str(e)}"
    
    def _process_command(self, user_input: str) -> Optional[str]:
        """Process special commands"""
        command = user_input.strip().lower()
        
        # Help command
        if command in ['help', '?', 'commands']:
            return self._get_help_text()
        
        # Clear screen
        if command in ['clear', 'cls']:
            os.system('cls' if os.name == 'nt' else 'clear')
            return "Screen cleared. How can I assist you?"
        
        # Time/date commands
        if command == 'time':
            return f"🕐 Current time: {self._get_current_time()}"
        if command == 'date':
            return f"📅 Today's date: {self._get_current_date()}"
        
        # System info
        if command in ['system', 'sysinfo', 'info']:
            return self._get_system_info()
        
        # Calculator
        if command.startswith('calc '):
            expression = command[5:].strip()
            if not expression:
                return "Please provide a mathematical expression to calculate (e.g., 'calc 2+2*3')"
            result = self._calculate_expression(expression)
            return f"🧮 {expression} = {result}"
        
        # File operations
        if command == 'files':
            return self._list_files()
        if command.startswith('files '):
            directory = command[6:].strip()
            return self._list_files(directory)
        
        if command.startswith('read '):
            filename = command[5:].strip()
            if not filename:
                return "Please specify a filename to read (e.g., 'read poem.txt')"
            return self._read_file(filename)
        
        # Dataset analysis
        if command.startswith('stats '):
            dataset_name = command[6:].strip()
            if not dataset_name:
                return "Please specify a dataset name (e.g., 'stats employees')"
            return self._analyze_dataset(dataset_name)
        if command == 'datasets':
            datasets = list(self.sample_datasets.keys())
            return f"📊 Available datasets: {', '.join(datasets)}\nUse 'stats <dataset_name>' to analyze a dataset."
        
        # Conversation history
        if command == 'history':
            if not self.conversation_history:
                return "No conversation history yet."
            history_text = "📜 **Conversation History:**\n"
            for i, (user_msg, bot_resp) in enumerate(self.conversation_history[-5:], 1):  # Show last 5
                history_text += f"{i}. You: {user_msg[:50]}{'...' if len(user_msg) > 50 else ''}\n"
                history_text += f"   Me: {bot_resp[:50]}{'...' if len(bot_resp) > 50 else ''}\n\n"
            return history_text
        
        # About me
        if command in ['about', 'whoami']:
            return f"""🤖 **About {self.name}**
Version: {self.version}
Session started: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}
Capabilities: Natural language understanding, knowledge base, calculations, file operations, data analysis, system info
Created by: {self.creator}
Currently chatting with: {self.user_name or 'Anonymous'}"""
        
        # Reset conversation
        if command in ['reset', 'clear history']:
            self.conversation_history = []
            return "Conversation history cleared. Fresh start!"
        
        return None  # Not a command, let AI handle it
    
    def _get_help_text(self) -> str:
        """Return help text"""
        return """🤖 **Hermes Assistant - Available Commands**

**General Chat:**
Just type your question or message normally!

**Utility Commands:**
• `help` or `?` - Show this help message
• `clear` or `cls` - Clear the terminal screen
• `time` - Show current time
• `date` - Show current date
• `system` or `sysinfo` - Show system information
• `history` - Show recent conversation history
• `about` or `whoami` - Information about me
• `reset` or `clear history` - Clear conversation history
• `exit`, `quit`, `bye` - End the conversation

**Calculations:**
• `calc <expression>` - Calculate mathematical expressions
  Examples: `calc 2+2*3`, `calc sqrt(144)`, `calc (5+3)^2`, `calc sin(pi/2)`

**File Operations:**
• `files` - List files in current directory
• `files <directory>` - List files in specified directory
• `read <filename>` - Display contents of a text file

**Data Analysis:**
• `datasets` - Show available sample datasets
• `stats <dataset_name>` - Analyze a sample dataset
  Available: employees, sales, products
  Example: `stats employees`

**Tips:**
• Be specific with your questions for better answers
• I can help with: AI concepts, programming, calculations, general knowledge, file operations, data analysis
• Try asking: "What is machine learning?" or "Calculate 15% of 200" or "Stats employees"
"""
    
    def process_message(self, user_input: str) -> str:
        """Process user message and generate response"""
        # Store original input for history
        original_input = user_input
        
        # Check if it's a command first
        command_response = self._process_command(user_input)
        if command_response is not None:
            # Store in history
            self.conversation_history.append((original_input, command_response))
            return command_response
        
        # Not a command, process as natural language
        user_input_lower = user_input.lower().strip()
        
        # Handle greetings
        if any(greeting in user_input_lower for greeting in ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']):
            response = random.choice(self.greetings)
            if self.user_name:
                response = f"Hello {self.user_name}! " + response[len("Hello!"):]
        
        # Handle farewells
        elif any(farewell in user_input_lower for farewell in ['bye', 'goodbye', 'see you', 'farewell', 'exit', 'quit']):
            response = random.choice(self.farewells)
        
        # Handle name setting
        elif 'my name is' in user_input_lower or 'i am' in user_input_lower or 'im' in user_input_lower:
            # Simple name extraction
            words = user_input.split()
            for i, word in enumerate(words):
                if word.lower() in ['is', 'am', 'im'] and i+1 < len(words):
                    # Fix: Create list first to avoid f-string generator issue
                    name_parts = words[i+1:]
                    potential_name = ' '.join(name_parts).strip('.,!?')
                    if potential_name and len(potential_name) < 20:  # Reasonable name length
                        self.user_name = potential_name
                        response = f"Nice to meet you, {self.user_name}! How can I assist you today?"
                        break
            else:
                response = "Hello! I'm here to help. What's your name?"
        
        # Handle thanks
        elif any(thanks in user_input_lower for thanks in ['thank', 'thanks', 'thx']):
            responses = [
                "You're welcome! Happy to help.",
                "My pleasure! Let me know if you need anything else.",
                "Anytime! That's what I'm here for.",
                "You're very welcome! Feel free to ask more questions."
            ]
            response = random.choice(responses)
        
        # Handle jokes
        elif 'joke' in user_input_lower or 'funny' in user_input_lower:
            response = f"😄 {random.choice(self.jokes)}"
        
        # Handle quotes/inspiration
        elif any(word in user_input_lower for word in ['quote', 'inspire', 'motivation', 'inspirational']):
            response = f"💫 \"{random.choice(self.quotes)}\""
        
        # Handle weather (simulated)
        elif 'weather' in user_input_lower:
            conditions = ['sunny', 'partly cloudy', 'cloudy', 'light rain', 'showers', 'clear']
            temp = random.randint(15, 30)
            condition = random.choice(conditions)
            response = f"🌤️ Simulated weather: {condition.title()}, {temp}°C\n*(Note: I don't have access to real-time weather data)*"
        
        # Handle knowledge questions
        else:
            knowledge_response = self._get_knowledge(user_input)
            if knowledge_response:
                response = f"📚 {knowledge_response}"
            else:
                # Try to handle as a general question
                response = self._generate_general_response(user_input)
        
        # Store in conversation history
        self.conversation_history.append((original_input, response))
        
        return response
    
    def _generate_general_response(self, user_input: str) -> str:
        """Generate a general response for unrecognized queries"""
        user_lower = user_input.lower()
        
        # Check for question words
        if any(word in user_lower for word in ['what', 'how', 'why', 'when', 'where', 'who', 'which']):
            responses = [
                f"That's an interesting question about '{user_input}'. While I don't have specific information on that topic in my knowledge base, I can help with calculations, explain AI/programming concepts, analyze data, or assist with other tasks. Would you like help with something else?",
                f"I'm not sure I have detailed information about '{user_input}' in my current knowledge base. However, I'm good at math, can explain technical concepts, help with file operations, analyze datasets, or just chat. What would you like to try?",
                f"That's a thoughtful question! My expertise is more focused on AI concepts, technical topics, science, and practical assistance like calculations and data analysis. Could you rephrase your question or ask about something I might know more about?"
            ]
            return random.choice(responses)
        else:
            # Statement or comment
            responses = [
                f"I see. Thanks for sharing that about '{user_input}'. Is there something specific you'd like me to help you with?",
                f"Interesting point about '{user_input}'. Would you like to explore that further, or is there something else I can assist you with?",
                f"Thanks for telling me! If you have any questions or need help with calculations, information, file operations, data analysis, or just want to chat, I'm here.",
                f"That's noteworthy! Is there a particular aspect you'd like to dive deeper into, or shall we talk about something else?"
            ]
            return random.choice(responses)
    
    def start_chat(self):
        """Start the interactive chat session"""
        # Clear screen for clean start
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 60)
        print(f"🤖 {self.name} v{self.version}")
        print("   Your Advanced AI Assistant")
        print("=" * 60)
        print("Type 'help' for available commands, or just start chatting!")
        print("Type 'exit', 'quit', or 'bye' to end the conversation.")
        print("-" * 60)
        
        # Initial greeting
        print(f"\n{self.name}: {random.choice(self.greetings)}")
        print("-" * 60)
        
        # Main chat loop
        while True:
            try:
                # Get user input
                user_input = input("\n> ").strip()
                
                # Check for exit commands
                if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                    farewell = random.choice(self.farewells)
                    if self.user_name:
                        farewell = f"Goodbye {self.user_name}! {farewell[len('Goodbye!'):]}"
                    print(f"\n{self.name}: {farewell}")
                    break
                
                # Skip empty input
                if not user_input:
                    continue
                
                # Process and get response
                response = self.process_message(user_input)
                
                # Display response
                print(f"\n{self.name}: {response}")
                print("-" * 40)
                
            except KeyboardInterrupt:
                print(f"\n\n{self.name}: Goodbye! (Interrupted)")
                break
            except EOFError:
                # Handle non-interactive environments gracefully
                print(f"\n\n{self.name}: Session ended. Goodbye!")
                break
            except Exception as e:
                print(f"\n{self.name}: Sorry, I encountered an error: {str(e)}")
                print("Please try again or type 'help' for assistance.")

# ==================== MAIN EXECUTION ====================

def main():
    """Main function to start the assistant"""
    assistant = HermesAssistant()
    assistant.start_chat()

if __name__ == "__main__":
    # Check if we're running in a terminal that supports input
    if not sys.stdin.isatty():
        print("Note: For full interactive experience, run this in a terminal/command prompt.")
        print("Starting in demo mode...\n")
        
        # Demo mode for non-interactive environments
        assistant = HermesAssistant()
        print(f"🤖 {assistant.name} v{assistant.version}")
        print("=" * 50)
        print("Demo: Sample interactions")
        print("-" * 50)
        
        # Show a few sample interactions
        samples = [
            "Hello!",
            "What is artificial intelligence?",
            "Calculate 25% of 2000",
            "Tell me a joke",
            "Stats employees",
            "About",
            "Thanks!",
            "Bye"
        ]
        
        for sample in samples:
            print(f"\n> {sample}")
            response = assistant.process_message(sample)
            print(f"{assistant.name}: {response}")
            print("-" * 30)
        
        print("\n💡 To use the full interactive version, run this script in your terminal!")
    else:
        try:
            main()
        except KeyboardInterrupt:
            print("\n\nChatbot terminated by user. Goodbye!")
        except Exception as e:
            print(f"\nFatal error: {str(e)}")
            sys.exit(1)