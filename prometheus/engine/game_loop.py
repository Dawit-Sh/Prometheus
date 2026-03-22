from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from prometheus.engine.game_state import GameState, GlobalProgress
from prometheus.story.loader import Choice, Ending, StoryNode
from prometheus.systems.events import EventOutcome, roll_random_event


@dataclass(slots=True)
class ChoiceResult:
    node: StoryNode
    alerts: list[tuple[str, str]]
    ending: Ending | None = None
    random_event: EventOutcome | None = None
    gained_items: list[str] | None = None


class GameLoop:
    def __init__(
        self,
        state: GameState,
        nodes: dict[str, StoryNode],
        endings: dict[str, Ending],
        progress: GlobalProgress,
    ) -> None:
        self.state = state
        self.nodes = nodes
        self.endings = endings
        self.progress = progress

    @property
    def current_node(self) -> StoryNode:
        return self.nodes[self.state.current_node_id]

    def begin(self) -> ChoiceResult:
        return self._enter_node(self.current_node.id)

    def available_choices(self) -> list[Choice]:
        return [choice for choice in self.current_node.choices if self._conditions_met(choice.conditions)]

    def choose(self, index: int) -> ChoiceResult:
        choices = self.available_choices()
        if index < 0 or index >= len(choices):
            raise IndexError("Choice out of range")
        choice = choices[index]
        alerts, gained_items = self._apply_effects(choice.effects)
        self.state.current_node_id = choice.next_node
        result = self._enter_node(choice.next_node)
        result.alerts = alerts + result.alerts
        result.gained_items = (gained_items or []) + (result.gained_items or [])
        result.random_event = result.random_event or roll_random_event(self.state)
        return result

    def restart(self, start_node_id: str) -> ChoiceResult:
        config = self.state.config
        slot = self.state.slot
        self.state = GameState(current_node_id=start_node_id, config=config, slot=slot)
        return self._enter_node(start_node_id)

    def swap_state(self, state: GameState) -> ChoiceResult:
        self.state = state
        return self._enter_node(state.current_node_id)

    def _enter_node(self, node_id: str, reenter: bool = False) -> ChoiceResult:
        node = self.nodes[node_id]
        alerts: list[tuple[str, str]] = []
        gained_items: list[str] = []
        first_visit = not self.state.has_seen(node_id)
        if first_visit or reenter:
            enter_alerts, enter_gains = self._apply_effects(node.effects)
            alerts.extend(enter_alerts)
            gained_items.extend(enter_gains)
        self.state.mark_visited(node_id)
        self.progress.note_node(node_id)
        self.progress.save()

        ending = None
        if node.ending_id:
            self.progress.note_ending(node.ending_id)
            self.progress.save()
            ending = self.endings[node.ending_id]
        return ChoiceResult(node=node, alerts=alerts, ending=ending, gained_items=gained_items)

    def _conditions_met(self, conditions: dict[str, Any]) -> bool:
        if not conditions:
            return True

        for item in conditions.get("inventory", []):
            if not self.state.inventory.has(item):
                return False

        stats = self.state.stats.as_dict()
        for stat, gates in conditions.get("stats", {}).items():
            value = stats.get(stat, 0)
            if "min" in gates and value < gates["min"]:
                return False
            if "max" in gates and value > gates["max"]:
                return False

        flags = self.state.flags
        if any(flag not in flags for flag in conditions.get("flags_all", [])):
            return False
        if conditions.get("flags_any") and not any(flag in flags for flag in conditions["flags_any"]):
            return False
        if any(flag in flags for flag in conditions.get("not_flags", [])):
            return False
        return True

    def _apply_effects(self, effects: dict[str, Any]) -> tuple[list[tuple[str, str]], list[str]]:
        alerts: list[tuple[str, str]] = []
        gained_items: list[str] = []
        if not effects:
            return alerts, gained_items

        for stat, delta in effects.get("stats", {}).items():
            if hasattr(self.state.stats, stat):
                setattr(self.state.stats, stat, getattr(self.state.stats, stat) + delta)
        self.state.stats.clamp()

        for item in effects.get("inventory_add", []):
            if not self.state.inventory.has(item):
                self.state.inventory.add(item)
                gained_items.append(item)

        for item in effects.get("inventory_remove", []):
            self.state.inventory.discard(item)

        for flag in effects.get("flags_add", []):
            self.state.flags.add(flag)
        for flag in effects.get("flags_remove", []):
            self.state.flags.discard(flag)

        for alert in effects.get("alerts", []):
            title = alert.get("title", "NOTICE")
            body = alert.get("body", "")
            alerts.append((title, body))
            self.state.add_alert(title)

        return alerts, gained_items
