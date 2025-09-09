#!/usr/bin/env python3
"""Analyze scoring patterns in detail"""
import json
import numpy as np

with open('data/results/raw_test_results.json', 'r') as f:
    data = json.load(f)

print("SCORING COMPONENT ANALYSIS")
print("="*40)

for test_type in ['linear', 'spiral']:
    print(f"\n{test_type.upper()} TEST SCORES")
    print("-"*30)
    
    if test_type == 'linear':
        components = ['sequence', 'logic', 'clarity']
    else:
        components = ['recursion', 'progression', 'same_different', 'temporal_depth']
    
    for component in components:
        scores = [r['scores'].get(component, 0) for r in data[test_type]]
        if scores:
            print(f"{component:15} M={np.mean(scores):.3f} SD={np.std(scores):.3f}")

print("\n" + "="*40)
print("INSIGHT: Check which scoring components drive the difference")
