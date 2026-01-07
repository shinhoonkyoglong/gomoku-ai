# Gomoku (Five in a Row) Player bot

> **An algorithmic Gomoku bot using pure Python(not machine learning), achieving Rank 2nd in the in-class AI Programming Tournament.**

<p align="center">
  <img width="774" height="452" alt="image" src="https://github.com/user-attachments/assets/87a806f9-097f-402f-beba-e614d70e4e51" />
  <img width="640" height="480" alt="Figure_1" src="https://github.com/user-attachments/assets/99abbd95-a363-4a49-9326-9901638d3fa3" />
</p>

## Project Overview
This project is an implementation of a Gomoku (Five in a Row) game AI without relying on machine learning libraries. The goal was to construct a high-performance player using only fundamental search algorithms and heuristic evaluations, demonstrating strong algorithmic problem-solving skills.

The AI player ranked **2nd** in the final class tournament, proving its robust and strategic gameplay capability.

## Core Algorithms & Logic
Unlike ML-based approaches, this AI makes decisions based on a set of prioritized rules inspired by the **Minimax algorithm principles**.

### 1. Strategic Priority System (Heuristics)
The AI evaluates the board and decides its move based on the following strict priority order:

1.  **Immediate Win:** If I can complete 5-in-a-row now, take it.
2.  **Block Opponent Win:** If the opponent can win next turn, block them immediately.
3.  **Create Threats (4-3 / Open 4):** If I can create a double threat (e.g., "four and three"), do it.
4.  **Block Threats:** Block the opponent's attempts to create threats.
5.  **Develop Board (Open 3 / Open 2):** If no immediate threats, make a strategic move to build open rows (e.g., open 3, open 2) for future attacks.

### 2. Algorithmic Implementation
* The core logic is implemented using extensive nested conditional statements (`if/else`) and loops (`for`) to scan the board and detect patterns.
* **Custom Pattern Recognition Functions:** Developed functions like `three_rule()` and `can_form_n_in_a_row()` to accurately identify complex board states like "open 3", "closed 4", "broken 3", etc.

## Gameplay Demo (How it works)
(See screenshots above)
1.  The game starts by asking who goes first.
2.  The user enters coordinates (e.g., `K, 10`) in the console.
3.  The AI instantly calculates its best move based on the priority logic and places its stone.
4.  The board state is visually updated using `matplotlib` after each move.

## Tech Stack
- **Languages:** Python
- **Libraries:** `matplotlib` (for board visualization), `numpy` (for calculations)
