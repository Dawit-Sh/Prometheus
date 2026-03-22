from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
STORY_DIR = ROOT / "story"


@dataclass(slots=True)
class Choice:
    id: str
    text: str
    next_node: str
    risk: str = "safe"
    conditions: dict[str, Any] = field(default_factory=dict)
    effects: dict[str, Any] = field(default_factory=dict)
    hotkey: str = ""


@dataclass(slots=True)
class StoryNode:
    id: str
    location: str
    text: str
    choices: list[Choice] = field(default_factory=list)
    effects: dict[str, Any] = field(default_factory=dict)
    ending_id: str | None = None


@dataclass(slots=True)
class Ending:
    id: str
    title: str
    category: str
    summary: str


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_story(path: Path | None = None) -> tuple[str, dict[str, StoryNode]]:
    payload = _load_json(path or STORY_DIR / "nodes.json")
    nodes: dict[str, StoryNode] = {}
    for raw in payload["nodes"]:
        nodes[raw["id"]] = StoryNode(
            id=raw["id"],
            location=raw["location"],
            text=raw["text"],
            choices=[
                Choice(
                    id=choice["id"],
                    text=choice["text"],
                    next_node=choice["next_node"],
                    risk=choice.get("risk", "safe"),
                    conditions=choice.get("conditions", {}),
                    effects=choice.get("effects", {}),
                    hotkey=choice.get("hotkey", ""),
                )
                for choice in raw.get("choices", [])
            ],
            effects=raw.get("effects", {}),
            ending_id=raw.get("ending_id"),
        )
    return payload["start_node"], nodes


def load_endings(path: Path | None = None) -> dict[str, Ending]:
    payload = _load_json(path or DATA_DIR / "endings.json")
    return {
        raw["id"]: Ending(
            id=raw["id"],
            title=raw["title"],
            category=raw["category"],
            summary=raw["summary"],
        )
        for raw in payload["endings"]
    }
