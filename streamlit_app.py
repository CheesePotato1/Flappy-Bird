import streamlit as st
import random
import time
import numpy as np
import cv2

class FlappyBirdGame:
    def __init__(self):
        # Game constants
        self.WIDTH = 400
        self.HEIGHT = 600
        self.BIRD_RADIUS = 20
        self.PIPE_WIDTH = 50
        self.PIPE_GAP = 200
        
        # Game state variables
        self.reset()
    
    def reset(self):
        # Bird position and physics
        self.bird_y = self.HEIGHT // 2
        self.bird_velocity = 0
        self.gravity = 0.5
        self.jump_strength = -10
        
        # Pipes
        self.pipes = []
        self.spawn_pipe()
        
        # Game state
        self.is_active = True
        self.is_game_over = False
        self.score = 0
    
    def spawn_pipe(self):
        # Randomly position pipe opening
        pipe_height = random.randint(100, self.HEIGHT - 100 - self.PIPE_GAP)
        self.pipes.append({
            'x': self.WIDTH,
            'top_height': pipe_height,
            'bottom_height': self.HEIGHT - (pipe_height + self.PIPE_GAP)
        })
    
    def update(self):
        if not self.is_active or self.is_game_over:
            return
        
        # Apply gravity to bird
        self.bird_velocity += self.gravity
        self.bird_y += self.bird_velocity
        
        # Check for ground collision
        if self.bird_y >= self.HEIGHT or self.bird_y <= 0:
            self.is_game_over = True
            self.is_active = False
            return
        
        # Move pipes
        for pipe in self.pipes:
            pipe['x'] -= 5
            
            # Check collision with pipes
            if (pipe['x'] < self.BIRD_RADIUS * 2 and 
                pipe['x'] + self.PIPE_WIDTH > 0):
                # Check vertical collision
                if (self.bird_y < pipe['top_height'] or 
                    self.bird_y > self.HEIGHT - pipe['bottom_height']):
                    self.is_game_over = True
                    self.is_active = False
                    return
        
        # Remove off-screen pipes and spawn new ones
        self.pipes = [p for p in self.pipes if p['x'] > -self.PIPE_WIDTH]
        
        # Spawn new pipes
        if not self.pipes or self.pipes[-1]['x'] < self.WIDTH - 200:
            self.spawn_pipe()
        
        # Update score
        for pipe in self.pipes:
            if pipe['x'] + self.PIPE_WIDTH < self.BIRD_RADIUS * 2:
                self.score += 1
    
    def jump(self):
        if self.is_active and not self.is_game_over:
            self.bird_velocity = self.jump_strength

def draw_game(game):
    # Create a blank canvas
    canvas = np.zeros((game.HEIGHT, game.WIDTH, 3), dtype=np.uint8)
    canvas.fill(135)  # Sky blue background
    
    # Draw ground
    cv2.rectangle(canvas, 
                  (0, game.HEIGHT - 50), 
                  (game.WIDTH, game.HEIGHT), 
                  (34, 139, 34), 
                  -1)  # Green ground
    
    # Draw pipes
    for pipe in game.pipes:
        # Top pipe
        cv2.rectangle(canvas, 
                      (int(pipe['x']), 0), 
                      (int(pipe['x'] + game.PIPE_WIDTH), int(pipe['top_height'])), 
                      (0, 255, 0), 
                      -1)
        
        # Bottom pipe
        cv2.rectangle(canvas, 
                      (int(pipe['x']), int(game.HEIGHT - pipe['bottom_height'])), 
                      (int(pipe['x'] + game.PIPE_WIDTH), game.HEIGHT), 
                      (0, 255, 0), 
                      -1)
    
    # Draw bird
    cv2.circle(canvas, 
               (int(game.BIRD_RADIUS), int(game.bird_y)), 
               game.BIRD_RADIUS, 
               (255, 0, 0), 
               -1)
    
    return canvas

def main():
    st.title("Flappy Bird Clone")
    
    # Initialize game state in session
    if 'game' not in st.session_state:
        st.session_state.game = FlappyBirdGame()
    
    # Game area
    game_container = st.empty()
    
    # Control buttons
    col1, col2 = st.columns(2)
    
    with col1:
        start_button = st.button("Start Game")
    
    with col2:
        jump_button = st.button("Jump")
    
    # Game logic
    if start_button:
        st.session_state.game.reset()
    
    if jump_button and st.session_state.game.is_active:
        st.session_state.game.jump()
    
    # Game loop
    if st.session_state.game.is_active:
        # Update game state
        st.session_state.game.update()
        
        # Draw game
        game_container.image(draw_game(st.session_state.game), 
                              caption=f"Score: {st.session_state.game.score}", 
                              use_column_width=True)
        
        # Check for game over
        if st.session_state.game.is_game_over:
            st.error("Game Over!")
            st.write(f"Final Score: {st.session_state.game.score}")
    
    # Refresh game state
    time.sleep(0.1)
    st.experimental_rerun()

if __name__ == "__main__":
    main()

# Generate requirements file
def create_requirements_txt():
    requirements = """
streamlit
numpy
opencv-python-headless
"""
    with open('requirements.txt', 'w') as f:
        f.write(requirements)

create_requirements_txt()
