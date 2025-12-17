from src.world.player import Player
from src.world.map import TileMap

def test_player_cannot_walk_into_wall():
    m = TileMap.demo(20, 20)
    p = Player(gx=1, gy=1)

    # forzamos una pared en (2,1)
    m.tiles[1][2] = 1
    p.try_step(dx=1, dy=0, tilemap=m)
    assert (p.gx, p.gy) == (1, 1)

def test_player_walks_on_floor():
    m = TileMap.demo(20, 20)
    p = Player(gx=1, gy=1)
    m.tiles[1][2] = 0
    p.try_step(dx=1, dy=0, tilemap=m)
    assert (p.gx, p.gy) == (2, 1)
