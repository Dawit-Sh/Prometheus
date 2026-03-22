from __future__ import annotations


RISK_COLORS = {
    "safe": "green",
    "warning": "yellow",
    "danger": "red",
}


def risk_to_rich_tag(risk: str) -> str:
    return RISK_COLORS.get(risk, "cyan")
