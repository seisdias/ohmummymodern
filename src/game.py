# src/game.py
import random

import pygame

from src.config import GameConfig, difficulty_config, stage_config
from src.render.renderer import Renderer
from src.run_settings import RunSettings
from src.settings import Settings
from src.world.camera import Camera
from src.world.collision import any_entity_on_player
from src.world.grid import Grid
from src.world.map import TileMap
from src.world.mummy import Mummy
from src.world.player import Player
from src.world.reveal import reveal_cross
from enum import Enum, auto

class GameStatus(Enum):
    RUNNING = auto()
    GAME_OVER = auto()


class Game:

    def __init__(self, screen: pygame.Surface, settings: Settings, config: GameConfig, run: RunSettings):
        self.screen = screen
        self.s = settings
        self.cfg = config
        self.run = run

        self.grid = Grid(tile_size=self.s.tile_size)
        self.camera = Camera()
        self.renderer = Renderer(screen, self.grid)

        self.score = 0

        self.player = Player(
            gx=3, gy=3,
            lives=self.cfg.player_start_lives,
            hit_cooldown_ms=self.cfg.player_hit_cooldown_ms,
            spawn_gx=3, spawn_gy=3,
        )

        # Construye mapa, salida, momias y world size
        self.build_stage(self.run.stage)

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            gained = reveal_cross(
                self.tilemap,
                self.player.gx,
                self.player.gy,
                treasure_score=self.cfg.treasure_score,
            )
            self.score += gained

    def handle_input(self, now_ms: int) -> None:
        keys = pygame.key.get_pressed()
        dc = difficulty_config(self.run.difficulty)
        if now_ms - self.player.last_step_ms < dc.player_step_cooldown_ms:
            return

        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1

        if dx != 0 or dy != 0:
            self.player.try_step(dx=dx, dy=dy, tilemap=self.tilemap)
            self.player.last_step_ms = now_ms

    def update(self, now_ms: int) -> GameStatus:
        ts = self.s.tile_size
        target_x = self.player.gx * ts + ts // 2
        target_y = self.player.gy * ts + ts // 2

        self.camera.follow_and_clamp(
            target_x=target_x,
            target_y=target_y,
            screen_w=self.s.screen_w,
            screen_h=self.s.screen_h,
            world_w=self.world_w_px,
            world_h=self.world_h_px,
        )

        for m in self.mummies:
            m.update(
                tilemap=self.tilemap,
                player_gx=self.player.gx,
                player_gy=self.player.gy,
                now_ms=now_ms,
            )

        # Colisión: si alguna momia está en la casilla del jugador
        mummy_positions = [(m.gx, m.gy) for m in self.mummies]
        if any_entity_on_player((self.player.gx, self.player.gy), mummy_positions):
            self.player.take_hit(now_ms)
            if self.player.lives <= 0:
                return GameStatus.GAME_OVER

        # Si llega a la salida, siguiente nivel
        if (self.player.gx, self.player.gy) == (self.exit_gx, self.exit_gy):
            self.run.stage += 1
            self.build_stage(self.run.stage)

        return GameStatus.RUNNING

    def draw(self) -> None:
        self.renderer.draw_world(
            tilemap=self.tilemap,
            player=self.player,
            camera=self.camera,
            score=self.score,
            mummies=self.mummies,
            exit_pos=(self.exit_gx, self.exit_gy),
            stage=self.run.stage,
            difficulty=self.run.difficulty,
        )
        pygame.display.flip()

    def build_stage(self, stage: int) -> None:
        dc = difficulty_config(self.run.difficulty)
        sc = stage_config(stage)

        self.tilemap = TileMap.demo(
            sc.map_w_tiles,
            sc.map_h_tiles,
            seed=1000 + stage,
            treasure_chance=sc.treasure_chance,
        )

        self.world_w_px = self.tilemap.w * self.s.tile_size
        self.world_h_px = self.tilemap.h * self.s.tile_size

        # spawn jugador
        self.player.spawn_gx, self.player.spawn_gy = 3, 3
        self.player.gx, self.player.gy = self.player.spawn_gx, self.player.spawn_gy

        # salida (MVP)
        self.exit_gx, self.exit_gy = self._find_walkable_near(self.tilemap.w - 4, self.tilemap.h - 4)

        # momias según dificultad
        rng = random.Random(2000 + stage + self.run.difficulty * 100)
        self.mummies = []
        for _ in range(dc.mummy_count):
            gx, gy = self._random_walkable_far_from_player(rng, min_dist=12)
            self.mummies.append(Mummy(gx=gx, gy=gy, move_cooldown_ms=dc.mummy_move_cooldown_ms))

    def _find_walkable_near(self, gx: int, gy: int) -> tuple[int, int]:
        # búsqueda en “anillos” alrededor del punto
        for r in range(0, 12):
            for dy in range(-r, r + 1):
                for dx in range(-r, r + 1):
                    x, y = gx + dx, gy + dy
                    if 0 <= x < self.tilemap.w and 0 <= y < self.tilemap.h and self.tilemap.is_walkable(x, y):
                        return x, y
        # fallback
        return 3, 3

    def _random_walkable_far_from_player(self, rng: random.Random, min_dist: int) -> tuple[int, int]:
        for _ in range(500):
            x = rng.randrange(1, self.tilemap.w - 1)
            y = rng.randrange(1, self.tilemap.h - 1)
            if not self.tilemap.is_walkable(x, y):
                continue
            if abs(x - self.player.gx) + abs(y - self.player.gy) < min_dist:
                continue
            if (x, y) == (self.exit_gx, self.exit_gy):
                continue
            return x, y
        return 10, 10



