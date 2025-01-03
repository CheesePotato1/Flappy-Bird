import pygame
import sys
import random

pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
SKY_BLUE = (135, 206, 235)
GREEN = (34, 139, 34)
YELLOW = (255, 255, 0)

class Bird:
    def __init__(self):
        self.y = 250
        self.x = 50
        self.vel = 0
        self.gravity = 0.3
        self.jump_strength = -7

    def jump(self):
        self.vel = self.jump_strength

    def update(self):
        self.vel += self.gravity
        self.y += self.vel
        self.y = max(0, min(self.y, HEIGHT - 30))

class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(100, 400)
        self.gap_size = 150
        self.width = 50
        self.speed = 3

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.gap_y))
        pygame.draw.rect(screen, GREEN, 
                        (self.x, self.gap_y + self.gap_size, 
                         self.width, HEIGHT - (self.gap_y + self.gap_size)))

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    bird = Bird()
    pipes = [Pipe(600)]
    game_started = False
    game_over = False
    score = 0
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        # Reset game
                        bird = Bird()
                        pipes = [Pipe(600)]
                        game_started = False
                        game_over = False
                        score = 0
                    else:
                        game_started = True
                        bird.jump()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    game_started = True
                    bird.jump()

        if game_started and not game_over:
            # Update bird
            bird.update()

            # Update and manage pipes
            for pipe in pipes:
                pipe.update()

                # Collision detection
                bird_rect = pygame.Rect(bird.x - 15, bird.y - 15, 30, 30)
                top_pipe = pygame.Rect(pipe.x, 0, pipe.width, pipe.gap_y)
                bottom_pipe = pygame.Rect(pipe.x, pipe.gap_y + pipe.gap_size, 
                                        pipe.width, HEIGHT)

                if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
                    game_over = True

            # Remove off-screen pipes
            pipes = [p for p in pipes if p.x > -50]

            # Add new pipes
            if pipes[-1].x < 300:
                pipes.append(Pipe(800))

            # Update score
            for pipe in pipes:
                if pipe.x == bird.x:
                    score += 1

            # Check boundaries
            if bird.y >= HEIGHT - 30:
                game_over = True

        # Draw everything
        screen.fill(SKY_BLUE)
        
        # Draw pipes
        for pipe in pipes:
            pipe.draw(screen)

        # Draw bird
        pygame.draw.circle(screen, YELLOW, (int(bird.x), int(bird.y)), 15)

        # Draw score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = font.render("Game Over! Press SPACE to restart", True, (255, 255, 255))
            screen.blit(game_over_text, (WIDTH//2 - 180, HEIGHT//2))
        elif not game_started:
            start_text = font.render("Press SPACE or CLICK to start", True, (255, 255, 255))
            screen.blit(start_text, (WIDTH//2 - 150, HEIGHT//2))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
