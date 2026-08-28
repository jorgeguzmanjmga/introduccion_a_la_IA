# Ejercicio 2 — Descripción PEAS de agentes inteligentes


### 1. Asistente virtual de voz

- **Performance:** Ejecuta lo que se le solicita, tiempo de respuesta y procesamiento, entiende lenguaje natural.
- **Environment:** Su entorno es el audio del mundo real. Por lo anterior es secuencial por la naturaleza de nuestro mundo, es estocástico pues puede otorgar diferentes respuestas a la misma solicitud, y es dinámico pues el entorno cambia de forma continua.
- **Actuators:** Lo que puede realizar depende de las aplicaciones que tenga conectadas. Puede enviar un mensaje de whats app, reproducir una canción, programar una alarma, establecer una ruta a alguna ubicación, decirnos qué hora es, étc.
- **Sensors:** Sensor de voz.

### 2. Robot aspirador doméstico

- **Performance:** Tiempo que tarda en limpiar, qué tan limpio deja el piso, capacidad de adaptarse al entorno y evitar obstáculos, capacidad de programarse y limpiar por períodos, batería y tiempo de recarga.
- **Environment:** El piso de una casa, departamento, étc. Es parcialmente observable pues no puede percibir todo el entorno.
- **Actuators:** Moverse, aspirar, regresar a su estación de carga, almacenar lo que ha aspirado, suspenderse/apagarse.
- **Sensors:** Detección de obstáculos, detectar suciedad, sensor de batería para saber cuando recargar y sensor de almacenamiento para saber cuando se está llenando de polvo.

### 3. Sistema de recomendación de streaming 

- **Performance:** Satisfacción del espectador a la película/serie recomendada (calificación otorgada después de verla), tiempo que permaneció el espectador viendo (retención).
- **Environment:** El catálogo de la página o la aplicación, el historial de visualización del cliente. Es observable, estocástico y secuencial pues se tiene conocimiento de todo el catálogo e historial, las recomendaciones deberían tener un factor de exploración y es secuencial por definición de historial.
- **Actuators:** Mostrar principales recomendaciones de películas con base al historial.
- **Sensors:** Base de datos vectorial del catálogo y del historial de las películas que permita calcular alguna medida de distancia entre ellas y elegir las más cercanas para recomendar.

### 4. Vehículo autónomo en ciudad

- **Performance:** Llegar al destino de forma segura, eficiente y sin haber ocasionado daños.
- **Environment:** Las calles de la ciudad, reglamento de tránsito, señalamientos, glorietas, semáforos, peatones, pasos peatonales, topes, baches, perros, gatos, étc. Es parcialmente observable, continuo y estocástico.
- **Actuators:** Encenderse, acelerar, frenar, girar el volante, cambiar velocidades o modo de conducción, usar direccionales, enceder las luces, estacionarse. 
- **Sensors:** velocímetro, detectores de proximidad y movimiento, cámaras de video.


### 5. Agente de trading algorítmico en bolsa

- **Performance:** Rendimiento anual del portafolio, rendimiento máximo y mínimo del portafolio, volatilidad.
- **Environment:** El mercado de acciones, en particular, la plataforma de algún broker. Es estocástico pues la misma decisión de inversión puede tener diferentes resultados en diferentes momentos, es  secuencial y continuo por la 
naturaleza de una serie de tiempo.
- **Actuators:** Comprar, vender, esperar (no hacer nada.)
- **Sensors:** Seguimiento en tiempo real al precio de diferentes acciones y de nuestro portafolio.


### 6. Sistema de diagnóstico médico asistido por IA

- **Performance:** Diágnostico oportuno y preciso, mejora de la salud del paciente.
- **Environment:** Hospital, pacientes, radiografías, expedientes médicos. Es estocástico pues el mismo procedimiento puede tener diferentes resultados en cada paciente. Es secuencial y continuo pues el número de padecimientos es infinito.
- **Actuators:** Predecir si tiene o no tiene X padecimiento. O arrojar la probabilidad de que lo tenga por medio de un modelo.
- **Sensors:** Visión computacional, OCR.


### 7. Dron de inspección de infraestructura

- **Performance:** Número de desperfectos encontrados, duración de la batería, distancia remota, protocolos de seguridad y rescate.
- **Environment:** Obras, proyectos, construcciones y edificaciones. Es secuencial, estocástico, continuo y parcialmente observable.
- **Actuators:** tomar fotos, grabar videos, elevarse y descender, desplazarse, rotar, regresar a base.
- **Sensors:** sensor de altitud, detección de movimiento y de obstáculos.

### 8. Agente jugador de ajedrez

- **Performance:** Gana la partida, número de turnos que le toma, piezas pérdidas o puntos obtenidos por pieza.
- **Environment:** Un tablero de ajedrez con piezas. Es observable pues se conoce todo el tablero y todas las ubicaciones de las piezas, es secuencial y estático pues se juega por turnos.
- **Actuators:** Mover pieza (según la pieza y el tablero en cuestión)
- **Sensors:** Visión computacional o matriz de ubicaciones de las piezas, con el historial de movimientos.

