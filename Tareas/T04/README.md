
# Sobre los archivos y la ejecución

- Para la interacción es necesario ejecutar el archivo main.py
- Para que no haya un error de lectura los archivos csv deben tener como HEADER lo siguiente (principalmente por las tildes):
	- productos.csv: Producto; Tipo; Precio; Calorias; Tasa Putrefacción; Vendido en  (da lo mismo el orden)
	- parametros_iniciales: días_susto, personalidad_jekyll, llamado_policial, concha_estéreo, moda_llegada_campus, limite_paciencia, rapidez_vendedores, traslado_campus, probabilidad_permiso, distribución_almuerzo, base_mesada, personalidad_hide, dinero_funcionarios, stock_vendedores
- La opción 1 de la interacción lleva a ejecutar la simulación con el archivo parametros_iniciales.csv y la opción 2 es la comparación de escenarios de escenarios.csv
- El archivo entidades.py contiene a los actores de la simulación (personas y quickdevil). Se usa para poblar el sistema
- El archivo simulator.py contiene la clase de simulación para los 4 meses del primer semestre académico (Marzo, Abril, Mayo, Junio)
- variables.py contiene las constantes


# Sobre el funcionamiento y alcance

- Cada simulación de los 4 meses dura aprox 40 segundos (por favor tener paciencia :) )
- Para el caso de un escenario particular (parametros_iniciales) se imprimen los cambios de precio al pasar un mes (decía en el enunciado que había que ponerlo en consola) y al final las estadísticas ordenadas.
- Para el caso de comparación de escenarios no se imprime el cambio de precios ni las estadísticas pero al final se imprime por el lugar que quedó según la métrica y el valor de la métrica. Se decidió que era más útil tener todos los lugares que solo los primeros 3 (o quizás se me olvidó restringirlo a que se imprimieran solo los primeros 3).
- Según lo que se entendió del enunciado un escenario era mejor si la sumatoria de la métrica era mayor a la de otro. Por lo tanto (ejemplo) para cantidad de enfermos un escenario sería mejor que otro si tiene mayor cantidad de enfermos en suma de sus réplicas (por muy ilógico que suene). Si esto está mal, leer la lista de posiciones desde abajo hacia arriba :)
- Todo debería estar funcionando a menos que exista algún problema o error que no haya ocurrido en las pruebas realizadas hasta hoy.
- Hay una gran cantidad de lineas comentadas, principalmente prints porque se usaban para seguir la simulación y también ver los eventos que ocurren. Se puede usar para seguir el desarrollo o para entender mejor el código también (saber cómo se llega a qué punto).


# Sobre el modelamiento

- Ocurre que si uno lo piensa entre Vendedores y Miembros UC, pasa que los Miembros tienen como preferencias a los vendedores y los vendedores tienen en sus filas a los Miembros.  Para evitar modelar circularmente lo que se hizo fue un decorador en la clase Vendedor que le entregara a los Miembros UC su cola (entrega_cola). De esta forma se formaba una lista de preferencias con el atributo cola de cada Vendedor, ya que eso es lo único a lo que los Miembros UC deberían tener acceso en la práctica. Luego, los vendedores tienen una cola con Miembros UC, donde ellos ingresan y abandonan.
- Se quiso separar las preferencias en 2, colas de snack y colas de almuerzo, ya que eran comidas distintas con vendedores distintos. Pero al ser tan parecidas existían funciones y métodos también parecidos pero unos enfocados a SNACK y otros a ALMUERZO. Para esto se hizo primero el snack y luego se hizo casi la misma función pero con las diferencias del almuerzo (por eso hay métodos que se llaman igual pero con un 1 (snack) y un 2 (almuerzo))
- La clase simulator quedó bastante larga (más aún con la documentación), pero no se separó en 2 módulos porque al ser una clase era más ordenado que estuviera todo dentro de un módulo (perdón si cuesta encontrar lo buscado, pero intenté que los métodos tuvieran nombres bastante descriptivos).
- El método y el evento "persona_compra_snack" aplica para snacks y almuerzo, pero se olvidó cambiar el nombre a solo "persona_compra".
- Hay algo que puede parecer raro: Después del primer mes se actualizan los precios según las ventas y ocurre que muchos vendedores no venden alguno de sus productos ni una vez en el mes, ya que los Alumnos siempre elegirán el más barato y los Funcionarios el de más calidad por lo que términos intermedios no se compran. Al ingresar esto en la fórmula queda como que el precio baja 30 * 5 % es decir más de su precio actual y queda en 0.01 de su precio (por restricción). Por eso bajan tanto los precios (quedan en 0.0algo) pero no afecta en el desarrollo de la simulación.


# Supuestos no aclarados en el enunciado

-  Las personas primero entran a la cola y ahí deciden si se quedan o si se cambian. Estos cambios no cuentan para las estadísticas de cambiarse de cola, sino que era para simplificar el algoritmo y aprovechar la función. Solamente se cuenta como rechazo o cambio de cola si es que llegó un funcionario y el movimiento para la cola hizo que algunos se quisieran ir (función actualizar_cola). Si ya se cambiaron a todas sus opciones, van al Quick Devil
- Se asume que cuando una persona termina de ser atendida y paga, se come instanteamente el producto, asi que se toma en ese instante la putrefaccion y calidad. De hecho para las estadísticas de calidad promedio, se toma como valor la calidad de los productos en el minuto que fueron comprados, ya que nos interesa estudiar un posible efecto en los queridos consumidores de la universidad.
- Se considera que en ir a comprar snack igual se demoran el tiempo T desde la universidad. Esto se cambió en el enunciado a mitad del plazo y se dijo que se podía dejar como antes, y pensé que era lo más lógico que también se demoraran un tiempo en caminar hacia afuera.
- Tiempo que se demoran carabineros en fiscalizar no influye en tiempo maximo de espera, ya que los consumidores con comprensivos y les da pena que el vendedor pierda su clientela por una simple fiscalización. Es decir solo se corre el tiempo de atención hasta que se deje de fiscalizar (a menos que se escape o sea confiscado).
- Para estadísticas se asume descompuesto como putrefacción > 0.9. Esto se decidió para usar una medida distinta a la calidad, la cual era muy cercana a 0 siempre y se dijo que se podía decidir ya que no estaba especificado
- Para estadísticas se consideró los dias de lluvias de hamburguesas como días en que los vendedores iban y no vendían nada, por lo que aplica para el mínimo de ventas diarias (hay días con 0 ventas)
- El día en que el vendedor se escapa por no tener permiso no cuenta como parte de los dias susto que no estará
- El dinero confiscado por los carabineros se obtiene multiplicando el stock por el promedio de los precios de cada producto del vendedor




