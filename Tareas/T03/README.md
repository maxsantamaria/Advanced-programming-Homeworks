# Archivos Python

- El archivo main.py sirve para ejecutar la interfaz y realizar consultas siguiendo el formato especificado. Puede cargar un archivo .json o también ingresar manualmente. Si se elige la opción de guardar un archivo se crea el archivo resultados.txt que guarda los resultados de todas las consultas cargadas.

- El archivo reader.py contiene funciones contiene funciones que permitieron procesar la base de datos. Es más bien un parser para el archivo genomas.txt conectándolo con listas.txt.

- El archivo fenotipo.py abre las bases de datos y usa las funciones de reader para obtener la información del genoma. Luego, transforma el genoma de cada persona a características físicas (fenotipo) y guarda esta información como namedtuple. Aparte contiene funciones para determinar parentezcos a partir de las distintas características.

- El archivo consultas.py contiene las funciones para realizar las consultas (se usan en la interfaz del main).

- El archivo excepciones.py contiene los errores utilizados en esta área (genes) y algunas funciones para detectarlos.

- El archivo testing.py contiene distintos tests para probar que funcione el manejo de errores y que los resultados esperados son correctos (a partir de una base de datos más pequeña y otra con errores que están dentro de la carpeta de testing)

# Sobre el alcance

- Todas las funciones requeridas deberían estar funcionando correctamente (por lo menos por lo que alcancé a probar)
- Se hizo el bonus de Bubble Chart también, pero para este se asumió que los errores de ingreso de parámetros iban a ser solo si se ingresaba visualizar y algún tipo que fuera distinto a "ojos" o "pelo". Se asumió que solo bastaba con poner los círculos de color y no el nombre de lo que representaban sobre ellos.
- Me guíe por el nombre de las consultas que aparecen en el enunciado, es decir con los tildes correspondientes, así que si no se ingresan igual que ahí, mi programa se va a caer.

# Sobre la programación funcional

- Como el objetivo de la tarea era trabajar con esta programación, se buscó una forma de guardar el genoma de cada persona sin tener que instanciar todas las letras que venían en la base de datos, ya que para un caso muy grande se iba a demorar mucho. Para esto se hizo uso de Counter y se guardó el genoma en este diccionario que entrega como key cada triplete y value es la cantidad que aparece, por lo que sin importar el largo del genoma, el espacio que ocupará en RAM va a ser el mismo.
- Se intentó usar generadores lo mayor posible y cuando no se encontraba la forma, se usaban listas por comprensión. También se hizo uso de map, zip y reduce. Hay un caso para el cual el uso de listas fue contraproducente y es que en la llamada a gemélo genético o pariente grado 0 o -1, el programa debe verificar si hay GenomeError para ver si lo levanta. Como se explicó, hay que ver para cada persona, todas sus características y si alguna tiene este error, se levanta. En una parte de esta verificación se usa listas, por lo que se demora un poco más esta consulta que si no se verificara (igual siguen siendo milisegundos para el test 1).
- Se usó diccionario también para el archivo listas.txt porque no era tan grande como para gastar tanto espacio y se asumió que el ID no iba a estar siempre ordenado como esta en los archivos de ejemplo.

# Otras especificaciones

- La lista personas es clave porque contiene informaciones de fenotipo de cada persona y además el genoma como Counter (no usa casi nada de espacio) por lo que está lista se importa desde los módulos y es necesaria para las consultas (es necesario tener una base de datos con la que trabajar). Esta es la explicación también por la cual en el testing se modifica esta lista por la del nuevo archivo txt que vamos a usar.
- El genoma incorrecto usado para el testing fue creado a partir de la base de datos del test 1 pero se tomó una muestra de 5 personas y a una se le cambió una letra en uno de los tripletes de su característica GTA (se puso una letra distinta a GTAC)
- Las funciones deberían estar todas atomizadas. Algunas tienen líneas separadas con "\" o comentarios entre medio, por favor tenerlos en cuenta.
- Hay algunos import que no se usan, pero es porque los deje como funciones comentadas, por ejemplo se puede descomentar las líneas 387 y 389 del archivo fenotipo.py para ver cuánto demora la lectura de la base de datos (esto lo usaba porque al principio era mucho pero después con funcional se redujo a milisegundos). 
