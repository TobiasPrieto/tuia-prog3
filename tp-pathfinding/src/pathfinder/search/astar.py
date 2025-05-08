from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class AStarSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using A* Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        
        def heuristica(inicio,final):
            resultado = abs(inicio[0] - final[0]) + abs(inicio[1] - final[1])
            return resultado
        
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)

        # Initialize the explored dictionary to be empty
        explored = {} 
        
        # Add the node to the explored dictionary
        explored[node.state] = True
        
        if node.state == grid.end:
            return Solution(node,explored)
        
        frontera = PriorityQueueFrontier()
        valor = node.cost + (heuristica(node.state,grid.end))
        frontera.add(node,valor)
        
        while not frontera.is_empty():
            nodo = frontera.pop()
            
            if nodo.state == grid.end:
                return Solution(nodo,explored)

            for accion,nuevoEstado in grid.get_neighbours(nodo.state).items():
                if nuevoEstado not in explored:
                    costo = nodo.cost + grid.get_cost(nuevoEstado)
                    h = heuristica(nuevoEstado,grid.end)
                    total= costo + h
                    nuevoNodo = Node('',nuevoEstado,costo,nodo,accion)
                    explored[nuevoEstado]=True
                    frontera.add(nuevoNodo,total)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        return NoSolution(explored)


# from ..models.grid import Grid
# from ..models.frontier import PriorityQueueFrontier
# from ..models.solution import NoSolution, Solution
# from ..models.node import Node


class AStarSearch:
    @staticmethod
    def heuristic(state, goal):
        # Distancia Manhattan
        return abs(state[0] - goal[0]) + abs(state[1] - goal[1])

    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using A* Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        node = Node("", grid.start, 0, parent=None, action=None)
        explored = {}
        explored[node.state] = True

        if node.state == grid.end:
            return Solution(node, explored)

        frontier = PriorityQueueFrontier()
        f = node.cost + AStarSearch.heuristic(node.state, grid.end)
        frontier.add(node, f)

        while not frontier.is_empty():
            node = frontier.pop()

            if node.state == grid.end:
                return Solution(node, explored)

            for action, new_state in grid.get_neighbours(node.state).items():
                if new_state not in explored:
                    # El costo real se acumula
                    g = node.cost + grid.get_cost(new_state)
                    h = AStarSearch.heuristic(new_state, grid.end)
                    f = g + h
                    new_node = Node("", new_state, g, parent=node, action=action)
                    explored[new_state] = True
                    frontier.add(new_node, f)

        return NoSolution(explored)
