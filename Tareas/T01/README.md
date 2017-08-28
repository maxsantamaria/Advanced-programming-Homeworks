# Manual del usuario:

- Para ejecutar la aplicación es necesario usar el archivo main.py
  Este contiene diferentes modulos, algunos de ellos son los siguientes:
	- User: módulo que contiene a la clase usuarios y sus subclases, además de algunas funciones que tenían relación con los usuarios
	- Mercado: módulo que contiene las clases Mercado y Moneda
	- Order: módulo que contiene la clase Order y sus subclases y además la clase Match que se genera con un Ask y un Bid
	- Sistema: módulo que agrupa las funcionalidades del sistema, principalmente con el método de determinar match y con las diferentes opciones en el menú de cada usuario
	- csv_reader: módulo que sirve para leer los archivos csv sin usar el módulo csv. También sirve para ordenarlos.

- Es importante mencionar una condición para que la aplicación funcione bien: la primera vez que se use no debe existir el archivo matches.csv, el cual se va a crear al finalizar el primer uso. Esto porque hay una condición dependiendo si existe o no ese archivo y se consideró que cuando no existía era equivalente a que era el primer uso de la aplicación.

- Primero uno tiene la opción de registrarse o de identificarse si ya está registrado. Así se entrega el saldo del usuario y sus orders hasta el momento. En cuanto al saldo, se entrega la cantidad de cada currency, pero para ver cuánto equivale eso a moneda DCC (usando precio actual y si no existe, 1:1), hay que seleccionar la opción 9 de consultar saldo. Sobre las orders propias, para los Trader se consideró que podían ver sus orders propias sin restricción de tiempo, para ver si habían hecho match o no, porque sino sería mucha la información que no disponen y no entenderían el funcionamiento. Para el resto de las orders sí tienen la restricción de los 7 días. Luego de eso se despliega el menú de opciones dependiendo del tipo de usuario que sea.

- Luego uno puede elegir la opción que desee ingresando el número correspondiente y ENTER. Todas las funcionalidades están disponibles para operar.

- En algunas ocasiones dentro de una opción hay que elegir otra y en algunas funcionalidades se consideró importante poder "arrepentirse" y volver al menú principal ingresando un 0 y ENTER, por ejemplo al elegir hacer una order, ya que se pensó en que el usuario se podía equivocar y no debería estar obligado a hacer una order para volver al principal. En las opciones que no se añadió esta "vuelta", se consideró que no era necesario, ya que eran funcionalidades que desplegaban información y no que pasaban a llevar los derechos del usuario.

- Está la opción de cerrar la sesión y dejar a otro usuario que entre o también de cerrar el sistema, lo cual cierra la aplicación pero guarda todo en los archivos correspondientes para cuando se abra otra vez.

# Sobre los archivos:

- Después del primer uso se actualiza users.csv ordenándolo en una secuencia definida de columnas la cual pareció lógica al creador del programa. También se agregan columnas: balance, el cual es un diccionario que guarda el saldo de cada currency; tipo, el cual guarda el tipo de usuario que es; mercados, que guarda los mercados (ticker) inscritos por cada usuario.
-orders.csv se ordena según id de menor a mayor para tener una mejor visualización de las acciones.
- Carpeta registros: después del primer uso se generan varios archivos en esta carpeta que son para los creadores del sistema para analizar el comportamiento de los usuarios. Es importante mencionar que para el archivo de consultar orders activas o historicas, se guardó en cada línea, todas las orders que se le desplegaban al usuario que consultaba en el sistema por ellas. Es por esto que puede quedar algo extenso el archivo.
- matches.csv: guarda los matches para el futuro
- Todos los archivos se sobreescriben al cerrar el sistema, por lo que si no lo cierran, los cambios no se guardan.

# Sobre los alcances:

- Todas las funcionalidades del menú están funcionando correctamente, a menos de que ocurra algún error no considerado en las pruebas. Para los usuarios ya existentes en la base de datos inicial, se decidió asignarles un premio de 300.000 DCC a cada uno en virtud de ser los primeros usuarios del sistema. El resto que se inscriba parte en 0 y si son mayores de edad se les entrega 100.000 DCC. Esto se hizo para que no fuera tedioso hacer un upgrade a Investor por parte de los primeros usuarios (inscribiéndose en los mercados DCC).
- Existe manejo y control de errores para todos los inputs, cosa de no asignarle presión al usuario de ingresar el formato correcto y que el sistema se caiga. Al ingresar algo mal, el sistema ingresa mensajes como Formato no válido o cosas por el estilo y repite la pregunta.
- Se usó programación orientada a objetos, herencia, properties, estructuras de datos.

# Sobre el código:

- Existen comentarios en el código explicando o aclarando algunas cosas que puedan quedar ambiguas.
- Se intentó mantenerse bajo las reglas del PEP8, lo cual al final significó algo de desorden en las líneas que eran muy largas (79 caracteres máximo) y se usaban separadores de línea, que pueden complicar un poco la lectura del código
- Existen circularidades, lamentablemente cuando me di cuenta de la mala práctica, tenía el código muy avanzado y hubiese sido mucho trabajo escribirlo todo de nuevo. Se aprendió la lección y no se volverá a repetir para programas en el futuro.

# Otras consideraciones:

- Cuando hay un match parcial y la order no se agota	por completo, se considera equivalente a que el usuario hizo 2 orders, es decir la primera que contiene la parte que hizo match y la segunda que es lo que faltó por hacer match y que permanece activo en el mercado. Esto aplicará para la restricción de hacer máximo 15 orders diarias (match parcial puede significar haber hecho más de una order)
- Para la prioridad de match se ordenó primero las orders según mejor precio de compra o venta y luego si había empate según fecha de creación. Para la creación se usó solo la fecha y no la hora, ya que la base de datos inicial no contenía lo segundo.
- Para el registro de match donde hay que guardar la hora, no se consideraron los match de la base de datos inicial, ya que no contenían la información de la hora.
- Hay match parciales al comienzo de la base de datos, se consideró la fecha de match como la actual, ya que el sistema los emparejó recién ahí.
- Todos los usuarios iniciales parten siendo Traders (a menos que tengan menos de 18 -> Underaged)
- Todos los mercados tienen una tasa de comisión fija igual a 0.10
- El saldo inicial de los usuarios se calcula viendo sus orders activas (tienen que tener lo que ofrecen) y los match realizados. Luego se usa la columna de balance en users.csv
- Underaged no tienen saldo ni orders realizadas.

