import pygame
import random
import time
import math
from typing import *
from quantumtester.reg import set_reg
import win32gui
import win32con

BALL_RADIUS = 20
BACKGROUND_COLOR = (0, 0, 0)
BALL_COLOR = (255, 0, 0)
GAME_DURATION_SECONDS = 20


def bring_to_foreground(window_title: str) -> None:
    """
    Bring the specified window to the foreground using its title.

    Args:
        window_title (str): The title of the window to bring to the foreground.
    """
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        # Bring the window to the topmost layer
        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOPMOST,
            0,
            0,
            0,
            0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
        )
        # Remove the topmost flag
        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_NOTOPMOST,
            0,
            0,
            0,
            0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
        )


def render_multiline_text(
    surface: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color: Tuple[int, ...],
    position: Tuple[int, ...],
    opacity: int = 255,
) -> None:
    """
    Render multiline text on a Pygame surface with a specified font, color, position, and opacity.

    Args:
        surface (pygame.Surface): The Pygame surface to render the text on.
        text (str): The multiline text to render.
        font (pygame.font.Font): The font to use for rendering.
        color (tuple): The color (R, G, B) for the text.
        position (tuple): The position (x, y) of the top-left corner of the rendered text.
        opacity (int, optional): The opacity of the text (0-255). Defaults to 255 (fully opaque).
    """
    text_surface = pygame.Surface(
        (surface.get_width(), surface.get_height()), pygame.SRCALPHA
    )

    lines = text.split("\n")
    line_height = font.get_linesize()
    for i, line in enumerate(lines):
        text_line = font.render(line, True, color)
        text_surface.blit(text_line, (0, i * line_height))

    text_surface.set_alpha(opacity)
    surface.blit(text_surface, position)


def run_game(value: int, static_text: str, iterations: int) -> float:
    """
    Run the game with specified parameters multiple times and return the average accuracy.

    Args:
        value (int): The Win32PrioritySeparation value to set.
        static_text (str): The static text to display on the game window.
        iterations (int): The number of round iterations to run.

    Returns:
        float: The average accuracy of mouse pointer time on the ball.
    """
    accuracies = []

    for x in range(iterations):
        ball_speed = 350 if x + 1 == iterations else 250
        ball_radius = 15
        direction_change_frequency = 6000 // 2 if x + 1 == iterations else 6000

        set_reg(value)

        pygame.init()
        font_file = "data/Arial.ttf"
        font_size = 18
        font = pygame.font.Font(font_file, font_size)

        info = pygame.display.Info()
        screen = pygame.display.set_mode(
            (info.current_w, info.current_h), pygame.FULLSCREEN
        )
        window_title = f"{value} ({x + 1} of {iterations})"
        pygame.display.set_caption(window_title)
        bring_to_foreground(window_title)
        time.sleep(0.5)

        ball_x = random.randint(ball_radius, info.current_w - ball_radius)
        ball_y = random.randint(ball_radius, info.current_h - ball_radius)
        direction_change_counter = random.randint(0, direction_change_frequency)
        # Initialize ball movement direction
        ball_direction = [random.uniform(-1, 1), random.uniform(-1, 1)]
        # Normalize the direction vector
        length = (ball_direction[0] ** 2 + ball_direction[1] ** 2) ** 0.5
        ball_direction[0] /= length
        ball_direction[1] /= length

        start_time = time.time()
        last_frame_time = start_time
        time_on_ball = 0

        running = True
        while running:
            current_time = time.time()
            frame_time = current_time - last_frame_time
            last_frame_time = current_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Update game time and check for end condition
            elapsed_time = current_time - start_time
            if elapsed_time >= GAME_DURATION_SECONDS:
                break

            # Ball movement logic
            ball_x += ball_direction[0] * ball_speed * frame_time
            ball_y += ball_direction[1] * ball_speed * frame_time

            # Collisions
            if ball_x - ball_radius <= 0 or ball_x + ball_radius >= info.current_w:
                ball_direction[0] *= -1
            if ball_y - ball_radius <= 0 or ball_y + ball_radius >= info.current_h:
                ball_direction[1] *= -1

            screen.fill(BACKGROUND_COLOR)
            pygame.draw.circle(
                screen, BALL_COLOR, (int(ball_x), int(ball_y)), ball_radius
            )
            render_multiline_text(
                screen, static_text, font, (255, 255, 255), (10, 10), opacity=60
            )

            pygame.display.flip()

            # Change direction at random intervals
            direction_change_counter -= frame_time * 1000
            if direction_change_counter <= 0:
                ball_direction = [random.uniform(-1, 1), random.uniform(-1, 1)]
                length = (ball_direction[0] ** 2 + ball_direction[1] ** 2) ** 0.5
                ball_direction[0] /= length
                ball_direction[1] /= length
                direction_change_counter = random.randint(0, direction_change_frequency)

            # Track mouse
            mouse_x, mouse_y = pygame.mouse.get_pos()
            distance = math.sqrt((mouse_x - ball_x) ** 2 + (mouse_y - ball_y) ** 2)
            if distance <= ball_radius:
                time_on_ball += frame_time

        pygame.quit()

        accuracy = (time_on_ball / elapsed_time) * 100
        accuracies.append(accuracy)

    average_accuracy = sum(accuracies) / len(accuracies)
    return average_accuracy
