from src.config import level_config

def test_level_1_is_harder_than_level_5_by_speed_and_mummies():
    l1 = level_config(1)
    l5 = level_config(5)

    assert l1.mummy_count > l5.mummy_count
    assert l1.mummy_move_cooldown_ms < l5.mummy_move_cooldown_ms
    assert l1.player_step_cooldown_ms < l5.player_step_cooldown_ms

def test_maps_grow_with_level():
    l2 = level_config(2)
    l4 = level_config(4)

    assert l4.map_w_tiles > l2.map_w_tiles
    assert l4.map_h_tiles > l2.map_h_tiles
