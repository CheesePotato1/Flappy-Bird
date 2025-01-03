import streamlit as st
import numpy as np
import time
from PIL import Image, ImageDraw
from streamlit.components.v1 import html

# Add JavaScript to handle spacebar
def add_spacebar_listener():
    html("""
        <script>
        document.addEventListener('keydown', function(e) {
            if (e.code === 'Space') {
                e.preventDefault();
                const jumpButton = document.querySelector('button[kind="secondary"]');
                if (jumpButton) jumpButton.click();
            }
        });
        </script>
    """)

# Game difficulty settings
DIFFICULTY_SETTINGS = {
    'easy': {
        'GRAVITY': 0.5,
        'JUMP_VELOCITY': -8,
        'PIPE_SPEED': 3,
        'PIPE_GAP': 140,  # Original Flappy Bird gap size
        'PIPE_SPAWN_TIME': 2,
        'COLOR': 'green'
    },
    'medium': {
        'GRAVITY': 0.6,
        'JUMP_VELOCITY': -9,
        'PIPE_SPEED': 4,
        'PIPE_GAP': 120,
        'PIPE_SPAWN_TIME': 1.8,
        'COLOR': 'green'
    },
    'hard': {
        'GRAVITY': 0.7,
        'JUMP_VELOCITY': -10,
        'PIPE_SPEED': 5,
        'PIPE_GAP': 100,
        'PIPE_SPAWN_TIME': 1.5,
        'COLOR': 'green'
    }
}

# Constants
GAME_WIDTH = 400
GAME_HEIGHT = 600

# Initialize game state
if 'game_state' not in st.session_state:
    st.session_state.game_state = {
        'bird_y': 200,
        'bird_velocity': 0,
        'pipes': [],
        'score': 0,
        'game_over': False,
        'game_active': False,
        'high_score': {'easy': 0, 'medium': 0, 'hard': 0},
        'difficulty': 'medium'
    }

def create_pipe_image(width, height, is_top=True):
    pipe = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(pipe)
    
    # Original Flappy Bird pipe colors
    pipe_color = (96, 184, 31)      # Light green
    pipe_shadow = (82, 158, 26)     # Darker green
    pipe_highlight = (116, 208, 37)  # Lighter green
    
    # Main pipe body
    draw.rectangle([0, 0, width-4, height], fill=pipe_color)
    draw.rectangle([width-4, 0, width, height], fill=pipe_shadow)
    
    # Pipe cap
    cap_height = 26
    if is_top:
        cap_y = height - cap_height
    else:
        cap_y = 0
        
    draw.rectangle([-4, cap_y, width+4, cap_y + cap_height], fill=pipe_color)
    draw.rectangle([width, cap_y, width+4, cap_y + cap_height], fill=pipe_shadow)
    draw.rectangle([-4, cap_y, width+4, cap_y + 3], fill=pipe_highlight)

    return pipe

