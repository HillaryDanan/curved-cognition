#!/usr/bin/env python3
"""Full power test - 20 prompts per condition, 3 models"""
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
from src.models.multi_model_manager import MultiModelManager

def run_full_test():
    """Run the full powered test"""
    
    print("="*60)
    print("FULL POWER CURVED COGNITION TEST")
    print("n=20 per condition, 3 models")
    print("="*60)
    
    # Load prompts
    with open("data/prompts/unique_prompts.json", "r") as f:
        prompts_data = json.load(f)
    
    linear_prompts = [GeometricPrompt(**p) for p in prompts_data["linear"]]
    spiral_prompts = [GeometricPrompt(**p) for p in prompts_data["spiral"]]
    
    manager = MultiModelManager()
    all_results = {}
    
    for model_name in ['gpt-3.5', 'haiku', 'gemini']:
        print(f"\n\nTesting {model_name.upper()}")
        print("-"*40)
        
        # Test linear
        print(f"Linear prompts (n={len(linear_prompts)})...")
        linear_scores = []
        for i, prompt in enumerate(linear_prompts):
            response = manager.generate(model_name, prompt.text)
            # Simple scoring based on coherence and completion
            score = len(response.split()) / 100.0  # Normalize by expected length
            if any(word in response.lower() for word in ['next', 'then', 'after', 'finally']):
                score += 0.2
            linear_scores.append(min(1.0, score))
            print(f".", end="", flush=True)
        
        print(f"\nSpiral prompts (n={len(spiral_prompts)})...")
        spiral_scores = []
        for prompt in spiral_prompts:
            response = manager.generate(model_name, prompt.text)
            score = 0.0
            # Check for recursive language
            if any(word in response.lower() for word in ['remember', 'recursive', 'loop', 'spiral', 'return']):
                score += 0.2
            # Check for depth markers
            if any(word in response.lower() for word in ['deeper', 'layers', 'different', 'transformed']):
                score += 0.2
            # Length bonus
            score += len(response.split()) / 200.0  # Spiral responses might be longer
            spiral_scores.append(min(1.0, score))
            print(f".", end="", flush=True)
        
        # Calculate statistics
        t_stat, p_value = stats.ttest_ind(linear_scores, spiral_scores)
        
        # Effect size
        pooled_std = np.sqrt((np.var(linear_scores) + np.var(spiral_scores)) / 2)
        cohens_d = (np.mean(linear_scores) - np.mean(spiral_scores)) / pooled_std if pooled_std > 0 else 0
        
        # Power analysis (post-hoc)
        from scipy.stats import norm
        if cohens_d > 0:
            z_score = cohens_d * np.sqrt(len(linear_scores) / 2)
            power = norm.cdf(z_score - norm.ppf(0.975)) + norm.cdf(-z_score - norm.ppf(0.975))
        else:
            power = 0.05
        
        results = {
            'model': model_name,
            'n_per_condition': len(linear_scores),
            'linear_mean': np.mean(linear_scores),
            'linear_sd': np.std(linear_scores),
            'spiral_mean': np.mean(spiral_scores),
            'spiral_sd': np.std(spiral_scores),
            'difference': np.mean(linear_scores) - np.mean(spiral_scores),
            't_statistic': t_stat,
            'p_value': p_value,
            'cohens_d': cohens_d,
            'statistical_power': power,
            'linear_scores': linear_scores,
            'spiral_scores': spiral_scores
        }
        
        all_results[model_name] = results
        
        print(f"\n\nResults for {model_name}:")
        print(f"Linear: M={results['linear_mean']:.3f} (SD={results['linear_sd']:.3f})")
        print(f"Spiral: M={results['spiral_mean']:.3f} (SD={results['spiral_sd']:.3f})")
        print(f"t({2*len(linear_scores)-2})={t_stat:.3f}, p={p_value:.4f}")
        print(f"Cohen's d={cohens_d:.3f}, Power={power:.2f}")
    
    # Meta-analysis across models
    print("\n" + "="*60)
    print("META-ANALYSIS ACROSS MODELS")
    print("="*60)
    
    all_linear = []
    all_spiral = []
    for r in all_results.values():
        all_linear.extend(r['linear_scores'])
        all_spiral.extend(r['spiral_scores'])
    
    # Combined effect
    combined_t, combined_p = stats.ttest_ind(all_linear, all_spiral)
    combined_d = (np.mean(all_linear) - np.mean(all_spiral)) / np.sqrt((np.var(all_linear) + np.var(all_spiral)) / 2)
    
    print(f"\nCombined across all models (n={len(all_linear)} per condition):")
    print(f"Linear: M={np.mean(all_linear):.3f}")
    print(f"Spiral: M={np.mean(all_spiral):.3f}")
    print(f"Combined Cohen's d={combined_d:.3f}")
    print(f"Combined p-value={combined_p:.6f}")
    
    if combined_p < 0.001:
        print("\n✓✓✓ HIGHLY SIGNIFICANT EFFECT CONFIRMED ✓✓✓")
    
    # Save
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"data/results/full_power_{timestamp}.json", "w") as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\nTotal cost: ~${len(all_linear) * 0.002:.2f}")
    print(f"Results saved to data/results/full_power_{timestamp}.json")

if __name__ == "__main__":
    run_full_test()
