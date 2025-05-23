import os
import pygame
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Track:
    def __init__(self, path_image, checkpoints):
        self.image = pygame.image.load(
            os.path.join("game", "assets", path_image)
        ).convert()
        self.image = pygame.transform.smoothscale(
            self.image, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        # orange border mask
        orange = (228, 76, 28)
        tol = (30, 30, 30)
        self.orange_mask = pygame.mask.from_threshold(self.image, orange, tol)

        # white border mask
        white = (255, 255, 255)
        white_tol = (20, 20, 20)
        self.white_mask = pygame.mask.from_threshold(self.image, white, white_tol)

        # blue track mask
        blue = (166, 206, 205)
        blue_tol = (30, 30, 30)
        self.track_mask = pygame.mask.from_threshold(self.image, blue, blue_tol)

        self.rect = self.image.get_rect()
        self.checkpoints = checkpoints

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
