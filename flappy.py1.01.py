import pygame
import random
import sys

# 1. INITIALIZE PYGAME
pygame.init()

# 2. GAME CONSTANTS
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Colors (RGB)
SKY_BLUE = (113, 197, 207)
YELLOW = (247, 216, 50)
GREEN = (115, 191, 46)
WHITE = (255, 255, 255)
DARK_GREEN = (83, 137, 33)

# 3. SET UP DISPLAY
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird (Python)")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30, bold=True)

# 4. GAME OBJECT CLASSES
class Bird:
    def __init__(self):
        self.x = 80
        self.y = SCREEN_HEIGHT // 2
        self.radius = 16
        self.gravity = 0.5
        self.lift = -8
        self.velocity = 0

    def update(self):
        self.velocity += self.gravity
        self.y += int(self.velocity)
        
        if self.y < self.radius:
            self.y = self.radius
            self.velocity = 0

    def flap(self):
        self.velocity = self.lift

    def draw(self):
        # Draw the yellow bird
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, WHITE, (self.x + 8, self.y - 4), 4)
        pygame.draw.circle(screen, (0, 0, 0), (self.x + 9, self.y - 4), 1.5)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)


class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.width = 65
        self.gap = 140
        self.top_height = random.randint(50, SCREEN_HEIGHT - self.gap - 100)
        self.bottom_y = self.top_height + self.gap
        self.bottom_height = SCREEN_HEIGHT - self.bottom_y
        self.speed = 3
        self.passed = False

    def update(self):
        self.x -= self.speed

    def draw(self):
        # 1. Top pipe column & lip
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.top_height))
        pygame.draw.rect(screen, DARK_GREEN, (self.x - 3, self.top_height - 20, self.width + 6, 20))
        
        # 2. Bottom pipe column & lip
        pygame.draw.rect(screen, GREEN, (self.x, self.bottom_y, self.width, self.bottom_height))
        pygame.draw.rect(screen, DARK_GREEN, (self.x - 3, self.bottom_y, self.width + 6, 20))

    def get_rects(self):
        top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        bottom_rect = pygame.Rect(self.x, self.bottom_y, self.width, self.bottom_height)
        return top_rect, bottom_rect


# 5. MAIN GAME LOOP UTILITIES
def check_collision(bird, pipes):
    if bird.y + bird.radius >= SCREEN_HEIGHT:
        return True
        
    bird_rect = bird.get_rect()
    for pipe in pipes:
        top_rect, bottom_rect = pipe.get_rects()
        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            return True
    return False

def show_score(score):
    score_surface = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surface, (10, 10))

def main():
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    spawn_pipe_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_pipe_event, 1500)
    
    game_active = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird.flap()
                if event.key == pygame.K_SPACE and not game_active:
                    bird = Bird()
                    pipes = [Pipe()]
                    score = 0
                    game_active = True

            if event.type == spawn_pipe_event and game_active:
                pipes.append(Pipe())

        if game_active:
            bird.update()
            
            for pipe in pipes:
                pipe.update()
                
                if not pipe.passed and pipe.x + pipe.width < bird.x:
                    pipe.passed = True
                    score += 1
            
            pipes = [pipe for pipe in pipes if pipe.x > -pipe.width]

            if check_collision(bird, pipes):
                game_active = False

        screen.fill(SKY_BLUE)
        
        for pipe in pipes:
            pipe.draw()
            
        bird.draw()
        show_score(score)

        if not game_active:
            game_over_surface = font.render("GAME OVER - Press SPACE", True, (200, 30, 30))
            text_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(game_over_surface, text_rect)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
