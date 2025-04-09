# ♟ Obi-Pawn Kenobot Roadmap

## 🧱 Phase 1: Core Bot MVP (With `python-chess`)
**Goal:** Get a basic bot running against a real game engine or user

- [x] Set up project structure & Git
- [ ] Install `python-chess` and create a minimal `main.py`
- [ ] Initialize a `chess.Board()` object and create a basic game loop
- [ ] Implement a simple material-counting evaluation function
- [ ] Create a function that selects the best move from legal ones based on evaluation
- [ ] Add a CLI interface for human vs bot play (e.g. `input()` for moves)
- [ ] Print move decisions and evaluation scores for debugging
- [ ] Set up unit tests for evaluation and bot logic

## 🌐 Phase 2: Lichess Integration
**Goal:** Play games online through Lichess bots API

- [ ] Register a bot account on Lichess and generate a personal API token
- [ ] Install `berserk` or `lichess-bot` library to interface with the Lichess API
- [ ] Set up API authentication using the token
- [ ] Poll for challenges using the API
- [ ] Accept a challenge and hook into the game loop
- [ ] Feed opponent moves into your local `chess.Board` instance
- [ ] Respond with your bot's moves using the same API
- [ ] Log game results and store PGNs locally

## 🚀 Phase 3: Smarter Engine (Still using `python-chess`)
**Goal:** Make the bot semi-decent

- [ ] Implement minimax search with fixed depth
- [ ] Add alpha-beta pruning to reduce unnecessary branches
- [ ] Improve evaluation function with basic heuristics (e.g., piece-square tables, king safety)
- [ ] Add clock-based time management (evaluate and move within X milliseconds)
- [ ] Add support for loading board states from FEN for easier testing
- [ ] Add PGN generation to store game history

## 🧠 Phase 4: Opening Book + Search Improvements
**Goal:** Optimize early game & speed up search

- [ ] Import or create an opening book (e.g., .bin or .pgn of known openings)
- [ ] Integrate book lookups in early moves
- [ ] Implement a transposition table (hashing)
- [ ] Add basic move ordering (captures, checks first)
- [ ] Integrate iterative deepening to manage depth dynamically
- [ ] Add logging for nodes searched, time taken, evaluation scores

## ⚙️ Phase 5: Partial Custom Engine
**Goal:** Replace parts of `python-chess` with your own logic

- [ ] Implement your own board representation (2D array or bitboard)
- [ ] Create custom move generation for each piece type
- [ ] Validate legality and check/checkmate logic
- [ ] Port your evaluation function to use your board instead of `python-chess`
- [ ] Add a comparison script to cross-check results against `python-chess`

## 🚡 Phase 6: Hybrid C++ Integration
**Goal:** Speed up heavy computation

- [ ] Profile Python code to identify bottlenecks
- [ ] Write C++ equivalents for slow parts (e.g., move gen, evaluation)
- [ ] Use `pybind11` or `cffi` to bind C++ modules into Python
- [ ] Create clean Python wrappers around C++ functions
- [ ] Replace Python versions selectively and benchmark improvements

## 🚀 Phase 7: GUI or Local Play
**Goal:** Make it playable outside the terminal

- [ ] Choose a GUI framework (e.g. `pygame`, `tkinter`, or `PyQt`)
- [ ] Design a basic board UI with move input
- [ ] Connect GUI board state to internal `chess.Board`
- [ ] Enable both human vs bot and bot vs bot modes
- [ ] Optionally add board flip, move history, and evaluation bar

## 🥺 Ongoing: Testing & Evaluation

- [ ] Add unit tests for each component (eval, search, move gen)
- [ ] Create test suites for edge cases (underpromotion, en passant, etc.)
- [ ] Log bot moves and compare with Stockfish
- [ ] Track win rate over time vs human or engine opponents
- [ ] Maintain performance and correctness regressions checks

