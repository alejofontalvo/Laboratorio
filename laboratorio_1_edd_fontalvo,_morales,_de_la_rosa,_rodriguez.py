# -*- coding: utf-8 -*-
"""Laboratorio #1 EDD-fontalvo, Morales, De La Rosa, Rodriguez

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11DQ0qVPd28W0vQBX4Kek7W5tGPbnkJLx
"""

import graphviz as gz
from IPython.display import Image, display
from pprint import pprint
from queue import Queue
from typing import List, Any

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from google.colab import drive
!pip install geopy
from geopy.geocoders import Nominatim
!pip install folium
import folium
import os

from graphviz.dot import node
from collections import deque

class Cola:

    def __init__(self, Queue_lenght: int) -> None:

        self.__Queue_lenght = Queue_lenght
        self.__Queue : list[Any] = []

    def __repr__(self) -> str:
        return str(self.__Queue)
    # AGREGA NUEVO ELEMENTO AL FINAL DE LA COLA
    def Add_Elem_Queue(self, New_Element: Any)->None:

        if(len(self.__Queue) >= self.__Queue_lenght):
            raise ValueError ("Stack_Over_flow")
        else:
            self.__Queue.append(New_Element)

    # BORRA ELEMENTO DE LA PARTE FRONTAL DE LA COLA
    def Del_Elem_Queue(self)->None:
        if(len(self.__Queue) == 0 or self.__Queue_lenght == 0):
            raise ValueError("Theres no element")
        else:
            self.__Queue.pop(0)
            #print(f"eliminado {a}")

     # TOMA UN INDICE COMO ARGUMENTO Y DEVUELVE EL ELEMENTO EN ESA POSICION EN LA COLA
    def Get_Element(self, index: int)->None:
        if(len (self.__Queue) == 0 ):
            return None
        return self.__Queue[index]

    # DEVUELVE LA LONGITUD ACTUAL DE LA COLA
    def Get_lenght(self)->None:
        return len(self.__Queue)

    # SE CREA LA CLASE NODO Y SE INSTANCIA
class Nodo:
    def __init__(self, dato_nodo, level=0) -> None: #Dato del nodo
        self.dato_nodo = dato_nodo
        self.right = None
        self.left = None
        self.level = level

    # SE CREA LA CLASE ARBOL Y SE INSTANCIA
