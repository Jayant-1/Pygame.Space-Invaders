import pygame
import random
import time

pygame.font.init()

WIDTH, HEIGHT = 1280, 720
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
VAL = 6

pygame.display.set_caption("Space Invaders")

# -------------------------------- load image -------------------------------- #

RED_SMALL_SPACE_SHIP = pygame.image.load("assets/pixel_ship_red_small.png")
GREEN_SMALL_SPACE_SHIP = pygame.image.load("assets/pixel_ship_green_small.png")
BLUE_SMALL_SPACE_SHIP = pygame.image.load("assets/pixel_ship_blue_small.png")

# -------------------------------- player ship ------------------------------- #

YELLOW_SPACE_SHIP = pygame.image.load("assets/pixel_ship_yellow.png")

# -------------------------------- Background -------------------------------- #

BG = pygame.transform.scale(pygame.image.load("assets/5.jpg"), (WIDTH, HEIGHT))

# ---------------------------------- lasers ---------------------------------- #

REd_LASER = pygame.image.load("assets/pixel_laser_red.png")
GREEN_LASER = pygame.image.load("assets/pixel_laser_green.png")
BLUE_LASER = pygame.image.load("assets/pixel_laser_blue.png")
YELLOW_LASER = pygame.image.load("assets/pixel_laser_yellow.png")

# ----------------------------------- Fonts ---------------------------------- #

MAIN_FONT = pygame.font.SysFont("comicsans", 30)
LOST_FONT = pygame.font.SysFont("comicsans", 70)


class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health


class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SMALL_SPACE_SHIP, REd_LASER),
        "green": (GREEN_SMALL_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SMALL_SPACE_SHIP, BLUE_LASER),
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel


def main():
    run = True
    level = 1
    live = 3
    enemies = []
    wave_length = 5
    enemy_vel = 5
    lost = False
    lost_count = 0
    clock = pygame.time.Clock()

    player = Player((WIDTH // 2) - 50, HEIGHT - 100)

    def redraw_window():
        WIN.blit(BG, (0, 0))
        lives_label = MAIN_FONT.render(f"Lives: {live}", 1, "white")
        level_label = MAIN_FONT.render(f"Level: {level}", 1, "white")

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = LOST_FONT.render("You Lost!!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):
                run = False

        if live <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(
                    random.randrange(50, WIDTH - 100),
                    random.randrange(-1500, -100),
                    random.choice(["red", "blue", "green"]),
                )
                enemies.append(enemy)

        redraw_window()
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):
                run = False
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT or key[pygame.K_a]] and player.x > 0:
                player.x -= VAL
            if key[pygame.K_RIGHT or pygame.K_d] and player.x < WIDTH - player.get_width():
                player.x += VAL
            if (key[pygame.K_UP or key[pygame.K_w]]
            and player.y + player.get_height() > player.get_height() + 50):
                player.y -= VAL
            if (
            key[pygame.K_DOWN or key[pygame.K_s]]
            and player.y < HEIGHT - player.get_height()):
                player.y += VAL
            if key[pygame.K_SPACE]:
                player.health -= 10

        for enemy in enemies:
            enemy.move(enemy_vel)
            if enemy.y + enemy.get_height() > HEIGHT:
                live -= 1
                enemies.remove(enemy)

        pygame.display.update()


if __name__ == "__main__":
    main()
