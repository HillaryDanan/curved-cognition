#!/usr/bin/env python3
"""Simple test runner to verify our framework works"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tests.spiral_temporal import SpiralTemporalTest
import json

def main():
    print("=== Running Basic Curved Cognition Test ===\n")
    
    # Create test instance
    test = SpiralTemporalTest(model_name="dummy_test")
    
    # Generate prompts
    print("Generating test prompts...")
    prompts = test.generate_prompts(n=3)
    
    for i, prompt in enumerate(prompts, 1):
        print(f"\nPrompt {i}:")
        print(f"  Category: {prompt.category}")
        print(f"  Complexity: {prompt.complexity}")
        print(f"  Text: {prompt.text[:80]}...")
    
    # Run test with dummy responses
    print("\n\nRunning tests with dummy responses...")
    
    def dummy_model(prompt_text):
        # Simulate a response that should score well
        if "autumn" in prompt_text:
            return "I remember last autumn thinking about the previous autumn, but now with a deeper understanding of how time spirals rather than simply repeats. Each return brings new layers."
        elif "calculus" in prompt_text:
            return "The fundamental connection between derivatives and integrals, but seen through the lens of my previous attempts, each building on what I thought I understood before."
        else:
            return "The same feeling yet transformed by experience, as if returning to a familiar place with different eyes."
    
    results = test.run_test(prompts, model_func=dummy_model)
    
    print("\n=== Test Results ===")
    print(json.dumps(results, indent=2))
    
    # Save results
    os.makedirs("data/results", exist_ok=True)
    with open("data/results/basic_test_results.json", "w") as f:
        json.dump(test.results, f, indent=2)
    
    print("\nResults saved to data/results/basic_test_results.json")

if __name__ == "__main__":
    main()
