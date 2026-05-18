"""Filter arXiv papers based on user interests."""

INTERESTS = {
    "architectures": {
        "keywords": [
            "mamba", "state-space", "alternative architecture", "beyond transformer",
            "jepa", "world model", "diffusion language", "recurrent neural",
            "hybrid architecture", "ssm", "structured state space",
            "attention alternative", "non-transformer"
        ],
        "weight": 1.0
    },
    "hardware": {
        "keywords": [
            "gpu", "tpu", "neuromorphic", "photonic", "quantum computing",
            "custom silicon", "cerebras", "groq", "hardware accelerator",
            "analog compute", "in-memory", "thermodynamic", "extropic",
            "compute substrate", "specialized hardware", "ai silicon"
        ],
        "weight": 0.9
    },
    "scaling": {
        "keywords": [
            "scaling laws", "scaling frontier", "compute optimal", "llm scaling",
            "emergent abilities", "frontier models", "large language model",
            "parameter efficiency", "sample efficiency", "data scaling",
            "training efficiency", "model scaling", "capacity limits"
        ],
        "weight": 0.85
    },
    "reasoning_structure": {
        "keywords": [
            "reasoning", "planning", "symbolic", "neuro-symbolic", "causal",
            "compositional", "generalization", "out-of-distribution",
            "next-token prediction", "structured reasoning",
            "formal reasoning", "rule-based", "inductive bias"
        ],
        "weight": 0.85
    },
    "scientific_ai": {
        "keywords": [
            "protein folding", "drug discovery", "biology", "physics",
            "scientific discovery", "neural surrogate", "simulation",
            "formal proof", "theorem proving", "mathematics",
            "molecular dynamics", "materials discovery", "scientific computing"
        ],
        "weight": 0.8
    },
    "alignment_training": {
        "keywords": [
            "rlhf", "rlaif", "alignment", "constitutional", "training",
            "preference", "fine-tuning", "instruction", "post-training",
            "safety", "interpretability", "mechanistic interpretation"
        ],
        "weight": 0.75
    }
}

NEGATIVE_KEYWORDS = [
    "prompt engineering", "prompt injection", "few-shot prompting",
    "benchmark", "leaderboard", "evaluation dataset",
    "fine-tuning", "lora", "adapters",
    "application", "product", "deployment",
    "chatbot", "assistant", "qa system",
    "tutorial", "survey only", "review only",
    "api", "web service", "api call"
]


def score_paper(title: str, abstract: str, categories: str = "") -> float:
    """Score a paper based on relevance to user interests.

    Returns a score from 0 to 1, where higher is more relevant.
    """
    text = f"{title} {abstract} {categories}".lower()

    total_score = 0.0
    max_possible_score = 0.0

    # Check positive keywords
    for category, config in INTERESTS.items():
        category_score = 0.0
        for keyword in config["keywords"]:
            if keyword in text:
                category_score = max(category_score, 1.0)

        weighted_score = category_score * config["weight"]
        total_score += weighted_score
        max_possible_score += config["weight"]

    # Penalize if matches negative keywords
    negative_penalty = 0.0
    for neg_keyword in NEGATIVE_KEYWORDS:
        if neg_keyword in text:
            negative_penalty += 0.15

    negative_penalty = min(negative_penalty, 1.0)

    # Normalize score
    if max_possible_score > 0:
        normalized_score = total_score / max_possible_score
    else:
        normalized_score = 0.0

    final_score = max(0, normalized_score - negative_penalty)
    return final_score


def is_relevant(title: str, abstract: str, categories: str = "", threshold: float = 0.3) -> bool:
    """Determine if a paper is relevant based on score threshold."""
    return score_paper(title, abstract, categories) >= threshold
