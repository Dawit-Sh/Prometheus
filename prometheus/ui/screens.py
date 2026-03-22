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

    @on(Button.Pressed)
    def select_slot(self, event: Button.Pressed) -> None:
        if event.button.id == "slot-cancel":
            self.dismiss(None)
            return
        slot = int(event.button.id.split("-")[-1])
        self.dismiss((self.mode, slot))
