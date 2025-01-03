import streamlit as st
import numpy as np
import random
import time

class FlappyBirdGame:
    def __init__(self, width=400, height=600):
        self.width = width
        self.height = height
        self.reset()
    
    def reset(self):
        # Bird properties
        self.bird_x = self.width // 4
        self.bird_y = self.height // 2  # Start in middle of screen
        self.bird_velocity = 0  # Initial velocity is zero
        self.gravity = 0.5  # Gravity constant
        self.jump_strength = -10  # Upward velocity when jumping
        self.bird_size = 30  # Bird size
        
        # Pipes
        self.pipes = []
        self.spawn_pipe()
        
        # Game state
        self.score = 0
        self.is_game_over = False
        self.last_update_time = time.time()
    
    def spawn_pipe(self):
        # Randomly position pipe opening
        pipe_height = random.randint(100, self.height - 250)
        gap_size = 200  # Size of gap between pipes
        self.pipes.append({
            'x': self.width,
            'top_height': pipe_height,
            'bottom_height': self.height - (pipe_height + gap_size)
        })
    
    def jump(self):
        if not self.is_game_over:
            # Apply upward velocity
            self.bird_velocity = self.jump_strength
    
    def update(self):
        # Calculate time since last update to make gravity consistent
        current_time = time.time()
        time_delta = current_time - self.last_update_time
        self.last_update_time = current_time

        # Apply gravity (increases downward velocity)
        self.bird_velocity += self.gravity * 10  # Multiplied to make gravity more noticeable
        self.bird_y += self.bird_velocity * time_delta * 50  # Scaled for visibility
        
        # Prevent bird from moving too fast
        self.bird_velocity = min(self.bird_velocity, 20)
        
        # Check ground and ceiling collision
        if self.bird_y >= self.height - 50 or self.bird_y <= 0:
            self.is_game_over = True
            return
        
        # Move pipes
        for pipe in self.pipes:
            pipe['x'] -= 5  # Move pipes to the left
            
            # Collision detection
            bird_left = self.bird_x - self.bird_size/2
            bird_right = self.bird_x + self.bird_size/2
            bird_top = self.bird_y - self.bird_size/2
            bird_bottom = self.bird_y + self.bird_size/2
            
            pipe_left = pipe['x']
            pipe_right = pipe['x'] + 50
            
            # Check collision with top pipe
            if (bird_right > pipe_left and bird_left < pipe_right and 
                bird_top < pipe['top_height']):
                self.is_game_over = True
                return
            
            # Check collision with bottom pipe
            if (bird_right > pipe_left and bird_left < pipe_right and 
                bird_bottom > self.height - pipe['bottom_height']):
                self.is_game_over = True
                return
        
        # Remove off-screen pipes
        self.pipes = [p for p in self.pipes if p['x'] > -50]
        
        # Spawn new pipes
        if not self.pipes or self.pipes[-1]['x'] < self.width - 200:
            self.spawn_pipe()
        
        # Update score
        for pipe in self.pipes:
            if pipe['x'] + 50 < self.bird_x and not pipe.get('scored', False):
                self.score += 1
                pipe['scored'] = True

def draw_game(game):
    # Create a blank canvas with sky blue background
    canvas = np.full((game.height, game.width, 3), 135, dtype=np.uint8)
    
    # Draw ground (darker green)
    canvas[game.height-50:, :] = [34, 139, 34]
    
    # Draw pipes
    for pipe in game.pipes:
        # Top pipe (green)
        canvas[:int(pipe['top_height']), pipe['x']:pipe['x']+50] = [0, 255, 0]
        
        # Bottom pipe (green)
        canvas[game.height-int(pipe['bottom_height']):game.height, 
               pipe['x']:pipe['x']+50] = [0, 255, 0]
    
    # Draw bird
    bird_size = game.bird_size
    x1 = max(0, int(game.bird_x - bird_size/2))
    x2 = min(game.width, int(game.bird_x + bird_size/2))
    y1 = max(0, int(game.bird_y - bird_size/2))
    y2 = min(game.height, int(game.bird_y + bird_size/2))
    
    # Red bird
    canvas[y1:y2, x1:x2] = [255, 0, 0]
    
    return canvas

def main():
    st.title("Flappy Bird with Gravity")
    
    # Initialize game state
    if 'game' not in st.session_state:
        st.session_state.game = FlappyBirdGame()
    
    # Game display container
    game_container = st.empty()
    
    # Control columns
    col1, col2 = st.columns(2)
    
    with col1:
        start_button = st.button("Start/Reset Game")
    
    with col2:
        jump_button = st.button("Jump")
    
    # Game logic
    if start_button:
        st.session_state.game.reset()
    
    if jump_button:
        st.session_state.game.jump()
    
    # Only update and draw if game is active
    if not st.session_state.game.is_game_over:
        st.session_state.game.update()
    
    # Draw game
    game_image = draw_game(st.session_state.game)
    game_container.image(game_image, caption=f"Score: {st.session_state.game.score}")
    
    # Game over check
    if st.session_state.game.is_game_over:
        st.error("Game Over!")
        st.write(f"Final Score: {st.session_state.game.score}")

def create_requirements_file():
    with open('requirements.txt', 'w') as f:
        f.write("""
streamlit
numpy
""")

# Create requirements file
create_requirements_file()

# Run the main function
if __name__ == "__main__":
    main()