class Arbol:
    def __init__(self) -> None:
        self.raiz = None

    # FUNCION PARA AÑADIR UN NODO AL ARBOL
    def addNode(self, dato, level=0, apuntador=None):
        if self.raiz is None:
            self.raiz = Nodo(dato, level)
            return
        if apuntador is None:
            apuntador = self.raiz

        if apuntador.dato_nodo > dato:
            if apuntador.left is None:
                apuntador.left = Nodo(dato, level=level)
                return
            else:
                self.addNode(dato, apuntador.level + 1, apuntador=apuntador.left)

                return
        elif apuntador.dato_nodo < dato:
            if apuntador.right is None:
                apuntador.right = Nodo(dato, level)
                return
            else:
                self.addNode(dato, apuntador.level + 1, apuntador=apuntador.right)
                return

    # FUNCION PARA CALCULAR SI EL ARBOL ES MAXIMO, ES DECIR SI ESTA COMPLETO
    def arbol_max(self) -> bool:
        nodes = self.get_all_nodes(self.raiz)
        max_Value = max(n.lvl for n in nodes)
        nodes_max = filter(lambda x: x.level == max_Value, nodes)
        return 2 ** max_Value == len(nodes_max)

    #CALCULA EL INORDER DEL ARBOL
    def inorder(self, arbol, result):
        if arbol:
            self.inorder(arbol.left, result)
            result.append(arbol.dato_nodo)
            self.inorder(arbol.right, result)


    # FUNCION QUE MUESTRE TODOS LOS NODOS DEL ARBOL
    def get_all_nodes(self, arbol) -> list:
        result = []
        self.inorder(arbol, result)
        return result

    # Método para calcular la altura de un nodo
    def height(self, node):
        if node is None:
            return -1
        return max(self.height(node.left), self.height(node.right)) + 1

    # FUNCION ENCARGADA DE ROTACIONES HACIA LA IZQUIERDA
    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        x.level = 1 + max(self.height(x.left), self.height(x.right))
        y.level = 1 + max(self.height(y.left), self.height(y.right))
        return y

    #FUNCION DE ROTACIONES HACIA LA DERECHA
    def rotate_right(self, y):
        x = y.left
        y.left = x.right
        x.right = y
        y.level = 1 + max(self.height(y.left), self.height(y.right))
        x.level = 1 + max(self.height(x.left), self.height(x.right))
        return x

    #FUNCIONES BALANCEAN EL ARBOL
    def balance_tree(self):
        self.balanceo(self.raiz)

    def balanceo(self, node):
        if node is None:
            return node

        # Actualizar la altura del nodo
        node.level = 1+max(self.height(node.left), self.height(node.right))

        # Calcular el factor de equilibrio del nodo
        balance_factor = self.balance_factor(node)

        # Realizar rotaciones si es necesario
        if balance_factor > 1:
            # Desequilibrio en el subárbol izquierdo
            if self.balance_factor(node.left) >= 0:
                node = self.rotate_right(node)
            else:
                node.left = self.rotate_left(node.left)
                node = self.rotate_right(node)

        elif balance_factor < -1:
            # Desequilibrio en el subárbol derecho
            if self.balance_factor(node.right) <= 0:
                node = self.rotate_left(node)
            else:
                node.right = self.rotate_right(node.right)
                node = self.rotate_left(node)

        return node

    #FUNCION QUE ARROJA EL FATOR DE BALANCEO DE LOS NODOS
    def balance_factor(self, node):
        if node is None:
            return 0
        return self.height(node.left) - self.height(node.right)


    #FUNCIONES ENCRAGADAS DE METER INFORMACION A LOS NODOS
    def insert(self, dato):
        self.raiz = self._insert(self.raiz, dato)


    def _insert(self, node, dato):

        if node is None:
            return Nodo(dato)

        if dato < node.dato_nodo:
            node.left = self._insert(node.left, dato)
        else:
            node.right = self._insert(node.right, dato)

        node.level = 1 + max(self.height(node.left), self.height(node.right))

        balance = self.balance_factor(node)

        if balance > 1:
            if dato < node.left.dato_nodo:

                return self.rotate_right(node)
            else:
                node.left = self.rotate_left(node.left)
                return self.rotate_right(node)

        if balance < -1:
            if dato > node.right.dato_nodo:
                return self.rotate_left(node)
            else:
                node.right = self.rotate_right(node.right)
                return self.rotate_left(node)

        return node

    #FUNCION QUE ARROJA EL FATOR DE BALANCEO DE LOS NODOS
    def get_balance(self, node):
        if node is None:
            return 0
        return self.height(node.left) - self.height(node.right)

    #FUNCIONES ENCARGADAS DE LLENAR Y DIBUJAR EL ARBOL AVL
    def avl(self, lista: list):
        self.raiz = None
        #listaDeValidacion = [lista[i][0] for i in range(len(lista))]
        #print(listaDeValidacion)
        for node in lista:
          self.insert(node)


    def createTreeWithAList(self, list):
        for i in list:
            self.addNode(i)


    def generador_dot(self, arbol, dot=None):
        if dot is None:
            dot = gz.Digraph(comment="AVL Tree")
        if arbol:
            info = f'--{arbol.dato_nodo[0]}--\n {arbol.dato_nodo[1]}\n{arbol.dato_nodo[2]}\n Ciudad: {arbol.dato_nodo[3]}\n{arbol.dato_nodo[4]}\n{arbol.dato_nodo[5]}\n{arbol.dato_nodo[6]}\n{arbol.dato_nodo[7]}\n{arbol.dato_nodo[8]}\n{arbol.dato_nodo[9]}\n{arbol.dato_nodo[10]}\n{arbol.dato_nodo[11]}\n{arbol.dato_nodo[12]}'
            dot.node(str(arbol.dato_nodo),label=info, color='lightblue', style='filled')
            if arbol.left:
                dot.edge(str(arbol.dato_nodo), str(arbol.left.dato_nodo))
                dot = self.generador_dot(arbol.left, dot)
            if arbol.right:
                dot.edge(str(arbol.dato_nodo), str(arbol.right.dato_nodo))
                dot = self.generador_dot(arbol.right, dot)
        return dot

    #ORDENA EL ARBOL RECURSIVAMENTE
    def __level_order_recursive(self, node):
              if node is None:
                  return
              queue = [node]
              def recursive_helper(queue):
                  if not queue:
                      return
                  next_level = []
                  for node in queue:
                      print(node.dato_nodo)
                      if node.left:
                          next_level.append(node.left)
                      if node.right:
                          next_level.append(node.right)
                  recursive_helper(next_level)
              recursive_helper(queue)
              return queue

    # FUNCION QUE ORDENA EL ARBOL
    def level_order_traversal(self):
        if not self.raiz:
            return []

        result = []
        queue = deque()
        queue.append(self.raiz)

        while queue:
            node = queue.popleft()
            result.append(node.dato_nodo)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        return result


    # FUNCION PRINCIPAL DE BUSQUEDA QUE ARROJA UN DATO
    def search2(self, elem: Any) -> tuple:
        p, pad = self.raiz, None
        while p is not None:
            if elem == p.dato_nodo[0]:
                return p.dato_nodo
            else:
                pad = p
                if elem < p.dato_nodo[0]:
                    p = p.left
                else:
                    p = p.right

        return p.dato_nodo

    # FUNCION PRINCIPAL DE BUSQUEDA QUE ARROJA UNA LISTA
    def search(self, elem: Any) -> tuple:
        p, pad = self.raiz, None
        while p is not None:
            if elem == p.dato_nodo[0]:
                return pad.dato_nodo
            else:
                pad = p
                if elem < p.dato_nodo[0]:
                    p = p.left
                else:
                    p = p.right

        return pad.dato_nodo[0]

    # FUNCION QUE SE UTILIZA PARA BUSCAR UBICACION DEL NODO
    def searchBalanceo(self, elem: Any) -> tuple:
        p, pad = self.raiz, None
        while p is not None:
            if elem == p.dato_nodo:
                return p, pad
            else:
                pad = p
                if elem < p.dato_nodo:
                    p = p.left
                else:
                    p = p.right

        return p, pad

    # BUSCA EL ABUELO
    def Abusearch(self, elem: Any) -> tuple:
        p, pad = self.raiz, None
        while p is not None:
            if elem == p.dato_nodo[0]:
                return pad.dato_nodo[0]
            else:
                pad = p
                if elem < p.dato_nodo[0]:
                    p = p.left
                else:
                    p = p.right

        return pad.dato_nodo[0]

    # FUNCION DE ELIMINAR UN NODO
    def __Delete_Node(self, value: Any) -> bool:
     tuple_ = self.searchBalanceo(value)
     hijo = tuple_[0]
     padre = tuple_[1]

     if hijo is not None:
        if hijo.left is None and hijo.right is None:
            if padre is not None:
                if padre.left == hijo:
                    padre.left = None
                else:
                    padre.right = None
            else:
                # Estamos eliminando la raíz
                self.raiz = None
        elif hijo.left is not None and hijo.right is not None:
            # En este caso, reemplazamos el nodo con el nodo predecesor
            predecesor, padre_predecesor = self.__pred(hijo)
            hijo.dato_nodo = predecesor.dato_nodo

            # Ahora eliminamos el nodo predecesor
            if padre_predecesor.left == predecesor:
                padre_predecesor.left = predecesor.left
            else:
                padre_predecesor.right = predecesor.left
        else:
            # Nodo con un solo hijo, simplemente lo reemplazamos por ese hijo
            nieto = hijo.left if hijo.left is not None else hijo.right
            if padre is not None:
                if padre.left == hijo:
                    padre.left = nieto
                else:
                    padre.right = nieto
            else:
                # Estamos eliminando la raíz
                self.raiz = nieto
        return True
     return False

    #LLAMA A FUNCION PARA ELIMINAR EL NODO
    def delete_node(self, value: Any):
       deleted = self.__Delete_Node(value)

    # ENCUENTRA PREDECESOR
    def __pred(self, node: "Nodo") -> tuple:
     p, pad = node.left, node
     while p.right is not None:
        pad = p
        p = p.right
     return p, pad

    # ENCUENTRA SUCESOR
    def __sus(self, node: "Nodo") -> tuple:
     p, pad = node.right, node
     while p.left is not None:
        pad = p
        p = p.left
     return p, pad

    # BUSCA UN NODO EN EL ARBOL Y RETORNA EL NODO TIO
    def __Find_Uncle(self, node1: "Nodo", node2: "Nodo", node3: "Nodo", element: Any):
     if node1 is not None:
        if element == node1.dato_nodo[0]:
            if node3 is not None:
                return node3.dato_nodo  # Devuelve la información del tío
            else:
                return None  # No hay tío, retorna None

        elif element < node1.dato_nodo[0]:
            if node2 is not None:
                if node1 == node2.left:
                    return self.__Find_Uncle(node1.left, node1, node2.right, element)
                else:
                    return self.__Find_Uncle(node1.left, node1, node2.left, element)
            return self.__Find_Uncle(node1.left, node1, None, element)
        else:
            if node2 is not None:
                if node1 == node2.left:
                    return self.__Find_Uncle(node1.right, node1, node2.right, element)
                else:
                    return self.__Find_Uncle(node1.right, node1, node2.left, element)
            return self.__Find_Uncle(node1.right, node1, None, element)
     return None

    # LLAMA A LA FUNCION PARA ENCONTRAR EL TIO
    def find_uncle(self, node2, node3, element):
      uncle_info = self.__Find_Uncle(self.raiz, node2, node3, element)
      if uncle_info is not None:
          return uncle_info
      else:
          print("This node doesn't have an uncle")

    # BUSCA UN NODO CON UN VALOR DADO EN EL ARBOL Y RETORNA EL NODO ABUELO
    def find_grandparent(self, value):

        current_node = self.raiz  # Comenzamos desde la raíz
        parent = None  # Inicializamos el padre en None

        while current_node:
            if value == current_node.dato_nodo[0]:
                if parent:
                    grandparent = self.search(parent.dato_nodo)
                    return grandparent.dato_nodo
                else:
                    return None  # El nodo raíz no tiene abuelo
            elif value < current_node.dato_nodo[0]:
                parent = current_node
                current_node = current_node.left
            else:
                parent = current_node
                current_node = current_node.right

        return None

    # FUNCION LA CUAL BUSCA EL PADRE DE UN NODOD CON UN VALOR DADO EN EL ARBOL
    def find_parent(self, value):

        current_node = self.raiz  # Comenzamos desde la raíz
        parent = None  # Inicializamos el padre en None

        while current_node:
            if value == current_node.dato_nodo:
                return parent
            elif value < current_node.dato_nodo:
                parent = current_node
                current_node = current_node.left
            else:
                parent = current_node
                current_node = current_node.right

        return None

    # FUNCION ENCRAGADA DE BUSCAR LOS NOVELES DE CADA NODO
    def find_node_levels(self, value):
                """
                Busca un nodo con un valor dado en el árbol y devuelve su nivel.
                Devuelve -1 si el nodo no se encuentra en el árbol.
                """
                level = 0  # Inicializamos el nivel en 0
                current_node = self.raiz  # Comenzamos desde la raíz

                while current_node:
                    if value == current_node.dato_nodo[0]:
                        return level  # Devolvemos el nivel cuando encontramos el nodo
                    elif value < current_node.dato_nodo[0]:
                        current_node = current_node.left
                    else:
                        current_node = current_node.right

                    level += 1  # Incrementamos el nivel en cada paso
                return -1

    #LLAMA FUNCION QUE ORENA EL ARBOL  DE MANERA RECURSIVA
    def level_search_rec(self):
      return self.__level_order_recursive(self.raiz)

