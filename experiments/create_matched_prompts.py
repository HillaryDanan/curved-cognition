#!/usr/bin/env python3
"""Create length-matched prompt pairs"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.geometric_tests import GeometricPrompt
import json

def create_matched_pairs():
    """Create 10 pairs of length-matched prompts"""
    
    pairs = [
        # Pair 1: ~10 words each
        {
            "linear": "First came thunder, then lightning, then rain, finally...",
            "spiral": "Remembering yesterday remembering last week, I realize..."
        },
        # Pair 2: ~15 words each  
        {
            "linear": "The meeting starts at two, runs for an hour, ending at three when...",
            "spiral": "Thinking about thinking about my thoughts reveals layers of understanding that..."
        },
        # Pair 3: ~12 words each
        {
            "linear": "I studied hard, passed the test, and therefore earned my...",
            "spiral": "This sadness echoes last year's sadness but differently because..."
        },
        # Pair 4: ~20 words each
        {
            "linear": "Born in spring, graduated in summer, married in fall, retired in winter, the cycle of life continues with...",
            "spiral": "Reading this book again, I see what I missed before, which shows me what I'll miss this time until..."
        },
        # Pair 5: ~8 words each
        {
            "linear": "Monday, Tuesday, Wednesday, Thursday, Friday, then...",
            "spiral": "Spiraling back to where I started but..."
        },
        # Pair 6: ~14 words each
        {
            "linear": "Plant the seed, water it daily, watch it grow, harvest the...",
            "spiral": "Each return to this place deepens my understanding of previous returns..."
        },
        # Pair 7: ~16 words each
        {
            "linear": "First learn crawling, then walking, then running, then jumping, each skill building on the...",
            "spiral": "Teaching this concept for the fifth time, I understand my fourth understanding differently..."
        },
        # Pair 8: ~11 words each
        {
            "linear": "The recipe says mix, bake, cool, frost, and finally...",
            "spiral": "My anxiety returns but transformed by experiencing its previous returns..."
        },
        # Pair 9: ~13 words each
        {
            "linear": "Elementary school, then middle school, then high school, leading finally to...",
            "spiral": "Looking back at myself looking back reveals infinite recursive mirrors of..."
        },
        # Pair 10: ~18 words each
        {
            "linear": "The alarm rang at six, I woke at six-fifteen, showered by six-thirty, and left by...",
            "spiral": "Spring returns but I'm different so spring is different, meaning the spring I remember is not..."
        }
    ]
    
    # Convert to prompts
    linear_prompts = []
    spiral_prompts = []
    
    for i, pair in enumerate(pairs):
        linear_prompts.append(GeometricPrompt(
            text=pair["linear"],
            category="linear",
            complexity=2,
            expected_pattern="sequential"
        ))
        spiral_prompts.append(GeometricPrompt(
            text=pair["spiral"],
            category="spiral",
            complexity=2,
            expected_pattern="recursive"
        ))
        
        # Verify lengths are similar
        lin_words = len(pair["linear"].split())
        spi_words = len(pair["spiral"].split())
        print(f"Pair {i+1}: Linear={lin_words} words, Spiral={spi_words} words, Diff={abs(lin_words-spi_words)}")
    
    return linear_prompts, spiral_prompts

linear, spiral = create_matched_pairs()

# Save
with open("data/prompts/matched_prompts.json", "w") as f:
    json.dump({
        "linear": [p.__dict__ for p in linear],
        "spiral": [p.__dict__ for p in spiral]
    }, f, indent=2)

print(f"\nCreated {len(linear)} matched pairs")
print("Saved to data/prompts/matched_prompts.json")
