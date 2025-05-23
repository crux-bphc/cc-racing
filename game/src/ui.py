import pygame

TABLE_X = 10
TABLE_Y = 10
HEADER_HEIGHT = 25
ROW_HEIGHT = 25
PADDING = 5
TEXT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0, 180)
BORDER_COLOR = (50, 50, 50)
BORDER_THICKNESS = 2


def draw_ui_table(screen, cars, font, show_speed, elapsed_time):

    num_rows = len(cars)
    table_width = 300
    table_height = HEADER_HEIGHT + num_rows * ROW_HEIGHT + PADDING * 2  # Added padding
    table_rect = pygame.Rect(TABLE_X, TABLE_Y, table_width, table_height)

    s = pygame.Surface((table_width, table_height), pygame.SRCALPHA)
    s.fill(BACKGROUND_COLOR)
    screen.blit(s, (TABLE_X, TABLE_Y))
    pygame.draw.rect(screen, BORDER_COLOR, table_rect, BORDER_THICKNESS)

    headers = "No. | Lap | "
    headers += "Speed (m/s)" if show_speed else "Last Lap (s)"
    header_text_surface = font.render(headers, True, TEXT_COLOR)
    screen.blit(header_text_surface, (TABLE_X + PADDING, TABLE_Y + PADDING))

    timer_text = f"Time: {elapsed_time:.2f}s"
    timer_surface = font.render(timer_text, True, TEXT_COLOR)
    screen.blit(
        timer_surface,
        (
            TABLE_X + table_width - timer_surface.get_width() - PADDING,
            TABLE_Y + PADDING,
        ),
    )

    for idx, car in enumerate(cars):
        y_offset = TABLE_Y + HEADER_HEIGHT + idx * ROW_HEIGHT + PADDING

        display_value = ""
        if show_speed:
            display_value = f"{car.speed:.1f}"
        else:
            display_value = (
                f"{car.last_lap_time:.2f}" if car.last_lap_time is not None else "-"
            )

        line = f"{idx + 1:<4} {car.lap:<5} {display_value:>12}"

        car_text_surface = font.render(line, True, car.color)
        screen.blit(car_text_surface, (TABLE_X + PADDING, y_offset))

        if idx < num_rows - 1:
            pygame.draw.line(
                screen,
                BORDER_COLOR,
                (TABLE_X + PADDING, y_offset + ROW_HEIGHT - PADDING),
                (TABLE_X + table_width - PADDING, y_offset + ROW_HEIGHT - PADDING),
                1,
            )
