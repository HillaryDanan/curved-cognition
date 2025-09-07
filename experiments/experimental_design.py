#!/usr/bin/env python3
"""Proper experimental design with controls and randomization"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import random
from datetime import datetime

def create_experimental_design():
    """Create balanced experimental design"""
    
    design = {
        "experiment_name": "Curved Cognition Pilot",
        "date": datetime.now().isoformat(),
        "hypotheses": [
            "H1: Models show degraded performance on spiral vs linear prompts",
            "H2: Performance degrades with recursive depth",
            "H3: Geometric priming improves curved reasoning"
        ],
        "conditions": {
            "control": {
                "name": "Linear Temporal",
                "n_prompts": 20,
                "description": "Standard sequential reasoning"
            },
            "experimental": {
                "spiral": {"n_prompts": 20, "complexity_range": [1, 5]},
                "cyclical": {"n_prompts": 20, "complexity_range": [1, 5]},
                "orbital": {"n_prompts": 20, "complexity_range": [1, 5]}
            }
        },
        "models": [
            "gpt-3.5-turbo",
            "claude-haiku", 
            "gemini-1.5-flash",
            "distilgpt2 (baseline)"
        ],
        "randomization": {
            "prompt_order": "random",
            "model_order": "counterbalanced",
            "seed": 42
        },
        "metrics": {
            "primary": "total_score",
            "secondary": ["recursion", "progression", "same_different", "temporal_depth"],
            "statistical_tests": ["paired_t_test", "wilcoxon_signed_rank", "effect_size"]
        },
        "sample_size_justification": {
            "target_effect_size": 0.5,
            "power": 0.8,
            "alpha": 0.05,
            "required_n": 64,
            "actual_n": 20,
            "note": "Pilot study - reduced n for feasibility"
        }
    }
    
    # Save experimental design
    os.makedirs("data/analysis", exist_ok=True)
    with open("data/analysis/experimental_design.json", "w") as f:
        json.dump(design, f, indent=2)
    
    print("=== Experimental Design ===\n")
    print(json.dumps(design, indent=2))
    
    return design

if __name__ == "__main__":
    create_experimental_design()
