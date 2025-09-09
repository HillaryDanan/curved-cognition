"""Manager for multiple AI models"""
import os
import openai
import anthropic
import google.generativeai as genai
from typing import Optional

class MultiModelManager:
    """Test multiple models on same prompts"""
    
    def __init__(self):
        self.costs = {}
        self.models = {}
        
        # OpenAI
        if os.getenv('OPENAI_API_KEY'):
            openai.api_key = os.getenv('OPENAI_API_KEY')
            self.models['gpt-3.5'] = self.generate_openai
            
        # Anthropic
        if os.getenv('ANTHROPIC_API_KEY'):
            self.anthropic_client = anthropic.Anthropic(
                api_key=os.getenv('ANTHROPIC_API_KEY')
            )
            self.models['haiku'] = self.generate_anthropic
            
        # Google
        if os.getenv('GOOGLE_API_KEY'):
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            self.models['gemini'] = self.generate_gemini
    
    def generate_openai(self, prompt: str) -> str:
        from openai import OpenAI
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        self.costs['gpt-3.5'] = self.costs.get('gpt-3.5', 0) + 0.002
        return response.choices[0].message.content
    
    def generate_anthropic(self, prompt: str) -> str:
        response = self.anthropic_client.messages.create(
            model="claude-3-5-haiku-20241022",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        self.costs['haiku'] = self.costs.get('haiku', 0) + 0.001
        return response.content[0].text
    
    def generate_gemini(self, prompt: str) -> str:
        response = self.gemini_model.generate_content(prompt)
        self.costs['gemini'] = self.costs.get('gemini', 0) + 0.001
        return response.text
    
    def generate(self, model_name: str, prompt: str) -> str:
        if model_name in self.models:
            try:
                return self.models[model_name](prompt)
            except Exception as e:
                print(f"Error with {model_name}: {e}")
                return f"Error: {str(e)}"
        else:
            return f"Model {model_name} not configured"
