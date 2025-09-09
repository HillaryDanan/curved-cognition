#!/usr/bin/env python3
"""Test GPT-4 on curved cognition"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
import json
import numpy as np
from scipy import stats
from src.tests.spiral_temporal import SpiralTemporalTest
from src.tests.control_linear import LinearTemporalTest

client = OpenAI()

def generate_gpt4(prompt_text):
    """Generate with GPT-4"""
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",  # or "gpt-4" for regular
        messages=[{"role": "user", "content": prompt_text}],
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message.content

print("TESTING GPT-4")
print("="*40)
print("WARNING: This costs ~$0.50-1.00")
response = input("Continue? (y/n): ")

if response.lower() != 'y':
    print("Aborted")
    exit()

# Quick test with just 5 prompts each to save money
linear_test = LinearTemporalTest(model_name="gpt-4")
linear_prompts = linear_test.generate_prompts(n=5)

print("Testing linear...")
linear_results = linear_test.run_test(
    linear_prompts,
    model_func=generate_gpt4
)

spiral_test = SpiralTemporalTest(model_name="gpt-4")
spiral_prompts = spiral_test.generate_prompts(n=5)

print("Testing spiral...")
spiral_results = spiral_test.run_test(
    spiral_prompts,
    model_func=generate_gpt4
)

# Stats
linear_scores = [r['scores']['total'] for r in linear_test.results]
spiral_scores = [r['scores']['total'] for r in spiral_test.results]

print(f"\nGPT-4 RESULTS:")
print(f"Linear: M={np.mean(linear_scores):.3f}")
print(f"Spiral: M={np.mean(spiral_scores):.3f}")
print(f"Difference: {np.mean(linear_scores) - np.mean(spiral_scores):.3f}")
