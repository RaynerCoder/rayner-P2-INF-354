# 3. Dado un problema combinatorio encontrar una combinacion mediante sistemas de vecinos.
# PROBLEMA DEL AGENTE VIAJERO

import numpy as np


# FUNCION 1: Para evaluar la función objetivo del TSP
"""
Evalúa la función objetivo del TSP para una solución dada.
Argumentos entrada:
- Dist_Matrix (array): Matriz de distancias.
- solution (array): Solución del TSP (orden de las ciudades).  
Devolver:
- float: El costo total del recorrido. 
"""

def Eval_TSP_instance(Dist_Matrix, solution):
    n = len(solution)
    total_distance = 0
    for i in range(n):
        total_distance += Dist_Matrix[solution[i] - 1, solution[(i + 1) % n] - 1]
    return total_distance


# METODOS PARA DIFENTES TIPOS DE VECINOS
# A continuación se presentan las funciones TwoOpt, Swap, Complement y Decrease 
# que implementan diferentes tipos de vecidandes para representaciones basadas en permutaciones.  
# Observe el resultado de la aplicación de los diferentes operadores de vecindad 



# METODOS 2: TwoOpt -----------------------------------------------------------
"""
- TwoOpt crea una vecindad basda en el operador two-opt de forma determinista 
- Todas las permutaciones que se pueden obtener con two-opt están en la vecindad 

Genera todos los vecinos de una solución utilizando el operador 2-opt.    
Argumentos: Solución del TSP (orden de las ciudades).
Retorna: Matriz donde cada fila es un vecino generado por 2-opt.
"""
def TwoOpt(perm):
    n = perm.shape[0]
    n_neighbors = int(n * (n - 1) / 2 - n)  # Número de vecinos
    neighbors = np.zeros((n_neighbors, n), dtype=int)  # Guardaremos todos los vecinos en neighbors = vecinos generados
    ind = 0
    for i in range(n - 1):
        for j in range(i + 2, n):  # Las posiciones a elegir para el two-opt no deben ser consecutivas
            if not (i == 0 and j == n - 1):  # Las posiciones no deben ser primera y última (son circularmente consecutivas)
                neighbors[ind, :] = perm
                aux = perm[i:j + 1].copy()
                neighbors[ind, i:j + 1] = aux[::-1]  # Se invierte el camino entre posiciones elegidas
                ind += 1
    return neighbors



# METODOS 3: Swap -------------------------------------------------------------
"""
- Swap crea una vecindad basada en el operador de intercambio entre posiciones 
- Todas las permutaciones que se pueden obtener como un swap entre la primera 
  posición y cualquiera de las restantes están en la vecindad 
"""
def Swap(perm):
    n = perm.shape[0]
    n_neighbors = n - 1  # Número de vecinos
    neighbors = np.zeros((n_neighbors, n), dtype=int)  # Guardaremos todos los vecinos en neighbors
    ind = 0
    for i in range(1, n):
        new_perm = perm.copy()
        new_perm[0], new_perm[i] = new_perm[i], new_perm[0]
        neighbors[ind, :] = new_perm
        ind += 1
    return neighbors



# METODOS 4: Complement -------------------------------------------------------
"""
- Complement crea una vecindad basada en el operador de complemento entre posiciones 
  en la cual cada valor i en la permutación es sustituido por el valor (n-i) excepto 
  para i=n, que permanece igual 
- Cada permutación tiene un único vecino 
"""
def Complement(perm):
    n = perm.shape[0]
    n_neighbors = 1  # Número de vecinos
    neighbors = np.zeros((n_neighbors, n), dtype=int)  # Guardaremos todos los vecinos en neighbors
    pos_n = np.where(perm == n)[0]
    neighbors[0, :] = (n - perm) + 1  # Se sustituye por el complemento
    neighbors[0, pos_n] = n  # Se mantiene el valor de n igual
    return neighbors



# METODOS 5: Decrease ---------------------------------------------------------
"""
- Decrease crea una vecindad basada en obtener una nueva solución restando un 
  valor "v" a cada posición y crear una solución vecina por cada valor de v 
  en (1,...,n-1). Cuando la resta da valor cero, se pasa a n 
  Ejemplo: 
  permutacion original:   5 3 4 2 1
  permutaciones vecinas:  (4 2 3 1 5),(3,1,2,5,4),(2,5,1,4,3),(1,4,5,3,2) 
"""
def Decrease(perm):
    n = perm.shape[0]
    n_neighbors = n - 1  # Número de vecinos
    neighbors = np.zeros((n_neighbors, n), dtype=int)  # Guardaremos todos los vecinos en neighbors
    auxperm = perm.copy()
    for i in range(n - 1):
        auxperm = (auxperm - 1) % n + 1
        neighbors[i, :] = auxperm
    return neighbors



