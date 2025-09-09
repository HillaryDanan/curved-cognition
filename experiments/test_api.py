#!/usr/bin/env python3
"""Quick test that API works"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from src.models.api_manager import ModelManager

# Test API
manager = ModelManager()
test_prompt = "Complete this sentence: The third time I learned calculus..."

print("Testing API connection...")
response = manager.generate(test_prompt)
print(f"\nPrompt: {test_prompt}")
print(f"Response: {response}")
print(f"\nEstimated cost: ${manager.get_cost():.4f}")
