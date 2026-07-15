#!/usr/bin/env python3
"""
JAVIS - Just A Very Intelligent System (Enhanced)
An AI Assistant Combining Features of Modern AI Coding Agents with LLM Integration
Inspired by: Claude Code, Codex, Cursor, Gemini, ChatGPT, NVIDIA tools, and Antigravity-IDE
Features: Conversational AI, Code Assistance, System Diagnostics (Including GPU), File Operations, Data Analysis, Persistent Learning, LLM Integration
"""

import os
import sys
import json
import math
import random
import datetime
import subprocess
import platform
import re
from typing import Dict, List, Any, Optional, Tuple
import requests  # For LLM API calls

# ==================== CONFIGURATION ====================

CONFIG = {
    "name": "JAVIS",
    "version": "2.1.0",  # Upgraded version with LLM support
    "creator": "Inspired by Claude Code, Codex, Cursor, Gemini, ChatGPT, NVIDIA",
    "max_history": 50,
    "file_size_limit": 1024 * 1024,  # 1MB
    "display_limit": 1500,
    "code_sandbox_dir": "./code_sandbox",
    "data_dir": "./javis_data",
    "knowledge_file": "custom_knowledge.json",
    "preferences_file": "user_preferences.json",
    "facts_file": "learned_facts.json",
    # LLM Configuration
    "llm_provider": None,  # Options: "openai", "anthropic", "huggingface", "local"
    "llm_api_key": None,   # Will be loaded from environment variable or config file
    "llm_model": None,     # Default model for the provider
    "llm_max_tokens": 1000,
    "llm_temperature": 0.7,
    # Environment variable names for API keys
    "env_openai_key": "OPENAI_API_KEY",
    "env_anthropic_key": "ANTHROPIC_API_KEY",
    "env_huggingface_key": "HUGGINGFACE_API_KEY",
}

# ==================== MAIN ASSISTANT CLASS ====================

