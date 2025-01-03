import streamlit as st
import pygame
import numpy as np
from PIL import Image
import time

FPS = 60
FRAME_TIME = 1.0 / FPS

class Bird:
    def __init__(self):
        self.y = 250
        self.x = 50
        self.vel = 0
        self.gravity = 0.3
        self.jump_strength = -7
        
    def jump(self):
        if not st.session_state.game_over:
            self.vel = self.jump_strength
        
    def update(self):
        if not st.session_state.game_over and st.session_state.game_started:
            self.vel += self.gravity
            self.y += self.vel
            # Keep bird within bounds
            self.y = max(0, min(self.y, 600))

class Pipe:
    MIN_GAP_Y = 100
    MAX_GAP_Y = 400
    GAP_SIZE = 150
    WIDTH = 50
    SPEED = 3
    
    def __init__(self, x):
        self.x = x
        self.gap_y = np.random.randint(self.MIN_GAP_Y, self.MAX_GAP_Y)
        
    def update(self):
        if not st.session_state.game_over:
            self.x -= self.SPEED
        
    def collides_with(self, bird):
        bird_rect = pygame.Rect(bird.x - 15, bird.y - 15, 30, 30)
        top_pipe = pygame.Rect(self.x, 0, self.WIDTH, self.gap_y)
        bottom_pipe = pygame.Rect(
            self.x, 
            self.gap_y + self.GAP_SIZE, 
            self.WIDTH, 
            600 - (self.gap_y + self.GAP_SIZE)
        )
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
    if 'last_frame_time' not in st.session_state:
        st.session_state.last_frame_time = time.time()

def reset_game():
    st.session_state.bird = Bird()
    st.session_state.pipes = [Pipe(600)]
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.game_started = False
    st.session_state.last_frame_time = time.time()

def update_game_state():
    try:
        # Update bird
        st.session_state.bird.update()
        
        # Update and manage pipes
        for pipe in st.session_state.pipes:
            pipe.update()
            
            # Check collisions
            if pipe.collides_with(st.session_state.bird):
                st.session_state.game_over = True
                return
                
        # Remove off-screen pipes
        st.session_state.pipes = [p for p in st.session_state.pipes if p.x > -Pipe.WIDTH]
        
        # Add new pipes with proper spacing
        if len(st.session_state.pipes) > 0 and st.session_state.pipes[-1].x < 300:
            st.session_state.pipes.append(Pipe(800))
            
        # Update score
        for pipe in st.session_state.pipes:
            if pipe.x == st.session_state.bird.x:
                st.session_state.score += 1
                
        # Check boundaries
        if st.session_state.bird.y <= 0 or st.session_state.bird.y >= 600:
            st.session_state.game_over = True
            
    except Exception as e:
        st.error(f"Game error: {str(e)}")
        st.session_state.game_over = True

def render_game(canvas):
    # Initialize pygame surface
    screen = pygame.Surface((800, 600))
    screen.fill((135, 206, 235))  # Sky blue background
    
    # Draw pipes
    for pipe in st.session_state.pipes:
        pygame.draw.rect(screen, (34, 139, 34), 
                        (pipe.x, 0, Pipe.WIDTH, pipe.gap_y))  # Top pipe
        pygame.draw.rect(screen, (34, 139, 34), 
                        (pipe.x, pipe.gap_y + Pipe.GAP_SIZE, 
                         Pipe.WIDTH, 600 - (pipe.gap_y + Pipe.GAP_SIZE)))  # Bottom pipe
    
    # Draw bird
    pygame.draw.circle(screen, (255, 255, 0), 
                      (st.session_state.bird.x, int(st.session_state.bird.y)), 15)
    
    # Convert to PIL Image
    string_image = pygame.image.tostring(screen, 'RGB')
    pil_image = Image.frombytes('RGB', (800, 600), string_image)
    
    # Update canvas
    canvas.image(pil_image)

def main():
    st.title("Flappy Bird")
    
    # Initialize game state
    init_game_state()
    
    # Game controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Jump", key="jump") or st.session_state.get("space_pressed", False):
            if not st.session_state.game_started:
                st.session_state.game_started = True
            st.session_state.bird.jump()
    with col2:
        if st.button("Reset Game", key="reset"):
            reset_game()
            
    # Create persistent canvas
    canvas = st.empty()
    
    # Game loop with fixed time step
    current_time = time.time()
    delta_time = current_time - st.session_state.last_frame_time
    
    if delta_time >= FRAME_TIME:
        st.session_state.last_frame_time = current_time
        if not st.session_state.game_over and st.session_state.game_started:
            update_game_state()
    
    # Render game
    render_game(canvas)
    
    # Display score and game over message
    st.write(f"Score: {st.session_state.score}")
    if st.session_state.game_over:
        st.write("Game Over! Press Reset to play again.")
    
    # Maintain frame rate
    time.sleep(max(0, FRAME_TIME - delta_time))
    st.experimental_rerun()

if __name__ == "__main__":
    main()
