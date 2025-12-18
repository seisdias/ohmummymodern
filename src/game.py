# src/game.py
import random

import pygame

from src.settings import Settings
from src.config import GameConfig, level_config
from src.world.grid import Grid
from src.world.camera import Camera
from src.world.map import TileMap, CellContent
from src.world.player import Player
from src.render.renderer import Renderer
from src.world.reveal import reveal_cross
from src.world.mummy import Mummy
from src.world.collision import any_entity_on_player







class Game:
    def __init__(self, screen: pygame.Surface, settings: Settings, config: GameConfig):

        self.level = 1
        self.screen = screen
        self.s = settings
        self.cfg = config

        self.grid = Grid(tile_size=self.s.tile_size)
        self.tilemap = TileMap.demo(
            self.s.map_w_tiles,
            self.s.map_h_tiles,
            treasure_chance=self.cfg.treasure_chance,
        )

        self.player = Player(
            gx=3,
            gy=3,
            lives=self.cfg.player_start_lives,
            hit_cooldown_ms=self.cfg.player_hit_cooldown_ms,
            spawn_gx=3,
            spawn_gy=3,
        )

        self.build_level(self.level)

        self.mummies = [
            Mummy(gx=15, gy=15, move_cooldown_ms=self.cfg.mummy_move_cooldown_ms)
        ]
        self.camera = Camera()

        self.renderer = Renderer(screen, self.grid)

        self.world_w_px = self.tilemap.w * self.s.tile_size
        self.world_h_px = self.tilemap.h * self.s.tile_size

        self.score = 0

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
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
        lc = level_config(self.level)
        if now_ms - self.player.last_step_ms < lc.player_step_cooldown_ms:
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

    def update(self, now_ms: int) -> None:
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

        now_ms = pygame.time.get_ticks()
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

        # Si llega a la salida, siguiente nivel
        if (self.player.gx, self.player.gy) == (self.exit_gx, self.exit_gy):
            self.level += 1
            if self.level > 5:
                # MVP: reinicia al nivel 1 (luego hacemos pantalla de victoria)
                self.level = 1
            self.build_level(self.level)
            return

    def draw(self) -> None:
        self.renderer.draw_world(
            tilemap=self.tilemap,
            player=self.player,
            camera=self.camera,
            score=self.score,
            mummies=self.mummies,
            exit_pos=(self.exit_gx, self.exit_gy),
            level=self.level,
        )
        pygame.display.flip()

    def build_level(self, level: int) -> None:
        lc = level_config(level)

        # mapa demo por ahora (luego lo sustituimos por procedural)
        self.tilemap = TileMap.demo(
            lc.map_w_tiles,
            lc.map_h_tiles,
            seed=1000 + level,
            treasure_chance=lc.treasure_chance,
        )

        # tamaños del mundo en píxeles
        self.world_w_px = self.tilemap.w * self.s.tile_size
        self.world_h_px = self.tilemap.h * self.s.tile_size

        # spawn jugador (simple)
        self.player.spawn_gx, self.player.spawn_gy = 3, 3
        self.player.gx, self.player.gy = self.player.spawn_gx, self.player.spawn_gy

        # salida (objetivo): cerca de esquina opuesta; si no es caminable, buscamos una cercana
        self.exit_gx, self.exit_gy = self._find_walkable_near(self.tilemap.w - 4, self.tilemap.h - 4)

        # momias
        rng = random.Random(2000 + level)
        self.mummies = []
        for _ in range(lc.mummy_count):
            gx, gy = self._random_walkable_far_from_player(rng, min_dist=12)
            self.mummies.append(Mummy(gx=gx, gy=gy, move_cooldown_ms=lc.mummy_move_cooldown_ms))

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

