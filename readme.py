# Space Invader Retro Arcade Game 🚀👾

A high-performance, object-oriented recreation of the classic retro arcade game **Space Invader** built using **Python** and **Pygame-CE (Community Edition)**. This project highlights custom digital signal processing (DSP) sound synthesis, stateful weapon mechanics, and pixel-perfect collision detection.

---

## ✨ Features

- **Procedural Audio Synthesis (DSP)**: Sound effects (lasers, explosions, game-over chime) and a background chiptune music loop are synthesized procedurally from scratch using Python's native `wave` and `struct` libraries, bypassing external audio asset dependencies.
- **Stateful Weapon Modes**: Toggle dynamically between two strategic fire patterns:
  - **Single Fire**: Balanced gameplay with a strict 400ms cooldown rate limit (Press `Q` to switch).
  - **Rapid Fire**: Unleash a stream of lasers for a 5-second window, followed by a stateful 5-second cooldown period (Press `E` to switch).
- **Pixel-Perfect Collisions**: Uses Pygame's bitmask-based overlay detection (`pygame.sprite.collide_mask`) to guarantee accurate projectile collision overlays.
- **Persistent High Score Tracking**: Leverages local filesystem caching to read, record, and display the player's lifetime record dynamically during runtime.
- **Resolution-Independent Rendering**: Programmed with a flexible viewport architecture that adjusts game boundaries and HUD positions dynamically based on screen dimensions.

---

## 🛠️ Installation & Setup

### Prerequisites
Make sure you have Python 3.10+ installed.

### 1. Clone the Repository
```bash
git clone https://github.com/AnkitKumarAman/SpaceInvader.git
cd SpaceInvader
