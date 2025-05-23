import pygame
import sys
import json

from game.src import SCREEN_HEIGHT, SCREEN_WIDTH, FPS, Track, Car, draw_ui_table


show_debug = False
show_speed = True

countdown_timer = -1
race_started = False


def load_ai(path):
    import importlib.util

    spec = importlib.util.spec_from_file_location("ai_module", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    if not hasattr(mod, "ai_step"):
        raise ValueError(f"AI module {path} does not have an 'ai_step' function.")
    if not callable(mod.ai_step):
        raise ValueError(f"AI module {path} 'ai_step' is not callable.")

    if not hasattr(mod, "TOP_SPEED"):
        raise ValueError(f"AI module {path} does not define 'TOP_SPEED'.")
    if not hasattr(mod, "ACCELARATION"):
        raise ValueError(f"AI module {path} does not define 'ACCELARATION'.")
    if not hasattr(mod, "TURN_SPEED"):
        raise ValueError(f"AI module {path} does not define 'TURN_SPEED'.")
    if not hasattr(mod, "SENSOR_RANGE"):
        raise ValueError(f"AI module {path} does not define 'SENSOR_RANGE'.")

    params = {
        "top_speed": mod.TOP_SPEED,
        "accel": mod.ACCELARATION,
        "turn": mod.TURN_SPEED,
        "sensor_dist": mod.SENSOR_RANGE,
    }
    return params, mod.ai_step


def main():
    global show_debug, show_speed, countdown_timer, race_started
    with open("config.json") as f:
        cfg = json.load(f)

    pygame.init()
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

    while True:
        dt = clock.tick(FPS) / 1000.0
        keys = pygame.key.get_pressed()

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
                    countdown_timer = 3.0

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
