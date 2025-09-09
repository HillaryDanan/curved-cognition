#!/usr/bin/env python3
import json
import numpy as np

# Load the results
with open('data/results/gpt35_scaled_20250909_100055.json', 'r') as f:
    data = json.load(f)

print("COMPONENT ANALYSIS")
print("="*40)

# Load raw results to get component scores
with open('data/results/real_model_results.json', 'r') as f:
    raw = json.load(f)

# Analyze what drives the difference
print("\nWhich components explain the effect?")
print("-"*40)

for test_type in ['linear_raw', 'spiral_raw']:
    if test_type in raw:
        results = raw[test_type]
        if test_type == 'linear_raw':
            print("\nLINEAR Components:")
            components = ['sequence', 'logic', 'clarity']
        else:
            print("\nSPIRAL Components:")  
            components = ['recursion', 'progression', 'same_different', 'temporal_depth']
        
        for comp in components:
            scores = [r['scores'].get(comp, 0) for r in results[:3]]  # First 3
            if scores:
                print(f"  {comp:15} = {np.mean(scores):.3f}")

print("\n" + "="*40)
print("This tells us WHERE the models fail")
