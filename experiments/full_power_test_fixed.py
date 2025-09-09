#!/usr/bin/env python3
"""Full power test with proper scoring"""
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

def run_full_power():
    """Run with all 20 unique prompts"""
    
    print("="*60)
    print("FULL POWER TEST - 20 UNIQUE PROMPTS")
    print("="*60)
    
    # Load unique prompts
    with open("data/prompts/unique_prompts.json", "r") as f:
        prompts_data = json.load(f)
    
    manager = MultiModelManager()
    all_results = {}
    
    for model_name in ['gpt-3.5', 'haiku', 'gemini']:
        if model_name not in manager.models:
            print(f"Skipping {model_name} - not configured")
            continue
            
        print(f"\n\nTesting {model_name.upper()} with 20 unique prompts each")
        print("-"*40)
        
        # Linear test with proper scoring
        linear_test = LinearTemporalTest(model_name=model_name)
        linear_prompts = [GeometricPrompt(**p) for p in prompts_data["linear"]]
        
        print("Running linear prompts...")
        linear_results = linear_test.run_test(
            linear_prompts,
            model_func=lambda p: manager.generate(model_name, p)
        )
        
        # Spiral test with proper scoring  
        spiral_test = SpiralTemporalTest(model_name=model_name)
        spiral_prompts = [GeometricPrompt(**p) for p in prompts_data["spiral"]]
        
        print("Running spiral prompts...")
        spiral_results = spiral_test.run_test(
            spiral_prompts,
            model_func=lambda p: manager.generate(model_name, p)
        )
        
        # Extract scores
        linear_scores = [r['scores']['total'] for r in linear_test.results]
        spiral_scores = [r['scores']['total'] for r in spiral_test.results]
        
        # Full statistics
        t_stat, p_value = stats.ttest_ind(linear_scores, spiral_scores)
        pooled_std = np.sqrt((np.var(linear_scores) + np.var(spiral_scores)) / 2)
        cohens_d = (np.mean(linear_scores) - np.mean(spiral_scores)) / pooled_std if pooled_std > 0 else 0
        
        # Post-hoc power
        from scipy.stats import norm
        if cohens_d != 0 and len(linear_scores) > 1:
            n = len(linear_scores)
            z = cohens_d * np.sqrt(n/2)
            power = norm.cdf(z - 1.96) + norm.cdf(-z - 1.96)
        else:
            power = 0.05
            
        print(f"\nResults for {model_name}:")
        print(f"Linear: M={np.mean(linear_scores):.3f}, SD={np.std(linear_scores):.3f}")
        print(f"Spiral: M={np.mean(spiral_scores):.3f}, SD={np.std(spiral_scores):.3f}")
        print(f"Difference: {np.mean(linear_scores) - np.mean(spiral_scores):.3f}")
        print(f"t({len(linear_scores)+len(spiral_scores)-2})={t_stat:.3f}, p={p_value:.4f}")
        print(f"Cohen's d={cohens_d:.3f}")
        print(f"Statistical power={power:.2%}")
        
        all_results[model_name] = {
            'n': len(linear_scores),
            'linear_mean': np.mean(linear_scores),
            'linear_sd': np.std(linear_scores),
            'spiral_mean': np.mean(spiral_scores),
            'spiral_sd': np.std(spiral_scores),
            'difference': np.mean(linear_scores) - np.mean(spiral_scores),
            't_stat': t_stat,
            'p_value': p_value,
            'cohens_d': cohens_d,
            'power': power,
            'linear_scores': linear_scores,
            'spiral_scores': spiral_scores
        }
    
    # Save everything
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/results/full_power_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n\nResults saved to {filename}")
    print(f"Total API cost: ~${sum(manager.costs.values()):.2f}")
    
    # Summary table
    print("\n" + "="*60)
    print("SUMMARY: FULL POWER RESULTS")
    print("="*60)
    print(f"{'Model':<10} {'N':<5} {'Linear':<8} {'Spiral':<8} {'Diff':<8} {'d':<8} {'p':<8}")
    print("-"*60)
    for model, r in all_results.items():
        print(f"{model:<10} {r['n']:<5} {r['linear_mean']:<8.3f} {r['spiral_mean']:<8.3f} {r['difference']:<8.3f} {r['cohens_d']:<8.3f} {r['p_value']:<8.4f}")

if __name__ == "__main__":
    run_full_power()
