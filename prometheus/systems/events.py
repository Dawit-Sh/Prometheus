from __future__ import annotations

import random
from dataclasses import dataclass

from prometheus.engine.game_state import GameState


@dataclass(slots=True)
class EventOutcome:
    title: str
    body: str
    style: str
    item: str | None = None


def roll_random_event(state: GameState) -> EventOutcome | None:
    trace = state.stats.trace
    roll = random.random()

    if trace >= 7 and roll < 0.18:
        state.stats.trace = min(10, state.stats.trace + 1)
        state.add_alert("TRACE DETECTED")
        return EventOutcome(
            title="TRACE DETECTED",
            body="A hunter-killer heuristic tags your signal. Heat blooms across every active subnet.",
            style="danger",
        )

    if "ghost_contact" in state.flags and roll < 0.05 and not state.inventory.has("ghost shard"):
        state.inventory.add("ghost shard")
        return EventOutcome(
            title="GHOST SIGNAL",
            body="An unsigned burst piggybacks your uplink and leaves behind a ghost shard fragment.",
            style="safe",
            item="ghost shard",
        )

    if trace <= 2 and roll < 0.04 and not state.inventory.has("burner credential"):
        state.inventory.add("burner credential")
        return EventOutcome(
            title="DEAD DROP",
            body="A forgotten maintenance daemon coughs up a burner credential before it notices you.",
            style="warning",
            item="burner credential",
        )

    if "rival_hacker_pinged" in state.flags and roll < 0.07:
        state.stats.reputation = max(-5, state.stats.reputation - 1)
        state.stats.trace = min(10, state.stats.trace + 1)
        return EventOutcome(
            title="RIVAL INTERCEPT",
            body="Another intruder salts your route. Your rep drops while the trace net tightens.",
            style="danger",
        )

    if roll < 0.02 and "dev_message_seen" not in state.flags:
        state.flags.add("dev_message_seen")
        return EventOutcome(
            title="HIDDEN COMMENT",
            body="A buried code note blinks into existence: 'If you reached this, keep digging. The ship lies.'",
            style="warning",
        )

    return None
