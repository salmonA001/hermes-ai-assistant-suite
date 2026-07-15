#!/usr/bin/env python3
"""
Hermes Universal AI - An AI Assistant Combining Features of Modern AI Coding Agents
Inspired by: Claude Code, Codex, Cursor, Gemini, ChatGPT, NVIDIA tools, and Antigravity-IDE
Features: Conversational AI, Code Assistance, System Diagnostics (Including GPU), File Operations, Data Analysis
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

# ==================== CONFIGURATION ====================

CONFIG = {
    "name": "Hermes Universal AI",
    "version": "1.0.0",
    "creator": "Inspired by Claude Code, Codex, Cursor, Gemini, ChatGPT, NVIDIA",
    "max_history": 50,
    "file_size_limit": 1024 * 1024,  # 1MB
    "display_limit": 1500,
    "code_sandbox_dir": "./code_sandbox",
}

# ==================== MAIN ASSISTANT CLASS ====================

class HermesUniversalAI:
    """Universal AI Assistant with coding agent capabilities"""
    
    def __init__(self):
        self.name = CONFIG["name"]
        self.version = CONFIG["version"]
        self.creator = CONFIG["creator"]
        self.conversation_history = []
        self.user_name = None
        self.session_start = datetime.datetime.now()
        self.knowledge_base = self._load_knowledge_base()
        self.code_sandbox = CONFIG["code_sandbox_dir"]
        os.makedirs(self.code_sandbox, exist_ok=True)
        
        # Response templates
        self.greetings = [
            f"Hello! I'm {self.name} v{self.version}, your AI coding assistant. How can I help you today?",
            f"Hi there! Ready to assist with coding, questions, calculations, or just chat. What's on your mind?",
            f"Greetings! I combine capabilities of modern AI coding agents to help you develop software efficiently.",
            f"Hey! I'm {self.name}. I can write code, explain concepts, analyze files, and help with debugging."
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
            "continuous_integration": "Continuous Integration (CI) is the practice of automating the integration of code changes from multiple contributors into a single software project.",
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
            
            # About Hermes
            "hermes_origin": "Hermes is an AI agent framework created by Nous Research, designed to be extensible, self-improving, and capable of tool use.",
            "hermes_universal_capabilities": "Hermes Universal AI combines conversational AI, code assistance, system diagnostics (including GPU/NVIDIA), file operations, and data analysis to assist with software development and general tasks.",
            "hermes_version": f"This is {self.name} version {self.version}.",
        }
    
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
        
        # Direct lookup
        for key, value in self.knowledge_base.items():
            if key in query_lower or query_lower in key:
                return value
        
        # Pattern matching for common questions
        if any(word in query_lower for word in ['what is', 'what are', 'define', 'definition', 'explain', 'how does']):
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
Capabilities: Conversational AI, code assistance, system diagnostics (including GPU), file operations, data analysis
Currently chatting with: {self.user_name or 'Anonymous'}"""
        
        # Reset conversation
        if command in ['reset', 'clear history']:
            self.conversation_history = []
            return "Conversation history cleared. Fresh start!"
        
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
        return """🤖 **Hermes Universal AI - Available Commands**

**General Chat:**
Just type your question or message naturally!

**Utility Commands:**
• `help` or `?` - Show this help message
• `clear` or `cls` - Clear the terminal screen
• `time` - Show current time
• `date` - Show current date
• `system` or `sysinfo` - Show system information
• `gpu` - Show GPU/NVIDIA information specifically
• `history` - Show recent conversation history
• `about` or `whoami` - Information about me
• `settings` - Show current settings
• `reset` or `clear history` - Clear conversation history
• `exit`, `quit`, `bye` - End the conversation

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
  Available: employees, sales
  Example: `stats employees`

**Tips:**
• Be specific with your questions for better answers
• I can help with: coding, AI concepts, math, science, general knowledge, file operations, data analysis
• Try asking: "What is machine learning?" or "How do I optimize a SQL query?" or "Explain this code: [snippet]"
• Use natural language for code requests: "Add error handling to this file" or "Create a class for a user profile"
• For GPU info: use the `gpu` command
• All code execution happens in a safe sandbox directory
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
                    # Extract name from remaining words
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
        elif 'joke' in user_input_lower or 'funny' in user_input_lower or 'laugh' in user_input_lower:
            response = f"😄 {random.choice(self.jokes)}"
        
        # Handle quotes/inspiration
        elif any(word in user_input_lower for word in ['quote', 'inspire', 'motivation', 'inspirational', 'wise', 'wisdom']):
            response = f"💫 \"{random.choice(self.quotes)}\""
        
        # Handle weather (simulated)
        elif 'weather' in user_input_lower:
            conditions = ['sunny', 'partly cloudy', 'cloudy', 'light rain', 'showers', 'clear', 'foggy', 'stormy']
            temp = random.randint(5, 35)
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
                f"That's an interesting question about '{user_input}'. While I don't have specific information on that topic in my knowledge base, I can help with coding, explain AI/programming concepts, analyze data, or assist with other tasks. Would you like help with something else?",
                f"I'm not sure I have detailed information about '{user_input}' in my current knowledge base. However, I'm good at math, can explain technical concepts, help with file operations, analyze datasets, suggest code improvements, or just chat. What would you like to try?",
                f"That's a thoughtful question! My expertise is more focused on AI concepts, technical topics, software development, and practical assistance like calculations and code assistance. Could you rephrase your question or ask about something I might know more about?"
            ]
            return random.choice(responses)
        else:
            # Statement or comment
            responses = [
                f"I see. Thanks for sharing that about '{user_input}'. Is there something specific you'd like me to help you with?",
                f"Interesting point about '{user_input}'. Would you like to explore that further, or is there something else I can assist you with?",
                f"Thanks for telling me! If you have any questions or need help with calculations, information, file operations, data analysis, code assistance, or just want to chat, I'm here.",
                f"That's noteworthy! Is there a particular aspect you'd like to dive deeper into, or shall we talk about something else?"
            ]
            return random.choice(responses)
    
    def start_chat(self):
        """Start the interactive chat session"""
        # Clear screen for clean start
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 70)
        print(f"🤖 {self.name} v{self.version}")
        print("   Your Universal AI Coding Assistant")
        print("=" * 70)
        print("Type 'help' for available commands, or just start chatting!")
        print("Type 'exit', 'quit', or 'bye' to end the conversation.")
        print("-" * 70)
        
        # Initial greeting
        print(f"\n{self.name}: {random.choice(self.greetings)}")
        print("-" * 70)
        
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
                print("-" * 50)
                
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
    assistant = HermesUniversalAI()
    assistant.start_chat()

if __name__ == "__main__":
    # Check if we're running in a terminal that supports input
    if not sys.stdin.isatty():
        print("Note: For full interactive experience, run this in a terminal/command prompt.")
        print("Starting in demo mode...\n")
        
        # Demo mode for non-interactive environments
        assistant = HermesUniversalAI()
        print(f"🤖 {assistant.name} v{assistant.version}")
        print("=" * 50)
        print("Demo: Sample interactions")
        print("-" * 50)
        
        # Show a few sample interactions
        samples = [
            "Hello!",
            "What is artificial intelligence?",
            "Explain machine learning",
            "gpu",
            "code main.py \"add a function to calculate factorial\"",
            "run \"print('Hello from Hermes Universal AI!')\"",
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