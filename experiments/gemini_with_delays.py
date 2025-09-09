#!/usr/bin/env python3
"""Test Gemini with rate limit delays"""
import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
from src.tests.spiral_temporal import SpiralTemporalTest
from src.tests.control_linear import LinearTemporalTest
import numpy as np
from scipy import stats

# Configure Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_with_delay(prompt_text):
    """Generate with 4 second delay to avoid rate limits"""
    time.sleep(4)  # Wait 4 seconds between calls (15 per minute limit)
    try:
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)  # If error, wait longer
        try:
            response = model.generate_content(prompt_text)
            return response.text
        except:
            return "Error generating response"

# Load unique prompts
import json
with open("data/prompts/unique_prompts.json", "r") as f:
    prompts_data = json.load(f)

from src.core.geometric_tests import GeometricPrompt

print("GEMINI RETEST WITH DELAYS")
print("="*40)

# Test linear
linear_test = LinearTemporalTest(model_name="gemini-1.5-flash")
linear_prompts = [GeometricPrompt(**p) for p in prompts_data["linear"]]

print("Testing linear (with 4s delays)...")
linear_results = linear_test.run_test(
    linear_prompts,
    model_func=generate_with_delay
)

# Test spiral  
spiral_test = SpiralTemporalTest(model_name="gemini-1.5-flash")
spiral_prompts = [GeometricPrompt(**p) for p in prompts_data["spiral"]]

print("Testing spiral (with 4s delays)...")
spiral_results = spiral_test.run_test(
    spiral_prompts,
    model_func=generate_with_delay
)

# Statistics
linear_scores = [r['scores']['total'] for r in linear_test.results]
spiral_scores = [r['scores']['total'] for r in spiral_test.results]

t_stat, p_value = stats.ttest_ind(linear_scores, spiral_scores)
pooled_std = np.sqrt((np.var(linear_scores) + np.var(spiral_scores)) / 2)
cohens_d = (np.mean(linear_scores) - np.mean(spiral_scores)) / pooled_std if pooled_std > 0 else 0

print(f"\nGEMINI RESULTS (FIXED):")
print(f"Linear: M={np.mean(linear_scores):.3f}, SD={np.std(linear_scores):.3f}")
print(f"Spiral: M={np.mean(spiral_scores):.3f}, SD={np.std(spiral_scores):.3f}")
print(f"t={t_stat:.3f}, p={p_value:.4f}, d={cohens_d:.3f}")

# Save
with open("data/results/gemini_fixed.json", "w") as f:
    json.dump({
        "linear_scores": linear_scores,
        "spiral_scores": spiral_scores,
        "stats": {"t": t_stat, "p": p_value, "d": cohens_d}
    }, f, indent=2)