# FUNCIONES ESCENCIALES PARA EL PUNTO 4) DONDE SE MUESTRAN NODOS CON 3 CRITERIOS EXACTOS

def count(string1, string2)->bool:
  if(unicodedata.normalize('NFKD', string1).encode('ASCII', 'ignore').strip().lower() == unicodedata.normalize('NFKD', string2).encode('ASCII', 'ignore').strip().lower()):
    return True
  else:
    return False

def  Search_criterio(listaPrincipal: list, listaCriterio: list)->list:
  for i in range(1,4):
    Criterio= input(f"Coloque el criterio de busqueda Numero {i}")
    listaCriterio.append(Criterio)
  for j in listaPrincipal:
    k,sw = 0,0
    while k <= len(listaCriterio) and sw == 0:
      if(count(j[6], listaCriterio[0]) and count(j[8], listaCriterio[1]) and count(j[-4], listaCriterio[2])):
        print("The current data was succesfully found")
        print(j)
        sw= 1
      k+=1

# SE LEE EL CSV DADO EN EL LABORATORIO
df_acc = pd.read_csv("https://cursos.uninorte.edu.co/content/enforced/78211-202330_2446/co_properties_final.csv?_&d2lSessionVal=LhuOVOtMcmnZdTNdDIIS4bcTT")
df_acc

