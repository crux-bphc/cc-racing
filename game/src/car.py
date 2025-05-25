import os
import pygame
import math


class Car:
    def __init__(self, x, y, sprite_path, color, params, ai_logic, size=25):
        img = pygame.image.load(
            os.path.join("game", "assets", sprite_path)
        ).convert_alpha()
        w = size
        h = int(img.get_height() * (w / img.get_width()))
        self.original_image = pygame.transform.smoothscale(img, (w, h))
        self.w, self.h = w, h
        self.image = self.original_image
        self.mask = pygame.mask.from_surface(self.original_image)
        self.x, self.y = x, y
        self.angle = 90
        self.speed = 0
        self.lap = 0
        self.checkpoint_index = 0
        self.color = color
        self.params = params
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.validate_and_adjust_params()

        self.ai_logic = ai_logic
        self.sensor_endpoints = {}
        self.sensor_origin = (x, y)

        # Trail: list of dicts with position and alpha
        self.trail = []
        self.trail_fade_rate = 100  # alpha units per second
        self.trail_interval = 0.05  # seconds between trail points
        self._trail_timer = 0
        self.last_lap_time = None

        self.engine_sound = pygame.mixer.Sound(
            os.path.join("game", "assets", "engine.wav")
        )
        self.engine_sound.set_volume(0.4)
        self.engine_channel = self.engine_sound.play(loops=-1)
        self.engine_channel.pause()  # Start paused

    def update(self, track, dt, is_muted=False):
        old = (self.x, self.y, self.angle, self.speed)
        sensor_data, endpoints, origin = self.read_sensors(track)
        self.sensor_endpoints = endpoints
        self.sensor_origin = origin
        controls = self.ai_logic(sensor_data, self.speed)

        throttle = max(-1, min(controls.get("throttle", 0), 1))
        self.speed += throttle * self.params["accel"] * dt

        if abs(throttle) < 0.01:
            if self.speed > 0:
                self.speed = max(self.speed - 0.1 * dt, 0)
            elif self.speed < 0:
                self.speed = min(self.speed + 0.1 * dt, 0)

        speed_ratio = abs(self.speed) / self.params["top_speed"]
        self.engine_channel.set_volume(0.6 + 0.4 * speed_ratio)

        if is_muted or self.speed < 10:
            self.engine_channel.pause()
        else:
            self.engine_channel.unpause()

        self.speed = max(
            -self.params["top_speed"], min(self.speed, self.params["top_speed"])
        )

        steering = max(-1, min(controls.get("steering", 0), 1))
        self.angle = (self.angle + steering * self.params["turn"] * dt) % 360

        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(self.x, self.y))

        rad = math.radians(self.angle)
        self.x += math.sin(rad) * self.speed * dt
        self.y -= math.cos(rad) * self.speed * dt

        # Collision
        self.rect.center = (self.x, self.y)
        offset = (int(self.rect.left), int(self.rect.top))
        if track.orange_mask.overlap(self.mask, offset) or track.white_mask.overlap(
            self.mask, offset
        ):
            # self.speed = -old[3] * 0.75
            if abs(self.speed) > 5:
                self.speed = -old[3] * 0.3
                self.x, self.y, self.angle = old[0], old[1], old[2]
            self.image = pygame.transform.rotate(self.original_image, -self.angle)
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect(center=(self.x, self.y))

        self.check_lap_progress(track)

        # Trail
        self._trail_timer += dt
        if self._trail_timer >= self.trail_interval:
            self._trail_timer -= self.trail_interval
            rad = math.radians(self.angle)
            fx = math.sin(rad)
            fy = -math.cos(rad)

            bx = self.x - fx * (self.h / 2)
            by = self.y - fy * (self.h / 2)
            px = -fy
            py = fx
            offset = (self.w * 0.7) / 2
            left_wheel = (int(bx + px * offset), int(by + py * offset))
            right_wheel = (int(bx - px * offset), int(by - py * offset))
            for wheel_pos in (left_wheel, right_wheel):
                self.trail.append({"pos": wheel_pos, "alpha": 255})

        # fade
        for pt in self.trail:
            pt["alpha"] -= self.trail_fade_rate * dt
        self.trail = [pt for pt in self.trail if pt["alpha"] > 0]

    def draw(self, screen, show_debug=False):
        # draw trail
        for pt in self.trail:
            alpha = max(0, min(255, int(pt["alpha"])))
            size = 1
            surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (25, 25, 25, alpha / 2), (size, size), size)
            x, y = pt["pos"]
            screen.blit(surf, (x - size, y - size))

        # draw sensors
        if show_debug:
            for endpoint in self.sensor_endpoints.values():
                pygame.draw.line(screen, (0, 255, 0), self.sensor_origin, endpoint, 2)

        # draw car
        screen.blit(self.image, self.rect)

    def read_sensors(self, track):
        sensor_data = {}
        endpoints = {}
        max_dist = self.params["sensor_dist"]
        rad = math.radians(self.angle)
        ox = self.x + math.sin(rad) * (self.h / 2)
        oy = self.y - math.cos(rad) * (self.h / 2)
        origin = (int(ox), int(oy))

        for name, offset_deg in [("front", 0), ("left", -45), ("right", 45)]:
            ray_angle = math.radians(self.angle + offset_deg)
            dist = 0
            hit = False
            while dist < max_dist:
                dist += 2
                rx = ox + math.sin(ray_angle) * dist
                ry = oy - math.cos(ray_angle) * dist
                if (
                    rx < 0
                    or ry < 0
                    or rx >= track.rect.width
                    or ry >= track.rect.height
                ):
                    break
                if track.track_mask.get_at((int(rx), int(ry))) == 0:
                    hit = True
                    break
            endpt = (
                int(ox + math.sin(ray_angle) * dist),
                int(oy - math.cos(ray_angle) * dist),
            )
            sensor_data[name] = dist if hit else max_dist
            endpoints[name] = endpt

        return sensor_data, endpoints, origin

    def check_lap_progress(self, track):
        if self.checkpoint_index < len(track.checkpoints):
            cx, cy = track.checkpoints[self.checkpoint_index]
            if math.hypot(self.x - cx, self.y - cy) < 100:
                self.checkpoint_index += 1
                if self.checkpoint_index == len(track.checkpoints):
                    self.lap += 1
                    self.last_lap_time = pygame.time.get_ticks() / 1000.0 - self.lap
                    self.checkpoint_index = 0

    def validate_and_adjust_params(self):
        if (
            self.params["top_speed"]
            + self.params["accel"]
            + self.params["turn"]
            + self.params["sensor_dist"]
            > 30
        ):
            raise ValueError(
                f"The sum of top_speed, accel, turn and sensor_dist must be less than or equal to 30 for car {self.color}."
            )

        if (
            self.params["top_speed"] < 0
            or self.params["accel"] < 0
            or self.params["turn"] < 0
            or self.params["sensor_dist"] < 0
        ):
            raise ValueError(
                f"All parameters must be non-negative for car {self.color}."
            )

        self.params["top_speed"] = 100 + self.params["top_speed"] * 10
        self.params["accel"] = 10 + self.params["accel"] * 5
        self.params["turn"] = 100 + self.params["turn"] * 5
        self.params["sensor_dist"] = 100 + self.params["sensor_dist"] * 12

        print(self.color, self.params)
