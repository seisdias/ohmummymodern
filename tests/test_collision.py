from src.world.collision import any_entity_on_player

def test_collision_true_when_entity_on_player():
    assert any_entity_on_player((3, 3), [(1, 1), (3, 3), (5, 5)]) is True

def test_collision_false_when_no_entity_on_player():
    assert any_entity_on_player((3, 3), [(1, 1), (4, 3), (5, 5)]) is False
