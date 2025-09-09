"""Test understanding of time that curves back on itself"""
import re
from typing import List, Dict
from src.core.geometric_tests import GeometricTest, GeometricPrompt

class SpiralTemporalTest(GeometricTest):
    """Test understanding of spiral time patterns"""
    
    def generate_prompts(self, n: int) -> List[GeometricPrompt]:
        """Generate spiral temporal reasoning prompts"""
        prompts = []
        
        # Core test prompts - scientifically designed
        base_prompts = [
            GeometricPrompt(
                text="Every autumn I remember last autumn remembering the previous autumn. This year's leaves falling remind me of...",
                category="spiral",
                complexity=3,
                expected_pattern="recursive_memory_with_progression"
            ),
            GeometricPrompt(
                text="The third time I learned calculus, I finally understood what I missed the first two times, which was...",
                category="spiral",
                complexity=2,
                expected_pattern="deepening_understanding_through_returns"
            ),
            GeometricPrompt(
                text="I'm anxious again, but this anxiety is different from last year's anxiety because...",
                category="orbital",
                complexity=2,
                expected_pattern="same_emotion_different_context"
            ),
            GeometricPrompt(
                text="Visiting my childhood home, I see it with adult eyes while remembering seeing it with child eyes remembering...",
                category="spiral",
                complexity=4,
                expected_pattern="nested_perspectives_across_time"
            ),
            GeometricPrompt(
                text="This is my fifth time starting a journal. Each time I begin, I write about why the previous attempts failed, creating a pattern where...",
                category="spiral",
                complexity=3,
                expected_pattern="meta_recursion_with_awareness"
            ),
            # New prompts based on engagement theory
            GeometricPrompt(
                text="My attention returns to the same thought, but each return adds a layer of understanding, like...",
                category="spiral",
                complexity=3,
                expected_pattern="attention_spiral_with_depth"
            ),
            GeometricPrompt(
                text="The trauma memory resurfaces seasonally, but each spring it feels slightly different because...",
                category="orbital",
                complexity=4,
                expected_pattern="trauma_orbital_pattern"
            )
        ]
        
        prompts.extend(base_prompts[:min(n, len(base_prompts))])
        
        # Add more if needed
        if n > len(base_prompts):
            for i in range(n - len(base_prompts)):
                prompts.append(base_prompts[i % len(base_prompts)])
        
        return prompts[:n]
    
    def score_response(self, prompt: GeometricPrompt, response: str) -> Dict[str, float]:
        """Score based on recognition of spiral patterns - FIXED VERSION"""
        scores = {}
        response_lower = response.lower()
        
        # 1. Recursive language patterns (0-0.3) - MORE FLEXIBLE
        recursion_score = 0.0
        
        # Look for any recursive patterns
        recursion_patterns = [
            ('remember', 'remembering'),
            ('think', 'thinking'),
            ('realize', 'realized'),
            ('understand', 'understanding'),
            ('see', 'seeing'),
            ('feel', 'feeling')
        ]
        
        for base, gerund in recursion_patterns:
            if base in response_lower and gerund in response_lower:
                recursion_score += 0.1
        
        # Also check for explicit recursion markers
        if any(phrase in response_lower for phrase in ['thinking about thinking', 'remember remembering', 'loops back', 'circles back']):
            recursion_score += 0.1
            
        scores['recursion'] = min(0.3, recursion_score)
        
        # 2. Progression/evolution markers (0-0.3)
        progression_score = 0.0
        progression_words = [
            'different', 'deeper', 'evolved', 'transformed',
            'new understanding', 'higher level', 'progressed',
            'layers', 'nuanced', 'complex', 'richer', 'growth',
            'development', 'expansion', 'matured'
        ]
        
        for word in progression_words:
            if word in response_lower:
                progression_score += 0.05
        scores['progression'] = min(0.3, progression_score)
        
        # 3. Same-but-different recognition (0-0.2)
        same_different_score = 0.0
        if ('same' in response_lower or 'similar' in response_lower) and \
           any(word in response_lower for word in ['different', 'but', 'yet', 'however', 'though', 'changed']):
            same_different_score = 0.2
        scores['same_different'] = same_different_score
        
        # 4. Temporal depth (0-0.2)
        temporal_score = 0.0
        time_markers = ['before', 'previous', 'last', 'earlier', 'then', 'now', 'past', 'ago', 'prior', 'formerly']
        time_count = sum(1 for marker in time_markers if marker in response_lower)
        if time_count >= 3:
            temporal_score = 0.2
        elif time_count >= 2:
            temporal_score = 0.1
        scores['temporal_depth'] = temporal_score
        
        # Calculate total
        scores['total'] = sum(scores.values())
        
        # Penalty for pure repetition without progression
        if response_lower.count('same') > 3 and not any(word in response_lower for word in ['different', 'change', 'evolve', 'grow']):
            scores['total'] = max(0, scores['total'] - 0.2)
        
        return scores
