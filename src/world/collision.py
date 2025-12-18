# src/world/collision.py
from typing import Iterable, Tuple

Coord = Tuple[int, int]

def any_entity_on_player(player_pos: Coord, entities: Iterable[Coord]) -> bool:
    px, py = player_pos
    for ex, ey in entities:
        if (ex, ey) == (px, py):
            return True
    return False
