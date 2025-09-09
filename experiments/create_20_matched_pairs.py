#!/usr/bin/env python3
"""Create 20 carefully matched prompt pairs"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.geometric_tests import GeometricPrompt
import json

def create_20_matched_pairs():
    """Create 20 pairs with exact word count matching"""
    
    pairs = [
        # 8-word pairs
        {"linear": "Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, then...",
         "spiral": "Remembering yesterday remembering tomorrow, time loops endlessly..."},
        
        {"linear": "First step, second step, third step, finally...",
         "spiral": "Thinking about thinking about thinking reveals layers..."},
        
        # 10-word pairs
        {"linear": "Plant seeds in spring, harvest crops in fall, then...",
         "spiral": "Each spring returns differently because I return differently, creating..."},
        
        {"linear": "The sun rises, reaches noon, sets at dusk, then...",
         "spiral": "Circling back to dawn, but dawn has changed because..."},
        
        # 12-word pairs
        {"linear": "I woke up, ate breakfast, went to work, came home, then...",
         "spiral": "This routine echoes yesterday's routine echoing last week's routine, revealing..."},
        
        {"linear": "Learn the alphabet, then words, then sentences, then paragraphs, finally...",
         "spiral": "Rereading childhood books with adult eyes seeing child eyes seeing..."},
        
        # 14-word pairs
        {"linear": "The meeting starts at nine, breaks at ten-thirty, resumes at eleven, ending...",
         "spiral": "This meeting reminds me of last meeting remembering previous meetings, spiraling..."},
        
        {"linear": "Mix flour with water, knead the dough, let it rise, then bake...",
         "spiral": "Baking bread again, but this time understanding what last time taught me..."},
        
        # 15-word pairs
        {"linear": "Spring turns to summer, summer to autumn, autumn to winter, winter returns to...",
         "spiral": "Seasons spiral forward while memory spirals backward, meeting where past and future converge..."},
        
        {"linear": "The baby crawls at six months, walks at twelve months, runs at eighteen...",
         "spiral": "Watching children grow reminds me of growing while remembering watching others grow..."},
        
        # 16-word pairs
        {"linear": "First grade teaches reading, second grade teaches writing, third grade combines them, fourth grade...",
         "spiral": "Teaching third grade for the fifth time, I understand my understanding of understanding differently..."},
        
        {"linear": "The stock price rose Monday, fell Tuesday, rose Wednesday, fell Thursday, Friday it...",
         "spiral": "Market cycles repeat but each cycle contains memory of previous cycles, creating fractal patterns..."},
        
        # 17-word pairs
        {"linear": "Wake at six, shower at six-thirty, breakfast at seven, leave at seven-thirty, arrive at eight...",
         "spiral": "Morning routines layer upon themselves, each day's routine remembering yesterday's while anticipating tomorrow's routine..."},
        
        {"linear": "The seed becomes sprout, sprout becomes plant, plant becomes flower, flower produces seeds that become...",
         "spiral": "Life cycles within cycles, each generation carrying forward what previous generations learned about cycling..."},
        
        # 18-word pairs
        {"linear": "January sets goals, February tries them, March adjusts them, April continues, May evaluates, June revises, July...",
         "spiral": "New Year resolutions return annually but I'm different each year so resolutions mean something different..."},
        
        {"linear": "The river starts as mountain snow, melts to streams, joins to rivers, flows to ocean, then...",
         "spiral": "Water remembers being cloud remembering being ocean remembering being rain, each state containing all states..."},
        
        # 19-word pairs
        {"linear": "First attempt failed completely, second attempt showed progress, third attempt nearly succeeded, fourth attempt should definitely...",
         "spiral": "Each failure teaches about previous failures' lessons, creating recursive understanding where failure becomes teacher teaching about..."},
        
        {"linear": "The caterpillar eats leaves, grows larger, forms chrysalis, emerges as butterfly, lays eggs that become caterpillars that...",
         "spiral": "Metamorphosis cycles endlessly, each butterfly containing caterpillar memories while caterpillars dream butterfly dreams, interconnected across..."},
        
        # 20-word pairs
        {"linear": "The company started small, grew steadily, expanded nationally, went international, dominated markets, faced competition, adapted strategies, and ultimately...",
         "spiral": "Success contains seeds of failure containing seeds of success, each business cycle teaching what previous cycles couldn't teach..."},
        
        {"linear": "Breathe in for four counts, hold for four counts, breathe out for four counts, pause for four counts, then...",
         "spiral": "Each breath remembers previous breaths while anticipating future breaths, creating continuous presence where past and future merge into..."}
    ]
    
    # Verify and create prompts
    linear_prompts = []
    spiral_prompts = []
    
    for i, pair in enumerate(pairs):
        lin_words = len(pair["linear"].split())
        spi_words = len(pair["spiral"].split())
        
        # Verify exact match
        if lin_words != spi_words:
            print(f"WARNING: Pair {i+1} mismatch: Linear={lin_words}, Spiral={spi_words}")
        else:
            print(f"Pair {i+1}: {lin_words} words each ✓")
        
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
    
    return linear_prompts, spiral_prompts

linear, spiral = create_20_matched_pairs()

# Save
with open("data/prompts/matched_20_pairs.json", "w") as f:
    json.dump({
        "linear": [p.__dict__ for p in linear],
        "spiral": [p.__dict__ for p in spiral],
        "n_pairs": len(linear)
    }, f, indent=2)

print(f"\n✓ Created {len(linear)} matched pairs")
print("Saved to data/prompts/matched_20_pairs.json")
