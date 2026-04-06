"""
Confidence score utilities and helpers.

Functions for normalizing, combining, and interpreting confidence scores.
"""

from typing import List


def normalize_confidence(score: float | int) -> float:
    """
    Normalize a confidence score to 0-1 range.
    
    Accepts confidence scores from various sources (percentages, decimals)
    and normalizes them to 0-1 range.
    
    Args:
        score: Raw confidence score or percentage
    
    Returns:
        float: Normalized confidence score (0.0-1.0)
    
    Raises:
        ValueError: If score is outside expected range after processing
    """
    score = float(score)
    
    # If score is in percentage range (0-100), convert to 0-1
    if score > 1:
        score = score / 100
    
    # Clamp to valid range
    score = max(0.0, min(1.0, score))
    
    return score


def combine_confidences(scores: List[float], method: str = "average") -> float:
    """
    Combine multiple confidence scores into a single score.
    
    Args:
        scores: List of confidence scores (all expected to be 0-1)
        method: Combination method ('average', 'minimum', 'maximum', 'harmonic_mean')
    
    Returns:
        float: Combined confidence score (0.0-1.0)
    
    Raises:
        ValueError: If scores list is empty or invalid method
    """
    if not scores:
        raise ValueError("Cannot combine empty list of confidence scores")
    
    # Normalize all scores
    normalized = [normalize_confidence(s) for s in scores]
    
    if method == "average":
        return sum(normalized) / len(normalized)
    elif method == "minimum":
        return min(normalized)
    elif method == "maximum":
        return max(normalized)
    elif method == "harmonic_mean":
        # Harmonic mean is useful for combining rates/scores
        n = len(normalized)
        return n / sum(1 / (s + 1e-10) for s in normalized)  # Add small epsilon to avoid division by zero
    else:
        raise ValueError(f"Unknown combination method: {method}")


def interpret_confidence(score: float) -> str:
    """
    Convert a confidence score to human-readable interpretation.
    
    Args:
        score: Confidence score (0.0-1.0)
    
    Returns:
        str: Human-readable confidence level
    """
    score = normalize_confidence(score)
    
    if score >= 0.95:
        return "very_high"
    elif score >= 0.80:
        return "high"
    elif score >= 0.60:
        return "medium"
    elif score >= 0.40:
        return "low"
    else:
        return "very_low"


def is_confident(score: float, threshold: float = 0.80) -> bool:
    """
    Check if a confidence score meets a minimum threshold.
    
    Args:
        score: Confidence score (0.0-1.0)
        threshold: Minimum required confidence (default: 0.80)
    
    Returns:
        bool: True if score >= threshold
    """
    return normalize_confidence(score) >= normalize_confidence(threshold)


def confidence_range_check(
    score: float,
    min_confidence: float = 0.60,
    max_confidence: float = 1.0,
    strict: bool = False
) -> tuple[bool, str]:
    """
    Check if a confidence score is within an acceptable range.
    
    Args:
        score: Confidence score to check
        min_confidence: Minimum acceptable confidence
        max_confidence: Maximum acceptable confidence
        strict: If True, raise exception if out of range; if False, return False
    
    Returns:
        tuple[bool, str]: (is_valid, reason_if_invalid)
    
    Raises:
        ValueError: If strict=True and score is out of range
    """
    normalized = normalize_confidence(score)
    min_norm = normalize_confidence(min_confidence)
    max_norm = normalize_confidence(max_confidence)
    
    if normalized < min_norm:
        reason = f"Confidence {normalized:.2%} is below minimum {min_norm:.2%}"
        if strict:
            raise ValueError(reason)
        return False, reason
    elif normalized > max_norm:
        reason = f"Confidence {normalized:.2%} is above maximum {max_norm:.2%}"
        if strict:
            raise ValueError(reason)
        return False, reason
    
    return True, ""
