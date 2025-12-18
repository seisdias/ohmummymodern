from src.config import difficulty_config, stage_config

def test_difficulty_1_is_harder_than_5():
    d1 = difficulty_config(1)
    d5 = difficulty_config(5)
    assert d1.mummy_count > d5.mummy_count
    assert d1.mummy_move_cooldown_ms < d5.mummy_move_cooldown_ms

def test_stage_grows_maps():
    s1 = stage_config(1)
    s5 = stage_config(5)
    assert s5.map_w_tiles > s1.map_w_tiles
    assert s5.map_h_tiles > s1.map_h_tiles
