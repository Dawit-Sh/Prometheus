from __future__ import annotations

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label
from textual.widget import Widget


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


class SlotLine(Widget):
    """A single line in the slot selection screen."""

    def __init__(self, text: str, slot_num: int | None) -> None:
        super().__init__()
        self.text = text
        self.slot_num = slot_num

    def compose(self) -> ComposeResult:
        yield Label(self.text, classes="slot-line-label")

    def on_click(self) -> None:
        self.screen._select(self.slot_num)


class SlotScreen(ModalScreen[tuple[str, int] | None]):
    BINDINGS = [
        ("up", "up", "Up"),
        ("down", "down", "Down"),
        ("enter", "select", "Select"),
        ("escape", "cancel", "Cancel"),
    ]

    def __init__(self, mode: str, metadata: list[dict]) -> None:
        super().__init__()
        self.mode = mode
        self.metadata = metadata
        self._idx = 0

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
                yield SlotLine(label, slot)
            yield SlotLine("  Cancel", None)
            yield Label("", id="slot-spacer")

    def on_mount(self) -> None:
        self._lines = list(self.query(SlotLine))
        if self._lines:
            self._lines[0].add_class("highlighted")
            self._lines[0].focus()

    def _select(self, slot_num: int | None) -> None:
        if slot_num is None:
            self.dismiss(None)
        else:
            self.dismiss((self.mode, slot_num))

    def action_up(self) -> None:
        if not self._lines:
            return
        self._lines[self._idx].remove_class("highlighted")
        self._idx = (self._idx - 1) % len(self._lines)
        self._lines[self._idx].add_class("highlighted")
        self._lines[self._idx].focus()

    def action_down(self) -> None:
        if not self._lines:
            return
        self._lines[self._idx].remove_class("highlighted")
        self._idx = (self._idx + 1) % len(self._lines)
        self._lines[self._idx].add_class("highlighted")
        self._lines[self._idx].focus()

    def action_select(self) -> None:
        if not self._lines:
            return
        self._select(self._lines[self._idx].slot_num)

    def action_cancel(self) -> None:
        self.dismiss(None)
