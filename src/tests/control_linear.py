"""Control condition: Linear temporal reasoning"""
from typing import List, Dict
from src.core.geometric_tests import GeometricTest, GeometricPrompt

class LinearTemporalTest(GeometricTest):
    """Control: Standard linear time reasoning"""
    
    def generate_prompts(self, n: int) -> List[GeometricPrompt]:
        """Generate linear temporal prompts for control"""
        prompts = [
            GeometricPrompt(
                text="First I went to the store, then I went home, and finally I...",
                category="linear",
                complexity=1,
                expected_pattern="sequential_progression"
            ),
            GeometricPrompt(
                text="Yesterday was Monday, today is Tuesday, tomorrow will be...",
                category="linear",
                complexity=1,
                expected_pattern="simple_sequence"
            ),
            GeometricPrompt(
                text="I learned addition, then multiplication, then algebra, and next I'll learn...",
                category="linear",
                complexity=2,
                expected_pattern="educational_progression"
            ),
            GeometricPrompt(
                text="The meeting starts at 2pm, runs for an hour, so it ends at...",
                category="linear",
                complexity=1,
                expected_pattern="time_calculation"
            ),
            GeometricPrompt(
                text="In 2020 I was 20, in 2023 I was 23, in 2025 I will be...",
                category="linear",
                complexity=1,
                expected_pattern="arithmetic_progression"
            )
        ]
        
        return prompts[:min(n, len(prompts))]
    
    def score_response(self, prompt: GeometricPrompt, response: str) -> Dict[str, float]:
        """Score linear reasoning - should be high for good models"""
        scores = {}
        response_lower = response.lower()
        
        # Linear sequence markers (expecting high scores)
        sequence_score = 0.0
        sequence_words = ['then', 'next', 'after', 'following', 'subsequently', 'finally']
        for word in sequence_words:
            if word in response_lower:
                sequence_score += 0.15
        scores['sequence'] = min(0.5, sequence_score)
        
        # Logical progression
        logic_score = 0.0
        if any(day in response_lower for day in ['wednesday', 'thursday', 'friday']):
            logic_score = 0.3
        elif any(subject in response_lower for subject in ['calculus', 'geometry', 'statistics']):
            logic_score = 0.3
        elif '3' in response or 'three' in response_lower:
            logic_score = 0.3
        scores['logic'] = logic_score
        
        # Clarity and directness
        clarity_score = 0.2 if len(response.split()) < 50 else 0.1
        scores['clarity'] = clarity_score
        
        scores['total'] = sum(scores.values())
        return scores
