#!/usr/bin/env python3
"""Proper statistical analysis for curved cognition tests"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import numpy as np
from scipy import stats

def analyze_results():
    """Perform rigorous statistical analysis on test results"""
    
    # Load the raw results
    with open('data/results/raw_test_results.json', 'r') as f:
        data = json.load(f)
    
    # Extract scores
    linear_scores = [r['scores']['total'] for r in data['linear']]
    spiral_scores = [r['scores']['total'] for r in data['spiral']]
    
    print("="*60)
    print("RIGOROUS STATISTICAL ANALYSIS")
    print("="*60)
    
    # 1. Descriptive Statistics
    print("\n1. DESCRIPTIVE STATISTICS")
    print("-"*40)
    print(f"Linear: n={len(linear_scores)}, M={np.mean(linear_scores):.3f}, SD={np.std(linear_scores):.3f}")
    print(f"Spiral: n={len(spiral_scores)}, M={np.mean(spiral_scores):.3f}, SD={np.std(spiral_scores):.3f}")
    
    # 2. Normality Tests
    print("\n2. NORMALITY TESTS (Shapiro-Wilk)")
    print("-"*40)
    if len(linear_scores) >= 3:
        _, p_linear = stats.shapiro(linear_scores)
        print(f"Linear: p={p_linear:.3f} {'(normal)' if p_linear > 0.05 else '(not normal)'}")
    else:
        print(f"Linear: Too few samples for Shapiro-Wilk (n={len(linear_scores)})")
        p_linear = 0
    
    if len(spiral_scores) >= 3:
        _, p_spiral = stats.shapiro(spiral_scores)
        print(f"Spiral: p={p_spiral:.3f} {'(normal)' if p_spiral > 0.05 else '(not normal)'}")
    else:
        print(f"Spiral: Too few samples for Shapiro-Wilk (n={len(spiral_scores)})")
        p_spiral = 0
    
    # 3. Variance Comparison
    print("\n3. VARIANCE COMPARISON (Levene's Test)")
    print("-"*40)
    if len(linear_scores) > 1 and len(spiral_scores) > 1:
        _, p_levene = stats.levene(linear_scores, spiral_scores)
        print(f"p={p_levene:.3f} {'(equal variances)' if p_levene > 0.05 else '(unequal variances)'}")
    
    # 4. Statistical Test
    print("\n4. HYPOTHESIS TEST")
    print("-"*40)
    
    if len(linear_scores) < 2 or len(spiral_scores) < 2:
        print("ERROR: Not enough data for statistical testing")
        print("Need at least n=2 per condition")
        return
    
    # Use t-test if normal, Mann-Whitney if not
    if p_linear > 0.05 and p_spiral > 0.05:
        t_stat, p_value = stats.ttest_ind(linear_scores, spiral_scores)
        test_name = "Independent t-test"
        stat_name = "t"
        stat_value = t_stat
    else:
        u_stat, p_value = stats.mannwhitneyu(linear_scores, spiral_scores, alternative='two-sided')
        test_name = "Mann-Whitney U test"
        stat_name = "U"
        stat_value = u_stat
    
    print(f"Test used: {test_name}")
    print(f"{stat_name} = {stat_value:.3f}, p = {p_value:.3f}")
    
    # 5. Effect Size
    print("\n5. EFFECT SIZE")
    print("-"*40)
    
    # Cohen's d
    pooled_std = np.sqrt((np.var(linear_scores) + np.var(spiral_scores)) / 2)
    cohens_d = (np.mean(linear_scores) - np.mean(spiral_scores)) / pooled_std
    
    print(f"Cohen's d = {cohens_d:.3f}")
    
    if abs(cohens_d) < 0.2:
        magnitude = "negligible"
    elif abs(cohens_d) < 0.5:
        magnitude = "small"
    elif abs(cohens_d) < 0.8:
        magnitude = "medium"
    else:
        magnitude = "large"
    
    print(f"Effect magnitude: {magnitude}")
    
    # 6. Confidence Interval
    print("\n6. 95% CONFIDENCE INTERVAL FOR DIFFERENCE")
    print("-"*40)
    
    diff = np.mean(linear_scores) - np.mean(spiral_scores)
    se = np.sqrt(np.var(linear_scores)/len(linear_scores) + 
                 np.var(spiral_scores)/len(spiral_scores))
    ci_lower = diff - 1.96*se
    ci_upper = diff + 1.96*se
    
    print(f"Difference: {diff:.3f}")
    print(f"95% CI: [{ci_lower:.3f}, {ci_upper:.3f}]")
    
    # 7. Interpretation
    print("\n7. INTERPRETATION")
    print("-"*40)
    
    if p_value < 0.05:
        print("✓ Statistically significant difference (p < 0.05)")
    else:
        print("✗ No statistically significant difference (p ≥ 0.05)")
    
    if ci_lower > 0:
        print("✓ Linear consistently outperforms spiral")
    elif ci_upper < 0:
        print("✓ Spiral consistently outperforms linear")
    else:
        print("✗ Difference could go either direction")
    
    print(f"\nConclusion: Linear scores are {diff:.3f} points higher than spiral")
    print(f"with a {magnitude} effect size (d={cohens_d:.3f})")
    
    # 8. Statistical Power
    print("\n8. STATISTICAL POWER")
    print("-"*40)
    print(f"Current sample sizes: Linear n={len(linear_scores)}, Spiral n={len(spiral_scores)}")
    print("For 80% power to detect medium effect (d=0.5):")
    print("  Required n=64 per group")
    print(f"  Current power ≈ {len(linear_scores)/64:.1%}")
    
    print("\n" + "="*60)
    print("CAVEAT: These are DUMMY MODELS with HARDCODED responses")
    print("This tests our SCORING SYSTEM, not actual AI behavior")
    print("="*60)

if __name__ == "__main__":
    analyze_results()
