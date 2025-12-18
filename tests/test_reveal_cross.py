from src.world.map import TileMap, CellContent
from src.world.reveal import reveal_cross


def test_reveal_cross_reveals_center_and_neighbors():
    m = TileMap.demo(10, 10, seed=1)

    cx, cy = 5, 5
    reveal_cross(m, cx, cy)

    assert m.is_revealed(cx, cy)
    assert m.is_revealed(cx + 1, cy)
    assert m.is_revealed(cx - 1, cy)
    assert m.is_revealed(cx, cy + 1)
    assert m.is_revealed(cx, cy - 1)


def test_reveal_cross_scores_treasures_only_once():
    m = TileMap.demo(10, 10, seed=1)

    # Forzamos un tesoro conocido
    m.contents[5][5] = CellContent.TREASURE

    score1 = reveal_cross(m, 5, 5)
    score2 = reveal_cross(m, 5, 5)

    assert score1 == 100
    assert score2 == 0
