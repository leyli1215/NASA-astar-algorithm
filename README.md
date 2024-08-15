# A* Pathfinding with Dynamic Obstacles

This Python project demonstrates the A* algorithm for pathfinding on a grid with dynamic and static obstacles. The grid is represented using the NetworkX library, and the visualization is done using Matplotlib. The A* algorithm is used to find the shortest path from a start node to a stop node, avoiding obstacles that may change position over time.

## Features

- **A* Algorithm:** Implements the A* pathfinding algorithm using Euclidean distance as the heuristic.
- **Dynamic Obstacles:** Obstacles move across the grid according to specified directions and speeds.
- **Static Obstacles:** Certain obstacles remain in place, modifying the pathfinding behavior.
- **Visualization:** The grid, obstacles, and path are visualized in real-time using Matplotlib.

## Installation

### Prerequisites

Ensure you have Python 3.x installed along with the following Python packages:

- `networkx`
- `matplotlib`

You can install these using pip:

```bash
pip install networkx matplotlib
