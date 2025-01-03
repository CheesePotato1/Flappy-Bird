import streamlit as st
import numpy as np
import random

class FlappyBirdGame:
    def __init__(self, width=400, height=600):
        self.width = width
        self.height = height
        self.reset()
    
    def reset(self):
        # Bird properties
        self.bird_x = self.width // 4
        self.bird_y = self.height // 2
        self.bird_velocity = 0
        self.gravity = 0.5
        self.jump_strength = -10
        
        # Pipes
        self.pipes = []
        self.spawn_pipe()
        
        # Game state
        self.score = 0
        self.is_game_over = False
    
    def spawn_pipe(self):
        # Randomly position pipe opening
        pipe_height = random.randint(100, self.height - 200)
        self.pipes.append({
            'x': self.width,
            'height': pipe_height
        })
    
    def jump(self):
        if not self.is_game_over:
            self.bird_velocity = self.jump_strength
    
    def update(self):
        # Apply gravity
        self.bird_velocity += self.gravity
        self.bird_y += self.bird_velocity
        
        # Check ground collision
        if self.bird_y >= self.height or self.bird_y <= 0:
            self.is_game_over = True
        
        # Move pipes
        for pipe in self.pipes:
            pipe['x'] -= 5
            
            # Check pipe collision
            if (self.bird_x < pipe['x'] + 50 and 
                self.bird_x + 20 > pipe['x'] and
                (self.bird_y < pipe['height'] or 
                 self.bird_y > pipe['height'] + 150)):
                self.is_game_over = True
        
        # Remove off-screen pipes
        self.pipes = [p for p in self.pipes if p['x'] > -50]
        
        # Spawn new pipes
        if not self.pipes or self.pipes[-1]['x'] < self.width - 200:
            self.spawn_pipe()
        
        # Update score
        if self.pipes and self.pipes[0]['x'] + 50 < self.bird_x:
            self.score += 1

def draw_game(game):
    # Create a blank canvas
    canvas = np.full((game.height, game.width, 3), 135, dtype=np.uint8)
    
    # Draw ground
    canvas[game.height-50:, :] = [34, 139, 34]
    
    # Draw pipes
    for pipe in game.pipes:
        # Top pipe
        canvas[:pipe['height'], pipe['x']:pipe['x']+50] = [0, 255, 0]
        # Bottom pipe
        canvas[pipe['height']+150:, pipe['x']:pipe['x']+50] = [0, 255, 0]
    
    # Draw bird
    bird_size = 20
    x1 = max(0, game.bird_x - bird_size//2)
    x2 = min(game.width, game.bird_x + bird_size//2)
    y1 = max(0, int(game.bird_y) - bird_size//2)
    y2 = min(game.height, int(game.bird_y) + bird_size//2)
    canvas[y1:y2, x1:x2] = [255, 0, 0]
    
    return canvas

def main():
    st.title("Flappy Bird")
    
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
