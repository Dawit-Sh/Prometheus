from __future__ import annotations

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label


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


class SlotScreen(ModalScreen[tuple[str, int] | None]):
    def __init__(self, mode: str, metadata: list[dict]) -> None:
        super().__init__()
        self.mode = mode
        self.metadata = metadata

    def compose(self) -> ComposeResult:
        with Vertical(id="slot-modal"):
            yield Label(f"{self.mode.title()} Slot", classes="alert-title")
            for entry in self.metadata:
                slot = entry["slot"]
                if entry.get("empty"):
                    label = f"Slot {slot}: empty"
                else:
                    label = (
                        f"Slot {slot}: {entry.get('node')} | trace {entry.get('trace')} | "
                        f"{entry.get('saved_at')}"
                    )
                yield Button(label, id=f"slot-{slot}")
            yield Button("Cancel", id="slot-cancel")

    def on_mount(self) -> None:
        self._buttons = list(self.query(Button))
        if self._buttons:
            self._buttons[0].focus()

    @on(Button.Pressed)
    def select_slot(self, event: Button.Pressed) -> None:
        if event.button.id == "slot-cancel":
            self.dismiss(None)
            return
        slot = int(event.button.id.split("-")[-1])
        self.dismiss((self.mode, slot))

    def on_key(self, event) -> None:
        if event.key == "escape":
            self.dismiss(None)
            event.prevent_default()
            return
        if event.key in ("up", "down"):
            if not self._buttons:
                return
            try:
                current_idx = next(i for i, b in enumerate(self._buttons) if b.has_focus)
            except StopIteration:
                current_idx = 0
                self._buttons[0].focus()
                event.prevent_default()
                return
            if event.key == "up":
                next_idx = (current_idx - 1) % len(self._buttons)
                self._buttons[next_idx].focus()
            elif event.key == "down":
                next_idx = (current_idx + 1) % len(self._buttons)
                self._buttons[next_idx].focus()
            event.prevent_default()
        elif event.key == "enter":
            focused = self.focused
            if isinstance(focused, Button):
                if focused.id == "slot-cancel":
                    self.dismiss(None)
                else:
                    slot = int(focused.id.split("-")[-1])
                    self.dismiss((self.mode, slot))
                event.prevent_default()
