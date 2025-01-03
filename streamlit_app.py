import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
import time

# Bird class
class Bird:
    def __init__(self):
        self.y = 250
        self.x = 50
        self.vel = 0
        self.gravity = 0.5
        self.jump_strength = -8

    def jump(self):
        self.vel = self.jump_strength

    def update(self):
        self.vel += self.gravity
        self.y += self.vel

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = np.random.randint(100, 400)
        self.gap_size = 150
        self.speed = 3

    def update(self):
        self.x -= self.speed

    def collides_with(self, bird):
        bird_rect = [bird.x, bird.y, bird.x + 30, bird.y + 30]
        top_pipe = [self.x, 0, self.x + 50, self.gap_y]
        bottom_pipe = [self.x, self.gap_y + self.gap_size, self.x + 50, 600]
        return (
            self.rect_overlap(bird_rect, top_pipe) or
            self.rect_overlap(bird_rect, bottom_pipe)
        )

    @staticmethod
    def rect_overlap(rect1, rect2):
        return not (
            rect1[2] < rect2[0] or
            rect1[0] > rect2[2] or
            rect1[3] < rect2[1] or
            rect1[1] > rect2[3]
        )

# Initialize game state
def init_game_state():
    if "bird" not in st.session_state:
        st.session_state.bird = Bird()
    if "pipes" not in st.session_state:
        st.session_state.pipes = [Pipe(600)]
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "game_started" not in st.session_state:
        st.session_state.game_started = False
    if "last_update" not in st.session_state:
        st.session_state.last_update = time.time()

# Reset game state
def reset_game():
    st.session_state.bird = Bird()
    st.session_state.pipes = [Pipe(600)]
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.game_started = False
    st.session_state.last_update = time.time()

# Main game function
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
    while not st.session_state.game_over:
        # Update bird
        st.session_state.bird.update()

        # Update pipes
        for pipe in st.session_state.pipes:
            pipe.update()

            # Check collisions
            if pipe.collides_with(st.session_state.bird):
                st.session_state.game_over = True

        # Remove pipes that are off-screen and add new ones
        st.session_state.pipes = [p for p in st.session_state.pipes if p.x > -50]
        if len(st.session_state.pipes) > 0 and st.session_state.pipes[-1].x < 400:
            st.session_state.pipes.append(Pipe(600))

        # Update score
        for pipe in st.session_state.pipes:
            if pipe.x + 50 < st.session_state.bird.x and not hasattr(pipe, "scored"):
                st.session_state.score += 1
                pipe.scored = True

        # Check if bird is out of bounds
        if st.session_state.bird.y < 0 or st.session_state.bird.y > 600:
            st.session_state.game_over = True

        # Render game state
        img = Image.new("RGB", (800, 600), color=(135, 206, 235))  # Sky blue background
        draw = ImageDraw.Draw(img)

        # Draw pipes
        for pipe in st.session_state.pipes:
            draw.rectangle([pipe.x, 0, pipe.x + 50, pipe.gap_y], fill=(34, 139, 34))  # Top pipe
            draw.rectangle(
                [pipe.x, pipe.gap_y + pipe.gap_size, pipe.x + 50, 600],
                fill=(34, 139, 34),
            )  # Bottom pipe

        # Draw bird
        draw.ellipse(
            [
                st.session_state.bird.x,
                st.session_state.bird.y,
                st.session_state.bird.x + 30,
                st.session_state.bird.y + 30,
            ],
            fill=(255, 255, 0),
        )  # Bird as a yellow circle

        # Display game
        canvas.image(img)

        # Display score
        st.write(f"Score: {st.session_state.score}")

        time.sleep(0.05)  # Control game speed (20 FPS)

    # Game over message
    st.write("Game Over! Press Reset to play again.")

if __name__ == "__main__":
    main()
