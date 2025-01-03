import streamlit as st

def gravity_simulation():
    # Initial conditions
    position = 0  # Starting position
    velocity = 0  # Initial velocity
    gravity = 0.5  # Gravity constant

    # Placeholder to show simulation steps
    output = st.empty()
    
    # Simulation loop
    for step in range(20):
        # Apply gravity to velocity
        velocity += gravity
        
        # Update position
        position += velocity
        
        # Display current state
        output.write(f"""
        Step {step}:
        Velocity: {velocity:.2f}
        Position: {position:.2f}
        """)

    st.write("Simulation Complete")

# Streamlit app
def main():
    st.title("Simple Gravity Simulation")
    
    if st.button("Run Gravity Simulation"):
        gravity_simulation()

if __name__ == "__main__":
    main()
