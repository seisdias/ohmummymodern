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



@dataclass(frozen=True)
class LevelConfig:
    level: int
    map_w_tiles: int
    map_h_tiles: int

    # Dificultad (tiempo real tile-based)
    player_step_cooldown_ms: int
    mummy_move_cooldown_ms: int
    mummy_count: int

    # Loot
    treasure_chance: float


LEVELS: dict[int, LevelConfig] = {
    # Nivel 1 = más difícil: más rápido y más momias.
    1: LevelConfig(1, 55, 40, player_step_cooldown_ms=110, mummy_move_cooldown_ms=180, mummy_count=5, treasure_chance=0.07),
    2: LevelConfig(2, 60, 45, player_step_cooldown_ms=115, mummy_move_cooldown_ms=200, mummy_count=4, treasure_chance=0.075),
    3: LevelConfig(3, 65, 50, player_step_cooldown_ms=120, mummy_move_cooldown_ms=220, mummy_count=3, treasure_chance=0.08),
    4: LevelConfig(4, 70, 55, player_step_cooldown_ms=125, mummy_move_cooldown_ms=240, mummy_count=2, treasure_chance=0.085),
    5: LevelConfig(5, 75, 60, player_step_cooldown_ms=130, mummy_move_cooldown_ms=260, mummy_count=1, treasure_chance=0.09),
}

def level_config(level: int) -> LevelConfig:
    return LEVELS[level]

