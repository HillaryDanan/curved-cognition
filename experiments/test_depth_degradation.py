#!/usr/bin/env python3
"""Test if performance degrades with recursion depth"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from src.models.multi_model_manager import MultiModelManager
import numpy as np

def test_depth():
    prompts_by_depth = {
        1: "I remember last week when...",
        2: "I remember last week remembering the previous week when...",
        3: "I remember last week remembering the previous week thinking about the week before when...",
        4: "I remember last week remembering the previous week thinking about the week before that, which reminded me of the week before that when...",
    }
    
    manager = MultiModelManager()
    
    print("RECURSION DEPTH DEGRADATION TEST")
    print("="*40)
    
    for model in ['gpt-3.5', 'haiku', 'gemini']:
        print(f"\n{model.upper()}:")
        for depth, prompt in prompts_by_depth.items():
            response = manager.generate(model, prompt)
            coherence = len(response.split()) / (50 * depth)  # Normalize by expected length
            print(f"  Depth {depth}: Coherence={coherence:.3f}")

if __name__ == "__main__":
    test_depth()
