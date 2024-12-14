import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Demo")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

MAX_RADIUS = 100

class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / mag, self.y / mag)

class Circle:
    def __init__(self, x, y, radius, color):
        self.position = Vector2D(x, y)
        self.radius = radius
        self.velocity = Vector2D(random.uniform(-2, 2), random.uniform(-2, 2))
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)

    def update(self):
        self.position += self.velocity
        self.check_boundaries()

    def check_boundaries(self):
        if self.position.x - self.radius < 0:
            self.position.x = self.radius
            self.velocity.x *= -1
        if self.position.x + self.radius > WIDTH:
            self.position.x = WIDTH - self.radius
            self.velocity.x *= -1
        if self.position.y - self.radius < 0:
            self.position.y = self.radius
            self.velocity.y *= -1
        if self.position.y + self.radius > HEIGHT:
            self.position.y = HEIGHT - self.radius
            self.velocity.y *= -1

    def is_colliding(self, other):
        distance = (self.position - other.position).magnitude()
        return distance < self.radius + other.radius

    def merge_or_bounce(self, other):
        if self.color == other.color:
            total_area = math.pi * self.radius**2 + math.pi * other.radius**2
            new_radius = math.sqrt(total_area / math.pi)
            if new_radius > MAX_RADIUS:
                new_radius = MAX_RADIUS
            self.radius = new_radius
            other.radius = 0
            other.velocity = Vector2D(0, 0)
        else:
            collision_vector = self.position - other.position
            collision_normal = collision_vector.normalize()
            overlap = self.radius + other.radius - collision_vector.magnitude()

            self.position += collision_normal * (overlap / 2)
            other.position -= collision_normal * (overlap / 2)

            self.velocity, other.velocity = other.velocity, self.velocity

def create_random_circles(num_circles):
    circles = []
    colors = [RED, BLUE, GREEN, YELLOW, PURPLE]
    for _ in range(num_circles):
        x = random.randint(100, WIDTH - 100)
        y = random.randint(100, HEIGHT - 100)
        radius = random.randint(20, 50)
        color = random.choice(colors)
        circles.append(Circle(x, y, radius, color))
    return circles

circles = create_random_circles(10)

running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for i, circle1 in enumerate(circles):
        if circle1.radius > 0:
            circle1.update()
            for j, circle2 in enumerate(circles):
                if i != j and circle2.radius > 0 and circle1.is_colliding(circle2):
                    circle1.merge_or_bounce(circle2)

    for circle in circles:
        if circle.radius > 0:
            circle.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
