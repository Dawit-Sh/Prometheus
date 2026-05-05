from __future__ import annotations

import asyncio

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Footer

from prometheus.engine.game_loop import ChoiceResult, GameLoop
from prometheus.engine.game_state import GameState, GlobalProgress
from prometheus.story.loader import load_endings, load_story
from prometheus.ui.components import ChoicePanel, HeaderBar, StatusPanel, StoryPanel
from prometheus.ui.screens import AlertScreen, SlotScreen


class PrometheusApp(App):
    CSS = """
    Screen {
        background: #05080d;
        color: #d8ffe7;
    }
    #root {
        layout: vertical;
    }
    #body {
        height: 1fr;
    }
    #main {
        width: 3fr;
        border: round #1dd48d;
        padding: 1 2;
        margin: 0 1 1 1;
        background: #071019;
    }
    #sidebar {
        width: 32;
        border: round #2fd9ff;
        padding: 1;
        margin: 0 1 1 0;
        background: #09131f;
    }
    #choices {
        height: 11;
        border: round #ffe66d;
        padding: 1 2;
        margin: 0 1 1 1;
        background: #141108;
    }
    #headerbar {
        height: 3;
        content-align: center middle;
        border-bottom: solid #164f3e;
        background: #07151c;
    }
    #story-copy {
        width: 100%;
    }
    #alert-modal, #slot-modal {
        width: 70;
        height: auto;
        padding: 1 2;
        border: round white;
        background: #111825;
        align: center middle;
    }
    #slot-list {
        width: 100%;
        height: auto;
        background: transparent;
        border: none;
    }
    #slot-list .option-list--option {
        padding: 1;
        color: #d8ffe7;
    }
    #slot-list .option-list--option-highlighted {
        background: #1a2744;
        color: cyan;
        text-style: bold;
    }
    #alert-modal.danger {
        border: round red;
    }
    #alert-modal.warning {
        border: round yellow;
    }
    #alert-modal.safe {
        border: round green;
    }
    .alert-title {
        text-style: bold;
        color: cyan;
        margin-bottom: 1;
    }
    .alert-body {
        margin-bottom: 1;
    }
    .glitch #headerbar {
        tint: red 20%;
    }
    """

    BINDINGS = [
        Binding("1", "choice(0)", "Choice 1"),
        Binding("2", "choice(1)", "Choice 2"),
        Binding("3", "choice(2)", "Choice 3"),
        Binding("4", "choice(3)", "Choice 4"),
        Binding("5", "choice(4)", "Choice 5"),
        Binding("6", "choice(5)", "Choice 6"),
        Binding("k", "skip_text", "Skip"),
        Binding("r", "restart", "Restart"),
        Binding("s", "save_game", "Save"),
        Binding("l", "load_game", "Load"),
        Binding("t", "toggle_typing", "Typing"),
        Binding("e", "toggle_effects", "Effects"),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.start_node_id, self.nodes = load_story()
        self.endings = load_endings()
        self.progress = GlobalProgress.load()
        self.loop = GameLoop(
            GameState(current_node_id=self.start_node_id),
            self.nodes,
            self.endings,
            self.progress,
        )
        self.skip_requested = False
        self.current_result: ChoiceResult | None = None

    def compose(self) -> ComposeResult:
        with Container(id="root"):
            yield HeaderBar(id="headerbar")
            with Horizontal(id="body"):
                yield StoryPanel(id="main")
                with Vertical(id="sidebar"):
                    yield StatusPanel(id="status")
            yield ChoicePanel(id="choices")
            yield Footer()

    async def on_mount(self) -> None:
        await self.present_result(self.loop.begin())

    async def present_result(self, result: ChoiceResult) -> None:
        self.current_result = result
        self.refresh_panels()
        await self.render_story_text(result.node.text)
        self.refresh_panels()
        for title, body in result.alerts:
            await self.push_screen(AlertScreen(title, body, "warning"))
        if result.random_event:
            if result.random_event.style == "danger":
                self.trigger_glitch()
            await self.push_screen(
                AlertScreen(
                    result.random_event.title,
                    result.random_event.body,
                    result.random_event.style,
                )
            )
        if result.gained_items:
            for item in result.gained_items:
                await self.push_screen(
                    AlertScreen("ITEM ACQUIRED", f"You secured {item}.", "safe")
                )
        if result.ending and self.loop.state.config.effects_enabled:
            self.trigger_glitch()

    def refresh_panels(self) -> None:
        state = self.loop.state
        node = self.loop.current_node
        self.query_one(HeaderBar).update_header(node.location, state)
        self.query_one(StatusPanel).update_state(state, self.progress)
        ending = self.current_result.ending if self.current_result else None
        self.query_one(ChoicePanel).update_choices(self.loop.available_choices(), ending)

    async def render_story_text(self, text: str) -> None:
        panel = self.query_one(StoryPanel)
        node_id = self.loop.current_node.id
        seen_before = self.loop.state.visit_counts.get(node_id, 0) > 1
        skip = self.loop.state.config.skip_seen_text and seen_before
        if skip or not self.loop.state.config.typing_animation:
            panel.displayed_text = text
            return

        self.skip_requested = False
        shown = []
        for char in text:
            if self.skip_requested:
                panel.displayed_text = text
                return
            shown.append(char)
            panel.displayed_text = "".join(shown)
            await asyncio.sleep(0.004)

    def trigger_glitch(self) -> None:
        if not self.loop.state.config.effects_enabled:
            return
        self.add_class("glitch")
        self.set_timer(0.45, lambda: self.remove_class("glitch"))

    async def action_choice(self, index: int) -> None:
        if self.current_result and self.current_result.ending:
            return
        try:
            result = self.loop.choose(index)
        except IndexError:
            return
        if result.random_event or self.loop.state.stats.trace >= 8:
            self.trigger_glitch()
        await self.present_result(result)

    def action_skip_text(self) -> None:
        self.skip_requested = True

    async def action_restart(self) -> None:
        await self.present_result(self.loop.restart(self.start_node_id))

    async def action_save_game(self) -> None:
        metadata = GameState.slot_metadata()
        worker = self.run_worker(self._save_game_flow(metadata))
        await worker.wait()

    async def _save_game_flow(self, metadata) -> None:
        selection = await self.push_screen_wait(SlotScreen("save", metadata))
        if selection:
            _, slot = selection
            self.loop.state.save_to_slot(slot)
            await self.push_screen(AlertScreen("SAVE COMPLETE", f"Slot {slot} updated.", "safe"))

    async def action_load_game(self) -> None:
        metadata = GameState.slot_metadata()
        worker = self.run_worker(self._load_game_flow(metadata))
        await worker.wait()

    async def _load_game_flow(self, metadata) -> None:
        selection = await self.push_screen_wait(SlotScreen("load", metadata))
        if not selection:
            return
        _, slot = selection
        loaded = GameState.load_slot(slot)
        if loaded is None:
            await self.push_screen(AlertScreen("LOAD FAILED", f"Slot {slot} is empty.", "danger"))
            return
        loaded.slot = slot
        await self.present_result(self.loop.swap_state(loaded))

    async def action_toggle_typing(self) -> None:
        self.loop.state.config.typing_animation = not self.loop.state.config.typing_animation
        state = "enabled" if self.loop.state.config.typing_animation else "disabled"
        await self.push_screen(AlertScreen("CONFIG", f"Typing animation {state}.", "safe"))

    async def action_toggle_effects(self) -> None:
        self.loop.state.config.effects_enabled = not self.loop.state.config.effects_enabled
        state = "enabled" if self.loop.state.config.effects_enabled else "disabled"
        await self.push_screen(AlertScreen("CONFIG", f"Visual effects {state}.", "safe"))
