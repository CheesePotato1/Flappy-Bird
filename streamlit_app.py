import streamlit as st
import pygame
import numpy as np
import time
from PIL import Image

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

class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = np.random.randint(100, 400)
        self.gap_size = 150
        self.speed = 3
        
    def update(self):
        self.x -= self.speed
        
    def collides_with(self, bird):
        bird_rect = pygame.Rect(bird.x, bird.y, 30, 30)
        top_pipe = pygame.Rect(self.x, 0, 50, self.gap_y)
        bottom_pipe = pygame.Rect(self.x, self.gap_y + self.gap_size, 50, 800)
        return bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe)

def init_game_state():
    if 'bird' not in st.session_state:
        st.session_state.bird = Bird()
    if 'pipes' not in st.session_state:
        st.session_state.pipes = [Pipe(600)]
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'last_update' not in st.session_state:
        st.session_state.last_update = time.time()

def reset_game():
    st.session_state.bird = Bird()
    st.session_state.pipes = [Pipe(600)]
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.game_started = False
    st.session_state.last_update = time.time()

def main():
    st.title("Flappy Bird")
    
    init_game_state()
    
    # Game controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Jump", key="jump"):
            if not st.session_state.game_started:
                st.session_state.game_started = True
            st.session_state.bird.jump()
    with col2:
        if st.button("Reset Game", key="reset"):
            reset_game()
            
    # Game canvas
    canvas = st.empty()
    
    # Game loop
    current_time = time.time()
    dt = current_time - st.session_state.last_update
    st.session_state.last_update = current_time
    
    if not st.session_state.game_over and st.session_state.game_started:
        # Update bird
        st.session_state.bird.update()
        
        # Update pipes
        for pipe in st.session_state.pipes:
            pipe.update()
            
            # Check collisions
            if pipe.collides_with(st.session_state.bird):
                st.session_state.game_over = True
                
        # Remove pipes that are off screen and add new ones
        st.session_state.pipes = [p for p in st.session_state.pipes if p.x > -50]
        if len(st.session_state.pipes) > 0 and st.session_state.pipes[-1].x < 200:
            st.session_state.pipes.append(Pipe(600))
            
        # Update score
        passed_pipe = next((p for p in st.session_state.pipes if p.x < st.session_state.bird.x and p.x > st.session_state.bird.x - 5), None)
        if passed_pipe:
            st.session_state.score += 1
            
        # Check if bird is out of bounds
        if st.session_state.bird.y < 0 or st.session_state.bird.y > 600:
            st.session_state.game_over = True
    
    # Render game state
    screen = pygame.Surface((800, 600))
    screen.fill((135, 206, 235))  # Sky blue background
    
    # Draw pipes
    for pipe in st.session_state.pipes:
        pygame.draw.rect(screen, (34, 139, 34), (pipe.x, 0, 50, pipe.gap_y))  # Top pipe
        pygame.draw.rect(screen, (34, 139, 34), 
                        (pipe.x, pipe.gap_y + pipe.gap_size, 50, 600 - (pipe.gap_y + pipe.gap_size)))  # Bottom pipe
    
    # Draw bird
    pygame.draw.circle(screen, (255, 255, 0), (st.session_state.bird.x, int(st.session_state.bird.y)), 15)
    
    # Convert Pygame surface to PIL Image
    string_image = pygame.image.tostring(screen, 'RGB')
    pil_image = Image.frombytes('RGB', (800, 600), string_image)
    
    # Display game
    canvas.image(pil_image)
    
    # Display score
    st.write(f"Score: {st.session_state.score}")
    
    if st.session_state.game_over:
        st.write("Game Over! Press Reset to play again.")
    
    # Rerun the app
    time.sleep(0.05)
    st.experimental_rerun()

if __name__ == "__main__":
    main()
