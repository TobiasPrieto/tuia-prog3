# from ..models.grid import Grid
# from ..models.frontier import PriorityQueueFrontier
# from ..models.solution import NoSolution, Solution
# from ..models.node import Node


# class GreedyBestFirstSearch:
#     @staticmethod
#     def search(grid: Grid) -> Solution:
#         """Find path between two points in a grid using Greedy Best First Search

#         Args:
#             grid (Grid): Grid of points

#         Returns:
#             Solution: Solution found
#         """
#         # Initialize a node with the initial position
#         node = Node("", grid.start, 0)

#         # Initialize the explored dictionary to be empty
#         explored = {} 
        
#         # Add the node to the explored dictionary
#         explored[node.state] = True
        
#         return NoSolution(explored)


from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class GreedyBestFirstSearch:
    @staticmethod
    def heuristic(state, goal):
        # Usamos distancia Manhattan como heurística
        return abs(state[0] - goal[0]) + abs(state[1] - goal[1])

    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Greedy Best First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Inicializar el nodo inicial
        node = Node("", grid.start, 0, parent=None, action=None)

        # Inicializar el diccionario de explorados
        explored = {}

        # Agregar el nodo inicial como explorado
        explored[node.state] = True

        # Si ya estamos en el objetivo
        if node.state == grid.end:
            return Solution(node, explored)

        # Inicializar la frontera como una priority queue
        frontier = PriorityQueueFrontier()
        frontier.add(node, GreedyBestFirstSearch.heuristic(node.state, grid.end))

        while not frontier.is_empty():
            node = frontier.pop()

            if node.state == grid.end:
                return Solution(node, explored)

            for action, new_state in grid.get_neighbours(node.state).items():
                if new_state not in explored:
                    new_node = Node("", new_state, 0, parent=node, action=action)
                    explored[new_state] = True
                    h = GreedyBestFirstSearch.heuristic(new_state, grid.end)
                    frontier.add(new_node, h)

        return NoSolution(explored)



class GreedyBestFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Greedy Best First Search

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
        
        frontera= PriorityQueueFrontier()
        frontera.add(node,heuristica(node.state,grid.end))
        
        while not frontera.is_empty():
            nodo = frontera.pop()
            if nodo.state == grid.end:
                return Solution(nodo,explored)
            for accion,nuevoEstado in grid.get_neighbours(nodo.state).items():
                if nuevoEstado not in explored:
                    nuevoNodo = Node('',nuevoEstado,0,parent=nodo,action=accion)
                    explored[nuevoEstado]=True
                    h= heuristica(nuevoEstado,grid.end)
                    frontera.add(nuevoNodo,h)
            
            

        return NoSolution(explored)