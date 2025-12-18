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

    cx, cy = 5, 5
    cross = [(cx, cy), (cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)]

    # Aseguramos determinismo: vaciamos la cruz
    for x, y in cross:
        m.contents[y][x] = CellContent.EMPTY
        m.revealed[y][x] = False

    # Forzamos UN tesoro conocido en el centro
    m.contents[cy][cx] = CellContent.TREASURE

    score1 = reveal_cross(m, cx, cy)
    score2 = reveal_cross(m, cx, cy)

    assert score1 == 100
    assert score2 == 0

