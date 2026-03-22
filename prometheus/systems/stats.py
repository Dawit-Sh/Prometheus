from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PlayerStats:
    stealth: int = 5
    intelligence: int = 5
    trace: int = 0
    reputation: int = 0

    def clamp(self) -> None:
        self.stealth = max(0, min(10, self.stealth))
        self.intelligence = max(0, min(10, self.intelligence))
        self.trace = max(0, min(10, self.trace))
        self.reputation = max(-5, min(10, self.reputation))

    def as_dict(self) -> dict[str, int]:
        return {
            "stealth": self.stealth,
            "intelligence": self.intelligence,
            "trace": self.trace,
            "reputation": self.reputation,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, int] | None) -> "PlayerStats":
        payload = payload or {}
        stats = cls(
            stealth=payload.get("stealth", 5),
            intelligence=payload.get("intelligence", 5),
            trace=payload.get("trace", 0),
            reputation=payload.get("reputation", 0),
        )
        stats.clamp()
        return stats