def create_bird_image(size):
    bird = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bird)
    
    # Original Flappy Bird colors
    body_color = (255, 203, 48)  # Yellow-orange
    wing_color = (212, 156, 35)  # Darker orange
    face_color = (241, 141, 41)  # Orange for beak
    
    # Main body
    draw.rectangle([4, 4, size-4, size-4], fill=body_color)
    # Wing
    draw.rectangle([6, size//2, size//2, size-6], fill=wing_color)
    # Eye (white)
    draw.ellipse([size//1.5, size//4, size-6, size//2], fill='white')
    # Eye (black)
    draw.ellipse([size//1.4, size//3.5, size-8, size//2.2], fill='black')
    # Beak
    draw.polygon([(size-6, size//2), (size-2, size//1.8), (size-6, size//1.5)], fill=face_color)
    
    return bird

def create_background():
    bg = Image.new('RGB', (GAME_WIDTH, GAME_HEIGHT), (78, 192, 202))  # Light blue
    draw = ImageDraw.Draw(bg)
    
    # Add clouds (simple white shapes)
    cloud_color = (255, 255, 255)
    for i in range(0, GAME_WIDTH, 120):
        y_pos = np.random.randint(50, 150)
        draw.ellipse([i, y_pos, i+60, y_pos+30], fill=cloud_color)
    
    # Add ground (original green color)
    ground_color = (221, 216, 148)  # Beige ground
    draw.rectangle([0, GAME_HEIGHT-70, GAME_WIDTH, GAME_HEIGHT], fill=ground_color)
    
    return bg

def create_game_frame():
    # Create background
    frame = create_background()
    
    # Get bird image
    bird = create_bird_image(40)
    bird = bird.rotate(-st.session_state.game_state['bird_velocity'] * 2)  # Tilt based on velocity
    
    # Paste bird onto frame
    bird_x = 100 - 20
    bird_y = int(st.session_state.game_state['bird_y']) - 20
    frame.paste(bird, (bird_x, bird_y), bird)
    
    # Add pipes
    for pipe in st.session_state.game_state['pipes']:
        # Top pipe
        top_height = pipe['height']
        if top_height > 0:
            top_pipe = create_pipe_image(50, top_height, True)
            frame.paste(top_pipe, (int(pipe['x']), 0), top_pipe)
        
        # Bottom pipe
        bottom_height = GAME_HEIGHT - (pipe['height'] + DIFFICULTY_SETTINGS[st.session_state.game_state['difficulty']]['PIPE_GAP'])
        if bottom_height > 0:
            bottom_pipe = create_pipe_image(50, bottom_height, False)
            frame.paste(bottom_pipe, (int(pipe['x']), pipe['height'] + DIFFICULTY_SETTINGS[st.session_state.game_state['difficulty']]['PIPE_GAP']), bottom_pipe)
    
    # Add score
    draw = ImageDraw.Draw(frame)
    draw.text((GAME_WIDTH//2 - 20, 50), str(st.session_state.game_state['score']), 
              fill='white', size=40)
    
    return frame

def reset_game():
    st.session_state.game_state['bird_y'] = 200
    st.session_state.game_state['bird_velocity'] = 0
    st.session_state.game_state['pipes'] = []
    st.session_state.game_state['score'] = 0
    st.session_state.game_state['game_over'] = False
    st.session_state.game_state['game_active'] = True

def update_game():
    if not st.session_state.game_state['game_active']:
        return

    difficulty = st.session_state.game_state['difficulty']
    settings = DIFFICULTY_SETTINGS[difficulty]

    # Update bird position
    st.session_state.game_state['bird_velocity'] += settings['GRAVITY']
    st.session_state.game_state['bird_y'] += st.session_state.game_state['bird_velocity']

    # Update pipes
    for pipe in st.session_state.game_state['pipes']:
        pipe['x'] -= settings['PIPE_SPEED']
        
        if pipe['x'] == 98 and not pipe.get('scored', False):
            st.session_state.game_state['score'] += 1
            pipe['scored'] = True

    # Remove off-screen pipes
    st.session_state.game_state['pipes'] = [p for p in st.session_state.game_state['pipes'] 
                                          if p['x'] > -60]

    # Spawn new pipes
    if not st.session_state.game_state['pipes'] or \
       st.session_state.game_state['pipes'][-1]['x'] < GAME_WIDTH - 200:
        new_height = np.random.randint(100, GAME_HEIGHT - settings['PIPE_GAP'] - 100)
        st.session_state.game_state['pipes'].append({
            'x': GAME_WIDTH,
            'height': new_height,
            'scored': False
        })

    # Check collisions
    if st.session_state.game_state['bird_y'] < 0 or \
       st.session_state.game_state['bird_y'] > GAME_HEIGHT-70:  # Ground collision
        game_over()
        return

    for pipe in st.session_state.game_state['pipes']:
        if (100 + 20 > pipe['x'] and 100 - 20 < pipe['x'] + 50):
            if (st.session_state.game_state['bird_y'] - 20 < pipe['height'] or 
                st.session_state.game_state['bird_y'] + 20 > pipe['height'] + settings['PIPE_GAP']):
                game_over()
                return

def game_over():
    difficulty = st.session_state.game_state['difficulty']
    st.session_state.game_state['game_over'] = True
    st.session_state.game_state['game_active'] = False
    if st.session_state.game_state['score'] > st.session_state.game_state['high_score'][difficulty]:
        st.session_state.game_state['high_score'][difficulty] = st.session_state.game_state['score']

# Main game UI
st.title('Flappy Bird')

# Add spacebar listener
add_spacebar_listener()

# Difficulty selection
if not st.session_state.game_state['game_active']:
    difficulty = st.selectbox(
        'Select Difficulty',
        ['easy', 'medium', 'hard'],
        index=['easy', 'medium', 'hard'].index(st.session_state.game_state['difficulty'])
    )
    st.session_state.game_state['difficulty'] = difficulty

# Game controls
col1, col2 = st.columns([2,1])

with col1:
    if not st.session_state.game_state['game_active']:
        if st.button('Start Game (Press Space to Jump)'):
            reset_game()
    
    if st.session_state.game_state['game_active']:
        if st.button('Jump', key='jump_button'):
            difficulty = st.session_state.game_state['difficulty']
            st.session_state.game_state['bird_velocity'] = DIFFICULTY_SETTINGS[difficulty]['JUMP_VELOCITY']

with col2:
    difficulty = st.session_state.game_state['difficulty']
    st.write(f"High Score ({difficulty.capitalize()}): {st.session_state.game_state['high_score'][difficulty]}")

# Game canvas
if st.session_state.game_state['game_active'] or st.session_state.game_state['game_over']:
    game_frame = create_game_frame()
    st.image(game_frame, use_column_width=True)

if st.session_state.game_state['game_over']:
    st.write(f"Game Over! Final Score: {st.session_state.game_state['score']}")
    if st.button('Play Again'):
        reset_game()

# Game loop
if st.session_state.game_state['game_active']:
    update_game()
    time.sleep(0.03)
    st.experimental_rerun()
