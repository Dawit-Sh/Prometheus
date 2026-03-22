from __future__ import annotations

from rich.markup import escape
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.widgets import Static

from prometheus.engine.game_state import GameState, GlobalProgress
from prometheus.story.loader import Choice, Ending
from prometheus.ui.effects import risk_to_rich_tag


class StoryPanel(VerticalScroll):
    displayed_text = reactive("")

    def compose(self):
        yield Static("", id="story-copy")

    def watch_displayed_text(self, value: str) -> None:
        self.query_one("#story-copy", Static).update(value)


class StatusPanel(Static):
    def update_state(self, state: GameState, progress: GlobalProgress) -> None:
        stats = state.stats.as_dict()
        items = state.inventory.as_list() or ["none"]
        latest_flags = sorted(state.flags)[-4:] or ["none"]
        content = "\n".join(
            [
                "[b cyan]Stats[/b cyan]",
                f"Stealth      {stats['stealth']}/10",
                f"Intelligence {stats['intelligence']}/10",
                f"Trace        {stats['trace']}/10",
                f"Reputation   {stats['reputation']:+d}",
                "",
                "[b cyan]Inventory[/b cyan]",
                *[f"- {escape(item)}" for item in items[:8]],
                "",
                "[b cyan]Flags[/b cyan]",
                *[f"- {escape(flag)}" for flag in latest_flags],
                "",
                "[b cyan]Discovery[/b cyan]",
                f"Endings found {len(progress.discovered_endings)}",
                f"Nodes seen    {len(progress.seen_nodes)}",
            ]
        )
        self.update(content)


class ChoicePanel(Static):
    def update_choices(self, choices: list[Choice], ending: Ending | None = None) -> None:
        if ending:
            self.update(
                "\n".join(
                    [
                        f"[b red]{escape(ending.title)}[/b red]",
                        escape(ending.summary),
                        "",
                        "[b]Commands[/b]",
                        "r restart  l load  s save  q quit",
                    ]
                )
            )
            return

        lines = ["[b cyan]Choices[/b cyan]"]
        for index, choice in enumerate(choices, start=1):
            color = risk_to_rich_tag(choice.risk)
            lines.append(f"[{color}]{index}.[/{color}] {escape(choice.text)}")
        lines.append("")
        lines.append("[b]Keys[/b] 1-6 choose  k skip  r restart  s save  l load  t typing  e effects")
        self.update("\n".join(lines))


class HeaderBar(Static):
    def update_header(self, location: str, state: GameState) -> None:
        self.update(
            f"[b green]PROMETHEUS[/b green]   [cyan]{escape(location)}[/cyan]   "
            f"[yellow]TRACE {state.stats.trace}/10[/yellow]"
        )
