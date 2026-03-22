from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Inventory:
    items: list[str] = field(default_factory=list)

    def add(self, item: str) -> None:
        if item not in self.items:
            self.items.append(item)

    def discard(self, item: str) -> None:
        if item in self.items:
            self.items.remove(item)

    def has(self, item: str) -> bool:
        return item in self.items

    def as_list(self) -> list[str]:
        return list(self.items)

    @classmethod
    def from_list(cls, payload: list[str] | None) -> "Inventory":
        return cls(items=list(payload or []))
