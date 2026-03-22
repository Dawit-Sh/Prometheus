from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from prometheus.systems.inventory import Inventory
from prometheus.systems.stats import PlayerStats


SAVE_DIR = Path(__file__).resolve().parents[1] / "saves"
PROGRESS_PATH = SAVE_DIR / "progress.json"


@dataclass(slots=True)
class GameConfig:
    typing_animation: bool = True
    effects_enabled: bool = True
    skip_seen_text: bool = False

    def as_dict(self) -> dict[str, bool]:
        return {
            "typing_animation": self.typing_animation,
            "effects_enabled": self.effects_enabled,
            "skip_seen_text": self.skip_seen_text,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any] | None) -> "GameConfig":
        payload = payload or {}
        return cls(
            typing_animation=payload.get("typing_animation", True),
            effects_enabled=payload.get("effects_enabled", True),
            skip_seen_text=payload.get("skip_seen_text", False),
        )


@dataclass(slots=True)
class GlobalProgress:
    discovered_endings: list[str] = field(default_factory=list)
    seen_nodes: list[str] = field(default_factory=list)

    @classmethod
    def load(cls) -> "GlobalProgress":
        SAVE_DIR.mkdir(parents=True, exist_ok=True)
        if not PROGRESS_PATH.exists():
            return cls()
        with PROGRESS_PATH.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        return cls(
            discovered_endings=payload.get("discovered_endings", []),
            seen_nodes=payload.get("seen_nodes", []),
        )

    def save(self) -> None:
        SAVE_DIR.mkdir(parents=True, exist_ok=True)
        with PROGRESS_PATH.open("w", encoding="utf-8") as handle:
            json.dump(
                {
                    "discovered_endings": self.discovered_endings,
                    "seen_nodes": self.seen_nodes,
                },
                handle,
                indent=2,
            )

    def note_node(self, node_id: str) -> None:
        if node_id not in self.seen_nodes:
            self.seen_nodes.append(node_id)

    def note_ending(self, ending_id: str) -> None:
        if ending_id not in self.discovered_endings:
            self.discovered_endings.append(ending_id)


@dataclass(slots=True)
class GameState:
    current_node_id: str
    stats: PlayerStats = field(default_factory=PlayerStats)
    inventory: Inventory = field(default_factory=Inventory)
    flags: set[str] = field(default_factory=set)
    visit_counts: dict[str, int] = field(default_factory=dict)
    recent_alerts: list[str] = field(default_factory=list)
    slot: int | None = None
    config: GameConfig = field(default_factory=GameConfig)
    last_saved_at: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "current_node_id": self.current_node_id,
            "stats": self.stats.as_dict(),
            "inventory": self.inventory.as_list(),
            "flags": sorted(self.flags),
            "visit_counts": self.visit_counts,
            "slot": self.slot,
            "config": self.config.as_dict(),
            "last_saved_at": self.last_saved_at,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "GameState":
        return cls(
            current_node_id=payload["current_node_id"],
            stats=PlayerStats.from_dict(payload.get("stats")),
            inventory=Inventory.from_list(payload.get("inventory")),
            flags=set(payload.get("flags", [])),
            visit_counts=dict(payload.get("visit_counts", {})),
            slot=payload.get("slot"),
            config=GameConfig.from_dict(payload.get("config")),
            last_saved_at=payload.get("last_saved_at"),
        )

    def mark_visited(self, node_id: str) -> None:
        self.visit_counts[node_id] = self.visit_counts.get(node_id, 0) + 1

    def has_seen(self, node_id: str) -> bool:
        return self.visit_counts.get(node_id, 0) > 0

    def add_alert(self, message: str) -> None:
        self.recent_alerts.append(message)
        self.recent_alerts = self.recent_alerts[-5:]

    def save_to_slot(self, slot: int) -> None:
        SAVE_DIR.mkdir(parents=True, exist_ok=True)
        self.slot = slot
        self.last_saved_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        path = SAVE_DIR / f"slot_{slot}.json"
        with path.open("w", encoding="utf-8") as handle:
            json.dump(self.as_dict(), handle, indent=2)

    @classmethod
    def load_slot(cls, slot: int) -> "GameState | None":
        path = SAVE_DIR / f"slot_{slot}.json"
        if not path.exists():
            return None
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        return cls.from_dict(payload)

    @staticmethod
    def slot_metadata() -> list[dict[str, Any]]:
        SAVE_DIR.mkdir(parents=True, exist_ok=True)
        slots: list[dict[str, Any]] = []
        for slot in range(1, 4):
            path = SAVE_DIR / f"slot_{slot}.json"
            if not path.exists():
                slots.append({"slot": slot, "empty": True})
                continue
            with path.open("r", encoding="utf-8") as handle:
                payload = json.load(handle)
            slots.append(
                {
                    "slot": slot,
                    "empty": False,
                    "node": payload.get("current_node_id"),
                    "saved_at": payload.get("last_saved_at"),
                    "trace": payload.get("stats", {}).get("trace", 0),
                }
            )
        return slots
