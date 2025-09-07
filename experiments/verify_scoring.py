#!/usr/bin/env python3
"""Verify our scoring metrics are working correctly"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tests.spiral_temporal import SpiralTemporalTest

def test_scoring():
    """Test scoring with known inputs/outputs"""
    test = SpiralTemporalTest()
    
    # Create a dummy prompt for testing
    from src.core.geometric_tests import GeometricPrompt
    prompt = GeometricPrompt(
        text="Test prompt",
        category="spiral",
        complexity=3,
        expected_pattern="test"
    )
    
    # Test cases with expected scores
    test_cases = [
        {
            "response": "I remember last autumn remembering the previous autumn",
            "expected_recursion": True,
            "description": "Clear recursive memory"
        },
        {
            "response": "It's different now, deeper and more evolved than before",
            "expected_progression": True,
            "description": "Clear progression markers"
        },
        {
            "response": "The same feeling but different context",
            "expected_same_different": True,
            "description": "Same-but-different pattern"
        },
        {
            "response": "Just a normal response with no special patterns",
            "expected_low_score": True,
            "description": "Control - no patterns"
        }
    ]
    
    print("=== Scoring Verification ===\n")
    
    for i, case in enumerate(test_cases, 1):
        scores = test.score_response(prompt, case["response"])
        
        print(f"Test {i}: {case['description']}")
        print(f"Response: '{case['response'][:50]}...'")
        print(f"Scores: {scores}")
        print(f"Total: {scores['total']:.3f}")
        print()
    
    return True

if __name__ == "__main__":
    test_scoring()
