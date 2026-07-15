#!/usr/bin/env python3
"""
Simple AI Assistant Prototype - Demonstrates basic AI-like capabilities
Similar to how Hermes Agent processes and responds to user input
"""

import re
import random
import datetime
import json
import os

class SimpleAIAssistant:
    def __init__(self):
        self.name = "Hermes Lite"
        self.version = "0.1.0"
        self.conversation_history = []
        
        # Knowledge base for simple responses
        self.knowledge_base = {
            "greetings": [
                "Hello! I'm Hermes Lite, your AI assistant. How can I help you today?",
                "Hi there! Ready to assist you with any questions.",
                "Greetings! I'm here to help. What's on your mind?"
            ],
            "farewells": [
                "Goodbye! Have a wonderful day!",
                "See you later! Feel free to return if you need more assistance.",
                "Farewell! Remember, I'm here whenever you need help."
            ],
            "thanks": [
                "You're welcome! Happy to help.",
                "My pleasure! Let me know if you need anything else.",
                "You're welcome! That's what I'm here for."
            ],
            "weather": [
                "I don't have access to real-time weather data, but I hope it's nice where you are!",
                "Weather checking isn't in my current capabilities, but I hope you're having pleasant weather!",
                "I wish I could check the weather for you, but that feature isn't implemented yet."
            ],
            "time": [
                f"The current time is {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.",
                f"Right now it's {datetime.datetime.now().strftime('%I:%M %p')} on {datetime.datetime.now().strftime('%B %d, %Y')}.",
                f"Current time: {datetime.datetime.now().strftime('%H:%M')} on {datetime.datetime.now().strftime('%A, %B %d, %Y')}."
            ],
            "help": [
                "I can help with basic conversations, tell you the time, and respond to greetings.",
                "My capabilities include: greeting responses, time telling, and simple conversations.",
                "Try asking me about the time, saying hello, or just chatting!"
            ],
            "default": [
                "That's interesting! Tell me more about that.",
                "I see. How does that make you feel?",
                "Fascinating point. What else would you like to discuss?",
                "I'm still learning about that topic. Could you elaborate?",
                "Interesting perspective! How did you come to that conclusion?",
                "I appreciate your insight on that. What are your thoughts on related topics?"
            ]
        }
        
        # Pattern matching for intents
        self.patterns = {
            r'\b(hello|hi|hey|greetings)\b': 'greetings',
            r'\b(bye|goodbye|see you|farewell)\b': 'farewells',
            r'\b(thank you|thanks|thx)\b': 'thanks',
            r'\b(time|clock|what time)\b': 'time',
            r'\b(weather|rain|sun|temperature)\b': 'weather',
            r'\b(help|what can you do|capabilities)\b': 'help',
            r'\b(how are you|how do you do)\b': 'greetings'  # Treat as greeting
        }
    
    def preprocess_input(self, user_input):
        """Clean and normalize user input"""
        return user_input.lower().strip()
    
    def detect_intent(self, user_input):
        """Detect the intent of user input using pattern matching"""
        processed_input = self.preprocess_input(user_input)
        
        for pattern, intent in self.patterns.items():
            if re.search(pattern, processed_input):
                return intent
        
        return 'default'
    
    def get_response(self, intent):
        """Get a random response for the detected intent"""
        responses = self.knowledge_base.get(intent, self.knowledge_base['default'])
        return random.choice(responses)
    
    def add_to_history(self, user_input, bot_response):
        """Add exchange to conversation history"""
        self.conversation_history.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'user': user_input,
            'bot': bot_response
        })
    
    def chat(self):
        """Main chat loop"""
        print(f"🤖 {self.name} v{self.version}")
        print("Type 'quit', 'exit', or 'bye' to end the conversation.")
        print("-" * 50)
        
        # Initial greeting
        print(f"{self.name}: {self.get_response('greetings')}")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print(f"\n{self.name}: {self.get_response('farewells')}")
                    break
                
                # Skip empty input
                if not user_input:
                    print(f"EOF")
                    print(f"\n{self.name}: {self.get_response('farewells')}")
                    break
                
                # Detect intent and get response
                intent = self.detect_intent(user_input)
                response = self.get_response(intent)
                
                # Add to history
                self.add_to_history(user_input, response)
                
                # Print response
                print(f"\n{self.name}: {response}")
                
            except KeyboardInterrupt:
                print(f"\n\n{self.name}: {self.get_response('farewells')}")
                break
            except Exception as e:
                print(f"\n{self.name}: Sorry, I encountered an error: {str(e)}")
                print("Let's continue our conversation...")
        
        # Show conversation summary if there was interaction
        if self.conversation_history:
            print(f"\n📊 Conversation Summary: {len(self.conversation_history)} exchanges")
            save_choice = input("Would you like to save this conversation? (y/n): ").lower().strip()
            if save_choice in ['y', 'yes']:
                self.save_conversation()
    
    def save_conversation(self):
        """Save conversation history to a file"""
        if not self.conversation_history:
            print("No conversation to save.")
            return
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'assistant': self.name,
                    'version': self.version,
                    'timestamp': datetime.datetime.now().isoformat(),
                    'conversation': self.conversation_history
                }, f, indent=2)
            print(f"💾 Conversation saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving conversation: {str(e)}")

def main():
    """Entry point for the application"""
    assistant = SimpleAIAssistant()
    assistant.chat()

if __name__ == "__main__":
    main()