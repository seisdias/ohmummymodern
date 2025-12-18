# src/config.py
from dataclasses import dataclass

@dataclass(frozen=True)
class GameConfig:
    # Player
    player_start_lives: int = 3
    player_hit_cooldown_ms: int = 900
    player_step_cooldown_ms: int = 120  # si lo quieres aquí, mueve desde Settings

    # Mummies
    mummy_move_cooldown_ms: int = 220

    # Scoring
    treasure_score: int = 100

    # Loot generation (demo)
    treasure_chance: float = 0.08
