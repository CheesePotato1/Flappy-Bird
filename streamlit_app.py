import streamlit as st
import numpy as np
import random

class FlappyBirdGame:
    def __init__(self, width=400, height=600):
        self.width = width
        self.height = height
        self.reset()
    
    def reset(self):
        # Bird starting position
        self.bird_y = self.height // 2
        
        # Physics variables
        self.velocity = 0
        self.gravity = 0.5
        
        # Game state
        self.score = 0
        self.game_over = False
    
    def jump(self):
        # Upward velocity when jumping
        self.velocity = -5
    
    def update(self):
        # Apply gravity
        self.velocity += self.gravity
        self.bird_y += self.velocity
        
        # Boundary checks
        if self.bird_y >= self.height or self.bird_y <= 0:
            self.game_over = True

def draw_bird(height, bird_y):
    # Create a canvas
    canvas = np.full((height, 400, 3), 135, dtype=np.uint8)
    
    # Draw ground
    canvas[height-50:, :] = [34, 139, 34]
    
    # Draw bird (red square)
    bird_size = 30
    x1 = 50
    x2 = x1 + bird_size
    y1 = int(bird_y) - bird_size // 2
    y2 = int(bird_y) + bird_size // 2
    
    # Ensure bird is within canvas bounds
    y1 = max(0, y1)
    y2 = min(height, y2)
    
    canvas[y1:y2, x1:x2] = [255, 0, 0]
    
    return canvas

def main():
    st.title("Simple Gravity Simulation")
    
    # Initialize game if not already initialized
    if 'game' not in st.session_state:
        st.session_state.game = FlappyBirdGame()
    
    # Game display
    game_container = st.empty()
    
    # Controls
    col1, col2 = st.columns(2)
    
    with col1:
        start_button = st.button("Reset")
    
    with col2:
        jump_button = st.button("Jump")
    
    # Game logic
    if start_button:
        st.session_state.game.reset()
    
    if jump_button:
        st.session_state.game.jump()
    
    # Update and draw game if not over
    if not st.session_state.game.game_over:
        st.session_state.game.update()
    
    # Draw game
    game_image = draw_bird(
        st.session_state.game.height, 
        st.session_state.game.bird_y
    )
    game_container.image(game_image, caption=f"Bird Y: {st.session_state.game.bird_y:.2f}")
    
    # Game over check
    if st.session_state.game.game_over:
        st.error("Game Over!")

# Run main function
if __name__ == "__main__":
    main()