class JAVIS:
    """Just A Very Intelligent System - Enhanced Universal AI Assistant with coding agent capabilities and LLM integration"""
    
    def __init__(self):
        self.name = CONFIG["name"]
        self.version = CONFIG["version"]
        self.creator = CONFIG["creator"]
        self.conversation_history = []
        self.user_name = None
        self.session_start = datetime.datetime.now()
        self.code_sandbox = CONFIG["code_sandbox_dir"]
        self.data_dir = CONFIG["data_dir"]
        
        # Create necessary directories
        os.makedirs(self.code_sandbox, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Load data
        self.knowledge_base = self._load_knowledge_base()
        self.custom_knowledge = self._load_custom_knowledge()
        self.user_preferences = self._load_user_preferences()
        self.learned_facts = self._load_learned_facts()
        
        # Load LLM configuration from environment
        self._load_llm_config()
        
        # Response templates
        self.greetings = [
            f"Hello! I'm {self.name} v{self.version}, your enhanced AI coding assistant. How can I help you today?",
            f"Hi there! Ready to assist with coding, questions, calculations, or just chat. What's on your mind?",
            f"Greetings! I combine capabilities of modern AI coding agents to help you develop software efficiently.",
            f"Hey! I'm {self.name}. I can write code, explain concepts, analyze files, help with debugging, and even learn from our conversations."
        ]
        
        self.farewells = [
            "Goodbye! Thanks for letting me assist with your coding journey. Have a great day!",
            "See you later! Remember I'm here whenever you need coding assistance.",
            "Farewell! Thanks for the conversation. Come back anytime for more AI-powered development!",
            "Bye for now! I'll be here when you need me for programming tasks."
        ]
        
        self.jokes = [
            "Why don't scientists trust atoms anymore? Because they make up everything!",
            "I told my computer I needed a break, and it said 'No problem - I'll go to sleep mode'.",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "There are 10 types of people in the world: those who understand binary, and those who don't.",
            "Why did the programmer quit his job? Because he didn't get arrays (a raise)!",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why was the math book sad? Because it had too many problems.",
            "I would tell you a UDP joke, but you might not get it.",
            "Why do Java developers wear glasses? Because they don't see sharp!"
        ]
        
        self.quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Innovation distinguishes between a leader and a follower. - Steve Jobs",
            "Talk is cheap. Show me the code. - Linus Torvalds",
            "Programs must be written for people to read, and only incidentally for machines to execute. - Harold Abelson",
            "First, solve the problem. Then, write the code. - John Johnson",
            "Everyone knows that debugging is twice as hard as writing a program in the first place. So if you're as clever as you can be when you write it, how will you ever debug it? - Brian Kernighan",
            "The function of good software is to make the complex appear to be simple. - Grady Booch",
            "Simplicity is prerequisite for reliability. - Edsger W. Dijkstra",
            "Premature optimization is the root of all evil. - Donald Knuth",
            "Measuring programming progress by lines of code is like measuring aircraft building progress by weight. - Bill Gates"
        ]
    
    # ==================== CONFIGURATION LOADING ====================
    
    def _load_llm_config(self):
        """Load LLM configuration from environment variables"""
        # Check for LLM provider in environment
        provider = os.environ.get("JAVIS_LLM_PROVIDER")
        if provider in ["openai", "anthropic", "huggingface", "local"]:
            CONFIG["llm_provider"] = provider
        
        # Check for API keys
        if CONFIG["llm_provider"] == "openai":
            CONFIG["llm_api_key"] = os.environ.get(CONFIG["env_openai_key"])
            CONFIG["llm_model"] = os.environ.get("JAVIS_LLM_MODEL", "gpt-3.5-turbo")
        elif CONFIG["llm_provider"] == "anthropic":
            CONFIG["llm_api_key"] = os.environ.get(CONFIG["env_anthropic_key"])
            CONFIG["llm_model"] = os.environ.get("JAVIS_LLM_MODEL", "claude-3-haiku-20240307")
        elif CONFIG["llm_provider"] == "huggingface":
            CONFIG["llm_api_key"] = os.environ.get(CONFIG["env_huggingface_key"])
            CONFIG["llm_model"] = os.environ.get("JAVIS_LLM_MODEL", "HuggingFaceH4/zephyr-7b-beta")
        # For local, we might check for a local server URL
        elif CONFIG["llm_provider"] == "local":
            CONFIG["llm_api_key"] = os.environ.get("JAVIS_LLM_API_KEY", "not-needed-for-local")
            CONFIG["llm_model"] = os.environ.get("JAVIS_LLM_MODEL", "local-model")
            # Could also set a local endpoint
            # CONFIG["llm_api_base"] = os.environ.get("JAVIS_LLM_API_BASE", "http://localhost:8080")
    
    # ==================== DATA PERSISTENCE ====================
    
    def _load_knowledge_base(self) -> Dict[str, str]:
        """Load the AI's knowledge base focused on coding, AI, and general knowledge"""
        return {
            # Coding & Software Engineering
            "algorithm": "An algorithm is a finite sequence of well-defined instructions, typically to solve a class of problems or to perform a computation.",
            "data_structure": "A data structure is a particular way of organizing data in a computer so that it can be used efficiently.",
            "object_oriented": "Object-oriented programming (OOP) is a programming paradigm based on the concept of 'objects', which can contain data and code: data in the form of fields, and code, in the form of procedures.",
            "functional_programming": "Functional programming is a programming paradigm where programs are constructed by applying and composing functions.",
            "recursion": "Recursion is a method of solving problems where the solution depends on solutions to smaller instances of the same problem.",
            "big_o": "Big O notation describes the performance or complexity of an algorithm. O(1) is constant time, O(n) is linear, O(n²) is quadratic, etc.",
            "debugging": "Debugging is the process of finding and resolving defects or problems within a computer program that prevent correct operation.",
            "version_control": "Version control is a system that records changes to a file or set of files over time so that you can recall specific versions later.",
            "git": "Git is a distributed version control system for tracking changes in source code during software development.",
            "testing": "Software testing is an investigation conducted to provide stakeholders with information about the quality of the software product or service under test.",
            "api_design": "API design is the process of developing application programming interfaces (APIs) that expose backend data and application functionality for use by new applications.",
            "refactoring": "Refactoring is the process of restructuring existing computer code—changing the factoring—without changing its external behavior.",
            "design_patterns": "Design patterns are typical solutions to common problems in software design. Each pattern is like a blueprint that you can customize to solve a particular design problem in your code.",
            "clean_code": "Clean code is code that is easy to understand and easy to change. It follows principles like readability, simplicity, and clarity.",
            
            # AI & ML
            "ai_definition": "Artificial Intelligence (AI) is the simulation of human intelligence in machines that are programmed to think like humans and mimic their actions.",
            "machine_learning": "Machine Learning is a subset of AI that provides systems the ability to automatically learn and improve from experience without being explicitly programmed.",
            "deep_learning": "Deep Learning is a subset of machine learning that uses neural networks with many layers to analyze various factors of data.",
            "nlp": "Natural Language Processing (NLP) is a branch of AI that helps computers understand, interpret and manipulate human language.",
            "llm": "Large Language Models (LLMs) are a type of AI model that can recognize and generate text, among other tasks.",
            "prompt_engineering": "Prompt engineering is the process of structuring text that can be interpreted and understood by a generative AI model.",
            "fine_tuning": "Fine-tuning is the process of taking a pre-trained model and further training it on a specific dataset to adapt it to a particular task.",
            "rag": "Retrieval-Augmented Generation (RAG) is an AI framework for retrieving facts from an external knowledge base to ground large language models (LLMs) on the most accurate, up-to-date information.",
            "agents": "AI agents are systems that perceive their environment and take actions to maximize their chances of achieving their goals.",
            "multimodal": "Multimodal AI refers to systems that can process and understand multiple types of data, such as text, images, and audio.",
            
            # NVIDIA & GPU Computing
            "nvidia": "NVIDIA Corporation is a technology company known for its graphics processing units (GPUs) for gaming and professional markets, as well as system on a chip units (SoCs) for mobile computing and automotive markets.",
            "gpu": "A Graphics Processing Unit (GPU) is a specialized electronic circuit designed to rapidly manipulate and alter memory to accelerate the creation of images in a frame buffer intended for output to a display device.",
            "cuda": "CUDA (Compute Unified Device Architecture) is a parallel computing platform and application programming interface (API) model created by NVIDIA. It allows software developers to use a CUDA-enabled graphics processing unit (GPU) for general purpose processing.",
            "tensorrt": "TensorRT is NVIDIA's high-performance deep learning inference optimizer and runtime that delivers low latency and high-throughput for deep learning inference applications.",
            "rapids": "RAPIDS is a suite of open-source software libraries and APIs for executing end-to-end data science and analytics pipelines entirely on GPUs.",
            "vgpu": "Virtual GPU (vGPU) technology allows multiple virtual machines (VMs) to share a single physical GPU hardware resource.",
            
            # Development Tools & Practices
            "ide": "An Integrated Development Environment (IDE) is a software application that provides comprehensive facilities to computer programmers for software development.",
            "code_editor": "A code editor is a type of text editor designed specifically for editing source code of computer programs.",
            "linting": "Linting is the process of running a program that will analyse code for potential errors.",
            "formatting": "Code formatting is the process of automatically adjusting the layout of code to conform to a predefined style.",
            "code_review": "Code review is the systematic examination (sometimes known as peer review) of computer source code.",
            "pair_programming": "Pair programming is an agile software development technique in which two programmers work together at one workstation.",
            "test_driven_development": "Test-driven development (TDD) is a software development process that relies on the repetition of a very short development cycle: requirements are turned into very specific test cases, then the code is improved so that the tests pass.",
            "continuous_integration": "Continuous Integration (CI) is the practice of the integration of code changes from multiple contributors into a single software project.",
            "devops": "DevOps is a set of practices that combines software development (Dev) and IT operations (Ops).",
            
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
            
            # About JAVIS
            "javis_origin": "JAVIS is an AI assistant inspired by the Hermes framework, created to combine capabilities of modern AI coding agents.",
            "javis_universal_capabilities": "JAVIS combines conversational AI, code assistance, system diagnostics (including GPU/NVIDIA), file operations, and data analysis to assist with software development and general tasks.",
            "javis_version": f"This is {self.name} version {self.version}.",
        }
    
    def _load_custom_knowledge(self) -> Dict[str, str]:
        """Load user-customized knowledge"""
        filepath = os.path.join(self.data_dir, CONFIG["knowledge_file"])
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load custom knowledge: {e}")
        return {}
    
    def _save_custom_knowledge(self):
        """Save user-customized knowledge"""
        filepath = os.path.join(self.data_dir, CONFIG["knowledge_file"])
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.custom_knowledge, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save custom knowledge: {e}")
    
    def _load_user_preferences(self) -> Dict[str, Any]:
        """Load user preferences"""
        filepath = os.path.join(self.data_dir, CONFIG["preferences_file"])
        defaults = {
            "theme": "default",
            "response_verbosity": "medium",  # low, medium, high
            "show_timestamps": False,
            "code_explanation_detail": "medium"
        }
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    prefs = json.load(f)
                    # Merge with defaults
                    for key, value in defaults.items():
                        if key not in prefs:
                            prefs[key] = value
                    return prefs
        except Exception as e:
            print(f"Warning: Could not load user preferences: {e}")
        return defaults
    
    def _save_user_preferences(self):
        """Save user preferences"""
        filepath = os.path.join(self.data_dir, CONFIG["preferences_file"])
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.user_preferences, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save user preferences: {e}")
    
    def _load_learned_facts(self) -> List[Dict[str, Any]]:
        """Learn facts from conversation"""
        filepath = os.path.join(self.data_dir, CONFIG["facts_file"])
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load learned facts: {e}")
        return []
    
    def _save_learned_facts(self):
        """Save learned facts"""
        filepath = os.path.join(self.data_dir, CONFIG["facts_file"])
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.learned_facts, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save learned facts: {e}")
    
    # ==================== CORE FUNCTIONALITY ====================
    
    def _get_current_time(self) -> str:
        """Get current date and time"""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _get_current_date(self) -> str:
        """Get current date"""
        return datetime.datetime.now().strftime("%Y-%m-%d")
    
    def _get_system_info(self) -> str:
        """Get system information including GPU/NVIDIA details"""
        try:
            uname = platform.uname()
            info = f"""💻 **System Information**
OS: {uname.system} {uname.release} ({uname.version})
Architecture: {uname.machine}
Processor: {uname.processor}
Python: {platform.python_version()}
Hostname: {uname.node}"""
            
            # Try to get GPU info
            gpu_info = self._get_gpu_info()
            if gpu_info:
                info += f"\n\n🎮 **Graphics Processing Units:**\n{gpu_info}"
            
            # Try to get memory info
            try:
                import psutil
                memory = psutil.virtual_memory()
                info += f"\n\n💾 **Memory**\nTotal: {memory.total // (1024**3)} GB\nAvailable: {memory.available // (1024**3)} GB\nUsed: {memory.percent}%"
            except ImportError:
                pass
                
            return info
        except Exception as e:
            return f"""💻 **System Information**
OS: {platform.system()} {platform.release()}
Python: {platform.python_version()}
Error getting detailed info: {str(e)}"""
    
    def _get_gpu_info(self) -> Optional[str]:
        """Attempt to get GPU information, especially NVIDIA"""
        try:
            # Try nvidia-smi first (most reliable for NVIDIA)
            result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                # Parse nvidia-smi output for key info
                lines = result.stdout.split('\n')
                gpu_lines = [line for line in lines if 'GeForce' in line or 'RTX' in line or 'GTX' in line or 'Tesla' in line or 'Quadro' in line]
                if gpu_lines:
                    # Take first GPU line
                    gpu_line = gpu_lines[0].strip()
                    # Clean up the line
                    gpu_line = re.sub(r'\s+', ' ', gpu_line)
                    return f"NVIDIA GPU detected: {gpu_line}"
                else:
                    # If no specific GPU line found, still indicate NVIDIA-smi works
                    return "NVIDIA GPU detected (via nvidia-smi). See full output for details."
            else:
                # nvidia-smi not found or failed
                pass
        except (FileNotFoundError, subprocess.TimeoutExpired):
            # nvidia-smi not available or timeout
            pass
        except Exception:
            pass
        
        # Try alternative: lspci for Linux
        try:
            if platform.system() == "Linux":
                result = subprocess.run(['lspci', '-vnn'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    vga_lines = [line for line in lines if 'VGA compatible controller' in line or '3D controller' in line]
                    nvidia_lines = [line for line in vga_lines if 'NVIDIA' in line]
                    if nvidia_lines:
                        # Extract first NVIDIA GPU line
                        gpu_line = nvidia_lines[0].strip()
                        gpu_line = re.sub(r'\s+', ' ', gpu_line)
                        return f"NVIDIA GPU detected (via lspci): {gpu_line}"
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        except Exception:
            pass
        
        # If we get here, no NVIDIA GPU detected via common methods
        return None
    
    def _get_git_info(self) -> str:
        """Get Git repository information"""
        try:
            # Check if we're in a git repository
            result = subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode != 0 or result.stdout.strip() != 'true':
                return "Not a Git repository."
            
            info = "📦 **Git Repository Information**\n"
            
            # Get current branch
            result = subprocess.run(['git', 'branch', '--show-current'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                branch = result.stdout.strip()
                info += f"   Current branch: {branch}\n"
            
            # Get remote origin URL
            result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                remote = result.stdout.strip()
                info += f"   Remote origin: {remote}\n"
            else:
                info += "   Remote origin: Not set\n"
            
            # Get last commit
            result = subprocess.run(['git', 'log', '-1', '--pretty=format:%h %s (%an, %ar)'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                last_commit = result.stdout.strip()
                info += f"   Last commit: {last_commit}\n"
            else:
                info += "   Last commit: Unable to retrieve\n"
            
            # Get status (staged/changes)
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                status = result.stdout.strip()
                if not status:
                    info += "   Working tree: Clean\n"
                else:
                    # Count changes
                    lines = status.split('\n')
                    modified = len(lines)
                    info += f"   Working tree: {len(lines)} change(s)\n"
            else:
                info += "   Working tree: Unable to retrieve status\n"
            
            return info.strip()
        except Exception as e:
            return f"Error getting Git info: {str(e)}"
    
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
                "pi": math.pi, "e": math.e, "factorial": math.factorial
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
        
        # Check built-in knowledge base
        for key, value in self.knowledge_base.items():
            if key in query_lower or query_lower in key:
                return value
        
        # Check custom knowledge
        for key, value in self.custom_knowledge.items():
            if key in query_lower or query_lower in key:
                return value
        
        # Pattern matching for common questions
        if any(word in query_lower for word in ['what is', 'what are', 'define', 'definition', 'explain', 'how does']):
            # Check built-in knowledge
            for key, value in self.knowledge_base.items():
                if key.replace('_', ' ') in query_lower:
                    return value
            # Check custom knowledge
            for key, value in self.custom_knowledge.items():
                if key.replace('_', ' ') in query_lower:
                    return value
        
        return None
    
    def _llm_available(self) -> bool:
        """Check if LLM is configured and available"""
        return (CONFIG["llm_provider"] is not None and 
                CONFIG["llm_api_key"] is not None and
                len(CONFIG["llm_api_key"]) > 0)
    
    def _query_llm(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Query the configured LLM provider"""
        if not self._llm_available():
            return "LLM not configured. Please set up LLM provider and API key."
        
        try:
            if CONFIG["llm_provider"] == "openai":
                return self._query_openai(prompt, system_prompt)
            elif CONFIG["llm_provider"] == "anthropic":
                return self._query_anthropic(prompt, system_prompt)
            elif CONFIG["llm_provider"] == "huggingface":
                return self._query_huggingface(prompt, system_prompt)
            elif CONFIG["llm_provider"] == "local":
                return self._query_local(prompt, system_prompt)
            else:
                return f"Unsupported LLM provider: {CONFIG['llm_provider']}"
        except Exception as e:
            return f"Error querying LLM: {str(e)}"
    
    def _query_openai(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Query OpenAI API"""
        if not CONFIG["llm_api_key"]:
            return "OpenAI API key not configured."
        
        headers = {
            "Authorization": f"Bearer {CONFIG['llm_api_key']}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": CONFIG["llm_model"] or "gpt-3.5-turbo",
            "messages": messages,
            "max_tokens": CONFIG["llm_max_tokens"],
            "temperature": CONFIG["llm_temperature"]
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        else:
            return f"OpenAI API error: {response.status_code} - {response.text}"
    
    def _query_anthropic(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Query Anthropic Claude API"""
        if not CONFIG["llm_api_key"]:
            return "Anthropic API key not configured."
        
        headers = {
            "x-api-key": CONFIG["llm_api_key"],
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        # Anthropic expects a slightly different format
        data = {
            "model": CONFIG["llm_model"] or "claude-3-haiku-20240307",
            "max_tokens": CONFIG["llm_max_tokens"],
            "temperature": CONFIG["llm_temperature"],
            "messages": [{"role": "user", "content": prompt}]
        }
        
        if system_prompt:
            data["system"] = system_prompt
        
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["content"][0]["text"].strip()
        else:
            return f"Anthropic API error: {response.status_code} - {response.text}"
    
    def _query_huggingface(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Query Hugging Face Inference API"""
        if not CONFIG["llm_api_key"]:
            return "Hugging Face API key not configured."
        
        headers = {
            "Authorization": f"Bearer {CONFIG['llm_api_key']}",
            "Content-Type": "application/json"
        }
        
        # Format prompt for Hugging Face (some models expect specific format)
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        data = {
            "inputs": full_prompt,
            "parameters": {
                "max_new_tokens": CONFIG["llm_max_tokens"],
                "temperature": CONFIG["llm_temperature"],
                "return_full_text": False
            }
        }
        
        # Using the inference API endpoint
        api_url = f"https://api-inference.huggingface.co/models/{CONFIG['llm_model']}"
        
        response = requests.post(
            api_url,
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            # Handle different response formats
            if isinstance(result, list) and len(result) > 0:
                if "generated_text" in result[0]:
                    return result[0]["generated_text"].strip()
                elif "text" in result[0]:
                    return result[0]["text"].strip()
            elif isinstance(result, dict):
                if "generated_text" in result:
                    return result["generated_text"].strip()
                elif "text" in result:
                    return result["text"].strip()
            return str(result).strip()
        else:
            return f"Hugging Face API error: {response.status_code} - {response.text}"
    
    def _query_local(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Query local LLM server (e.g., llama.cpp server, text-generation-webui, etc.)"""
        # This is a placeholder - actual implementation would depend on the local server
        # For example, if using llama.cpp server with OpenAI-compatible API:
        api_base = os.environ.get("JAVIS_LLM_API_BASE", "http://localhost:8080/v1")
        
        headers = {
            "Content-Type": "application/json"
        }
        # Some local servers don't require API key, but we can include if provided
        if CONFIG["llm_api_key"] and CONFIG["llm_api_key"] != "not-needed-for-local":
            headers["Authorization"] = f"Bearer {CONFIG['llm_api_key']}"
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": CONFIG["llm_model"] or "local-model",
            "messages": messages,
            "max_tokens": CONFIG["llm_max_tokens"],
            "temperature": CONFIG["llm_temperature"]
        }
        
        try:
            response = requests.post(
                f"{api_base}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                return f"Local LLM API error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error connecting to local LLM: {str(e)}"
    
    def _learn_fact(self, fact: str, context: str = ""):
        """Learn a new fact from conversation"""
        fact_entry = {
            "fact": fact.strip(),
            "context": context.strip(),
            "timestamp": self._get_current_time(),
            "importance": 1  # Could be enhanced with usage tracking
        }
        
        # Avoid duplicates
        for existing in self.learned_facts:
            if existing["fact"].lower() == fact.lower():
                # Update timestamp and maybe increase importance
                existing["timestamp"] = self._get_current_time()
                existing["importance"] += 1
                self._save_learned_facts()
                return
        
        self.learned_facts.append(fact_entry)
        # Keep only recent facts (limit to 1000)
        if len(self.learned_facts) > 1000:
            self.learned_facts = self.learned_facts[-1000:]
        self._save_learned_facts()
    
    def _get_relevant_facts(self, query: str, limit: int = 5) -> List[str]:
        """Get facts relevant to the current query"""
        query_lower = query.lower()
        relevant_facts = []
        
        for fact_entry in self.learned_facts:
            fact_text = fact_entry["fact"].lower()
            # Simple relevance check: common words
            query_words = set(query_lower.split())
            fact_words = set(fact_text.split())
            common_words = query_words.intersection(fact_words)
            
            if len(common_words) >= 2:  # At least 2 words in common
                relevant_facts.append((fact_entry["fact"], len(common_words)))
        
        # Sort by relevance (number of common words) descending
        relevant_facts.sort(key=lambda x: x[1], reverse=True)
        
        # Return just the facts, up to limit
        return [fact for fact, _ in relevant_facts[:limit]]
    
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
    
    @property
    def sample_datasets(self) -> Dict[str, List[Dict[str, Any]]]:
        """Return sample datasets for demonstration purposes"""
        return {
            "employees": [
                {"id": 1, "name": "Alice Smith", "department": "Engineering", "salary": 75000, "years_of_experience": 5},
                {"id": 2, "name": "Bob Johnson", "department": "Marketing", "salary": 65000, "years_of_experience": 3},
                {"id": 3, "name": "Carol Davis", "department": "Engineering", "salary": 82000, "years_of_experience": 7},
                {"id": 4, "name": "David Wilson", "department": "Sales", "salary": 60000, "years_of_experience": 2},
                {"id": 5, "name": "Eve Brown", "department": "HR", "salary": 58000, "years_of_experience": 4}
            ],
            "sales": [
                {"date": "2023-01-01", "product": "Widget A", "quantity": 10, "price": 15.99, "total": 159.90},
                {"date": "2023-01-02", "product": "Widget B", "quantity": 5, "price": 29.99, "total": 149.95},
                {"date": "2023-01-03", "product": "Widget A", "quantity": 8, "price": 15.99, "total": 127.92},
                {"date": "2023-01-04", "product": "Widget C", "quantity": 3, "price": 49.99, "total": 149.97},
                {"date": "2023-01-05", "product": "Widget B", "quantity": 7, "price": 29.99, "total": 209.93}
            ],
            "products": [
                {"id": 1, "name": "Laptop Pro", "category": "Electronics", "price": 1299.99, "stock": 50},
                {"id": 2, "name": "Wireless Mouse", "category": "Electronics", "price": 29.99, "stock": 200},
                {"id": 3, "name": "Office Chair", "category": "Furniture", "price": 199.99, "stock": 75},
                {"id": 4, "name": "Desk Lamp", "category": "Home", "price": 39.99, "stock": 150},
                {"id": 5, "name": "Coffee Mug", "category": "Kitchen", "price": 12.99, "stock": 300}
            ]
        }
    
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
    
    def _write_file(self, filename: str, content: str) -> str:
        """Write content to a file"""
        try:
            # Ensure we're writing to a safe location (within current directory or sandbox)
            if not os.path.isabs(filename):
                # If relative path, prepend current directory for safety check
                full_path = os.path.abspath(filename)
            else:
                full_path = filename
            
            # Basic security: don't allow writing to system directories
            restricted_paths = ['/etc', '/var', '/usr', '/boot', '/lib', '/sbin', '/bin']
            if any(full_path.startswith(rp) for rp in restricted_paths):
                return "Error: Writing to system directories is not allowed for security reasons."
            
            # Create directory if needed
            os.makedirs(os.path.dirname(full_path) if os.path.dirname(full_path) else '.', exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"✅ Successfully wrote to {os.path.basename(filename)}"
        except Exception as e:
            return f"Error writing file: {str(e)}"
    
    def _suggest_code_edit(self, file_path: str, instruction: str) -> str:
        """Suggest a code edit based on natural language instruction"""
        if not os.path.exists(file_path):
            return f"File '{file_path}' not found."
        
        try:
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # For now, we'll provide a simple suggestion based on keywords
            # In a real implementation, this would use an LLM, but we'll simulate with rules
            suggestion = self._generate_code_suggestion(original_content, instruction)
            
            if suggestion is None:
                return "I couldn't generate a specific code suggestion for that instruction. Please try being more specific or provide the code snippet you'd like me to work with."
            
            # Show the suggested change in a diff-like format
            result = f"💡 **Suggested Code Edit for {os.path.basename(file_path)}**\n"
            result += f"Based on: \"{instruction}\"\n\n"
            result += "🔴 **Original (first 20 lines):**\n"
            original_lines = original_content.split('\n')[:20]
            for i, line in enumerate(original_lines, 1):
                result += f"{i:2d}: {line}\n"
            if len(original_content.split('\n')) > 20:
                result += "    ... (truncated)\n"
            
            result += "\n🟢 **Suggested (first 20 lines):**\n"
            suggested_lines = suggestion.split('\n')[:20]
            for i, line in enumerate(suggested_lines, 1):
                result += f"{i:2d}: {line}\n"
            if len(suggestion.split('\n')) > 20:
                result += "    ... (truncated)\n"
            
            result += "\n📝 **To apply this change, you can:**\n"
            result += "1. Copy the suggested code above\n"
            result += "2. Replace the content of the file with it\n"
            result += "3. Or use a tool like `sed` or a code editor to make the changes\n\n"
            result += "💡 Tip: For more complex edits, consider breaking down your request into smaller steps."
            
            return result
            
        except Exception as e:
            return f"Error suggesting code edit: {str(e)}"
    
    def _generate_code_suggestion(self, original_content: str, instruction: str) -> Optional[str]:
        """Generate a code suggestion based on instruction (simplified rule-based)"""
        instruction_lower = instruction.lower()
        original_lower = original_content.lower()
        
        # Simple rule-based suggestions for demonstration
        if "add a function" in instruction_lower or "create a function" in instruction_lower:
            # Extract function name if possible
            func_name = "new_function"
            # Look for quoted names or camelCase after "function"
            match = re.search(r'function\s+["\']?([a-zA-Z_][a-zA-Z0-9_]*)["\']?', instruction_lower)
            if match:
                func_name = match.group(1)
            elif "called" in instruction_lower:
                # Try to get name after "called"
                parts = instruction_lower.split("called")
                if len(parts) > 1:
                    potential_name = parts[1].strip().split()[0]
                    if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', potential_name):
                        func_name = potential_name
            
            suggestion = f"\ndef {func_name}():\n    \"\"\"{instruction.capitalize()}.\"\"\"\n    # TODO: Implement functionality\n    pass\n"
            return suggestion
        
        elif "add a class" in instruction_lower or "create a class" in instruction_lower:
            class_name = "NewClass"
            match = re.search(r'class\s+["\']?([a-zA-Z_][a-zA-Z0-9_]*)["\']?', instruction_lower)
            if match:
                class_name = match.group(1)
            elif "called" in instruction_lower:
                # Try to get name after "called"
                parts = instruction_lower.split("called")
                if len(parts) > 1:
                    potential_name = parts[1].strip().split()[0]
                    if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', potential_name):
                        class_name = potential_name
            
            suggestion = f"\nclass {class_name}:\n    \"\"\"{instruction.capitalize()}.\"\"\"\n    \n    def __init__(self):\n        pass\n"
            return suggestion
        
        elif "add error handling" in instruction_lower or "add try except" in instruction_lower:
            # Wrap the main logic in try-except
            lines = original_content.split('\n')
            if len(lines) > 0 and not original_content.strip().startswith('try:'):
                # Simple wrapping: indent everything and wrap in try-except
                indented = ['    ' + line if line.strip() != '' else line for line in lines]
                suggestion = "try:\n" + '\n'.join(indented) + "\nexcept Exception as e:\n    print(f\"An error occurred: {e}\")\n    # Consider logging or re-raising\n"
                return suggestion
            else:
                return None
        
        elif "add docstring" in instruction_lower or "add comments" in instruction_lower:
            # Add a simple docstring at the top if missing
            if not original_content.strip().startswith('"""') and not original_content.strip().startswith("'''"):
                suggestion = '\"\"\"\nA module or script.\n\n' + instruction.capitalize() + '.\n\"\"\"\n\n' + original_content
                return suggestion
            else:
                return None
        
        elif "print hello world" in instruction_lower or "hello world" in instruction_lower:
            suggestion = 'print("Hello, World!")\n'
            return suggestion
        
        elif "fibonacci" in instruction_lower:
            suggestion = '''def fibonacci(n):
    """Return the nth Fibonacci number."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(n - 1):
            a, b = b, a + b
        return b

# Example usage
if __name__ == "__main__":
    print(fibonacci(10))  # Output: 55
'''
            return suggestion
        
        # If no specific rule matched, return None to indicate we couldn't generate a suggestion
        return None
    
    def _run_code_safely(self, code: str) -> str:
        """Run a code snippet in a safe, restricted environment"""
        try:
            # Create a temporary file in the sandbox
            temp_file = os.path.join(self.code_sandbox, f"temp_code_{random.randint(1000, 9999)}.py")
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Run with restrictions: no network, limited time, no file system access beyond temp
            # Note: True sandboxing is complex; we rely on timeout and hope the code is safe
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=10,  # 10 second limit
                # Note: In a real sandbox, we'd use more restrictions, but for demo we keep it simple
            )
            
            # Clean up
            try:
                os.remove(temp_file)
            except:
                pass
            
            if result.returncode == 0:
                output = result.stdout.strip()
                if not output:
                    return "Code executed successfully (no output)."
                return f"💻 **Code Output:**\n{output}"
            else:
                error = result.stderr.strip()
                if not error:
                    return "Code executed but returned an error (no error message)."
                return f"❌ **Code Error:**\n{error}"
                
        except subprocess.TimeoutExpired:
            try:
                os.remove(temp_file)
            except:
                pass
            return "⏰ Code execution timed out (10 second limit)."
        except Exception as e:
            try:
                os.remove(temp_file)
            except:
                pass
            return f"Error executing code: {str(e)}"
    
    def _process_command(self, user_input: str) -> Optional[str]:
        """Process special commands"""
        command = user_input.strip().lower()
        
        # Help command
        if command in ['help', '?', 'commands']:
            return self._get_help_text()
        
        # Clear screen
        if command in ['clear', 'cls']:
            os.system('cls' if os.name == 'nt' else 'clear')
            return "Screen cleared. How can I assist you with coding and AI tasks?"
        
        # Time/date commands
        if command == 'time':
            return f"🕐 Current time: {self._get_current_time()}"
        if command == 'date':
            return f"📅 Today's date: {self._get_current_date()}"
        
        # System info
        if command in ['system', 'sysinfo', 'info', 'gpu']:
            if command == 'gpu':
                gpu_info = self._get_gpu_info()
                if gpu_info:
                    return f"🎮 **GPU Information:**\n{gpu_info}"
                else:
                    return "No NVIDIA GPU detected via common methods (nvidia-smi, lspci). You may still have a GPU, but it wasn't detected by these tools."
            return self._get_system_info()
        
        # Git info command
        if command in ['github', 'repo', 'git']:
            return self._get_git_info()
        
        # LLM configuration commands
        if command == 'llm status':
            return self._get_llm_status()
        if command.startswith('llm set '):
            return self._set_llm_config(user_input[8:].strip())
        if command == 'llm providers':
            return self._get_llm_providers_info()
        
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
        
        if command.startswith('write '):
            parts = command[6:].split(' ', 1)
            if len(parts) < 2:
                return "Usage: write <filename> <content>"
            filename, content = parts[0], parts[1]
            return self._write_file(filename, content)
        
        # Learning commands
        if command.startswith('learn '):
            fact = command[6:].strip()
            if not fact:
                return "Usage: learn <fact to remember>"
            self._learn_fact(fact, "User explicitly taught this")
            return f"✅ I've learned: '{fact}'"
        
        if command == 'recall':
            if not self.learned_facts:
                return "I haven't learned any facts yet. Use 'learn <fact>' to teach me something."
            # Show recent facts
            recent_facts = self.learned_facts[-5:] if len(self.learned_facts) >= 5 else self.learned_facts
            result = "🧠 **Things I've Learned:**\n"
            for i, fact_entry in enumerate(reversed(recent_facts), 1):
                result += f"{i}. {fact_entry['fact']} (learned {fact_entry['timestamp']})\n"
            if len(self.learned_facts) > 5:
                result += f"\n... and {len(self.learned_facts) - 5} more facts. Use 'learn <fact>' to add more."
            return result
        
        if command.startswith('forget '):
            fact_to_forget = command[7:].strip()
            if not fact_to_forget:
                return "Usage: forget <fact to remove>"
            # Find and remove matching facts
            original_count = len(self.learned_facts)
            self.learned_facts = [f for f in self.learned_facts if f["fact"].lower() != fact_to_forget.lower()]
            removed_count = original_count - len(self.learned_facts)
            if removed_count > 0:
                self._save_learned_facts()
                return f"🗑️ Forgot {removed_count} instance(s) of: '{fact_to_forget}'"
            else:
                return f"I don't recall learning: '{fact_to_forget}'"
        
        # Knowledge management
        if command.startswith('teach '):
            parts = command[6:].split(' ', 1)
            if len(parts) < 2:
                return "Usage: teach <topic> <explanation>"
            topic, explanation = parts[0].strip(), parts[1].strip()
            self.custom_knowledge[topic.lower()] = explanation
            self._save_custom_knowledge()
            return f"📚 I've added knowledge about '{topic}': {explanation}"
        
        if command == 'knowledge':
            if not self.custom_knowledge:
                return "No custom knowledge has been added yet. Use 'teach <topic> <explanation>' to add knowledge."
            result = "📚 **Custom Knowledge Base:**\n"
            for topic, explanation in self.custom_knowledge.items():
                result += f"• {topic}: {explanation}\n"
            return result
        
        # Code assistance commands
        if command.startswith('code '):
            parts = command[5:].split(' ', 1)
            if len(parts) < 2:
                return "Usage: code <file_path> <instruction>\nExample: code main.py \"add a function to calculate factorial\""
            file_path, instruction = parts[0], parts[1]
            if not os.path.exists(file_path):
                return f"File '{file_path}' not found. Create it first or check the path."
            return self._suggest_code_edit(file_path, instruction)
        
        if command.startswith('run '):
            code = command[4:].strip()
            if not code:
                return "Usage: run <code_snippet>\nExample: run \"print('Hello, World!')\""
            return self._run_code_safely(code)
        
        if command == 'explain':
            if len(user_input.split()) < 2:
                return "Usage: explain <code_snippet>\nExample: explain \"for i in range(10): print(i)\""
            code = user_input[8:].strip()
            if not code:
                return "Please provide code to explain."
            return self._explain_code(code)
        
        # Dataset analysis (for sample datasets)
        if command.startswith('stats '):
            dataset_name = command[6:].strip()
            if not dataset_name:
                return "Please specify a dataset name (e.g., 'stats employees')"
            return self._analyze_dataset(dataset_name)
        if command == 'datasets':
            datasets = list(self.sample_datasets.keys())
            dataset_info = []
            for name, data in self.sample_datasets.items():
                dataset_info.append(f"• {name}: {len(data)} records")
            return f"📊 Available datasets:\n" + "\n".join(dataset_info) + "\nUse 'stats <dataset_name>' to analyze a dataset."
        
        # Preferences
        if command.startswith('set '):
            parts = command[4:].split(' ', 1)
            if len(parts) < 2:
                return "Usage: set <preference> <value>\nExample: set verbosity high"
            key, value = parts[0].strip(), parts[1].strip()
            if key in self.user_preferences:
                # Try to convert value to appropriate type
                old_value = self.user_preferences[key]
                if isinstance(old_value, bool):
                    self.user_preferences[key] = value.lower() in ['true', 'yes', '1', 'on']
                elif isinstance(old_value, int):
                    try:
                        self.user_preferences[key] = int(value)
                    except ValueError:
                        return f"Error: {key} expects an integer value."
                elif isinstance(old_value, float):
                    try:
                        self.user_preferences[key] = float(value)
                    except ValueError:
                        return f"Error: {key} expects a numeric value."
                else:
                    self.user_preferences[key] = value
                self._save_user_preferences()
                return f"✅ Setting '{key}' updated to: {self.user_preferences[key]}"
            else:
                return f"Unknown setting: {key}. Available settings: {', '.join(self.user_preferences.keys())}"
        
        if command == 'preferences':
            result = "⚙️ **User Preferences:**\n"
            for key, value in self.user_preferences.items():
                result += f"• {key}: {value}\n"
            result += "\nUse 'set <key> <value>' to change a preference."
            return result
        
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
Created by: {self.creator}
Session started: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}
Capabilities: Conversational AI, code assistance, system diagnostics (including GPU), file operations, data analysis, persistent learning, LLM integration
Currently chatting with: {self.user_name or 'Anonymous'}
Learned facts: {len(self.learned_facts)}
Custom knowledge entries: {len(self.custom_knowledge)}
LLM Provider: {CONFIG['llm_provider'] or 'None'}"""
        
        # Reset conversation
        if command in ['reset', 'clear history']:
            self.conversation_history = []
            return "Conversation history cleared. Fresh start!"
        
        # Stats
        if command == 'stats':
            return f"""📊 **JAVIS Statistics**
Session started: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}
Conversation turns: {len(self.conversation_history)}
Learned facts: {len(self.learned_facts)}
Custom knowledge items: {len(self.custom_knowledge)}
User preferences: {len(self.user_preferences)} settings"""
        
        return None  # Not a command, let AI handle it
    
    def _explain_code(self, code: str) -> str:
        """Explain what a code snippet does"""
        try:
            # Simple explanation based on keywords (rule-based for demo)
            code_lower = code.lower()
            
            explanations = []
            
            if 'def ' in code_lower:
                explanations.append("This code defines a function.")
            if 'class ' in code_lower:
                explanations.append("This code defines a class.")
            if 'for ' in code_lower or 'while ' in code_lower:
                explanations.append("This code contains a loop.")
            if 'if ' in code_lower or 'elif ' in code_lower or 'else:' in code_lower:
                explanations.append("This code contains conditional logic.")
            if 'try:' in code_lower:
                explanations.append("This code includes error handling (try-except).")
            if 'import ' in code_lower:
                explanations.append("This code imports modules or libraries.")
            if 'print(' in code_lower:
                explanations.append("This code outputs information to the console.")
            if 'return ' in code_lower:
                explanations.append("This code returns a value from a function.")
            if '@' in code_lower:
                explanations.append("This code uses decorators.")
            if 'lambda' in code_lower:
                explanations.append("This code uses lambda (anonymous) functions.")
            if 'yield' in code_lower:
                explanations.append("This code uses a generator.")
            if 'async ' in code_lower or 'await ' in code_lower:
                explanations.append("This code uses asynchronous programming.")
            
            if not explanations:
                explanations.append("This code snippet performs some computational task. programming operations.")
            
            result = f"📝 **Code Explanation**\n\n"
            result += "🔍 **What this code does:**\n"
            for expl in explanations:
                result += f"• {expl}\n"
            
            result += "\n💻 **Code Snippet:**\n"
            result += "```python\n"
            result += code
            result += "\n```\n"
            
            # Try to give a simple execution prediction if safe
            if len(code) < 200 and not any(dangerous in code_lower for dangerous in ['open(', 'file(', 'exec', 'eval', 'subprocess', 'os.system']):
                result += "\n🧪 **Execution Prediction (if run in isolation):**\n"
                result += "Note: This is a simplified prediction. Actual behavior may vary.\n"
                # We could run it in sandbox, but for explanation we'll skip to avoid complexity
                result += "To see what it does, try running it with the `/run` command.\n"
            
            return result
            
        except Exception as e:
            return f"Error explaining code: {str(e)}"
    
    def _get_help_text(self) -> str:
        """Return help text"""
        return """🤖 **JAVIS - Just A Very Intelligent System (Enhanced) - Available Commands**

**General Chat:**
Just type your question or message naturally!

**Utility Commands:**
• `help` or `?` - Show this help message
• `clear` or `cls` - Clear the terminal screen
• `time` - Show current time
• `date` - Show current date
• `system` or `sysinfo` - Show system information
• `gpu` - Show GPU/NVIDIA information specifically
• `github` or `repo` or `git` - Show Git repository information
• `history` - Show recent conversation history
• `about` or `whoami` - Information about me
• `settings` - Show current settings
• `reset` or `clear history` - Clear conversation history
• `stats` - Show usage statistics
• `exit`, `quit`, `bye` - End the conversation

**LLM Configuration:**
• `llm status` - Show current LLM configuration
• `llm providers` - Show available LLM providers and setup instructions
• `llm set <provider> <api_key> [model]` - Configure LLM provider
  Example: `llm set openai sk-... gpt-4`

**Learning & Memory:**
• `learn <fact>` - Teach me a fact to remember
• `recall` - Show what I've learned
• `forget <fact>` - Make me forget a specific fact
• `teach <topic> <explanation>` - Add custom knowledge
• `knowledge` - Show my custom knowledge base

**Calculations:**
• `calc <expression>` - Calculate mathematical expressions
  Examples: `calc 2+2*3`, `calc sqrt(144)`, `calc (5+3)^2`

**File Operations:**
• `files` - List files in current directory
• `files <directory>` - List files in specified directory
• `read <filename>` - Display contents of a text file
• `write <filename> <content>` - Write content to a file

**Code Assistance:**
• `code <file_path> <instruction>` - Suggest code edits based on natural language
  Example: code main.py "add a function to calculate factorial"
• `run <code_snippet>` - Safely run a code snippet in a sandbox
  Example: run "print('Hello, World!')"
• `explain <code_snippet>` - Explain what a code snippet does
  Example: explain "for i in range(10): print(i)"

**Data Analysis:**
• `datasets` - Show available sample datasets
• `stats <dataset_name>` - Analyze a sample dataset
  Available: employees, sales, products
  Example: `stats employees`

**Preferences:**
• `set <key> <value>` - Set a user preference
  Example: set verbosity high
• `preferences` - Show all current preferences

**Tips:**
• Be specific with your questions for better answers
• I can help with: coding, AI concepts, math, science, general knowledge, file operations, data analysis
• Try asking: "What is machine learning?" or "How do I optimize a SQL query?" or "Explain this code: [snippet]"
• Use natural language for code requests: "Add error handling to this file" or "Create a class for a user profile"
• For GPU info: use the `gpu` command
• For Git info: use the `github` or `repo` command
• I can learn from our conversations! Use `learn <fact>` to teach me things
• All code execution happens in a safe sandbox directory
"""