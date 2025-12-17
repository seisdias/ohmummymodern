from src.world.camera import Camera

def test_camera_clamps_to_world_bounds():
    cam = Camera()
    cam.follow_and_clamp(
        target_x=10_000, target_y=10_000,
        screen_w=200, screen_h=100,
        world_w=500, world_h=300
    )
    assert cam.x == 500 - 200
    assert cam.y == 300 - 100
