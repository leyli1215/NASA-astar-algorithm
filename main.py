import networkx as nx
import matplotlib.pyplot as plt
import heapq
import random
from matplotlib.animation import FuncAnimation

class AStarAlgorithm:
    def __init__(self, graph):
        self.G = graph

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star_algo(self, start_node, stop_node):
        open_set = []
        heapq.heappush(open_set, (0, start_node))
        closed_set = set()
        g = {start_node: 0}
        parents = {start_node: start_node}

        while open_set:
            current_cost, current_node = heapq.heappop(open_set)
            if current_node == stop_node:
                path = []
                while parents[current_node] != current_node:
                    path.append(current_node)
                    current_node = parents[current_node]
                path.append(start_node)
                path.reverse()
                return path

            closed_set.add(current_node)

            for neighbor in self.get_neighbors(current_node):
                if neighbor in closed_set:
                    continue
                weight = self.G[current_node][neighbor]['weight']
                tentative_g = g[current_node] + weight

                if neighbor not in g or tentative_g < g[neighbor]:
                    g[neighbor] = tentative_g
                    f = tentative_g + self.heuristic(neighbor, stop_node)
                    heapq.heappush(open_set, (f, neighbor))
                    parents[neighbor] = current_node

        return None

    def get_neighbors(self, node):
        return list(self.G.neighbors(node))


class Obstacle:
    def __init__(self, graph, speed, direction, weight, start_position):
        print(f"Creating Obstacle at {start_position}")
        self.G = graph
        self.speed = speed
        self.direction = direction
        self.weight = weight
        self.position = start_position

    def update(self):
        self.change_weights(1)  
        if self.direction == 'up':
            new_position = (self.position[0], self.position[1] + self.speed)
        elif self.direction == 'down':
            new_position = (self.position[0], self.position[1] - self.speed)
        elif self.direction == 'left':
            new_position = (self.position[0] - self.speed, self.position[1])
        elif self.direction == 'right':
            new_position = (self.position[0] + self.speed, self.position[1])
        else:
            new_position = self.position

        if 0 <= new_position[0] < self.G.graph['width'] and 0 <= new_position[1] < self.G.graph['height']:
            self.position = new_position
        self.change_weights(100)

    def change_weights(self, num):
       
        if self.position in self.G:
            neighbors = list(self.G.neighbors(self.position))
            for neighbor in neighbors:
                self.G.edges[self.position, neighbor]['weight'] = num
                self.G.edges[neighbor, self.position]['weight'] = num



