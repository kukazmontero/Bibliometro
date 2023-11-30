## Algoritmos de Ruteo y Redes Resilientes - Bibliometro

| **Integrantes del Grupo 1**                           |
|------------------------------------------------------|
| Hugo Jerez                                           |
| Lukas Montero                                        |
| David Salas                                          |

| **Profesor**                                          |
|------------------------------------------------------|
| Nicolas Boettcher                                    |

| **Descripción del Proyecto**                           |
|------------------------------------------------------|
| El proyecto se centra en el servicio de bibliotecas pequeñas "Bibliometro" del metro de Santiago de Chile, abordando el problema de la eficiencia en la solicitud de libros. El objetivo es optimizar las rutas para los usuarios que buscan libros específicos en diferentes estaciones de metro, utilizando algoritmos de ruteo resiliente. |

| **Problemática Identificada**                         |
|------------------------------------------------------|
| Los usuarios de Bibliometro enfrentan dificultades para solicitar libros de manera eficiente. El proyecto busca encontrar la ruta de menor tiempo y costo en caso de que un libro no esté disponible o surjan incidentes relacionados con el libro. |

| **Solución Hipotética**                               |
|------------------------------------------------------|
| La solución propuesta utiliza ruteo resiliente para optimizar el acceso a los bibliometros, minimizando el tiempo de viaje y asegurando la disponibilidad de los libros. Se considera el uso del algoritmo A* por su eficiencia en grafos grandes y capacidad de adaptarse a cambios dinámicos. |

| **Objetivos**                                         |
|------------------------------------------------------|
| - Proporcionar una mejor experiencia a los usuarios de las estaciones de bibliometro. |
| - Crear un sistema que encuentre la ruta óptima para la búsqueda física de libros. |

| **Infraestructura**                                   |
|------------------------------------------------------|
| El sistema utiliza múltiples microservicios con alta disponibilidad y baja latencia, integrando tecnologías como WordPress Rest API, Google Cloud Function, MongoDB, y Google Cloud Scheduler. |
