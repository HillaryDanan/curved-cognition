#!/usr/bin/env python3
"""Statistical power analysis for curved cognition experiments"""
import numpy as np
from scipy import stats

def calculate_sample_size(effect_size=0.5, alpha=0.05, power=0.8):
    """
    Calculate required sample size for paired t-test
    
    Cohen's d effect sizes:
    - Small: 0.2
    - Medium: 0.5  
    - Large: 0.8
    """
    from scipy.stats import norm
    
    z_alpha = norm.ppf(1 - alpha/2)
    z_beta = norm.ppf(power)
    
    n = ((z_alpha + z_beta) ** 2) / (effect_size ** 2)
    
    return int(np.ceil(n))

def main():
    print("=== Statistical Power Analysis ===\n")
    
    # Different effect sizes
    effect_sizes = [0.2, 0.5, 0.8]
    effect_labels = ['Small', 'Medium', 'Large']
    
    print("Required sample sizes (prompts per condition):")
    print("-" * 50)
    
    for size, label in zip(effect_sizes, effect_labels):
        n = calculate_sample_size(effect_size=size)
        print(f"{label} effect (d={size}): n = {n} prompts")
    
    print("\nRecommendation:")
    print("- For robust results: 64 prompts per condition")
    print("- For pilot study: 20 prompts per condition")
    print("- Minimum viable: 10 prompts per condition")
    
    # Multiple testing correction
    n_tests = 5  # spiral, cyclical, orbital, fractal, recursive
    bonferroni_alpha = 0.05 / n_tests
    
    print(f"\nBonferroni correction for {n_tests} tests:")
    print(f"Adjusted alpha = {bonferroni_alpha:.4f}")

if __name__ == "__main__":
    main()
