
# Ejercicio 1

## Mi cueva

```text
Y
4 |  [ POZO ]  | [ WUMPUS ] |  [ POZO ]  |  [ ORO ]   |
3 |     .      |     .      |     .      |     .      |
2 |     .      |     .      |     .      |     .      |
1 | [AGENTE >] |     .      |  [ POZO ]  |     .      |
  +------------+------------+------------+------------+
        1            2            3            4        X
```

## ¿Qué agentes lograron salir con el oro en tu mapa y cuáles no?

| Agente | ¿Logró salir? | Comentarios |
| :--- | :--- | :--- |
| Simple Reflex | No | Se quedó atascado y empezó a dar vueltas |
| Model Base | No | Exploró y cuando se encontró acorralado empezó a dar vueltas |
| Goal Based | No | Exploró y cuando se encontró accoralado empezó a dar vueltas |
| Utility Based | Sí | Exploró y logró encontrar el camino al oro y de regreso a la salida |
| Learning | Sí | Requirió aumentar los episodios a 15,000 para darle más información en su exploración |
|  |  |  |

El agente de reflejo simple falla pues sólo puede percibir su entorno actual, por lo tanto al verse en una situación donde podría caer en un pit o ser comido por el wumpus, decide quedarse en su lugar y dar vueltas.

Al alejar los pits de la casilla inicial el agente basado en modelo explora más. Sin embargo, al caer en una situación donde no tiene certeza de su camino se queda atascado.