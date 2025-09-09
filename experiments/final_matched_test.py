#!/usr/bin/env python3
"""Final test with 20 matched pairs across 3 models"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

import json
import numpy as np
from scipy import stats
from datetime import datetime
from src.core.geometric_tests import GeometricPrompt
from src.tests.spiral_temporal import SpiralTemporalTest
from src.tests.control_linear import LinearTemporalTest
from src.models.multi_model_manager import MultiModelManager
from openai import OpenAI

# Load matched prompts
with open("data/prompts/matched_20_pairs.json", "r") as f:
    prompts_data = json.load(f)

linear_prompts = [GeometricPrompt(**p) for p in prompts_data["linear"]]
spiral_prompts = [GeometricPrompt(**p) for p in prompts_data["spiral"]]

print("="*60)
print("FINAL TEST: 20 LENGTH-MATCHED PAIRS")
print("="*60)
print(f"Testing {len(linear_prompts)} exactly matched prompt pairs\n")

manager = MultiModelManager()
client = OpenAI()

def test_gpt4(prompt_text):
    """GPT-4 generation"""
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[{"role": "user", "content": prompt_text}],
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message.content

all_results = {}

# Test each model
models_to_test = [
    ("gpt-3.5", lambda p: manager.generate("gpt-3.5", p)),
    ("haiku", lambda p: manager.generate("haiku", p)),
    ("gpt-4", test_gpt4)
]

for model_name, model_func in models_to_test:
    print(f"\nTesting {model_name.upper()}...")
    print("-"*40)
    
    # Linear test
    linear_test = LinearTemporalTest(model_name=model_name)
    linear_results = linear_test.run_test(linear_prompts, model_func=model_func)
    
    # Spiral test
    spiral_test = SpiralTemporalTest(model_name=model_name)
    spiral_results = spiral_test.run_test(spiral_prompts, model_func=model_func)
    
    # Extract scores
    linear_scores = [r['scores']['total'] for r in linear_test.results]
    spiral_scores = [r['scores']['total'] for r in spiral_test.results]
    
    # Statistics
    t_stat, p_value = stats.ttest_rel(linear_scores, spiral_scores)  # PAIRED test since matched
    pooled_std = np.sqrt((np.var(linear_scores) + np.var(spiral_scores)) / 2)
    cohens_d = (np.mean(linear_scores) - np.mean(spiral_scores)) / pooled_std if pooled_std > 0 else 0
    
    # Power calculation
    from scipy.stats import norm
    if cohens_d != 0:
        n = len(linear_scores)
        z = cohens_d * np.sqrt(n)
        power = norm.cdf(z - 1.96)
    else:
        power = 0.05
    
    # Results
    results = {
        'n_pairs': len(linear_scores),
        'linear_mean': np.mean(linear_scores),
        'linear_sd': np.std(linear_scores),
        'spiral_mean': np.mean(spiral_scores),
        'spiral_sd': np.std(spiral_scores),
        'difference': np.mean(linear_scores) - np.mean(spiral_scores),
        't_statistic': t_stat,
        'p_value': p_value,
        'cohens_d': cohens_d,
        'power': power
    }
    
    all_results[model_name] = results
    
    print(f"Linear: M={results['linear_mean']:.3f} (SD={results['linear_sd']:.3f})")
    print(f"Spiral: M={results['spiral_mean']:.3f} (SD={results['spiral_sd']:.3f})")
    print(f"Difference: {results['difference']:.3f}")
    print(f"t({len(linear_scores)-1})={t_stat:.3f}, p={p_value:.4f}")
    print(f"Cohen's d={cohens_d:.3f}, Power={power:.1%}")
    
    if p_value < 0.05:
        print("✓ SIGNIFICANT with length control!")
    else:
        print("✗ Not significant with length control")

# Summary
print("\n" + "="*60)
print("SUMMARY: LENGTH-CONTROLLED RESULTS")
print("="*60)
print(f"{'Model':<10} {'N':<5} {'Linear':<8} {'Spiral':<8} {'Diff':<8} {'d':<8} {'p':<8} {'Sig':<5}")
print("-"*60)

for model, r in all_results.items():
    sig = "YES" if r['p_value'] < 0.05 else "NO"
    print(f"{model:<10} {r['n_pairs']:<5} {r['linear_mean']:<8.3f} {r['spiral_mean']:<8.3f} "
          f"{r['difference']:<8.3f} {r['cohens_d']:<8.3f} {r['p_value']:<8.4f} {sig:<5}")

# Save everything
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"data/results/final_matched_{timestamp}.json"
with open(filename, "w") as f:
    json.dump(all_results, f, indent=2)

print(f"\nResults saved to {filename}")

# Final verdict
significant_models = [m for m, r in all_results.items() if r['p_value'] < 0.05]
print("\n" + "="*60)
if len(significant_models) >= 2:
    print("PUBLICATION READY!")
    print(f"Effect confirmed in {len(significant_models)}/3 models with length control")
else:
    print("NEEDS MORE WORK")
    print("Length confound may explain much of the effect")
