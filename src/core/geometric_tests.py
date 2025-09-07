"""Base classes for curved cognition testing"""
import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime
import json

@dataclass
class GeometricPrompt:
    """Single test prompt with metadata"""
    text: str
    category: str  # spiral, cyclical, orbital, fractal, recursive
    complexity: int  # 1-5 scale
    expected_pattern: str  # what we're looking for
    prompt_id: str = None
    
    def __post_init__(self):
        if not self.prompt_id:
            self.prompt_id = f"{self.category}_{datetime.now().timestamp()}"

class GeometricTest(ABC):
    """Base class for all curved cognition tests"""
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name
        self.results = []
        
    @abstractmethod
    def generate_prompts(self, n: int) -> List[GeometricPrompt]:
        """Generate test prompts for this pattern type"""
        pass
        
    @abstractmethod
    def score_response(self, prompt: GeometricPrompt, response: str) -> Dict[str, float]:
        """Score how well response captures curved pattern"""
        pass
        
    def run_test(self, prompts: List[GeometricPrompt], model_func=None) -> Dict:
        """Run complete test battery"""
        test_results = []
        
        for prompt in prompts:
            # Use provided model function or dummy response for testing
            if model_func:
                response = model_func(prompt.text)
            else:
                response = f"Test response for: {prompt.text[:50]}..."
            
            scores = self.score_response(prompt, response)
            
            result = {
                'prompt': prompt.__dict__,
                'response': response,
                'scores': scores,
                'model': self.model_name,
                'timestamp': datetime.now().isoformat()
            }
            
            test_results.append(result)
            self.results.append(result)
            
        return self.analyze_results(test_results)
    
    def analyze_results(self, results: List[Dict]) -> Dict:
        """Analyze test results"""
        if not results:
            return {'error': 'No results to analyze'}
            
        # Calculate aggregate scores
        all_scores = []
        for r in results:
            if 'scores' in r and 'total' in r['scores']:
                all_scores.append(r['scores']['total'])
        
        if all_scores:
            return {
                'mean_score': np.mean(all_scores),
                'std_score': np.std(all_scores),
                'min_score': np.min(all_scores),
                'max_score': np.max(all_scores),
                'n_tests': len(all_scores),
                'model': self.model_name
            }
        return {'error': 'No valid scores found'}
