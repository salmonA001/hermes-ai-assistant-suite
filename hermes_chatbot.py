#!/usr/bin/env python3
"""
Hermes ChatBot - Simple Interactive AI Assistant for Terminal
"""

import os
import sys
import json
import math
import random
import datetime
import re

class HermesChatBot:
    def __init__(self):
        self.name = "Hermes AI"
        self.version = "2.0.0"
        self.conversation_history = []
        self.user_name = None
        self.session_start = datetime.datetime.now()
        
        # Initialize knowledge base
        self.knowledge_base = {
            "ai_definition": "Artificial Intelligence (AI) is the simulation of human intelligence in machines that are programmed to think like humans and mimic their actions.",
            "machine_learning": "Machine Learning is a subset of AI that provides systems the ability to automatically learn and improve from experience without being explicitly programmed.",
            "deep_learning": "Deep Learning is a subset of machine learning that uses neural networks with many layers to analyze various factors of data.",
            "nlp": "Natural Language Processing (NLP) is a branch of AI that helps computers understand, interpret and manipulate human language.",
            "python": "Python is a high-level, interpreted programming language known for its simplicity and readability.",
            "git": "Git is a distributed version control system for tracking changes in source code during software development.",
            "algorithm": "An algorithm is a finite sequence of well-defined instructions to solve a class of problems.",
            "statistics": "Statistics is the science of collecting, analyzing, presenting, and interpreting data.",
        }
        
        # Response templates
        self.greetings = [
            "Hello! I'm Hermes AI, your intelligent assistant. How can I help you today?",
            "Hi there! Ready to assist you with questions or just chat. What's on your mind?",
            "Greetings! I'm here to help with information or friendly conversation."
        ]
        
        self.farewells = [
            "Goodbye! Have a",
            "See you later! Remember I'm here whenever you need assistance.",
            "Farewell! Thanks for the conversation. Come back anytime!",
            "Bye for now! I'll be here when you need me again."
        ]
        
        self.jokes = [
            "Why don't scientists trust atoms anymore? Because they make up everything!",
            "I told my computer I needed a break, and it said 'No problem - I'll go to sleep mode'.",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "There are 10 types of people in the world: those who understand binary, and those who don't.",
            "Why was the math book sad? Because it had too many problems."
        ]
        
        self.quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Innovation distinguishes between a leader and a follower. - Steve Jobs",
            "Life is what happens when you're busy making other plans. - John Lennon",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "In the middle of difficulty lies opportunity. - Albert Einstein"
        ]
        
        # Sample datasets
        self.sample_datasets = {
            "employees": [
                {"id": 1, "name": "Alice Smith", "age": 29, "department": "Engineering", "salary": 75000},
                {"id": 2, "name": "Bob Johnson", "age": 35, "department": "Marketing", "salary": 65000},
                {"id": 3, "name": "Carol Davis", "age": 42, "department": "Sales", "salary": 80000},
                {"id": 4, "name": "David Wilson", "age": 31, "department": "Engineering", "salary": 72000},
                {"id": 5, "name": "Eva Brown", "age": 28, "department": "HR", "salary": 58000}
            ]
        }
    
    def _get_current_time(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _calculate_expression(self, expr):
        try:
            # Safe evaluation - only allow basic math
            allowed = set('0123456789+-*/().%^ ')
            cleaned = ''.join(c for c in expr if c in allowed)
            cleaned = cleaned.replace('^', '**')
            result = eval(cleaned, {"__builtins__": {}}, {"abs": abs, "round": round})
            if isinstance(result, float):
                if result.is_integer():
                    return str(int(result))
                else:
                    return f"{result:.4f}".rstrip('0').rstrip('.')
            else:
                return str(result)
        except:
            return f"Could not calculate '{expr}'"
    
    def _get_knowledge(self, query):
        query_lower = query.lower()
        for key, value in self.knowledge_base.items():
            if key in query_lower:
                return value
        return None
    
    def _analyze_dataset(self, name):
        if name not in self.sample_datasets:
            return f"Dataset '{name}' not found. Available: {', '.join(self.sample_datasets.keys())}"
        
        data = self.sample_datasets[name]
        if not data:
            return f"Dataset '{name}' is empty."
        
        result = f"📊 Dataset: {name}\nRecords: {len(data)}\n"
        if data:
            fields = list(data[0].keys())
            result += f"Fields: {', '.join(fields)}\n\n"
            
            # Numeric analysis
            numeric_fields = {}
            for record in data:
                for k, v in record.items():
                    if isinstance(v, (int, float)) and not isinstance(v, bool):
                        if k not in numeric_fields:
                            numeric_fields[k] = []
                        numeric_fields[k].append(v)
            
            if numeric_fields:
                result += "📈 Numeric Summary:\n"
                for field, values in numeric_fields.items():
                    if len(values) >= 2:
                        mean_val = sum(values)/len(values)
                        min_val = min(values)
                        max_val = max(values)
                        result += f"  {field}: Mean={mean_val:.2f}, Range=[{min_val}-{max_val}]\n"
        return result
    
    def _list_files(self, directory="."):
        try:
            items = os.listdir(directory)
            files = [f for f in items if os.path.isfile(os.path.join(directory, f))]
            dirs = [d for d in items if os.path.isdir(os.path.join(directory, d))]
            
            result = f"📁 Contents of '{directory}':\n"
            if dirs:
                result += "📂 Directories:\n"
                for d in sorted(dirs):
                    result += f"  • {d}/\n"
            if files:
                result += "📄 Files:\n"
                for f in sorted(files):
                    try:
                        size = os.path.getsize(os.path.join(directory, f))
                        if size < 1024:
                            size_str = f"{size} B"
                        elif size < 1024*1024:
                            size_str = f"{size/1024:.1f} KB"
                        else:
                            size_str = f"{size/(1024*1024):.1f} MB"
                        result += f"  • {f} ({size_str})\n"
                    except:
                        result += f"  • {f}\n"
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _read_file(self, filename):
        try:
            if not os.path.exists(filename):
                return f"File '{filename}' not found."
            
            if os.path.getsize(filename) > 1024*1024:  # 1MB limit
                return f"File '{filename}' is too large to display."
            
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if len(content) > 1500:
                content = content[:1500] + "\n\n... (truncated)"
            
            return f"📄 Contents of '{filename}':\n{'-'*40}\n{content}\n{'-'*40}"
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def process_input(self, user_input):
        original = user_input
        user_input = user_input.strip().lower()
        
        # Handle special commands
        if user_input in ['help', '?']:
            return self._get_help()
        elif user_input in ['clear', 'cls']:
            os.system('cls' if os.name == 'nt' else 'clear')
            return "Screen cleared."
        elif user_input == 'time':
            return f"🕐 Current time: {self._get_current_time()}"
        elif user_input == 'date':
            return f"📅 Today's date: {datetime.datetime.now().strftime('%Y-%m-%d')}"
        elif user_input.startswith('calc '):
            expr = user_input[5:].strip()
            if not expr:
                return "Usage: calc <expression>"
            result = self._calculate_expression(expr)
            return f"🧮 {expr} = {result}"
        elif user_input == 'files':
            return self._list_files()
        elif user_input.startswith('files '):
            directory = user_input[6:].strip()
            return self._list_files(directory)
        elif user_input.startswith('read '):
            filename = user_input[5:].strip()
            if not filename:
                return "Usage: read <filename>"
            return self._read_file(filename)
        elif user_input.startswith('stats '):
            dataset = user_input[6:].strip()
            if not dataset:
                return "Usage: stats <dataset_name>"
            return self._analyze_dataset(dataset)
        elif user_input == 'datasets':
            return f"📊 Available datasets: {', '.join(self.sample_datasets.keys())}"
        elif user_input == 'history':
            if not self.conversation_history:
                return "No conversation history."
            hist = "📜 Recent conversation:\n"
            for i, (u, b) in enumerate(self.conversation_history[-3:], 1):
                hist += f"{i}. You: {u[:40]}{'...' if len(u) > 40 else ''}\n"
                hist += f"   Me: {b[:40]}{'...' if len(b) > 40 else ''}\n\n"
            return hist
        elif user_input in ['about', 'whoami']:
            return f"""🤖 {self.name} v{self.version}
Session: {self.session_start.strftime('%Y-%m-%d %H:%M')}
Chatting with: {self.user_name or 'Anonymous'}"""
        elif user_input in ['reset', 'clear history']:
            self.conversation_history = []
            return "Conversation history cleared."
        
        # Handle greetings
        if any(g in user_input for g in ['hello', 'hi', 'hey']):
            response = random.choice(self.greetings)
            if self.user_name:
                response = f"Hello {self.user_name}! " + response[len("Hello!"):]
        
        # Handle farewells
        elif any(f in user_input for f in ['bye', 'goodbye', 'see you']):
            response = random.choice(self.farewells)
        
        # Handle name setting
        elif 'my name is' in user_input or 'i am' in user_input:
            # Extract name
            parts = user_input.split()
            for i, word in enumerate(parts):
                if word in ['is', 'am'] and i+1 < len(parts):
                    name_parts = parts[i+1:]
                    name = ' '.join(name_parts).strip('.,!?')
                    if name and len(name) < 20:
                        self.user_name = name
                        response = f"Nice to meet you, {self.user_name}! How can I help you?"
                        break
            else:
                response = "Hello! I'm here to help. What's your name?"
        
        # Handle thanks
        elif any(t in user_input for t in ['thank', 'thanks']):
            response = random.choice([
                "You're welcome!",
                "Happy to help!",
                "Anytime!",
                "My pleasure!"
            ])
        
        # Handle jokes
        elif 'joke' in user_input or 'funny' in user_input:
            response = f"😄 {random.choice(self.jokes)}"
        
        # Handle quotes
        elif any(q in user_input for q in ['quote', 'inspire']):
            response = f"💫 \"{random.choice(self.quotes)}\""
        
        # Handle weather (simulated)
        elif 'weather' in user_input:
            conditions = ['sunny', 'cloudy', 'rainy', 'partly cloudy']
            temp = random.randint(10, 30)
            condition = random.choice(conditions)
            response = f"🌤️ Simulated: {condition}, {temp}°C"
        
        # Handle knowledge questions
        else:
            knowledge = self._get_knowledge(user_input)
            if knowledge:
                response = f"📚 {knowledge}"
            else:
                # General response
                if any(w in user_input for w in ['what', 'how', 'why']):
                    response = f"That's interesting! I can help with AI concepts, calculations, or just chat. Try asking about machine learning or Python."
                else:
                    response = f"I see. Is there something specific you'd like help with?"
        
        # Store in history
        self.conversation_history.append((original, response))
        return response
    
    def _get_help(self):
        return """🤖 Hermes AI - Help

General Chat: Just type your message!

Commands:
• help, ? - Show this help
• clear, cls - Clear screen
• time - Current time
• date - Today's date
• calc <expr> - Calculate (e.g., calc 2+2*3)
• files - List files
• files <dir> - List files in directory
• read <file> - Show file contents
• stats <dataset> - Analyze dataset
• datasets - List datasets
• history - Show conversation
• about, whoami - About me
• reset - Clear history
• exit, quit, bye - End chat

Examples:
• What is AI?
• Calculate 15% of 200
• Tell me a joke
• Read poem.txt
• Stats employees"""
    
    def start(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 50)
        print(f"🤖 {self.name} v{self.version}")
        print("   Your AI Assistant")
        print("=" * 50)
        print("Type 'help' for commands, or just start chatting!")
        print("Type 'exit' to end the conversation.")
        print("-" * 50)
        print(f"\n{self.name}: {random.choice(self.greetings)}")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\n> ").strip()
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    farewell = random.choice(self.farewells)
                    if self.user_name:
                        farewell = f"Goodbye {self.user_name}! {farewell[len('Goodbye!'):]}"
                    print(f"\n{self.name}: {farewell}")
                    break
                
                response = self.process_input(user_input)
                print(f"\n{self.name}: {response}")
                print("-" * 30)
                
            except KeyboardInterrupt:
                print(f"\n\n{self.name}: Goodbye!")
                break
            except Exception as e:
                print(f"\n{self.name}: Error: {str(e)}")

def main():
    if not sys.stdin.isatty():
        print("Error: Run this in an interactive terminal.")
        return
    chatbot = HermesChatBot()
    chatbot.start()

if __name__ == "__main__":
    main()