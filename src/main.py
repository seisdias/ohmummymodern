# src/main.py
from __future__ import annotations

from enum import Enum, auto
from typing import Optional, List

import pygame

from src.settings import Settings
from src.config import GameConfig
from src.run_settings import RunSettings
from src.game import Game, GameStatus


class AppState(Enum):
    MENU = auto()
    SELECT_DIFFICULTY = auto()
    PLAY = auto()
    GAME_OVER = auto()
    HIGHSCORES = auto()
    OPTIONS = auto()


def _draw_text_screen(
    screen: pygame.Surface,
    font: pygame.font.Font,
    lines: List[str],
    *,
    x: int = 80,
    y0: int = 80,
    line_h: int = 36,
) -> None:
    screen.fill((10, 10, 14))
    y = y0
    for text in lines:
        surf = font.render(text, True, (240, 240, 240))
        screen.blit(surf, (x, y))
        y += line_h
    pygame.display.flip()


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Oh Mummy Modern")

    # Environment / window settings
    s = Settings()
    screen = pygame.display.set_mode((s.screen_w, s.screen_h))
    clock = pygame.time.Clock()

    # Global gameplay config (tuning defaults)
    cfg = GameConfig()

    # App state machine
    state = AppState.MENU
    run = RunSettings(difficulty=3, stage=1)  # default selection
    game: Optional[Game] = None

    game_over_at_ms: int = 0
    last_score: int = 0
    last_stage: int = 1

    # Simple UI font
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        clock.tick(s.fps)
        now_ms = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if state == AppState.PLAY:
                    # Back to menu
                    state = AppState.MENU
                    game = None
                else:
                    # Exit app
                    running = False
                continue

            # State-specific key handling
            if event.type == pygame.KEYDOWN:
                if state == AppState.MENU:
                    if event.key == pygame.K_n:
                        state = AppState.SELECT_DIFFICULTY
                    elif event.key == pygame.K_h:
                        state = AppState.HIGHSCORES
                    elif event.key == pygame.K_o:
                        state = AppState.OPTIONS

                elif state == AppState.SELECT_DIFFICULTY:
                    if pygame.K_1 <= event.key <= pygame.K_5:
                        run.difficulty = event.key - pygame.K_0
                        run.stage = 1
                        game = Game(screen, s, cfg, run)
                        state = AppState.PLAY
                    elif event.key == pygame.K_BACKSPACE:
                        state = AppState.MENU

                elif state in (AppState.HIGHSCORES, AppState.OPTIONS):
                    if event.key in (pygame.K_RETURN, pygame.K_BACKSPACE):
                        state = AppState.MENU

                elif state == AppState.GAME_OVER:
                    if event.key in (pygame.K_RETURN, pygame.K_BACKSPACE):
                        state = AppState.MENU

                elif state == AppState.PLAY:
                    # Forward events to game (e.g., SPACE reveal)
                    if game is not None:
                        game.handle_events(event)


        # Update/render depending on state
        if state == AppState.PLAY and game is not None:
            game.handle_input(now_ms)
            status = game.update(now_ms)
            game.draw()

            if status == GameStatus.GAME_OVER:
                # MVP: vuelve al menú. (Más adelante: pantalla "Game Over" o guardar score)
                last_score = game.score
                last_stage = game.run.stage
                game_over_at_ms = now_ms
                state = AppState.GAME_OVER
                game = None

        else:
            if state == AppState.MENU:
                lines = [
                    "OH MUMMY MODERN",
                    "",
                    "[N] New Game",
                    "[H] High Scores (placeholder)",
                    "[O] Options (placeholder)",
                    "",
                    "ESC: Quit",
                ]
            elif state == AppState.SELECT_DIFFICULTY:
                lines = [
                    "Select difficulty (1=hardest, 5=easiest)",
                    "",
                    "[1] [2] [3] [4] [5]",
                    "",
                    "BACKSPACE: Return",
                ]
            elif state == AppState.HIGHSCORES:
                lines = [
                    "High Scores (placeholder)",
                    "",
                    "ENTER/BACKSPACE: Return",
                ]
            elif state == AppState.GAME_OVER:
                lines = [
                    "GAME OVER",
                    "",
                    f"Score: {last_score}",
                    f"Stage reached: {last_stage}",
                    "",
                    "Press ENTER to return",
                    "(or wait a moment)",
                ]
            else:  # OPTIONS
                lines = [
                    "Options (placeholder)",
                    "",
                    "ENTER/BACKSPACE: Return",
                ]

            if state == AppState.GAME_OVER and (now_ms - game_over_at_ms) >= 10000:
                state = AppState.MENU

            _draw_text_screen(screen, font, lines)

    pygame.quit()


if __name__ == "__main__":
    main()
