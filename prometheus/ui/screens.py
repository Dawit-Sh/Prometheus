from __future__ import annotations

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static


class AlertScreen(ModalScreen[None]):
    def __init__(self, title: str, body: str, style: str = "warning") -> None:
        super().__init__()
        self.title = title
        self.body = body
        self.style = style

    def compose(self) -> ComposeResult:
        with Container(id="alert-modal", classes=self.style):
            yield Label(self.title, classes="alert-title")
            yield Label(self.body, classes="alert-body")
            yield Button("Dismiss", id="dismiss-alert")

    @on(Button.Pressed, "#dismiss-alert")
    def handle_dismiss(self) -> None:
        self.dismiss(None)


class SlotRow(Static):
    """A single row in the slot list."""

    can_focus = True

    def __init__(self, text: str, slot_num: int | None) -> None:
        super().__init__(text, classes="slot-text")
        self.slot_num = slot_num

    def on_click(self) -> None:
        self.screen._pick(self.slot_num)


class SlotScreen(ModalScreen[tuple[str, int] | None]):
    BINDINGS = [
        Binding("up", "move(-1)", show=False),
        Binding("down", "move(1)", show=False),
        Binding("enter", "confirm", show=False),
        Binding("escape", "cancel", show=False),
    ]

    def __init__(self, mode: str, metadata: list[dict]) -> None:
        super().__init__()
        self.mode = mode
        self.metadata = metadata
        self._index = 0

    def compose(self) -> ComposeResult:
        with Vertical(id="slot-modal"):
            yield Label(f"{self.mode.title()} Slot", classes="alert-title slot-header")
            for entry in self.metadata:
                slot = entry["slot"]
                if entry.get("empty"):
                    label = f"  Slot {slot}: empty"
                else:
                    label = (
                        f"  Slot {slot}: {entry.get('node')} | "
                        f"trace {entry.get('trace')} | {entry.get('saved_at')}"
                    )
                yield SlotRow(label, slot)
            yield SlotRow("  Cancel", None)
            yield Label("", id="spacer")

    def on_mount(self) -> None:
        self._rows = list(self.query(SlotRow))
        if self._rows:
            self._rows[0].add_class("active")
            self._rows[0].focus()

    def action_move(self, delta: int) -> None:
        self._move(delta)

    def action_confirm(self) -> None:
        if not self._rows:
            self.dismiss(None)
            return
        self._pick(self._rows[self._index].slot_num)

    def action_cancel(self) -> None:
        self.dismiss(None)

    def _move(self, delta: int) -> None:
        if not self._rows:
            return
        self._rows[self._index].remove_class("active")
        self._index = (self._index + delta) % len(self._rows)
        self._rows[self._index].add_class("active")
        self._rows[self._index].focus()

    def _pick(self, slot_num: int | None) -> None:
        if slot_num is None:
            self.dismiss(None)
        else:
            self.dismiss((self.mode, slot_num))
