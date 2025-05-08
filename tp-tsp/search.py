"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo. Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from time import time
from problem import OptProblem
from collections import deque

class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)

        while True:

            # Buscamos la acción que genera el sucesor con mayor valor objetivo
            act, succ_val = problem.max_action(actual)

            # Retornar si estamos en un maximo local:
            # el valor objetivo del sucesor es menor o igual al del estado actual
            if succ_val <= value:

                self.tour = actual
                self.value = value
                end = time()
                self.time = end-start
                return

            # Sino, nos movemos al sucesor
            actual = problem.result(actual, act)
            value = succ_val
            self.niters += 1


class HillClimbingReset(LocalSearch):
    """Ascensión de colinas con reinicio aleatorio."""

    def __init__(self, n_reinicios=10):
        super().__init__()
        self.n_reinicios = n_reinicios

    def solve(self, problem: OptProblem):
        """Resuelve un problema con múltiples reinicios aleatorios."""
        start = time()

        mejor_tour = None
        mejor_valor = float('-inf')
        total_iters = 0

        for _ in range(self.n_reinicios):
            actual = problem.random_reset()  # Distinto a problem.init
            value = problem.obj_val(actual)

            while True:
                act, succ_val = problem.max_action(actual)

                if succ_val <= value:
                    break

                actual = problem.result(actual, act)
                value = succ_val
                total_iters += 1

            if value > mejor_valor:
                mejor_valor = value
                mejor_tour = actual

        self.tour = mejor_tour
        self.value = mejor_valor
        self.niters = total_iters
        self.time = time() - start





class Tabu(LocalSearch):
    """Clase que representa el algoritmo de búsqueda con lista tabú."""

    def __init__(self, tabu_size=10, max_iters=1000):
        """Construye una instancia del algoritmo de búsqueda tabú."""
        super().__init__()
        self.tabu_size = tabu_size
        self.max_iters = max_iters

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimización usando búsqueda tabú."""

        start = time()

        actual = problem.init
        best = actual

        value = problem.obj_val(actual)
        best_value = value

        tabu_list = deque(maxlen=self.tabu_size)

        for _ in range(self.max_iters):
            self.niters += 1

            # Generamos todos los sucesores y sus valores
            successors = problem.successors(actual)
            filtered = []

            for act, succ in successors:
                if succ not in tabu_list:
                    succ_val = problem.obj_val(succ)
                    filtered.append((succ_val, act, succ))

            # Si todos los sucesores están en la lista tabú, terminamos
            if not filtered:
                break

            # Elegimos el mejor sucesor no tabú
            filtered.sort(reverse=True, key=lambda x: x[0])
            best_succ_val, best_act, best_succ = filtered[0]

            # Nos movemos
            actual = best_succ
            value = best_succ_val
            tabu_list.append(actual)

            # Actualizamos el mejor global
            if value > best_value:
                best = actual
                best_value = value

        self.tour = best
        self.value = best_value
        self.time = time() - start
