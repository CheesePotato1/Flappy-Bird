import streamlit as st
import numpy as np
import random

class FlappyBirdGame:
    def __init__(self, width=400, height=600):
        self.width = width
        self.height = height
        self.bird_size = 30
        self.reset()
    
    def reset(self):
        # Bird starting position
        self.bird_x = self.width // 4
        self.bird_y = self.height // 2
        
        # Physics variables
        self.vertical_speed = 0
        self.gravity = 100  # EXTREME GRAVITY
        
        # Game state
        self.pipes = []
        self.score = 0
        self.is_game_over = False
        
        # Spawn initial pipe
        self.spawn_pipe()
    
    def spawn_pipe(self):
        # Create a pipe with a random height
        gap_height = 200  # Size of the gap
        pipe_height = random.randint(100, self.height - gap_height - 100)
        
        self.pipes.append({
            'x': self.width,
            'top_height': pipe_height,
            'bottom_height': self.height - (pipe_height + gap_height)
        })
    
    def jump(self):
        # Give upward velocity when jumping (POSITIVE 50)
        self.vertical_speed = 50  # Upward push
    
    def update(self):
        # Apply EXTREME gravity (increase downward speed)
        self.vertical_speed -= self.gravity
        self.bird_y += self.vertical_speed
        
        # Check ground collision
        if self.bird_y >= self.height - 50:
            self.is_game_over = True
            return
        
        # Move pipes
        for pipe in self.pipes:
            pipe['x'] -= 5  # Move pipes to the left
            
            # Collision detection
            if (self.bird_x + self.bird_size/2 > pipe['x'] and 
                self.bird_x - self.bird_size/2 < pipe['x'] + 50):
                # Check top pipe collision
                if self.bird_y - self.bird_size/2 < pipe['top_height']:
                    self.is_game_over = True
                    return
                
                # Check bottom pipe collision
                if self.bird_y + self.bird_size/2 > self.height - pipe['bottom_height']:
                    self.is_game_over = True
                    return
        
        # Remove old pipes
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
    # Create canvas
    canvas = np.full((game.height, game.width, 3), 135, dtype=np.uint8)
    
    # Draw ground
    canvas[game.height-50:, :] = [34, 139, 34]
    
    # Draw pipes
    for pipe in game.pipes:
        # Top pipe
        canvas[:int(pipe['top_height']), pipe['x']:pipe['x']+50] = [0, 255, 0]
        
        # Bottom pipe
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
    st.title("Flappy Bird EXTREME Gravity")
    
    # Initialize game state
    if 'game' not in st.session_state:
        st.session_state.game = FlappyBirdGame()
    
    # Game display
    game_container = st.empty()
    
    # Controls
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
    
    # Update game if not game over
    if not st.session_state.game.is_game_over:
        st.session_state.game.update()
    
    # Draw game
    game_image = draw_game(st.session_state.game)
    game_container.image(game_image, caption=f"Score: {st.session_state.game.score}")
    
    # Game over check
    if st.session_state.game.is_game_over:
        st.error("Game Over!")
        st.write(f"Final Score: {st.session_state.game.score}")

# Create requirements file
def create_requirements_file():
    with open('requirements.txt', 'w') as f:
        f.write("streamlit\nnumpy")

create_requirements_file()

# Run main function
if __name__ == "__main__":
    main()
