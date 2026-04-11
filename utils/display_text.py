"""Plain-language labels for symptoms (dataset uses underscores)."""


def symptom_plain(canonical: str) -> str:
    return " ".join(part.capitalize() for part in str(canonical).replace("_", " ").split())
