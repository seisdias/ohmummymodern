from src.world.player import Player
from src.world.map import TileMap

def test_player_take_hit_decrements_lives_and_respawns():
    m = TileMap.demo(20, 20, seed=1)
    p = Player(gx=10, gy=10, spawn_gx=3, spawn_gy=3, lives=3)

    p.take_hit(now_ms=1000)
    assert p.lives == 2
    assert (p.gx, p.gy) == (3, 3)

def test_player_hit_cooldown_prevents_multiple_hits():
    p = Player(gx=10, gy=10, spawn_gx=3, spawn_gy=3, lives=3, hit_cooldown_ms=900)

    p.take_hit(now_ms=1000)
    p.take_hit(now_ms=1500)  # 500ms después, aún en cooldown

    assert p.lives == 2  # no baja a 1
