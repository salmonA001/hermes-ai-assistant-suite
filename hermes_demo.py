#!/usr/bin/env python3
"""
Hermes Lite - A simple AI assistant demonstration
This version demonstrates capabilities without requiring interactive input
"""

import datetime
import json
import os
import random
from pathlib import Path

class HermesLite:
    def __init__(self):
        self.name = "Hermes Lite"
        self.version = "0.1.0"
        self.conversation_history = []
        self.knowledge_base = {
            "ai": "Artificial Intelligence is the simulation of human intelligence processes by machines, especially computer systems.",
            "python": "Python is a high-level, interpreted programming language known for its simplicity and readability.",
            "hermes": "Hermes is an AI agent framework created by Nous Research that provides tool use, memory, and extensibility.",
            "technology": "Technology encompasses the tools, machines, and techniques used to solve problems and achieve goals."
        }
        
        # Sample jokes and quotes
        self.jokes = [
            "Why don't scientists trust atoms anymore? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "Why don't skeletons fight each other? They don't have the guts!",
            "What do you call a fake noodle? An impasta!"
        ]
        
        self.quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Innovation distinguishes between a leader and a follower. - Steve Jobs",
            "Life is what happens when you're busy making other plans. - John Lennon",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "It is during our darkest moments that we must focus to see the light. - Aristotle"
        ]
    
    def get_time(self):
        """Get current timestamp"""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def get_response(self, user_input):
        """Generate a response based on user input"""
        user_input_lower = user_input.lower().strip()
        
        # Handle special commands
        if user_input_lower in ['time', 'time now', 'current time']:
            return f"The current time is: {self.get_time()}"
        
        if user_input_lower in ['date', 'today', 'current date']:
            return f"Today's date is: {self.get_time().split()[0]}"
        
        if user_input_lower in ['help', 'commands', 'what can you do']:
            return self.get_help()
        
        if user_input_lower in ['knowledge', 'info', 'information']:
            return self.get_knowledge_info()
        
        if user_input_lower.startswith('tell me about') or user_input_lower.startswith('what is'):
            topic = user_input_lower.replace('tell me about', '').replace('what is', '').strip()
            if topic in self.knowledge_base:
                return f"About {topic}: {self.knowledge_base[topic]}"
            else:
                return f"I don't have specific information about '{topic}' in my knowledge base. I can tell you about: {', '.join(self.knowledge_base.keys())}"
        
        if user_input_lower in ['joke', 'tell me a joke', 'funny']:
            return self.get_joke()
        
        if user_input_lower in ['quote', 'inspiration', 'motivate']:
            return self.get_quote()
        
        # Default response
        return self.get_default_response()
    
    def get_help(self):
        """Return help information"""
        return """Available commands:
        - time: Get current time
        - date: Get today's date
        - help: Show this help message
        - knowledge: Show available knowledge topics
        - tell me about [topic]: Get information about a topic
        - joke: Get a random joke
        - quote: Get an inspirational quote
        - quit/exit/bye: End the conversation"""
    
    def get_knowledge_info(self):
        """Return information about available knowledge"""
        topics = ", ".join(self.knowledge_base.keys())
        return f"I have knowledge about: {topics}. Ask me about any of these topics!"
    
    def get_joke(self):
        """Return a random joke"""
        return random.choice(self.jokes)
    
    def get_quote(self):
        """Return a random inspirational quote"""
        return random.choice(self.quotes)
    
    def get_default_response(self):
        """Return a default response for unrecognized input"""
        responses = [
            "That's interesting! Tell me more about that.",
            "I see. How does that make you feel?",
            "Interesting perspective. What else is on your mind?",
            "I'm still learning. Could you rephrase that or ask about something else?",
            "Thanks for sharing! Is there anything specific you'd like to know?",
            "I appreciate your input. How can I assist you further?"
        ]
        return random.choice(responses)
    
    def add_to_history(self, user_input, bot_response):
        """Add exchange to conversation history"""
        self.conversation_history.append({
            "timestamp": self.get_time(),
            "user": user_input,
            "bot": bot_response
        })
    
    def save_conversation(self, filename=None):
        """Save conversation history to file"""
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    "assistant": self.name,
                    "version": self.version,
                    "timestamp": self.get_time(),
                    "conversation": self.conversation_history
                }, f, indent=2)
            return f"Conversation saved to {filename}"
        except Exception as e:
            return f"Error saving conversation: {str(e)}"
    
    def demo_conversation(self):
        """Run a demonstration conversation"""
        print(f"🤖 {self.name} v{self.version}")
        print("=" * 50)
        print("Demo Mode: Running a sample conversation\n")
        
        # Sample conversation
        sample_inputs = [
            "Hello!",
            "What time is it?",
            "Tell me about AI",
            "Tell me a joke",
            "Give me an inspirational quote",
            "What can you do?",
            "Thanks for the chat!",
            "bye"
        ]
        
        for user_input in sample_inputs:
            print(f"You: {user_input}")
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print(f"{self.name}: Goodbye! Have a great day!")
                break
            
            response = self.get_response(user_input)
            print(f"{self.name}: {response}")
            
            # Add to history
            self.add_to_history(user_input, response)
            print()
        
        # Save conversation
        save_result = self.save_conversation("demo_conversation.json")
        print(f"💾 {save_result}")
        print("\nDemo completed!")

def main():
    """Main function to run the demo"""
    assistant = HermesLite()
    assistant.demo_conversation()

if __name__ == "__main__":
    main()