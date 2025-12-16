import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Number Sum Game")
clock = pygame.time.Clock()

font_large = pygame.font.Font(None, 80)
font_medium = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 36)

WHITE = (255, 255, 255)
GRAY = (180, 180, 180)

modes = {
    "easy": {"count": 5, "speed": 3},
    "medium": {"count": 7, "speed": 4},
    "hard": {"count": 10, "speed": 6}
}

def choose_mode():
    while True:
        screen.fill((20, 20, 40))
        title = font_large.render("Choose Mode", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 180))

        options = [
            ("1 - EASY", (0,255,100)),
            ("2 - MEDIUM", (255,200,0)),
            ("3 - HARD", (255,80,80))
        ]

        for i, (text, color) in enumerate(options):
            label = font_medium.render(text, True, color)
            screen.blit(label, (WIDTH//2 - label.get_width()//2, 300 + i*70))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "easy"
                if event.key == pygame.K_2:
                    return "medium"
                if event.key == pygame.K_3:
                    return "hard"

class FallingNumber:
    def __init__(self, speed):
        self.value = random.randint(1, 9)
        self.x = random.randint(80, WIDTH - 80)
        self.y = random.randint(-300, -50)
        self.speed = speed
        self.color = (
            random.randint(150,255),
            random.randint(150,255),
            random.randint(150,255)
        )

    def move(self):
        self.y += self.speed

    def draw(self):
        text = font_large.render(str(self.value), True, self.color)
        screen.blit(text, (self.x, self.y))

def run_game(mode, score, lives):
    config = modes[mode]
    numbers = [FallingNumber(config["speed"]) for _ in range(config["count"])]
    correct_sum = sum(n.value for n in numbers)

    input_text = ""
    start_time = time.time()
    duration = 10
    paused = False

    while True:
        screen.fill((25, 25, 45))
        pygame.draw.rect(screen, (35,35,65), (0,0,WIDTH,120))

        time_left = max(0, int(duration - (time.time() - start_time)))
        screen.blit(font_small.render(f"Time: {time_left}", True, WHITE), (20, 20))
        screen.blit(font_small.render(f"Mode: {mode.upper()}", True, WHITE), (20, 60))
        screen.blit(font_small.render(f"Score: {score}", True, WHITE), (750, 20))
        screen.blit(font_small.render(f"Lives: {lives}", True, WHITE), (750, 60))

        if not paused:
            for n in numbers:
                n.move()
                n.draw()

        box = pygame.Rect(WIDTH//2 - 170, HEIGHT - 110, 340, 55)
        pygame.draw.rect(screen, WHITE, box, 2, border_radius=12)

        txt = font_medium.render(input_text, True, WHITE)
        screen.blit(txt, (box.x + 15, box.y + 10))
        screen.blit(font_small.render("Enter Sum:", True, GRAY), (box.x, box.y - 30))

        if time_left == 0:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if not paused:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        break
                    elif event.unicode.isdigit():
                        input_text += event.unicode

        pygame.display.update()
        clock.tick(60)

    screen.fill((15, 15, 30))

    if input_text == str(correct_sum):
        score += 1
        result = font_large.render("Correct!", True, (0,255,120))
    else:
        lives -= 1
        result = font_large.render(f"Wrong! Sum = {correct_sum}", True, (255,80,80))

    screen.blit(result, (WIDTH//2 - result.get_width()//2, 260))
    screen.blit(font_small.render("Press ENTER to continue", True, WHITE),
                (WIDTH//2 - 140, 360))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

    return score, lives

score = 0
lives = 3

while lives > 0:
    mode = choose_mode()
    score, lives = run_game(mode, score, lives)

screen.fill((0,0,0))
screen.blit(font_large.render("GAME OVER", True, (255,0,0)),
            (WIDTH//2 - 200, 250))
screen.blit(font_medium.render(f"Final Score: {score}", True, WHITE),
            (WIDTH//2 - 170, 340))

pygame.display.update()
pygame.time.wait(3000)
pygame.quit()
