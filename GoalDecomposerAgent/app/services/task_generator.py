def generate_tasks(subgoal_title: str) -> list[str]:
    """Deterministic MVP task generation; replaceable by an LLM later."""
    return [
        f"Study the basics of {subgoal_title}",
        f"Practice {subgoal_title}",
        f"Complete a small exercise on {subgoal_title}",
    ]