class Simulator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.G = self.create_graph()
        self.G.graph['width'] = width
        self.G.graph['height'] = height
        self.obstacle_nodes = []
        self.static_obstacle_nodes = []
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.ax.set_xlim(-1, width)
        self.ax.set_ylim(-height, 1)

    def create_graph(self):
        G = nx.grid_2d_graph(self.width, self.height)

        for edge in G.edges():
            G.edges[edge]['weight'] = 1

          
        for x in range(self.width - 1):
            for y in range(self.height - 1):
                center_node = (x + 0.5, y + 0.5)
                G.add_node(center_node)

                G.add_edge((x, y), center_node, weight=1)
                G.add_edge((x + 1, y), center_node, weight=1)
                G.add_edge((x, y + 1), center_node, weight=1)
                G.add_edge((x + 1, y + 1), center_node, weight=1)

        return G



    def draw_graph(self, path=None):
                pos = {(x, y): (y, -x) for x, y in self.G.nodes() if isinstance(x, int) and isinstance(y, int)}

               
                for x in range(self.width - 1):
                    for y in range(self.height - 1):
                        center_node = (x + 0.5, y + 0.5)
                        pos[center_node] = (y + 0.5, -(x + 0.5))

                self.ax.clear()

                nx.draw(self.G,
                        pos=pos,
                        node_color='lightgreen',
                        with_labels=True,
                        node_size=300,  
                        font_size=10,   
                        ax=self.ax)

                normal_edges = [(u, v) for u, v in self.G.edges()
                                if self.G[u][v]['weight'] != 100]
                obstacle_edges = [(u, v) for u, v in self.G.edges()
                                  if self.G[u][v]['weight'] == 100]
                static_obstacle_edges = [(u, v) for u, v in self.G.edges()
                      if self.G[u][v]['weight'] == 50]
                nx.draw_networkx_nodes(self.G,
                                       pos,
                                       nodelist=self.obstacle_nodes,
                                       node_color='red',
                                       node_size=300,  
                                       ax=self.ax)
                nx.draw_networkx_nodes(self.G,
                       pos,
                       nodelist=self.static_obstacle_nodes,
                       node_color='purple',
                       node_size=300,
                       ax=self.ax)
                nx.draw_networkx_edges(self.G,
                                       pos,
                                       edgelist=normal_edges,
                                       edge_color='black',
                                       width=1.5,  
                                       ax=self.ax)
                nx.draw_networkx_edges(self.G,
                       pos,
                       edgelist=static_obstacle_edges,
                       edge_color='purple',
                       width=1.5,  
                       ax=self.ax)
                nx.draw_networkx_edges(self.G,
                                       pos,
                                       edgelist=obstacle_edges,
                                       edge_color='red',
                                       width=2,   
                                       ax=self.ax)

                edge_labels = nx.get_edge_attributes(self.G, 'weight')
                nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, font_size=8, bbox=dict(facecolor='white', edgecolor='none', alpha=0.7), ax=self.ax)   

                if path:
                    path_edges = list(zip(path, path[1:]))
                    nx.draw_networkx_nodes(self.G,
                                           pos,
                                           nodelist=path,
                                           node_color='orange',
                                           node_size=300,   
                                           ax=self.ax)
                    nx.draw_networkx_edges(self.G,
                                           pos,
                                           edgelist=path_edges,
                                           edge_color='orange',
                                           width=2.5,   
                                           ax=self.ax)


initialized = False  

def animate(frame):
    global simulator, obstacles, initialized

    
    if frame == 0 and not initialized:
         
        static_obstacle = Obstacle(simulator.G, 0, 'none', 100, (4, 0))
        obstacles.append(static_obstacle)
        static_obstacle = Obstacle(simulator.G, 0, 'none', 100, (3, 2))
        obstacles.append(static_obstacle)
        static_obstacle2 = Obstacle(simulator.G, 0, 'none', 100, (2, 3))
        obstacles.append(static_obstacle2)

        
        moving_obstacle = Obstacle(simulator.G, 1, 'left', 100, (5,1))
        obstacles.append(moving_obstacle)
        moving_obstacle2 = Obstacle(simulator.G, 1, 'up', 100, (1,0))
        obstacles.append(moving_obstacle2)
        moving_obstacle3 = Obstacle(simulator.G, 1, 'up', 100, (4,1))
        obstacles.append(moving_obstacle3)
         
        initialized = True  

    
    simulator.obstacle_nodes.clear()

    
    for obstacle in obstacles:
        obstacle.update()
        simulator.obstacle_nodes.append(obstacle.position)

   
    for obstacle in obstacles:
        if obstacle.speed == 0:
            obstacle.change_weights(50)
            simulator.static_obstacle_nodes.append(obstacle.position)

   
    path = astar.a_star_algo(start_node, stop_node)
    simulator.draw_graph(path)

   
    if frame > 50:
        anim.event_source.stop()

if __name__ == "__main__":
    width, height = 6, 6
    simulator = Simulator(width, height)
    astar = AStarAlgorithm(simulator.G)
    obstacles = []

    start_node = (0, 0)
    stop_node = (5,5)

    anim = FuncAnimation(simulator.fig, animate, frames=100, interval=1200)
    plt.tight_layout()
    plt.show()



