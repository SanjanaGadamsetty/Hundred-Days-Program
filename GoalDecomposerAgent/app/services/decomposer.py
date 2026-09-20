def decompose_goal(goal_title: str) -> list[str]:
    """Deterministic MVP decomposition; replaceable by an LLM later."""
    return [
        f"Understand the basics of {goal_title}",
        f"Practice {goal_title}",
        f"Build a small project using {goal_title}",
        f"Review and improve {goal_title}",
    ]