# METODOS 6: ------------------------------------------------------------------
# Función que realiza la búsqueda local con un método de vecindad específico
"""
Realiza una búsqueda local utilizando un operador de vecindad específico para resolver el TSP.
Argumentos:
- Dist_Matrix: Matriz de distancias entre ciudades.
- neighbor_func: Función que genera los vecinos de una solución.    
Retorna: 
- Mejor valor encontrado, mejor solución encontrada y número de evaluaciones.
"""
def Local_Search_TSP(Dist_Matrix, neighbor_func):
    n = Dist_Matrix.shape[1]
    init_sol = np.random.permutation(n) + 1
    best_val = Eval_TSP_instance(Dist_Matrix, init_sol)
    best_sol = init_sol
    number_evaluations = 1
    
    improvement = True
    sw = True
    while improvement:
        neighbors = neighbor_func(best_sol)
        n_neighbors = neighbors.shape[0]
        number_evaluations += n_neighbors
        
        best_val_among_neighbors = best_val
        for i in range(n_neighbors):
            sol = neighbors[i, :]
            fval = Eval_TSP_instance(Dist_Matrix, sol)
            if fval < best_val_among_neighbors:
                best_val_among_neighbors = fval
                best_sol_among_neighbors = sol
        
        improvement = (best_val_among_neighbors < best_val)
        if improvement:
            best_val = best_val_among_neighbors
            best_sol = best_sol_among_neighbors
            print(f"->Mejor valor encontrado: {best_val}")
            print(f"->Mejor solución encontrada (orden de ciudades): {best_sol}")
            print(f"->Número total de evaluaciones realizadas: {number_evaluations}")
            print()
            sw = False
    if sw:
        print("No se encontraron mejoras en la última iteración.")
       
    return best_val, best_sol, number_evaluations


#------------------------------------------------------------------------------
# Definir una matriz de distancias específica (ejemplo: 5 ciudades)
n_cities = 5
Dist_Matrix = np.array([
    [0, 7, 9, 8, 20],   # Distancias desde la ciudad A a las demás ciudades
    [7, 0, 10, 4, 11],  # Distancias desde la ciudad B a las demás ciudades
    [9, 10, 0, 15, 5],  # Distancias desde la ciudad C a las demás ciudades
    [8, 4, 15, 0, 17],  # Distancias desde la ciudad D a las demás ciudades
    [20, 11, 5, 17, 0]  # Distancias desde la ciudad E a las demás ciudades
])



# Resolver el TSP utilizando diferentes métodos de vecindad y mostrar los resultados
print("\nMétodo TwoOpt:")
best_val_twoopt, best_sol_twoopt, evals_twoopt = Local_Search_TSP(Dist_Matrix, TwoOpt)
print("\nRESULTADOS CON MÉTODO TwoOpt:")
print("Mejor valor encontrado:", best_val_twoopt)
print("Mejor solución encontrada (orden de ciudades):", best_sol_twoopt)
print("Número total de evaluaciones realizadas:", evals_twoopt)

print("\n----------------------------------------------")

print("\nMétodo Swap:")
best_val_swap, best_sol_swap, evals_swap = Local_Search_TSP(Dist_Matrix, Swap)
print("\nRESULTADOS CON MÉTODO Swap:")
print("Mejor valor encontrado:", best_val_swap)
print("Mejor solución encontrada (orden de ciudades):", best_sol_swap)
print("Número total de evaluaciones realizadas:", evals_swap)

print("\n----------------------------------------------")

print("\nMétodo Complement:")
best_val_complement, best_sol_complement, evals_complement = Local_Search_TSP(Dist_Matrix, Complement)
print("\nRESULTADOS CON MÉTODO Complement:")
print("Mejor valor encontrado:", best_val_complement)
print("Mejor solución encontrada (orden de ciudades):", best_sol_complement)
print("Número total de evaluaciones realizadas:", evals_complement)

print("\n----------------------------------------------")

print("\nMétodo Decrease:")
best_val_decrease, best_sol_decrease, evals_decrease = Local_Search_TSP(Dist_Matrix, Decrease)
print("\nRESULTADOS CON MÉTODO Decrease:")
print("Mejor valor encontrado:", best_val_decrease)
print("Mejor solución encontrada (orden de ciudades):", best_sol_decrease)
print("Número total de evaluaciones realizadas:", evals_decrease)