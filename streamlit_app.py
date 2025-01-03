import streamlit as st
import numpy as np
import time
from PIL import Image, ImageDraw

# Game difficulty settings
DIFFICULTY_SETTINGS = {
    'easy': {
        'GRAVITY': 0.3,
        'JUMP_VELOCITY': -7,
        'PIPE_SPEED': 2,
        'PIPE_GAP': 180,
        'PIPE_SPAWN_TIME': 2.5,
        'COLOR': 'green'
    },
    'medium': {
        'GRAVITY': 0.5,
        'JUMP_VELOCITY': -8,
        'PIPE_SPEED': 3,
        'PIPE_GAP': 150,
        'PIPE_SPAWN_TIME': 2,
        'COLOR': 'orange'
    },
    'hard': {
        'GRAVITY': 0.7,
        'JUMP_VELOCITY': -9,
        'PIPE_SPEED': 4,
        'PIPE_GAP': 120,
        'PIPE_SPAWN_TIME': 1.5,
        'COLOR': 'red'
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
    
    # Main pipe body - lighter green
    draw.rectangle([0, 0, width-4, height], fill=(100, 200, 50))
    # Right shadow - darker green
    draw.rectangle([width-4, 0, width, height], fill=(80, 180, 40))
    
    # Pipe cap
    cap_height = 30
    if is_top:
        cap_y = height - cap_height
    else:
        cap_y = 0
        
    # Cap main body - lighter green
    draw.rectangle([-5, cap_y, width+5, cap_y + cap_height], fill=(100, 200, 50))
    # Cap shadow - darker green
    draw.rectangle([width+1, cap_y, width+5, cap_y + cap_height], fill=(80, 180, 40))
    # Cap highlight
    draw.rectangle([-5, cap_y, width+5, cap_y + 4], fill=(120, 220, 60))
    
    return pipe

def create_bird_image(size):
    bird = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bird)
    
    # Body - yellow
    draw.ellipse([2, 2, size-2, size-2], fill=(255, 215, 0))
    # Wing - darker yellow
    draw.ellipse([size//4, size//2, size//2, size-4], fill=(230, 180, 0))
    # Eye - white
    draw.ellipse([size//1.5, size//4, size-4, size//2], fill='white')
    # Pupil - black
    draw.ellipse([size//1.3, size//3.5, size-6, size//2.2], fill='black')
    # Beak - orange
    draw.polygon([(size-4, size//2), (size, size//1.8), (size-4, size//1.5)], fill=(255, 140, 0))
    
    return bird

def create_background():
    # Create sky
    bg = Image.new('RGB', (GAME_WIDTH, GAME_HEIGHT), (135, 206, 235))  # Sky blue
    draw = ImageDraw.Draw(bg)
    
    # Add clouds
    cloud_color = (255, 255, 255)
    for i in range(0, GAME_WIDTH, 100):
        draw.ellipse([i, GAME_HEIGHT-150, i+60, GAME_HEIGHT-120], fill=cloud_color)
    
    # Add city skyline
    city_color = (100, 200, 100)  # Light green
    for i in range(0, GAME_WIDTH, 50):
        height = np.random.randint(50, 100)
        draw.rectangle([i, GAME_HEIGHT-height, i+30, GAME_HEIGHT], fill=city_color)
    
    # Add ground
    draw.rectangle([0, GAME_HEIGHT-50, GAME_WIDTH, GAME_HEIGHT], fill=(150, 220, 50))  # Green
    
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
    draw.text((10, 10), f"Score: {st.session_state.game_state['score']}", fill='white')
    
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
       st.session_state.game_state['bird_y'] > GAME_HEIGHT:
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
        if st.button('Start Game'):
            reset_game()
    
    if st.session_state.game_state['game_active']:
        if st.button('Jump'):
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

DIFFICULTY_SETTINGS = {
    'easy': {
        'GRAVITY': 0.3,  # Lightest gravity
        ...
    },
    'medium': {
        'GRAVITY': 0.5,  # Medium gravity
        ...
    },
    'hard': {
        'GRAVITY': 0.7,  # Strongest gravity
        ...
    }
}
