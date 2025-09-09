# ... existing code ...
def score_response(self, prompt: GeometricPrompt, response: str) -> Dict[str, float]:
    scores = {}
    response_lower = response.lower()
    
    # ... other scoring ...
    
    # FIX: Variable clarity based on actual response length
    word_count = len(response.split())
    if word_count < 20:
        clarity_score = 0.25
    elif word_count < 40:
        clarity_score = 0.20  
    elif word_count < 60:
        clarity_score = 0.15
    else:
        clarity_score = 0.10
    scores['clarity'] = clarity_score
    
    scores['total'] = sum(scores.values())
    return scores
