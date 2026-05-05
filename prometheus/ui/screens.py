from __future__ import annotations

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, OptionList


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
        ("s", "do_nothing", "Save"),
        ("l", "do_nothing", "Load"),
    ]

    def __init__(self, mode: str, metadata: list[dict]) -> None:
        super().__init__()
        self.mode = mode
        self.metadata = metadata

    def compose(self) -> ComposeResult:
        with Vertical(id="slot-modal"):
            yield Label(f"{self.mode.title()} Slot", classes="alert-title")
            option_list = OptionList(id="slot-list")
            for entry in self.metadata:
                slot = entry["slot"]
                if entry.get("empty"):
                    label = f"Slot {slot}: empty"
                else:
                    label = (
                        f"Slot {slot}: {entry.get('node')} | trace {entry.get('trace')} | "
                        f"{entry.get('saved_at')}"
                    )
                option_list.add_option(label)
            option_list.add_option("Cancel")
            yield option_list

    def on_mount(self) -> None:
        self.query_one("#slot-list", OptionList).focus()

    def action_do_nothing(self) -> None:
        """Override s and l keys so they don't trigger App actions."""
        pass

    @on(OptionList.OptionSelected, "#slot-list")
    def select_slot(self, event: OptionList.OptionSelected) -> None:
        if event.option_index == len(self.metadata):
            self.dismiss(None)
        else:
            slot = self.metadata[event.option_index]["slot"]
            self.dismiss((self.mode, slot))
