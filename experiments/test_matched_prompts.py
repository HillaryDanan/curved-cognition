#!/usr/bin/env python3
"""Test with length-matched prompts to eliminate confound"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

import json
import numpy as np
from scipy import stats
from src.core.geometric_tests import GeometricPrompt
from src.tests.spiral_temporal import SpiralTemporalTest
from src.tests.control_linear import LinearTemporalTest
from src.models.multi_model_manager import MultiModelManager

# Load matched prompts
with open("data/prompts/matched_prompts.json", "r") as f:
    prompts_data = json.load(f)

linear_prompts = [GeometricPrompt(**p) for p in prompts_data["linear"]]
spiral_prompts = [GeometricPrompt(**p) for p in prompts_data["spiral"]]

manager = MultiModelManager()

print("LENGTH-MATCHED PROMPT TEST")
print("="*40)
print("Testing 10 matched pairs (same word count)")

results = {}

for model_name in ['gpt-3.5', 'haiku']:
    print(f"\n{model_name.upper()}:")
    
    # Test
    linear_test = LinearTemporalTest(model_name=model_name)
    linear_results = linear_test.run_test(
        linear_prompts,
        model_func=lambda p: manager.generate(model_name, p)
    )
    
    spiral_test = SpiralTemporalTest(model_name=model_name)
    spiral_results = spiral_test.run_test(
        spiral_prompts,
        model_func=lambda p: manager.generate(model_name, p)
    )
    
    # Stats
    linear_scores = [r['scores']['total'] for r in linear_test.results]
    spiral_scores = [r['scores']['total'] for r in spiral_test.results]
    
    t_stat, p_value = stats.ttest_ind(linear_scores, spiral_scores)
    pooled_std = np.sqrt((np.var(linear_scores) + np.var(spiral_scores)) / 2)
    cohens_d = (np.mean(linear_scores) - np.mean(spiral_scores)) / pooled_std if pooled_std > 0 else 0
    
    print(f"  Linear: M={np.mean(linear_scores):.3f}")
    print(f"  Spiral: M={np.mean(spiral_scores):.3f}")
    print(f"  Difference: {np.mean(linear_scores) - np.mean(spiral_scores):.3f}")
    print(f"  Cohen's d: {cohens_d:.3f}, p={p_value:.4f}")
    
    if p_value < 0.05:
        print(f"  ✓ Effect persists with matched lengths!")
    
    results[model_name] = {
        "linear_mean": np.mean(linear_scores),
        "spiral_mean": np.mean(spiral_scores),
        "cohens_d": cohens_d,
        "p_value": p_value
    }

# Save
with open("data/results/matched_prompts_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n" + "="*40)
if all(r["p_value"] < 0.05 for r in results.values()):
    print("LENGTH CONFOUND ELIMINATED!")
    print("Effect persists with matched word counts")
else:
    print("Mixed results - needs investigation")