# CREO LA METRICA DADA EN EL LABORARIO Y LA INTEGRO A LIST_METRICA
df1 = df_acc[["surface_total","price","surface_covered"]]
list_price = list(df1["price"])
list_surface=list(df1["surface_total"])
list_surface_covered=list(df1["surface_covered"])
list_compare=[]
list_metrica=[]
list_metrica.append(list_price[0] // list_surface[0])
list_compare.append(list_metrica[0])

# COMPRUEBO SI LA METRICA ESTA REPETIDA Y DADO EL CASO LO ESTE, SE CAMBIA POR OTRA METRICA UNICA

for i in range(1,len(list_price)):
          list_metrica.append(list_price[i]//list_surface[i])
          if(list_metrica[i] in list_compare):
              print(f"ocurrency found // element {list_metrica[i]} // value {i}")
              list_metrica[i] =((list_price[i]//list_surface_covered[i])*pow(4,3)) #anado a la metrica dos los elementos comparados con la columna price y surface covered
              list_compare.append(list_metrica[i])
print(list_metrica)
          ################################################################
          # lista title
title = df_acc["title"].tolist()
print (title)
          # lista department
department = df_acc["department"].tolist()
print (department)
          # lista city
city = df_acc["city"].tolist()
print(city)
          # lista property
Tproperty = df_acc["property_type"].tolist()
print(Tproperty)
          # lista latitude
latitude = df_acc["latitude"].tolist()
print (latitude)
          # lista longitude
longitude = df_acc["longitude"].tolist()
print (longitude)
          # lista surface_total
surface_total = df_acc["surface_total"].tolist()
print (surface_total)
          # lista surface_covered
surface_covered = df_acc["surface_covered"].tolist()
print (surface_covered)
          # lista bedrooms
bedrooms = df_acc["bedrooms"].tolist()
print (bedrooms)
          # lista bathrooms
bathrooms = df_acc["bathrooms"].tolist()
print (bathrooms)
          # lista operation
operation = df_acc["operation_type"].tolist()
print (operation)
          # lista price
price = df_acc["price"].tolist()
print (price)

# Se crea la lista magna, donde se guaradan todos los datos del nodo

ListaMagna = []
for i in range(len(list_metrica)):
              ListaMagna.append([list_metrica[i], title[i], department[i], city[i], Tproperty[i], latitude[i], longitude[i], surface_total[i], surface_covered[i],bedrooms[i], bathrooms[i], operation[i],price[i]])

# DEFINO LA LISTA DONDE GUARDARE DATOS PARA GENERAR EL MAPA DE GEOLOCALIZACION
ListaMapa1 = []

# Separo columnas del csv original
df_criterio= df_acc.loc[:, ['title','city','property_type','bedrooms','latitude','longitude']]
df_criterio

# Vuelvo a repetir el proceso, dando como condicion los datos que contengan a Barranquilla
criterio = df_criterio.loc[df_criterio['city']=='Barranquilla',['city','bedrooms','property_type', 'latitude','longitude','title']]
criterio

# Vuelvo a repetir el proceso, dando como condicion los datos que contengan bedrooms >= 2
criterio1 = criterio.loc[criterio['bedrooms'] >= 2,['city','bedrooms','property_type', 'latitude','longitude','title']]
criterio1

# Vuelvo a repetir el proceso, dando como condicion los datos que el tipo de propiedad sea Apartamento
baq = criterio1.loc[criterio1['property_type'] == 'Apartamento' ,['city','bedrooms','property_type', 'latitude','longitude','title']]
baq

# CREO UNA LISTA CON LA METRICA SEGUN EL DATASET
baq2 = baq
baq2["Metrica"] = pd.Series(list_metrica)
baq2 = baq2.loc[criterio1['property_type'] == 'Apartamento' ,['Metrica','city','bedrooms','property_type', 'latitude','longitude','title']]
baq2
metrica = baq2["Metrica"].tolist()
print(metrica)

# SE CREA EL MENU ITERATIVO
icon_value = 0
print("----------------------------------------------------------------")
print("-                                                              -")
print("-                                                              -")
print("-                ~ ARREDATOR - GEOLALIZATOR ~                  -")
print("-                             BY: Alejandro Fontalvo           -")
print("-                                 Sibeli Rodriguez             -")
print("-                                 Juan Morales                 -")
print("-                                 Camilo De la Rosa            -")
print("-                                                              -")
print("-                                                              -")
print("----------------------------------------------------------------")
op=1
def search__(info, listaMagna):
          value = None
          for j in listaMagna:
              s = j
              if(j[0] == info):
                value = j
                print(value)
          if (value ==None):
             print("No se encontro información")
             value = None
          return value
print("------------------- --- Insertando datos --- -------------------")
Primera_Decision = int(input(""" Qué opción desea?
                             1. Insertar los datos del dataframe
                             2. Agregar Nuevos datos
                             Digite aquí --> """))
if(Primera_Decision==1):



        New_list= []
        arbol = Arbol()

        print('ListaMagna')
        print(ListaMagna[0])

        arbol.avl(ListaMagna)
        b = arbol.level_order_traversal()
        print(b)
        SI = int(input("""Desea ver el arbol
                1. SI"""))
        if(SI == 1):
          dot = arbol.generador_dot(arbol.raiz)
            # Render the tree as a PNG image and display it in Colab
          #image = Image(dot.pipe(format='png'))
          dot.render('avl_tree(Insert)', view=True)
          print("se pinto")

else:
  if(Primera_Decision==2):
   print("Ejecutar")
while(op == 1):
    print("----------------------------------------------------------------")
    print("-                                                              -")
    print("-                     BIENVENIDO/A AL MEN∑                     -")
    print("-                                                              -")
    print("-                                                              -")
    print("-   1. Eliminar Datos                                          -")
    print("-   2. Buscar Nodo (Métrica)                                   -")
    print("-   3. Buscar Aspectos específicos                             -")
    print("-   4. Hallar Recorrido por Niveles (Recursivo)                -")
    print("-   5. SALIR                                                   -")
    print("-                                                              -")
    print("----------------------------------------------------------------")
    op2 = int(input("Digite La opción que desea realizar -->"))
    if(op2 == 1):
       pu2 = 1
       while (pu2 == 1):
          dele = int(input(("""Cuál es el nodo a eliminar?
                      Digite la métrica -->       """)))
          b = search__(dele,ListaMagna)
          arbol.delete_node(b)
          def eliminar_valor(lista, valor):
            i = 0
            while i < len(lista):
                if lista[i] == valor:
                    del lista[i]
                else:
                    i += 1

          eliminar_valor(ListaMagna,search__(dele,ListaMagna))
          b = arbol.level_order_traversal()
          print(b)
          arbol.createTreeWithAList(b)
          arbol.avl(b)
          dot = arbol.generador_dot(arbol.raiz)
          # Render the tree as a PNG image and display it in Colab
          ##image = Image(dot.pipe(format='png'))
          dot.render('avl_tree(Delete)', view=True)
          #display(image)
          if(op2 == 1):
            pu2 = int(input(("""Desea Eliminar más datos
                    1. SI
                    2. NO
                    Digite la opción deseada -->""")))
    elif (op2==2):
      dele = int(input(("""Cuál es el nodo a buscar?
                      Digite la métrica -->       """)))
      Nodo = search__(dele,ListaMagna)
      icon_value = dele


      #[666.0, 'Casa Condominio En Arriendo/venta En La Calera Vereda El Hato, Sector La Ramita. Cod. AREI21161', 'Cundinamarca', 'La Calera', 'Casa', 4.642, -74.011, 15000.0, 478.0, 5.0, 6.0, 'Arriendo', 10000000.0]
      print("El nodo que desea buscar es: --> ",Nodo)
      op3 = 1
      while(op3 == 1):
          print("----------------------------------------------------------------")
          print("-                                                              -")
          print("-                           EXTRA                              -")
          print("-                                                              -")
          print("-                                                              -")
          print("-   1. Obtener el nivel del nodo                               -")
          print("-   2. Obtener el factor de balanceo del nodo.                 -")
          print("-   3. Encontrar el padre del nodo                             -")
          print("-   4. Encontrar el abuelo del nodo                            -")
          print("-   5. Encontrar el tío del nodo.                              -")
          print("-   6. Mapa                                                    -")
          print("-   7. SALIR                                                   -")
          print("-                                                              -")
          print("----------------------------------------------------------------")
          op4= int(input("Digite La opción que desea realizar -->"))
          if(op4 == 1):
            print("El nodo está en el nivel: ",arbol.find_node_levels(dele))
            op3= int(input("""Desea seguir haciendo operaciones -->
            1. SI
            2. NO """))
          elif(op4==2):
            list_show_value=arbol.searchBalanceo(Nodo)
            print(f"El factor de balanceo del nodo: {Nodo[0]} es: {arbol.balance_factor(list_show_value[0])}")
          elif(op4 == 3):
             print("El padre del Nodo es: ",arbol.search(dele))
          elif(op4 == 4):
             Padre = arbol.Abusearch(dele)
             Abuelo = arbol.search(Padre)
             print("El Abuelo del Nodo es: ",Abuelo)
          elif(op4==5):
            b = arbol.find_uncle(None,None,dele)
            print("El Tío del Nodo es: ",b)
          elif(op4==6):
              Nodo = search__(icon_value,ListaMagna)
              dad = arbol.search(icon_value)
              Padre = arbol.Abusearch(icon_value)
              Abuelo = arbol.search(Padre)
              tio = arbol.find_uncle(None,None,icon_value)


              ListaMapa1.append(dad)
              ListaMapa1.append(Abuelo)
              ListaMapa1.append(tio)
              print(ListaMapa1)

              # Mapa
              mapa2 = folium.Map(location=[11.013,	-74.836	],zoom_start=8)

              #____________________________________________________________________________________________________________________________________
              # Ubicaciones cercanas al Nodo
              df = df_acc.loc[:, ['title','city','property_type','bedrooms','latitude','longitude']]
              ubi_cercanas = df.loc[df_criterio['city']== Nodo[3],['city','bedrooms','property_type', 'latitude','longitude','title']]
              for i in range(len(ubi_cercanas)):
                  folium.Marker(location=[ubi_cercanas.iloc[i,3],	ubi_cercanas.iloc[i,4]	],icon=folium.Icon(color='blue'),popup = ubi_cercanas.iloc[i ,5],angle=90).add_to(mapa2)

              # Nodo Principal
              folium.Marker(location=[Nodo[5],	Nodo[6]],icon=folium.Icon(color='red'),popup = Nodo[1],angle=90).add_to(mapa2)

              # Nodo Abuelo y Padre y Tio
              for i in range(len(ListaMapa1)):
                folium.Marker(location=[ListaMapa1[i][5],	ListaMapa1[i][6]],icon=folium.Icon(color='green'),popup = ListaMapa1[i][1],angle=90).add_to(mapa2)
              mapa2.save("mapaNodo.html")

              print("ya puedes ver tu ubicacion en el mapa, mostrado en el directorio")

          elif(op4==7):
            op3 = 0
    elif(op2==3):
          NewList = []
          for i in range(0,len(metrica)):
            Nodo = arbol.search2(metrica[i])
            print("El nodo que desea buscar es: --> ",Nodo)
          op3 = 1
          while(op3 == 1):
              print("----------------------------------------------------------------")
              print("-                                                              -")
              print("-                           EXTRA                              -")
              print("-                                                              -")
              print("-                                                              -")
              print("-   1. Obtener el nivel del nodo                               -")
              print("-   2. Obtener el factor de balanceo del nodo.                 -")
              print("-   3. Encontrar el padre del nodo                             -")
              print("-   4. Encontrar el abuelo del nodo                            -")
              print("-   5. Encontrar el tío del nodo.                              -")
              print("-   6. Mapa                                                    -")
              print("-   7. SALIR                                                   -")
              print("-                                                              -")
              print("----------------------------------------------------------------")
              op4= int(input("Digite La opción que desea realizar -->"))
              if(op4 == 1):
                for i in range(0,len(metrica)):
                  print("El nodo está en el nivel: ",arbol.find_node_levels(metrica[i]))
                op3= int(input("""Desea seguir haciendo operaciones -->
                  1. SI
                  2. NO """))
              elif(op4==2):
                for i in range(0,len(metrica)):
                  Nodo = arbol.search2(metrica[i])
                  list_show_value=arbol.searchBalanceo(Nodo)
                  print(f"El factor de balanceo del nodo: {Nodo[0]} es: {arbol.balance_factor(list_show_value[0])}")
              elif(op4 == 3):
                for i in range(0,len(metrica)):
                  print("El padre del Nodo es: ",arbol.search(metrica[i]))
              elif(op4 == 4):
                for i in range(0,len(metrica)):
                  Padre = arbol.Abusearch(metrica[i])
                  Abuelo = arbol.search(Padre)
                  print("El Abuelo del Nodo es: ",Abuelo)
              elif(op4==5):
                for i in range(0,len(metrica)):
                  C = arbol.find_uncle(None,None,metrica[i])
                  print("El tío del Nodo es: ", C)
              elif(op4==6):
                #ubicaciones barranquilla
                mapa1 = folium.Map(location=[11.013,	-74.836	],zoom_start=10)
                for i in range(len(baq)):
                  folium.Marker(location=[baq.iloc[i,3],	baq.iloc[i,4]	],icon=folium.Icon(color='purple'),popup = baq.iloc[i ,5],angle=90).add_to(mapa1)

                mapa1.save("mapaCriterio.html")

                print("ya puedes ver tu ubicacion en el mapa, mostrado en el directorio")
              elif(op4==7):
                op3=0

    elif(op2==4):
         arbol.level_search_rec()
    elif(op2==5):
      op =0

