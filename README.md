# Curved Cognition: Geometric Constraints in LLM Temporal Reasoning

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)

## 🌀 Key Discovery

**Transformer-based language models demonstrate significantly impaired performance on recursive temporal reasoning compared to linear temporal reasoning** - a finding that suggests fundamental geometric constraints in current AI architectures.

## 📊 Results at a Glance

| Model | Effect Size (Cohen's d) | p-value | Statistical Power |
|-------|------------------------|---------|-------------------|
| GPT-3.5 | 0.764 | 0.043* | 92.7% |
| Claude-3.5-Haiku | 1.710 | <0.001*** | 100% |
| GPT-4 | 0.816 | 0.035* | 95.4% |

**All effects measured with length-matched prompts (n=20 pairs)**

### Depth Degradation

Performance degrades monotonically with recursion depth:
- 1 level: ~100% coherence
- 2 levels: ~45% coherence  
- 3 levels: ~35% coherence
- 4 levels: ~20% coherence

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/HillaryDanan/curved-cognition.git
cd curved-cognition

# Install dependencies
pip install -r requirements.txt

# Set up API keys (create .env file)
echo "OPENAI_API_KEY=your-key-here" > .env
echo "ANTHROPIC_API_KEY=your-key-here" >> .env
```

### Run Basic Test

```bash
# Test framework with dummy models (no API needed)
python3 experiments/run_basic_test.py

# Test with real models (requires API keys)
python3 experiments/test_matched_prompts.py
```

### Reproduce Full Results

```bash
# Run complete analysis with 20 matched pairs
python3 experiments/final_matched_test_fixed.py

# Test depth degradation
python3 experiments/test_depth_degradation.py
```

## 📁 Repository Structure

```
curved-cognition/
├── docs/                      # Papers and theory
│   ├── journal_paper.md      # Full research paper
│   ├── theory.md             # Theoretical framework
│   ├── engagement_theory.md  # Attention and consciousness theory
│   └── trauma_embodiment.md  # Embodied cognition background
│
├── src/                       # Core framework
│   ├── core/                 # Base test classes
│   │   └── geometric_tests.py
│   ├── tests/                # Specific test implementations
│   │   ├── spiral_temporal.py
│   │   └── control_linear.py
│   └── models/               # API management
│       ├── api_manager.py
│       └── multi_model_manager.py
│
├── experiments/              # Experimental scripts
│   ├── run_basic_test.py    # Framework validation
│   ├── test_matched_prompts.py # Length-controlled test
│   ├── final_matched_test_fixed.py # Full analysis
│   └── test_depth_degradation.py # Recursion depth analysis
│
├── data/                     # Data and results
│   ├── prompts/             # Test prompts
│   │   ├── unique_prompts.json
│   │   └── matched_20_pairs.json
│   └── results/             # Experimental results
│       └── *.json
│
└── requirements.txt         # Python dependencies
```

## 🔬 Methodology

### Prompt Types

**Linear Temporal** (Sequential reasoning):
```
"First I went to the store, then I went home, and finally I..."
```

**Spiral Temporal** (Recursive reasoning):
```
"Every autumn I remember last autumn remembering the previous autumn..."
```

### Scoring Framework

Responses evaluated on four dimensions:
1. **Recursion Recognition** (0-0.3)
2. **Progression Markers** (0-0.3)
3. **Same-but-Different Patterns** (0-0.2)
4. **Temporal Depth** (0-0.2)

### Statistical Analysis

- Paired t-tests for matched samples
- Cohen's d for effect sizes
- Post-hoc power analysis
- Bonferroni correction for multiple comparisons

## 📈 Key Findings

1. **Universal Effect**: All tested models show impaired recursive reasoning
2. **Large Effect Sizes**: Cohen's d ranging from 0.76 to 1.71
3. **Robust to Controls**: Effect persists with length-matched prompts
4. **Depth Degradation**: Performance decreases systematically with recursion depth

## 💡 Theoretical Implications

This research suggests that:
- Transformer attention matrices impose geometric constraints on reasoning
- Current positional encodings cannot represent curved temporal paths
- Achieving AGI may require architectures beyond rectangular matrices

## 📝 Citation

If you use this work, please cite:

```bibtex
@article{danan2025curved,
  title={Geometric Constraints in Transformer-Based Language Models: Evidence for Impaired Recursive Temporal Reasoning},
  author={Danan, Hillary and Claude},
  year={2025},
  url={https://github.com/HillaryDanan/curved-cognition}
}
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Run tests with your changes
4. Submit a pull request

## 📜 License

MIT License - see [LICENSE](LICENSE) file

## 👤 Author

**Hillary Danan**  
ORCID: [0009-0005-5963-9807](https://orcid.org/0009-0005-5963-9807)

## 🙏 Acknowledgments

- Claude (Anthropic) for collaboration on theoretical framework and analysis
- Open source community for making this research possible
- Panera Bread for the optimal research environment

## 📊 Raw Data

All experimental data available in `data/results/`. Key files:
- `final_matched_20250909_*.json` - Main results with matched prompts
- `multimodel_*.json` - Cross-model comparisons
- `gpt35_scaled_*.json` - Full-scale GPT-3.5 analysis

## 🔗 Related Work

See [`docs/theory.md`](docs/theory.md) for theoretical background and [`docs/journal_paper.md`](docs/journal_paper.md) for the complete research paper.

---

*"Because the world is round, it turns me on"* - The Beatles understood that consciousness operates in curves, not lines. 🌀
