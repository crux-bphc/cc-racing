import pygame
import sys
import json

from game.src import SCREEN_HEIGHT, SCREEN_WIDTH, FPS, Track, Car, draw_ui_table
from game.src.utils import load_ai

show_debug = False
show_speed = True

countdown_timer = -1
race_started = False


def main():
    global show_debug, show_speed, countdown_timer, race_started
    with open("config.json") as f:
        cfg = json.load(f)

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("game/assets/bgm.mp3")
    pygame.mixer.music.set_volume(0.25)
    pygame.mixer.music.play(-1)  # loop forever

    font = pygame.font.SysFont(None, 24)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("CRUx CC Racing")
    clock = pygame.time.Clock()

    track = Track(cfg["track_image"], cfg["checkpoints"])
    cars = [
        Car(
            c["start_x"],
            c["start_y"],
            c["sprite"],
            c["color"],
            load_ai(c["ai_path"])[0],
            load_ai(c["ai_path"])[1],
        )
        for c in cfg["cars"]
    ]

    time_font = pygame.font.SysFont(None, 48)
    race_timer = 0.0

    is_muted = False

    while True:
        dt = clock.tick(FPS) / 1000.0

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_d:
                    show_debug = not show_debug
                elif e.key == pygame.K_t:
                    show_speed = not show_speed
                elif (
                    e.key == pygame.K_SPACE and countdown_timer < 0 and not race_started
                ):
                    s = pygame.mixer.Sound("game/assets/start.mp3")
                    s.set_volume(0.5)
                    s.play(loops=0)

                    countdown_timer = 3.0
                elif e.key == pygame.K_m:
                    is_muted = not is_muted
                    if is_muted:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

        if countdown_timer >= 0:
            countdown_timer -= dt
            if countdown_timer <= 0:
                countdown_timer = -1
                race_started = True
                race_timer = 0.0
        elif race_started:
            race_timer += dt
            for car in cars:
                car.update(track, dt)

        screen.fill((0, 0, 0))
        track.draw(screen)
        for car in cars:
            car.draw(screen, show_debug=show_debug)
            if show_debug:
                for pt in track.checkpoints:
                    pygame.draw.circle(screen, (255, 255, 0), pt, 5)
                for ep in car.sensor_endpoints.values():
                    pygame.draw.circle(screen, (255, 0, 0), ep, 3)
                    pygame.draw.line(screen, (0, 255, 0), car.sensor_origin, ep, 2)

        if not race_started:
            if countdown_timer >= 0:
                count = str(int(countdown_timer) + 1)
            else:
                count = "Press SPACE to Start"
            text = time_font.render(count, True, (255, 255, 0))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 20))
        else:
            timer_text = time_font.render(f"{race_timer:.1f}", True, (255, 255, 0))
            screen.blit(
                timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, 20)
            )

        draw_ui_table(screen, cars, font, show_speed, race_timer)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
