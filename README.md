# ♟ Obi-Pawn Kenobot

Obi-Pawn Kenobot is a command-line chess bot built with [python-chess](https://pypi.org/project/python-chess/), designed to play games against humans or itself using a modular, extensible architecture. It supports PGN output, logging, colorized board rendering, and multiple play modes including infinite self-play loops.

## 🚀 Features

- ✅ Human vs Bot or Bot vs Bot play
- ✅ Alpha-beta pruning and move evaluation
- ✅ Clean and colored board rendering
- ✅ PGN game recording with engine metadata
- ✅ Infinite self-play loop for training/test runs
- ✅ Modular logging and performance counters
- ✅ Command-line arguments for customization

## 🛠 Usage

### Play a Game

```bash
python src/python/main.py --player choose_later
```

You'll be prompted to select a color. You can also set it directly:

```bash
python src/python/main.py --player white --depth 4 --color
```

### Self-Play Mode (One Game)

```bash
python src/python/main.py --player none
```

### Infinite Self-Play Loop

```bash
python src/python/main.py --player none --selfplay-loop
```

### Logging Levels

```bash
--log info        # Minimal
--log playing     # Standard commentary (recommended for play)
--log debug       # Includes internal debug logs
```

## 🎨 Board Output

Enable colored board display:

```bash
--color
```

If omitted, a clean Unicode text board will be printed.

## 🧹 Project Structure

```
.
├── README.md
├── Requirements.txt
├── roadmap.md
└── src
    └── python
        ├── bot_vs_bot_games.pgn
        ├── engine
        │   ├── __init__.py
        │   ├── board.py
        │   ├── move_gen.py
        │   ├── search.py
        │   └── evaluation
        │       ├── PSTs.py
        │       └── evaluation.py
        ├── main.py
        ├── tests
        ├── ui
        └── utils
            ├── counters.py
            └── log.py
```

## ⚙️ Development Roadmap

Obi-Pawn Kenobot is actively evolving through structured phases:

- **Phase 1:** ✅ MVP bot & CLI loop
- **Phase 2:** 🔄 Search improvements (alpha-beta, PSTs)
- **Phase 3:** 🔸 Lichess bot integration (via API)
- **Phase 4+:** Opening books, transposition tables, GUI, and C++ acceleration

See [`roadmap.md`](roadmap.md) for full breakdown.

## 🧪 Testing

Unit tests and regression comparisons to Stockfish are planned for advanced stages. PGN logs include metadata like evaluation count and time taken.

## 🧠 Requirements

- Python 3.8+
- [`python-chess`](https://pypi.org/project/python-chess/)

Install dependencies:

```bash
pip install -r Requirements.txt
```

*If ****`Requirements.txt`**** is missing, just manually install:*

```bash
pip install python-chess
```

##

---

