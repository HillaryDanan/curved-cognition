"""Simple API manager for testing real models"""
import os
from openai import OpenAI
from typing import Optional

class ModelManager:
    """Manage API calls to real models"""
    
    def __init__(self):
        # Load API key from environment
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("Set OPENAI_API_KEY environment variable")
        
        self.client = OpenAI(api_key=api_key)
        self.total_cost = 0.0
    
    def generate(self, prompt: str, model: str = "gpt-3.5-turbo") -> str:
        """Generate response from OpenAI model"""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.7
            )
            
            # Track approximate cost (GPT-3.5: ~$0.002 per 1K tokens)
            self.total_cost += 0.002
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"API Error: {e}")
            return f"Error: {str(e)}"
    
    def get_cost(self) -> float:
        """Return total estimated cost"""
        return self.total_cost
