# FlappyBird-AI-Agent


This project implements a Flappy Bird game using the Pygame library and incorporates a Q-learning agent to play the game. The Q-learning agent learns to navigate the game environment and maximize its score through trial and error.

## Requirements

- Python 3.x
- Pygame 2.1.2 (Install with `pip install pygame==2.1.2`)

## Project Overview

This project consists of a Flappy Bird game from this [repo](https://github.com/ivandradivojevic/FlappyBird-Game-Clone) and a Q-learning agent that controls the bird's actions. Here's a brief overview of the project components:

### Game Components

- **Flappy Bird Game**: The game environment is created using the Pygame library. It features a bird that the player (or Q-learning agent) can control to navigate through a series of pipes.

- **Game Display**: The game displays the player's score, high score, and the current iteration. It also includes a background, floor, pipes, and a bird character.

### Q-learning Agent

- **Q-table**: The Q-learning agent uses a Q-table to store and update Q-values for different state-action pairs. The Q-table has dimensions (10, 300, 2) to represent the state space and possible actions. It is initialized with zeros.

- **State Representation**: The state of the game is represented by the bird's x and y positions and the position of the closest bottom pipe. These values are discretized to fit into the Q-table.

- **Actions**: The agent can choose between two actions: jumping or not jumping. It selects an action based on the Q-values in the Q-table.

- **Q-learning Updates**: After each action, the agent updates the Q-values in the Q-table using the Q-learning algorithm with a learning rate (α) and discount factor (γ). The Q-learning update formula is as follows:

$$Q(s, a) = (1-α) * Q(s, a) + α * [R(s) + γ * max(Q(s', a')) - Q(s, a)]$$

Where:
- `Q(s, a)` is the Q-value for state `s` and action `a`.
- `α` is the learning rate (0 < α ≤ 1), controlling the step size of updates.
- `R(s)` is the immediate reward received after taking action `a` in state `s`.
- `γ` is the discount factor (0 < γ ≤ 1), determining the importance of future rewards.
- `max(Q(s', a'))` is the maximum Q-value for the next state `s'` and all possible actions `a'`.


## How to Run

1. Install Python 3.x if not already installed.

2. Install Pygame 2.1.2 using the following command:

```bash
pip install pygame==2.1.2
```

3. Download the project files, including the game assets and Python script.

4. Run the Python script:

```bash
python q-learning_on_flappy.py
```

5. Observe the smart bird performance.


## Project Structure

- `q-learning_on_flappy.py`: The main Python script containing the game and Q-learning agent implementation.
- `assets/`: Directory containing game assets such as images.
- `04B_19.ttf`: Font file for text rendering.


Feel free to modify and extend this project for your own learning or enjoyment!
