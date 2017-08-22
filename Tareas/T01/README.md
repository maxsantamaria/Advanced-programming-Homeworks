No se pueden hacer mas de 15 order al dia por usuario:
	cuando hay un match parcial se considera y la order no se agota
	por completo, se considera equivalente a que el usuario hizo 2 orders, es decir la primera que contiene la parte que hizo match y la segunda que es lo que faltó por hacer match y que permanece activo en el mercado


Falta:
	- Guardar archivos cuando se cierra el programa
		- Generar nueva columna de saldo
		- Hacer if para que la primera vez no chequee la columna de saldo sino que vea el saldo con las orders realizadas
		- Asociar orders con usuario (order_id)
	- Restringir valores negativos