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
            accion, valor_sucesor = problem.max_action(actual)

            # Retornar si estamos en un maximo local:
            # el valor objetivo del sucesor es menor o igual al del estado actual
            if valor_sucesor <= value:

                self.tour = actual
                self.value = value
                end = time()
                self.time = end-start
                return

            # Sino, nos movemos al sucesor
            actual = problem.result(actual, accion)
            value = valor_sucesor
            self.niters += 1


class HillClimbingReset(LocalSearch):
    """Ascensión de colinas con reinicio aleatorio."""

    def __init__(self, n_reinicios=15):
        super().__init__()
        self.n_reinicios = n_reinicios

    def solve(self, problem: OptProblem):
        """Resuelve un problema con múltiples reinicios aleatorios."""
        start = time()

        mejor_tour = None
        mejor_valor = float('-inf')
        total_iters = 0

        for _ in range(self.n_reinicios):
            actual = problem.random_reset()  
            value = problem.obj_val(actual)

            while True:
                accion, valor_sucesor = problem.max_action(actual)

                if valor_sucesor <= value:
                    break

                actual = problem.result(actual, accion)
                value = valor_sucesor
                total_iters += 1

            if value > mejor_valor:
                mejor_valor = value
                mejor_tour = actual

        self.tour = mejor_tour
        self.value = mejor_valor
        self.niters = total_iters
        self.time = time() - start






class Tabu(LocalSearch):
    """Algoritmo de búsqueda tabú."""
    def solve(self, problem, max_stops=5500):
        stops = 0
        actual = problem.init
        mejor_estado = actual
        mejor_valor = problem.obj_val(actual)
        tabu = []
        tabu_len = 20
        start = time()

        while stops <= max_stops:
            # Generar acciones posibles y filtrar las que están en la lista tabú
            candidatos = []
            for a in problem.actions(actual):
                if a not in tabu:
                    candidatos.append(a)

            # Si no hay candidatos posibles, terminamos
            if not candidatos:
                break

            # Buscar la mejor acción entre las candidatas
            maximo_valor = float('-inf')
            mejor_accion = None
            for a in candidatos:
                next_estado = problem.result(actual, a)
                val = problem.obj_val(next_estado)
                if val > maximo_valor:
                    maximo_valor = val
                    mejor_accion = a

            accion = mejor_accion
            valor_sucesor = maximo_valor
            next_estado = problem.result(actual, accion)

            self.niters += 1

            if valor_sucesor > mejor_valor:
                mejor_valor = valor_sucesor
                mejor_estado = next_estado
                stops = 0
            else:
                stops += 1

            tabu.append(accion)
            if len(tabu) > tabu_len:
                tabu.pop(0)

            actual = next_estado

        end = time()
        self.tour = mejor_estado
        self.value = mejor_valor
        self.time = end - start
