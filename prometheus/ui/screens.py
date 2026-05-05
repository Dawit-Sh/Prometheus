from __future__ import annotations

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, ListItem, ListView


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
    BINDINGS = [
        ("escape", "cancel", "Cancel"),
    ]

    def __init__(self, mode: str, metadata: list[dict]) -> None:
        super().__init__()
        self.mode = mode
        self.metadata = metadata

    def compose(self) -> ComposeResult:
        with Vertical(id="slot-modal"):
            yield Label(f"{self.mode.title()} Slot", classes="alert-title slot-header")
            items = []
            for entry in self.metadata:
                slot = entry["slot"]
                if entry.get("empty"):
                    label = f"Slot {slot}: empty"
                else:
                    label = (
                        f"Slot {slot}: {entry.get('node')} | "
                        f"trace {entry.get('trace')} | {entry.get('saved_at')}"
                    )
                items.append(ListItem(Label(label, classes="slot-label")))
            items.append(ListItem(Label("Cancel", classes="slot-label")))
            yield ListView(*items, id="slot-list")

    def on_mount(self) -> None:
        self.query_one("#slot-list", ListView).focus()

    @on(ListView.Selected, "#slot-list")
    def on_select(self, event: ListView.Selected) -> None:
        idx = event.list_view.index
        if idx >= len(self.metadata):
            self.dismiss(None)
        else:
            slot = self.metadata[idx]["slot"]
            self.dismiss((self.mode, slot))

    def action_cancel(self) -> None:
        self.dismiss(None)
