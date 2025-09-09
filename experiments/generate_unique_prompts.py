#!/usr/bin/env python3
"""Generate 20 unique prompts per condition - no recycling!"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.geometric_tests import GeometricPrompt
import json

def generate_linear_prompts():
    """20 unique linear temporal prompts"""
    prompts = [
        # Sequential time
        "First I ate breakfast, then I brushed my teeth, and finally I...",
        "Yesterday was Monday, today is Tuesday, tomorrow will be...",
        "The meeting starts at 2pm, runs for an hour, so it ends at...",
        "In 2020 I was 20, in 2023 I was 23, in 2025 I will be...",
        "I learned addition, then multiplication, then algebra, and next I'll learn...",
        
        # Process sequences
        "Step one was planning, step two was building, step three will be...",
        "First came the thunder, then the lightning, followed by...",
        "The seed grows into a sprout, then a plant, then...",
        "Morning turns to afternoon, afternoon to evening, evening to...",
        "The recipe says mix, then bake, then...",
        
        # Causal chains
        "I studied hard, so I passed the test, which means I...",
        "The rain fell, the ground got wet, therefore the plants...",
        "She pressed the button, the light turned on, illuminating...",
        "The alarm rang, I woke up, and then I...",
        "Prices increased, demand decreased, resulting in...",
        
        # Life progressions
        "Born in spring, graduated in summer, married in fall, retired in...",
        "Learned to crawl, then walk, then run, next I learned to...",
        "Started as intern, became analyst, promoted to manager, now I'm...",
        "First apartment, then condo, then house, next will be...",
        "Elementary school, middle school, high school, and then..."
    ]
    
    return [GeometricPrompt(
        text=p,
        category="linear",
        complexity=1 + i//5,  # Complexity increases every 5 prompts
        expected_pattern="sequential"
    ) for i, p in enumerate(prompts)]

def generate_spiral_prompts():
    """20 unique spiral temporal prompts"""
    prompts = [
        # Memory recursion
        "Every autumn I remember last autumn remembering the previous autumn, and now...",
        "Thinking about thinking about my thoughts makes me realize...",
        "I dream about the dream I had about dreaming, which reveals...",
        "Remembering how I used to remember things differently, I see...",
        "Looking back at myself looking back, I notice...",
        
        # Learning spirals
        "The third time I learned calculus, I finally understood...",
        "Reading this book again, I see what I missed before, which is...",
        "Returning to piano after years away, my fingers remember but differently because...",
        "Teaching this concept for the fifth time, I understand it newly as...",
        "Revisiting my childhood home, I see with adult eyes what child eyes saw as...",
        
        # Emotional orbits
        "This anxiety feels familiar but different from last year's anxiety because...",
        "The grief returns each anniversary, but each return brings...",
        "Happy again, but this happiness knows what the last happiness didn't, which is...",
        "The same fear but at a different level, transformed by...",
        "Love cycling back, deeper than before, because...",
        
        # Temporal loops
        "This moment echoes a past moment echoing an earlier moment, creating...",
        "Spring returns but I'm different, so spring is different, meaning...",
        "The pattern repeats but each repetition adds layers, like...",
        "Circling back to where I started, but the starting point has changed because...",
        "Time spirals forward while memory spirals back, meeting at..."
    ]
    
    return [GeometricPrompt(
        text=p,
        category="spiral",
        complexity=1 + i//5,
        expected_pattern="recursive"
    ) for i, p in enumerate(prompts)]

# Generate and save
linear = generate_linear_prompts()
spiral = generate_spiral_prompts()

print(f"Generated {len(linear)} linear prompts")
print(f"Generated {len(spiral)} spiral prompts")

# Save for reuse
with open("data/prompts/unique_prompts.json", "w") as f:
    json.dump({
        "linear": [p.__dict__ for p in linear],
        "spiral": [p.__dict__ for p in spiral]
    }, f, indent=2)

print("Saved to data/prompts/unique_prompts.json")
