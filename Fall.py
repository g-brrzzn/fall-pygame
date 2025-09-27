import pygame
import sys
from random import randint, uniform
from dataclasses import dataclass
from typing import Tuple, List
from pygame.math import Vector2
from pygame.locals import QUIT, KEYDOWN, K_y, K_t, K_o, K_k, K_m

WINDOW_SIZE = (800, 600)
FPS = 120
INITIAL_DENSITY = 600
SPEED_SCALER = 100.0

EFFECT_SETTINGS = {
    "snow":  {"gravity": 0.3, "wind": 0.3,  "color": (150, 150, 150)},
    "rain":  {"gravity": 3.0, "wind": -1.0, "color": (60, 60, 150)},
    "laser": {"gravity": -2.0, "wind": 0.0,  "color": (170, 30, 30)},
}

@dataclass
class Drop:
    pos: Vector2
    fall_speed: float
    depth: float
    radius: int

class ParticleSystem:
    def __init__(self, amount: int, window_size: Tuple[int, int]):
        self.window_width, self.window_height = window_size
        self.drops: List[Drop] = []
        self.set_density(amount)

    def _make_drop(self) -> Drop:
        depth = uniform(0.0, 1.0)
        x = uniform(0, self.window_width)
        y = uniform(-self.window_height * 0.2, self.window_height)  
        base_speed = uniform(0.2, 1.2)
        fall_speed = base_speed * (0.5 + depth)
        radius = max(1, int(1 + depth * 3))
        return Drop(pos=Vector2(x, y), fall_speed=fall_speed, depth=depth, radius=radius)

    def create_drops(self, amount: int) -> None:
        self.drops = [self._make_drop() for _ in range(amount)]

    def add_drops(self, n: int) -> None:
        for _ in range(n):
            self.drops.append(self._make_drop())

    def remove_drops(self, n: int) -> None:
        if n <= 0:
            return
        del self.drops[-n:]

    def set_density(self, amount: int) -> None:
        amount = max(0, int(amount))
        cur = len(self.drops)
        if amount == cur:
            return
        if amount > cur:
            self.add_drops(amount - cur)
        else:
            self.remove_drops(cur - amount)

    def update(self, gravity: float, wind: float, dt: float) -> None:
        dt = min(dt, 0.05)
        for drop in self.drops:
            depth_factor = 0.5 + drop.depth 
            drop.pos.y += (gravity * depth_factor + drop.fall_speed) * SPEED_SCALER * dt
            drop.pos.x += wind * (0.3 + 0.7 * drop.depth) * SPEED_SCALER * dt

            if drop.pos.y > self.window_height + 50:
                drop.pos.y = uniform(-50, -5)
                drop.pos.x = uniform(0, self.window_width)
                drop.depth = uniform(0.0, 1.0)
                drop.radius = max(1, int(1 + drop.depth * 3))
                drop.fall_speed = uniform(0.2, 1.2) * (0.5 + drop.depth)

            if drop.pos.x > self.window_width + 50:
                drop.pos.x = -10
            elif drop.pos.x < -50:
                drop.pos.x = self.window_width + 10
            if drop.pos.y > self.window_height + 50:
                drop.pos.y = -10
            elif drop.pos.y < -50:
                drop.pos.y = self.window_height + 10


    def draw(self, surf: pygame.Surface, color: Tuple[int, int, int], mode: str) -> None:
        if mode == "rain":
            for drop in self.drops:
                length = int(2 + drop.fall_speed * 6 + drop.depth * 4)
                x = int(drop.pos.x)
                y = int(drop.pos.y)
                end_y = y - length
                pygame.draw.line(surf, color, (x, y), (x, end_y), max(1, drop.radius))
        elif mode == "laser":
            for drop in self.drops:
                x, y = int(drop.pos.x), int(drop.pos.y)
                pygame.draw.circle(surf, color, (x, y), max(1, drop.radius + 1))
        else: 
            for drop in self.drops:
                pygame.draw.circle(surf, color, (int(drop.pos.x), int(drop.pos.y)), drop.radius)

def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()

    density = INITIAL_DENSITY
    effect_mode = "snow"

    particle_system = ParticleSystem(density, WINDOW_SIZE)
    mode_keys = {K_o: "snow", K_k: "rain", K_m: "laser"}

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_y:
                    density += 20
                    particle_system.set_density(density)
                if event.key == K_t:
                    density = max(0, density - 20)
                    particle_system.set_density(density)
                if event.key in mode_keys:
                    effect_mode = mode_keys[event.key]

        current_settings = EFFECT_SETTINGS[effect_mode]
        particle_system.update(
            gravity=current_settings["gravity"],
            wind=current_settings["wind"],
            dt=dt
        )

        screen.fill((10, 10, 20))
        particle_system.draw(screen, color=current_settings["color"], mode=effect_mode)

        caption = (
            f"FallPygame | FPS: {int(clock.get_fps())} | "
            f"Density: {len(particle_system.drops)} | Mode: {effect_mode.capitalize()}"
        )
        pygame.display.set_caption(caption)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
