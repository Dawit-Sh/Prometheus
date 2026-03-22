# PROMETHEUS

> A cyberpunk terminal infiltration game built with Textual.

Welcome to **Prometheus**, an exhilarating space adventure where you play as a skilled hacker infiltrating military starships to obtain classified information. Navigate through security protocols, evade detection, and outsmart security forces to accomplish your objectives.

## Overview

**Prometheus** is a text-based "Choose Your Own Adventure" game with a modern terminal UI.

- Built with **Python**, **Textual**, and **Rich**
- Play through multiple military starships and hidden off-grid routes
- Make high-impact decisions with stat checks, inventory gates, and branching outcomes
- Discover **40 unique endings**
- Save progress, replay routes, and hunt for secret storylines

## Features

- Cyberpunk terminal interface
- Typing animation for story text
- Color-coded risk feedback
- Modal alerts for detection, trace spikes, and item pickups
- Player stats:
  - Stealth
  - Intelligence
  - Trace Level
  - Reputation
- Inventory and route-specific tools
- Multiple save slots
- Global ending tracker
- Hidden paths, random encounters, lore fragments, and easter eggs

## Project Structure

```text
Prometheus/
├── main.py
├── README.md
├── .gitignore
└── prometheus/
    ├── app.py
    ├── main.py
    ├── data/
    │   └── endings.json
    ├── engine/
    │   ├── game_loop.py
    │   └── game_state.py
    ├── saves/
    ├── story/
    │   ├── loader.py
    │   └── nodes.json
    ├── systems/
    │   ├── events.py
    │   ├── inventory.py
    │   └── stats.py
    └── ui/
        ├── components.py
        ├── effects.py
        └── screens.py
```

## Installation

Install requirements inside a virtual environment.

### Windows

Create the virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install textual rich
```

### macOS

Create the virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install textual rich
```

### Linux

Create the virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install textual rich
```

## Run The Game

From the project root:

```bash
python main.py
```

## How To Play

Once the game opens:

- Read the story panel in the center
- Watch your stats and inventory in the right sidebar
- Use the numbered choices at the bottom to progress
- Manage your **Trace Level** carefully, because high trace increases danger
- Replay different routes to uncover hidden storylines and all **40 endings**

## Controls

| Key | Action |
| --- | --- |
| `1-6` | Choose an option |
| `k` | Skip current typing animation |
| `r` | Fast restart |
| `s` | Save game |
| `l` | Load game |
| `t` | Toggle typing animation |
| `e` | Toggle visual effects |
| `q` | Quit |

## GitHub Push Commands

If this repository is already connected to GitHub and you want to push your changes:

```bash
git status
git add .
git commit -m "Build Prometheus Textual adventure game"
git push origin main
```

If your default branch is `master` instead of `main`, use:

```bash
git push origin master
```

If you have not connected the local repository to GitHub yet, replace `<REPO_URL>` with your repository URL:

```bash
git remote add origin <REPO_URL>
git branch -M main
git add .
git commit -m "Build Prometheus Textual adventure game"
git push -u origin main
```

## Notes

- The game is launched with `python main.py`
- Only `textual` and `rich` are required beyond the Python standard library
- Progress saves are stored locally in `prometheus/saves/`
- Ending discovery is tracked across runs
