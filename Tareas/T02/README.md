# Estructuras de datos a implementar
- ListaLigada():
	- Va a simular lo que hace una lista. Para hacerla se hacen nodos que guarden un valor y al nodo siguiente
	- Va a contener los metodos getitem, setitem, delitem para poder mutar la lista y obtener sus valores
	- Va a ser iterable gracias a __iter__ y __self__
	- Se va a poder crear entregandole una secuencia de elementos. Para eso se usa *args en __init__
	- Esta estructura se usará para distintas partes de la tarea, como guardar datos ordenados, piezas de los jugadores, piezas disponibles, etc.

- Diccionario():
	- Simula el comportamiento de un diccionario. Se hacen nodos con atributo key, valor y nodo siguiente
	- Se puede acceder a sus elementos utilizando la key adecuada (no la posicion como en la ListaLigada)
	- Es iterable para recorrer sus elementos
	- Se puede acceder a una lista de keys, a una lista de values y a una lista de items llamando a la función correspondiente
	- Se va a usar en la tarea para relacionar los bordes con sus segmentos. También para ver la cantidad de piezas de un tipo que hay. También para guardar la info de algún usuario se podría usar, como la cantidad de ciudades, caminos, etc.

- Tuplas():
	- Simula el comportamiento de las tuplas. Se usan los mismo nodos de lista ligada
	- Esta estructura no es mutable, por lo que si bien se puede acceder a sus elementos, no se pueden modificar
	- Se va a implementar principalmente para las posiciones dentro del tablero ya que serán tuplas (posiciónx, posicióny) y cada posición dentro del tablero no cambiará
	- Es iterable con __iter__ y __next__
	- Se va a poder crear entregandole una secuencia de elementos. Para eso se usa *args en __init__


Se asume que si una ciudad esta en el borde del tablero y tiene un camino conectado que sigue por el borde del tablero, entonces si se le asignan los puntos correspondientes a que el camino lo unio a la grilla
Ejemplo:

 ![Image](https://github.com/IIC2233/mesantamaria-iic2233-2017-2/tree/master/Tareas/T02/images/camino_grilla.png)
Lo anterior es válido para tener puntos de uníon entre ciudad y grilla gracias a un camino.