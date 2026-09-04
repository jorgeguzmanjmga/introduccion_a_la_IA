
# Ejercicio 1 - Búsqueda no informada

## Pareja elegida

* **Origen**: Zerind
* **Destino**: Craiova

![](map.png)


| Algoritmo | Path | Depth | Cost (km) | Expanded (nodes) | Generated (nodes) | Status |
| :--- | :--- | :---: | :---: | :---: | :---: |:---: |
| **BFS** | Zerind → Arad → Sibiu → Rimnicu Vilcea → Craiova | 4 | 441 | 7 | 17 | success | 
| **UCS** | Zerind → Arad → Sibiu → Rimnicu Vilcea → Craiova | 4 | 441 | 10 | 26 | success |
| **DFS** | Zerind → Arad → Sibiu → Fagaras → Bucharest → Pitesti → Craiova | 6 | 764 |7|20|sucess|
| **DLS** (limit 2) | NA | NA | NA |3|8|cutoff|
| **DLS** (limit 3) | NA | NA | NA |6|18|cutoff|
| **DLS** (limit 4) | Zerind → Arad → Sibiu → Rimnicu Vilcea → Craiova| 4 | 441 |6|12|sucess|
| **IDS** | Zerind → Arad → Sibiu → Rimnicu Vilcea → Craiova| 4 | 441 |16|42|sucess|

## Observaciones

* **BFS** y **UCS** encontraron el mismo camino pues en este ejemplo el camino de menos carreteras y el de menos km coinciden.

* **DFS** nos arroja una ruta más larga en este caso y se debe a que el algoritmo procesa diferente el grafo, pues expande primero los nodos más profundos (*LIFO*).

* **BFS** encuentra la meta a la profundidad mínima posible ($depth=4$) en este caso. Debido a lo anterior, al utilizar **DLS** con un límite inferior a 4 el algoritmo se detiene antes de llegar a la profundidad mínima de la solución.

## Evidencias

![](evidencias_01.png)

![](evidencias_02.png)

![](evidencias_03.png)

