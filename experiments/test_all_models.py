#!/usr/bin/env python3
"""Test all available models on curved cognition"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from src.tests.spiral_temporal import SpiralTemporalTest
from src.tests.control_linear import LinearTemporalTest
from src.models.multi_model_manager import MultiModelManager
import json
import numpy as np
from scipy import stats
from datetime import datetime

def test_model(model_name, manager, n_prompts=10):
    """Test one model"""
    print(f"\nTesting {model_name.upper()}...")
    print("-"*40)
    
    # Linear test
    linear_test = LinearTemporalTest(model_name=model_name)
    linear_prompts = linear_test.generate_prompts(n=5)  # Use our 5 unique ones
    
    linear_results = linear_test.run_test(
        linear_prompts,
        model_func=lambda p: manager.generate(model_name, p)
    )
    
    # Spiral test
    spiral_test = SpiralTemporalTest(model_name=model_name)
    spiral_prompts = spiral_test.generate_prompts(n=7)  # Use our 7 unique ones
    
    spiral_results = spiral_test.run_test(
        spiral_prompts,
        model_func=lambda p: manager.generate(model_name, p)
    )
    
    # Calculate stats
    linear_scores = [r['scores']['total'] for r in linear_test.results]
    spiral_scores = [r['scores']['total'] for r in spiral_test.results]
    
    linear_mean = np.mean(linear_scores)
    spiral_mean = np.mean(spiral_scores)
    
    # T-test if we have enough data
    if len(linear_scores) > 1 and len(spiral_scores) > 1:
        t_stat, p_value = stats.ttest_ind(linear_scores, spiral_scores)
        
        # Cohen's d
        pooled_std = np.sqrt((np.var(linear_scores) + np.var(spiral_scores)) / 2)
        if pooled_std > 0:
            cohens_d = (linear_mean - spiral_mean) / pooled_std
        else:
            cohens_d = 0
    else:
        t_stat, p_value, cohens_d = 0, 1, 0
    
    print(f"Linear: M={linear_mean:.3f}")
    print(f"Spiral: M={spiral_mean:.3f}")
    print(f"Difference: {linear_mean - spiral_mean:.3f}")
    print(f"Cohen's d: {cohens_d:.3f}")
    print(f"p-value: {p_value:.4f}")
    
    return {
        'model': model_name,
        'linear_mean': linear_mean,
        'spiral_mean': spiral_mean,
        'difference': linear_mean - spiral_mean,
        'cohens_d': cohens_d,
        'p_value': p_value,
        'linear_scores': linear_scores,
        'spiral_scores': spiral_scores
    }

def main():
    print("="*60)
    print("MULTI-MODEL CURVED COGNITION TEST")
    print("="*60)
    
    manager = MultiModelManager()
    available_models = list(manager.models.keys())
    
    print(f"\nAvailable models: {available_models}")
    
    all_results = {}
    
    # Test each model
    for model in available_models:
        try:
            results = test_model(model, manager)
            all_results[model] = results
        except Exception as e:
            print(f"Failed to test {model}: {e}")
    
    # Summary comparison
    print("\n" + "="*60)
    print("CROSS-MODEL COMPARISON")
    print("="*60)
    
    print("\n{:<12} {:>8} {:>8} {:>8} {:>8} {:>8}".format(
        "Model", "Linear", "Spiral", "Diff", "Cohen's d", "p-value"
    ))
    print("-"*60)
    
    for model, results in all_results.items():
        print("{:<12} {:>8.3f} {:>8.3f} {:>8.3f} {:>8.3f} {:>8.4f}".format(
            model,
            results['linear_mean'],
            results['spiral_mean'],
            results['difference'],
            results['cohens_d'],
            results['p_value']
        ))
    
    # Save everything
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"data/results/multimodel_{timestamp}.json", "w") as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n\nTotal costs: {manager.costs}")
    print(f"Results saved to data/results/multimodel_{timestamp}.json")
    
    # Scientific conclusion
    consistent_effect = all([r['difference'] > 0 for r in all_results.values()])
    if consistent_effect:
        print("\n" + "="*60)
        print("CONSISTENT EFFECT ACROSS MODELS!")
        print("All models show linear > spiral performance")
        print("This suggests architectural constraint, not model-specific")
        print("="*60)

if __name__ == "__main__":
    main()
