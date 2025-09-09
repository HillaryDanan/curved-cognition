#!/usr/bin/env python3
"""Check if spiral prompts are just more complex"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tests.spiral_temporal import SpiralTemporalTest
from src.tests.control_linear import LinearTemporalTest

linear_test = LinearTemporalTest()
spiral_test = SpiralTemporalTest()

linear_prompts = linear_test.generate_prompts(5)
spiral_prompts = spiral_test.generate_prompts(7)

print("COMPLEXITY ANALYSIS")
print("="*40)

# Word count
linear_words = [len(p.text.split()) for p in linear_prompts]
spiral_words = [len(p.text.split()) for p in spiral_prompts]

print(f"\nWord count:")
print(f"Linear: M={sum(linear_words)/len(linear_words):.1f} words")
print(f"Spiral: M={sum(spiral_words)/len(spiral_words):.1f} words")

# Sentence complexity (commas, subclauses)
linear_commas = [p.text.count(',') for p in linear_prompts]
spiral_commas = [p.text.count(',') for p in spiral_prompts]

print(f"\nSubclauses (commas):")
print(f"Linear: M={sum(linear_commas)/len(linear_commas):.1f}")
print(f"Spiral: M={sum(spiral_commas)/len(spiral_commas):.1f}")

# Print examples
print("\n" + "="*40)
print("EXAMPLE PROMPTS")
print("="*40)
print("\nLinear example:")
print(f'"{linear_prompts[0].text}"')
print("\nSpiral example:")
print(f'"{spiral_prompts[0].text}"')
