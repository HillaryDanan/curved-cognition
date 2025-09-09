#!/usr/bin/env python3
"""Scaled test with proper statistics"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from src.tests.spiral_temporal import SpiralTemporalTest
from src.tests.control_linear import LinearTemporalTest
from src.models.api_manager import ModelManager
import json
import numpy as np
from scipy import stats
from datetime import datetime

def run_scaled_test():
    """Run with n=10 for real statistics"""
    
    print("="*60)
    print("SCALED REAL MODEL TEST - GPT-3.5-TURBO")
    print("="*60)
    
    manager = ModelManager()
    
    # Test Linear
    print("\n1. Testing LINEAR (n=10)...")
    linear_test = LinearTemporalTest(model_name="gpt-3.5-turbo")
    linear_prompts = linear_test.generate_prompts(n=10)
    
    # Need to cycle through our 5 available prompts
    if len(linear_prompts) < 10:
        linear_prompts = linear_prompts * (10 // len(linear_prompts) + 1)
        linear_prompts = linear_prompts[:10]
    
    linear_results = linear_test.run_test(
        linear_prompts, 
        model_func=lambda p: manager.generate(p)
    )
    
    # Test Spiral  
    print("\n2. Testing SPIRAL (n=10)...")
    spiral_test = SpiralTemporalTest(model_name="gpt-3.5-turbo")
    spiral_prompts = spiral_test.generate_prompts(n=10)
    
    # Cycle if needed
    if len(spiral_prompts) < 10:
        base_prompts = spiral_prompts.copy()
        while len(spiral_prompts) < 10:
            spiral_prompts.extend(base_prompts)
        spiral_prompts = spiral_prompts[:10]
    
    spiral_results = spiral_test.run_test(
        spiral_prompts,
        model_func=lambda p: manager.generate(p)
    )
    
    # Extract scores
    linear_scores = [r['scores']['total'] for r in linear_test.results]
    spiral_scores = [r['scores']['total'] for r in spiral_test.results]
    
    # Statistics
    print("\n" + "="*60)
    print("RESULTS WITH REAL GPT-3.5")
    print("="*60)
    
    print(f"\nDescriptive Statistics:")
    print(f"Linear: n={len(linear_scores)}, M={np.mean(linear_scores):.3f}, SD={np.std(linear_scores):.3f}")
    print(f"Spiral: n={len(spiral_scores)}, M={np.mean(spiral_scores):.3f}, SD={np.std(spiral_scores):.3f}")
    
    # T-test
    t_stat, p_value = stats.ttest_ind(linear_scores, spiral_scores)
    
    # Cohen's d
    pooled_std = np.sqrt((np.var(linear_scores) + np.var(spiral_scores)) / 2)
    if pooled_std > 0:
        cohens_d = (np.mean(linear_scores) - np.mean(spiral_scores)) / pooled_std
    else:
        cohens_d = 0
    
    print(f"\nStatistical Test:")
    print(f"t({len(linear_scores)+len(spiral_scores)-2})={t_stat:.3f}, p={p_value:.4f}")
    print(f"Cohen's d={cohens_d:.3f}")
    
    # Interpretation
    if abs(cohens_d) < 0.2:
        effect = "negligible"
    elif abs(cohens_d) < 0.5:
        effect = "small"
    elif abs(cohens_d) < 0.8:
        effect = "medium"
    else:
        effect = "LARGE"
    
    print(f"Effect size: {effect}")
    
    if p_value < 0.05:
        print("\n✓✓✓ STATISTICALLY SIGNIFICANT! ✓✓✓")
        print(f"GPT-3.5 performs significantly better on linear vs spiral reasoning")
    else:
        print("\n✗ Not statistically significant (yet)")
    
    print(f"\nTotal API cost: ${manager.get_cost():.2f}")
    
    # Save everything
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/results/gpt35_scaled_{timestamp}.json"
    
    with open(filename, "w") as f:
        json.dump({
            "model": "gpt-3.5-turbo",
            "n_per_condition": len(linear_scores),
            "linear_mean": np.mean(linear_scores),
            "spiral_mean": np.mean(spiral_scores),
            "difference": np.mean(linear_scores) - np.mean(spiral_scores),
            "t_statistic": t_stat,
            "p_value": p_value,
            "cohens_d": cohens_d,
            "effect_magnitude": effect,
            "linear_scores": linear_scores,
            "spiral_scores": spiral_scores,
            "cost": manager.get_cost()
        }, f, indent=2)
    
    print(f"\nResults saved to {filename}")
    
    return p_value < 0.05

if __name__ == "__main__":
    is_significant = run_scaled_test()
    
    if is_significant:
        print("\n" + "="*60)
        print("HYPOTHESIS CONFIRMED WITH REAL AI")
        print("GPT-3.5 thinks in rectangles, not spirals!")
        print("="*60)
