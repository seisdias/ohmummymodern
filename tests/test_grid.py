from src.world.grid import Grid

def test_grid_to_world_and_back():
    g = Grid(tile_size=32)

    wx, wy = g.to_world(5, 7)
    assert (wx, wy) == (160, 224)

    gx, gy = g.to_grid(wx, wy)
    assert (gx, gy) == (5, 7)