No se pueden hacer mas de 15 order al dia por usuario:
	cuando hay un match parcial se considera y la order no se agota
	por completo, se considera equivalente a que el usuario hizo 2 orders, es decir la primera que contiene la parte que hizo match y la segunda que es lo que faltó por hacer match y que permanece activo en el mercado

Para la prioridad de match se ordenó primero las orders según mejor precio de compra o venta y luego si había empate según fecha de creación. Para la creación se usó solo la fecha y no la hora, ya que la base de datos inicial no contenía lo segundo.

Falta:
	- Guardar archivos cuando se cierra el programa
		- Generar nueva columna de saldo
		- Hacer if para que la primera vez no chequee la columna de saldo sino que vea el saldo con las orders realizadas
		- Asociar orders con usuario (order_id) para escribirlo en el archivo
	- Restringir valores negativos
	- Desplegar informacion programa mas ordenado
	- Agregar la tasa de comision
	- Quizas hacer un csv para los match
	- Guardar registros de hora cuando hay match, saldo, etc..
	- No transferir dinero a underaged	