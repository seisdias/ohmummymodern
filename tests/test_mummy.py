from src.world.map import TileMap, TileKind
from src.world.mummy import choose_step_towards, Mummy

def test_choose_step_towards_moves_right_when_player_right():
    m = TileMap.demo(20, 20, seed=1)

    dx, dy = choose_step_towards(m, mx=5, my=5, px=8, py=5)
    assert (dx, dy) == (1, 0)

def test_choose_step_towards_avoids_wall():
    m = TileMap.demo(20, 20, seed=1)

    # Bloqueamos el paso directo a la derecha
    m.tiles[5][6] = TileKind.WALL

    dx, dy = choose_step_towards(m, mx=5, my=5, px=8, py=5)
    assert (dx, dy) != (1, 0)

def test_mummy_update_respects_cooldown():
    m = TileMap.demo(20, 20, seed=1)
    mummy = Mummy(gx=5, gy=5, move_cooldown_ms=200)

    mummy.update(tilemap=m, player_gx=8, player_gy=5, now_ms=1000)
    pos1 = (mummy.gx, mummy.gy)

    # Aún en cooldown
    mummy.update(tilemap=m, player_gx=8, player_gy=5, now_ms=1100)
    pos2 = (mummy.gx, mummy.gy)

    assert pos2 == pos1

    # Ya fuera de cooldown
    mummy.update(tilemap=m, player_gx=8, player_gy=5, now_ms=1300)
    pos3 = (mummy.gx, mummy.gy)

    assert pos3 != pos1
