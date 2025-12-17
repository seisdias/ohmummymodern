# src/main.py
import pygame

from src.settings import Settings
from src.game import Game

def main() -> None:
    pygame.init()
    pygame.display.set_caption("Oh Mummy Modern (Hito 0)")

    s = Settings()
    screen = pygame.display.set_mode((s.screen_w, s.screen_h))
    clock = pygame.time.Clock()

    game = Game(screen, s)

    running = True
    while running:
        dt = clock.tick(s.fps)
        now_ms = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        game.handle_input(now_ms)
        game.update()
        game.draw()

    pygame.quit()

if __name__ == "__main__":
    main()
