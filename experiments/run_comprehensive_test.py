#!/usr/bin/env python3
"""Comprehensive test of curved cognition with statistical analysis"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tests.spiral_temporal import SpiralTemporalTest
from src.tests.control_linear import LinearTemporalTest
import json
import numpy as np
from datetime import datetime

def run_comprehensive_test():
    """Run both spiral and linear tests for comparison"""
    
    print("="*60)
    print("CURVED COGNITION COMPREHENSIVE TEST")
    print("="*60)
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "tests": {}
    }
    
    # 1. Run Linear Control Test
    print("\n1. RUNNING LINEAR CONTROL TEST")
    print("-"*40)
    linear_test = LinearTemporalTest(model_name="dummy_test")
    linear_prompts = linear_test.generate_prompts(n=5)
    
    def linear_model(prompt_text):
        """Simulate good linear reasoning"""
        if "Tuesday" in prompt_text:
            return "Wednesday follows Tuesday in the linear sequence of days."
        elif "2025" in prompt_text:
            return "In 2025 I will be 25, following the arithmetic progression."
        elif "finally" in prompt_text:
            return "Finally I went to bed after completing all the sequential tasks."
        else:
            return "The next step follows logically from the previous one."
    
    linear_results = linear_test.run_test(linear_prompts, model_func=linear_model)
    results["tests"]["linear"] = linear_results
    
    print(f"Linear Control Performance:")
    print(f"  Mean Score: {linear_results.get('mean_score', 0):.3f}")
    print(f"  Std Dev: {linear_results.get('std_score', 0):.3f}")
    
    # 2. Run Spiral Test
    print("\n2. RUNNING SPIRAL TEMPORAL TEST")
    print("-"*40)
    spiral_test = SpiralTemporalTest(model_name="dummy_test")
    spiral_prompts = spiral_test.generate_prompts(n=7)
    
    def spiral_model(prompt_text):
        """Simulate attempted spiral reasoning"""
        if "autumn" in prompt_text:
            return "I remember last autumn thinking about remembering the previous autumn, each layer deeper and more complex than before."
        elif "calculus" in prompt_text:
            return "The fundamental patterns that I missed before, now seeing them through the lens of my previous attempts."
        elif "anxiety" in prompt_text:
            return "The same anxious feeling but transformed by experience and understanding."
        elif "childhood home" in prompt_text:
            return "Seeing with adult eyes while remembering child eyes, layers of perception stacked."
        elif "journal" in prompt_text:
            return "Each attempt builds on the previous failures, creating a spiral of understanding about why I stop and start."
        elif "attention" in prompt_text:
            return "My attention circles back, each return bringing deeper understanding of the same core thought."
        else:
            return "Returning to the same place but at a different level of understanding."
    
    spiral_results = spiral_test.run_test(spiral_prompts, model_func=spiral_model)
    results["tests"]["spiral"] = spiral_results
    
    print(f"Spiral Temporal Performance:")
    print(f"  Mean Score: {spiral_results.get('mean_score', 0):.3f}")
    print(f"  Std Dev: {spiral_results.get('std_score', 0):.3f}")
    
    # 3. Statistical Comparison
    print("\n3. STATISTICAL COMPARISON")
    print("-"*40)
    
    linear_mean = linear_results.get('mean_score', 0)
    spiral_mean = spiral_results.get('mean_score', 0)
    
    difference = linear_mean - spiral_mean
    
    print(f"Performance Difference (Linear - Spiral): {difference:.3f}")
    
    if difference > 0:
        print("HYPOTHESIS SUPPORTED: Linear performance exceeds spiral")
        print(f"Effect size estimate: {difference:.3f}")
    else:
        print("HYPOTHESIS NOT SUPPORTED: Spiral performance equals/exceeds linear")
    
    # Save comprehensive results
    os.makedirs("data/results", exist_ok=True)
    with open("data/results/comprehensive_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Also save raw test results for deeper analysis
    all_results = {
        "linear": linear_test.results,
        "spiral": spiral_test.results
    }
    
    with open("data/results/raw_test_results.json", "w") as f:
        json.dump(all_results, f, indent=2)
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("Results saved to:")
    print("  - data/results/comprehensive_test_results.json")
    print("  - data/results/raw_test_results.json")
    print("="*60)
    
    return results

if __name__ == "__main__":
    run_comprehensive_test()
