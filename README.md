# Manual de Usuario para Arredator - Geolocalizador

## Descripción
Este proyecto, llamado "Arredator - Geolocalizador", es una herramienta que permite gestionar y visualizar datos relacionados con propiedades inmobiliarias. El programa se basa en una estructura de árbol AVL para organizar los datos y proporciona funciones como inserción, eliminación, búsqueda y visualización de información relevante.

## Requisitos Previos
- Python 3.x instalado en su sistema.
- Paquetes adicionales instalados:
  - pandas
  - seaborn
  - matplotlib
  - geopy
  - folium
  - graphviz

## Instalación
1. Clona este repositorio en tu máquina local o descarga el código fuente como un archivo ZIP.
2. Abre una terminal o línea de comandos.
3. Navega al directorio donde se encuentra el proyecto.
4. Ejecuta el siguiente comando para instalar las dependencias necesarias:
pip install pandas seaborn matplotlib geopy folium graphviz


## Uso
1. Abre un entorno de desarrollo de Python (por ejemplo, Jupyter Notebook o una terminal).
2. Importa el archivo `arredator.py` en tu entorno de desarrollo.
3. Crea una instancia de la clase `Arbol` para comenzar a trabajar con los datos.
4. Utiliza las funciones proporcionadas por la clase `Arbol` para realizar operaciones como la inserción, eliminación y búsqueda de datos.
5. Utiliza las funciones de búsqueda específicas para encontrar información basada en ciertos criterios, como la ciudad, el tipo de propiedad o la cantidad de dormitorios.

A continuación, se proporcionan algunas operaciones comunes:

- Para insertar un nuevo nodo con datos en el árbol:
```python
arbol.insert(dato)
Para eliminar un nodo del árbol basado en su métrica:

python
Copy code
arbol.delete_node(metrica)
Para buscar un nodo basado en su métrica:

python
Copy code
nodo = arbol.search(metrica)
Para buscar información específica utilizando criterios:

python
Copy code
lista_criterio = []
Search_criterio(listaPrincipal, listaCriterio)
Para obtener el recorrido por niveles del árbol:

python
Copy code
recorrido_niveles = arbol.level_order_traversal()
Para visualizar el árbol AVL:
Utiliza la función generador_dot y visualiza el archivo de imagen generado.

Contribución
Si deseas contribuir a este proyecto, puedes hacerlo de la siguiente manera:

Fork este repositorio.
Realiza tus cambios en tu repositorio fork.
Crea una solicitud de extracción (pull request) a este repositorio para revisar tus cambios.
Problemas Conocidos
No se han identificado problemas conocidos en este momento.
Soporte
Si necesitas ayuda o tienes alguna pregunta sobre el uso de esta herramienta, puedes contactar a los autores del proyecto:

Alejandro Fontalvo
Sibeli Rodriguez
Juan Morales
Camilo De la Rosa
Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para obtener más detalles.

Agradecimientos
Agradecemos a todos los desarrolladores y proyectos de código abierto que hicieron posible la creación de esta herramienta.
