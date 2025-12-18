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
class DifficultyConfig:
    difficulty: int
    player_step_cooldown_ms: int
    mummy_move_cooldown_ms: int
    mummy_count: int
    mummy_ai_mistake_chance: float = 0.0  # (lo usaremos luego)

DIFFICULTIES: dict[int, DifficultyConfig] = {
    # 1 = más difícil (más rápido y más momias)
    1: DifficultyConfig(1, player_step_cooldown_ms=110, mummy_move_cooldown_ms=180, mummy_count=5),
    2: DifficultyConfig(2, player_step_cooldown_ms=115, mummy_move_cooldown_ms=200, mummy_count=4),
    3: DifficultyConfig(3, player_step_cooldown_ms=120, mummy_move_cooldown_ms=220, mummy_count=3),
    4: DifficultyConfig(4, player_step_cooldown_ms=125, mummy_move_cooldown_ms=240, mummy_count=2),
    5: DifficultyConfig(5, player_step_cooldown_ms=130, mummy_move_cooldown_ms=260, mummy_count=1),
}

def difficulty_config(difficulty: int) -> DifficultyConfig:
    return DIFFICULTIES[difficulty]


@dataclass(frozen=True)
class StageConfig:
    stage: int
    map_w_tiles: int
    map_h_tiles: int
    treasure_chance: float

def stage_config(stage: int) -> StageConfig:
    # MVP: mapas crecen con el stage (profundidad)
    w = 55 + stage * 3
    h = 40 + stage * 2
    # ligera subida de tesoros para “premiar” avanzar (ajustable)
    treasure_chance = min(0.12, 0.07 + stage * 0.005)
    return StageConfig(stage=stage, map_w_tiles=w, map_h_tiles=h, treasure_chance=treasure_chance)


