# CHANGELOG

## [Unreleased]

## Alpha [v0.1] - 2020-06-08

### Added

- Added type hints
- Added README, LICENSE, CHANGELOG, requirements.txt and .gitignore
- Added ai.py, board.py
- Added hovering token

### Changed

- Updated to pygame 2.0.0.dev10
- Renamed icon_icon.png to icon.png
- Renamed checker_*.png to token_*.png
- Code was rewritten in order to remove global variables
- Created and implemented Board and Token classes (Replaces 2D List of strings)
- Added score attribute to Player objects
- Renamed config.py to constants.py
- **Logging:**
  - Implemented Path objects instead of strings and os.path
  - A new log is created for each day, and stored in logs/
  - Centered log messages

### Fixed

- Draw function only updates cells that change 
(Previously every cell in the board was rerendered)

### Removed

- Removed display_winner() and end images 
(Will be rendered using vistor.ttf by end_message())
- Removed turn()
- Removed has_won(), ai_turn(). 
(Will be replaced by Board.negamax() and Board.has_won())
