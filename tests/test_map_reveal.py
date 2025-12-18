from src.world.map import TileMap, CellContent

def test_reveal_marks_cell_and_returns_content():
    m = TileMap.demo(20, 20, seed=1)
    gx, gy = 2, 2

    assert m.is_revealed(gx, gy) is False
    found = m.reveal(gx, gy)
    assert m.is_revealed(gx, gy) is True
    assert found in (CellContent.EMPTY, CellContent.TREASURE)

def test_reveal_twice_returns_empty_second_time():
    m = TileMap.demo(20, 20, seed=1)
    gx, gy = 2, 2

    _ = m.reveal(gx, gy)
    found2 = m.reveal(gx, gy)
    assert found2 == CellContent.EMPTY
