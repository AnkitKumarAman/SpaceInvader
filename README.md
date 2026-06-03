# Space Invader Retro Arcade Game 🚀👾

A high-performance, object-oriented 8-bit retro arcade game built with **Python**, **Pygame-CE (Community Edition)**, and **SDL**, featuring a custom **DSP procedural audio synthesis engine** and stateful weapon systems.

---

## Key Features 🚀

### ⚙️ Stateful Dual-Fire Weapon System
- Toggle dynamically between two strategic firing patterns:
  - **Single Fire Mode** (Press `S`): Controlled shooting with a strict $400\text{ms}$ cooldown rate limit to prevent spamming.
  - **Rapid Fire Mode** (Press `R`): High-speed firing for a $5$-second continuous window, followed by a stateful $5$-second cooldown cycle where the player's weapon must cool down.

### 🔊 DSP Procedural Audio Engine
- Sounds and background chiptune music are generated programmatically via Python's native `wave` and `struct` libraries, bypassing external binary audio dependencies.
- Features frequency-swept square waves for lasers, triangle-wave bass lines for background chiptunes, and exponentially decaying white noise for explosions.

### 🧩 Dynamic Rotational Physics & Hazard Spawning
- Meteors are spawned with custom trajectory vectors (`pygame.Vector2`) and continuous rotational zoom (`pygame.transform.rotozoom`) to create a realistic tumbling effect in space.

### 🎯 Pixel-Perfect Collisions
- Utilizes Pygame's bitmask overlay detection (`pygame.sprite.collide_mask`) to guarantee ultra-precise projectile collision overlays and reliable hitboxes under high sprite counts.

### 📈 Persistent Session Statistics
- Tracks and displays player high scores dynamically during runtime using local filesystem I/O caching to save the lifetime record.

---

## Repository Files Navigation 📁

### Key Components Breakdown

#### Assets & Media 🖥️
- **`Images/`**: Contains core graphical sprite sheets and icons (`player.png`, `laser.png`, `meteor.png`, `star.png`, `game_icon.png`).
- **`Sound/`**: Holds synthesized audio files (`laser.wav`, `rapid_fire_sound.wav`, `explosion.wav`, `game_over.wav`, `game_music.wav`).
- **`explosion/explosion/`**: A sequential 21-frame list of sprite images (`0.png` to `20.png`) utilized by the animation handler for explosion sprites.
- **`Rustic_Barn.ttf`**: Digital font asset for in-game HUD score displays.

#### Engine Modules 🔌
- **`SpaceInvader.py`**: The game entry point coordinating the Pygame canvas initialization, event loop tick clock, custom timer events, and game updates.
- **`player.py`**: Declares the `Player` class managing user controls, screen boundary constraints, and weapon fire state machines.
- **`meteor.py`**: Defines the `Meteor` sprite behavior, speed vectors, decay timers, and continuous rotation.
- **`laser.py`**: Standard laser projectile class handling directional velocity.
- **`star.py`**: Handles background star generation for the scrolling parallax effect.
- **`functions.py`**: Implements collision check states, high score filesystem load/save functions, and HUD draw coordinates.
- **`generate_sounds.py`**: The DSP math synthesis engine file used to generate all WAV sound effects.

#### Build Tools 🛠️
- **`setup.py` & `SpaceInvader.spec`**: Configuration templates for compiling the game into standalone desktop executables.
- **`.gitignore`**: Excludes virtual environment files (`Lib`, `Include`), pycache, and compilation outputs from repository tracking.

---

## Setup and Usage 🛠

### 1. Prerequisites
Ensure you have Python 3.10 or higher installed on your system.

### 2. Clone the Repository
```bash
git clone https://github.com/AnkitKumarAman/SpaceInvader.git
cd SpaceInvader
```

### 3. Install Dependencies
```bash
pip install pygame-ce
```

### 4. Synthesize Sounds (Optional)
If you want to re-generate the 8-bit sound library:
```bash
python generate_sounds.py
```

### 5. Run the Game
```bash
python SpaceInvader.py
```

---

## Game Controls 🕹️

| Action | Control Key |
| :--- | :--- |
| **Move Spaceship** | Arrow Keys / `A`, `D`, `W`, `S` |
| **Shoot Laser** | `Spacebar` |
| **Single Fire Mode** | `S` |
| **Rapid Fire Mode** | `R` |

---

## Credits 📚

- **Pygame-CE**: High-performance SDL wrapper library for Python game development.
- **SDL (Simple DirectMedia Layer)**: Low-level access to audio, keyboard, mouse, and graphics hardware.
- **DSP Reference**: Standard digital signal processing formulas for wave-shape sound synthesis.

---

## License 📜

This project is licensed under the MIT License. See the `LICENSE` file for more details.
