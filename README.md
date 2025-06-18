# 🏺 The Lost Artifact of Zyx - A Text Adventure Game

Welcome to "The Lost Artifact of Zyx"! This is a classic text-based adventure game where you explore an ancient ruin, solve a simple puzzle, and aim to find the legendary artifact.

---

## 📜 How to Play

Navigate through the ruins by typing commands into the prompt. Your goal is to find and take the Lost Artifact of Zyx.

### Game Premise
You are an adventurer exploring an ancient ruin. Legend speaks of the Lost Artifact of Zyx hidden within. Overcome obstacles, interact with your environment, and claim your prize!

### Available Commands
*   **`go [direction]`**: Moves your character in the specified direction (e.g., `go north`, `go east`, `go south`, `go west`).
*   **`look`** or **`look around`**: Describes your current room, including any visible items.
*   **`take [item]`**: Picks up an item from the current room and adds it to your inventory (e.g., `take torch`).
*   **`use [item]`**: Uses an item from your inventory (e.g., `use torch`). This is crucial for solving puzzles.
*   **`inventory`** or **`i`**: Lists the items you are currently carrying.
*   **`quit`**: Exits the game.

All commands and item names are case-insensitive.

---

## 🚀 Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

```bash
# 1. Clone the repository (if you haven't already)
# git clone https://github.com/your-username/your-project-name.git
# cd your-project-name

# 2. Set up a virtual environment
# It's highly recommended to use a virtual environment for Python projects.
python3 -m venv venv
source venv/bin/activate

# (To deactivate later: deactivate)

# 3. Install dependencies
# Note: requirements.txt is currently empty but is included for good practice and future dependencies.
pip install -r requirements.txt

# 4. Run the application
python run.py
```

---

## 🧪 Run Tests

The game includes a suite of unit tests to ensure functionality. Python's built-in `unittest` framework is used.

To discover and run all unit tests:
```bash
python -m unittest discover -s tests
```

---
This project was developed iteratively, building features and tests step-by-step.
Enjoy your adventure!
