# Curved Cognition

Testing the geometric mismatch between biological cognition (curves, spirals, cycles) and artificial intelligence architectures (rectangular matrices).

## Core Hypothesis

Biological minds operate in curved geometries - neural dendrites branch fractally, memories reconsolidate in spirals, emotions orbit and return transformed. Yet we model intelligence using rectangular attention matrices and linear position encodings. This fundamental geometric mismatch may explain specific limitations in current AI systems' ability to understand temporal recursion, cyclical causality, and embodied reasoning.

## Research Questions

1. Do language models show systematic degradation when processing spiral/recursive temporal patterns?
2. Can models distinguish cyclical causation from linear sequences?
3. Do different architectures (GPT, Claude, Gemini, BERT) show different geometric biases?
4. Can geometric priming improve performance on curved reasoning tasks?

## Key Findings (In Progress)

- Baseline experiments establishing linear reasoning performance across models
- Spiral temporal degradation tests showing performance decline with recursive depth
- Orbital return pattern recognition comparing "same-but-different" understanding
- Fractal nesting tests for scale-invariant pattern recognition

## Repository Structure

```
curved-cognition/
├── src/               # Core testing framework
├── experiments/       # Systematic experiments
├── notebooks/         # Interactive analysis
├── data/             # Prompts, results, analysis
└── docs/             # Theory and documentation
```

## Related Research

This work builds on several interconnected frameworks:

### Foundational Frameworks
- [**Multi-Geometric Attention**](https://github.com/HillaryDanan/multi-geometric-attention) - Proposes that different cognitive operations require different geometric bases (square, hexagonal, triangular, etc.)
- [**TIDE**](https://github.com/HillaryDanan/TIDE) (Temporal-Internal Dimensional Encoding) - Framework for how different minds organize temporal and self-referential information

### Embodiment & Causality Studies
- [**Embodied Cognition**](https://github.com/HillaryDanan/embodied-cognition) - Testing whether genuine temporal-causal reasoning requires physical embodiment
- [**Causal Attention Geometry**](https://github.com/HillaryDanan/causal-attention-geometry) - How attention patterns reveal causal understanding
- [**Retroactive Causality**](https://github.com/HillaryDanan/retroactive-causality) - Architecture-dependent causal reasoning patterns in transformers

### Pattern & Learning Dynamics
- [**Ouroboros Learning**](https://github.com/HillaryDanan/ouroboros-learning) - Self-consuming cycles in knowledge evolution
- [**Relativistic Interpretability**](https://github.com/HillaryDanan/relativistic-interpretability) - Frame-dependent understanding in AI systems

## Installation

```bash
# Clone repository
git clone https://github.com/HillaryDanan/curved-cognition.git
cd curved-cognition

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up API keys (see docs/api_setup.md)
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"
export GOOGLE_API_KEY="your-key"
```

## Quick Start

```python
# Run baseline linear reasoning test
python experiments/01_baseline_rectangular.py

# Test spiral temporal degradation
python experiments/02_spiral_degradation.py

# Visualize results
jupyter notebook notebooks/explore_results.ipynb
```

## Test Categories

### 1. Spiral Temporal Reasoning
Tests understanding of recursive time patterns:
- "Every spring I think about last spring thinking about..."
- "The third time I learned this, I understood what I missed..."

### 2. Cyclical Causality
Tests feedback loop comprehension:
- "Stress causes insomnia which causes stress..."
- "The economy affects mood affects productivity affects economy..."

### 3. Orbital Returns
Tests "same-but-different" recognition:
- "I'm sad again, but differently than last time..."
- "We're having the same argument at a new level..."

### 4. Fractal Nesting
Tests scale-invariant pattern recognition:
- "Daily patterns mirror weekly mirror yearly..."
- "Cell division, organism growth, population expansion all..."

### 5. Recursive Self-Reference
Tests consciousness examining itself:
- "Thinking about thinking about thinking..."
- "This sentence describes itself describing..."

## Theoretical Foundation

This research connects embodied cognition theory with AI interpretability. Key citations:

- Grid cells use hexagonal (not rectangular) organization (Hafting et al., 2005)
- Neural dendrites branch in fractal patterns (Cuntz et al., 2010)
- Trauma disrupts temporal continuity into fragments (van der Kolk, 2014)
- Current transformers use rectangular attention matrices (Vaswani et al., 2017)

## Contributing

This is open research. Contributions welcome:
- Additional test prompts exploring curved patterns
- Analysis of results across different models
- Theoretical extensions to non-Euclidean attention mechanisms
- Visualizations of geometric reasoning patterns

## Methodology

All tests follow rigorous protocols:
- Multiple runs per prompt (n=10) for statistical stability
- Control conditions comparing curved vs linear versions
- Paired statistical tests for model comparisons
- Effect size reporting beyond significance

## Current Status

- ✅ Theoretical framework established
- ✅ Test battery designed
- ✅ API integration for multiple models
- 🔄 Baseline experiments running
- 📊 Initial results being analyzed
- 📝 Paper in preparation

## Author

Hillary Danan - PhD Cognitive Neuroscience, Independent AI Researcher

Exploring consciousness at the intersection of neuroscience and artificial intelligence. This work examines whether rectangular matrices can truly capture minds that think in spirals.

## License

MIT License - Open science for open minds

## Citation

If you use this framework:
```
@software{danan2025curved,
  author = {Danan, Hillary},
  title = {Curved Cognition: Testing Geometric Mismatches in AI},
  year = {2025},
  url = {https://github.com/HillaryDanan/curved-cognition}
}
```

---

*"Because the world is round, it turns me on"* - The Beatles understood that consciousness operates in curves, not lines.
