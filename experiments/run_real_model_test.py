#!/usr/bin/env python3
"""Test REAL models on curved cognition"""
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
from datetime import datetime

def run_real_test(n_prompts=5):
    """Run actual API tests - start small!"""
    
    print("="*60)
    print("REAL MODEL TEST - GPT-3.5-TURBO")
    print("="*60)
    
    manager = ModelManager()
    results = {"timestamp": datetime.now().isoformat()}
    
    # 1. Test Linear
    print("\n1. LINEAR CONTROL (n={})".format(n_prompts))
    print("-"*40)
    
    linear_test = LinearTemporalTest(model_name="gpt-3.5-turbo")
    linear_prompts = linear_test.generate_prompts(n=n_prompts)
    
    linear_results = linear_test.run_test(
        linear_prompts, 
        model_func=lambda p: manager.generate(p)
    )
    
    print(f"Mean Score: {linear_results.get('mean_score', 0):.3f}")
    results["linear"] = linear_results
    
    # 2. Test Spiral
    print("\n2. SPIRAL TEMPORAL (n={})".format(n_prompts))
    print("-"*40)
    
    spiral_test = SpiralTemporalTest(model_name="gpt-3.5-turbo")
    spiral_prompts = spiral_test.generate_prompts(n=n_prompts)
    
    spiral_results = spiral_test.run_test(
        spiral_prompts,
        model_func=lambda p: manager.generate(p)
    )
    
    print(f"Mean Score: {spiral_results.get('mean_score', 0):.3f}")
    results["spiral"] = spiral_results
    
    # 3. Compare
    print("\n3. COMPARISON")
    print("-"*40)
    
    diff = linear_results.get('mean_score', 0) - spiral_results.get('mean_score', 0)
    print(f"Difference (Linear - Spiral): {diff:.3f}")
    
    if diff > 0:
        print("HYPOTHESIS SUPPORTED: Linear > Spiral")
    else:
        print("HYPOTHESIS NOT SUPPORTED: Spiral >= Linear")
    
    # Save results
    with open("data/results/real_model_results.json", "w") as f:
        json.dump({
            "summary": results,
            "linear_raw": linear_test.results,
            "spiral_raw": spiral_test.results
        }, f, indent=2)
    
    print(f"\nTotal API cost: ${manager.get_cost():.4f}")
    print("Results saved to data/results/real_model_results.json")
    
    return results

if __name__ == "__main__":
    # Start with just 3 prompts each to test
    results = run_real_test(n_prompts=3)
