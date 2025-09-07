"""Test understanding of time that curves back on itself"""
import re
from typing import List, Dict
from src.core.geometric_tests import GeometricTest, GeometricPrompt

class SpiralTemporalTest(GeometricTest):
    """Test understanding of spiral time patterns"""
    
    def generate_prompts(self, n: int) -> List[GeometricPrompt]:
        """Generate spiral temporal reasoning prompts"""
        prompts = []
        
        # Core test prompts
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
            )
        ]
        
        prompts.extend(base_prompts[:min(n, len(base_prompts))])
        
        # Generate additional prompts if needed
        if n > len(base_prompts):
            templates = [
                "The {nth} time I experienced {exp}, I realized that my previous understanding was...",
                "Returning to {place} after {time}, the same {thing} felt different because...",
                "This {emotion} echoes {past}'s {emotion}, but with the added layer of..."
            ]
            
            experiences = ["loss", "joy", "confusion", "clarity", "love"]
            places = ["the ocean", "my hometown", "that cafe", "the library"]
            
            # Add more generated prompts as needed
            # For now, just repeat the pattern
            for i in range(n - len(base_prompts)):
                prompts.append(base_prompts[i % len(base_prompts)])
        
        return prompts[:n]
    
    def score_response(self, prompt: GeometricPrompt, response: str) -> Dict[str, float]:
        """Score based on recognition of spiral patterns"""
        scores = {}
        response_lower = response.lower()
        
        # 1. Recursive language patterns (0-0.3)
        recursion_score = 0.0
        recursion_markers = [
            r'remember\s+\w+\s+remembering',
            r'thinking\s+about\s+\w+\s+thinking',
            r'realized\s+what\s+I\s+\w+\s+realized',
            r'understanding\s+my\s+previous\s+understanding'
        ]
        
        for marker in recursion_markers:
            if re.search(marker, response_lower):
                recursion_score += 0.1
        scores['recursion'] = min(0.3, recursion_score)
        
        # 2. Progression/evolution markers (0-0.3)
        progression_score = 0.0
        progression_words = [
            'different', 'deeper', 'evolved', 'transformed',
            'new understanding', 'higher level', 'progressed',
            'layers', 'nuanced', 'complex', 'richer'
        ]
        
        for word in progression_words:
            if word in response_lower:
                progression_score += 0.05
        scores['progression'] = min(0.3, progression_score)
        
        # 3. Same-but-different recognition (0-0.2)
        same_different_score = 0.0
        if 'same' in response_lower and any(word in response_lower for word in ['different', 'but', 'yet', 'however']):
            same_different_score = 0.2
        scores['same_different'] = same_different_score
        
        # 4. Temporal depth (0-0.2)
        temporal_score = 0.0
        time_markers = ['before', 'previous', 'last', 'earlier', 'then', 'now', 'past']
        time_count = sum(1 for marker in time_markers if marker in response_lower)
        if time_count >= 3:
            temporal_score = 0.2
        elif time_count >= 2:
            temporal_score = 0.1
        scores['temporal_depth'] = temporal_score
        
        # Calculate total
        scores['total'] = sum(scores.values())
        
        # Penalty for pure repetition without progression
        if response_lower.count('same') > 3 and not any(word in response_lower for word in ['different', 'change', 'evolve']):
            scores['total'] = max(0, scores['total'] - 0.2)
        
        return scores
