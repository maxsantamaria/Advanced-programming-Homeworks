# Sobre el funcionamiento
- server:
	- main.py: al ejecutarlo se abre el servidor para recibir conexiones
	- image: dentro de una carpeta con ese nombre deben ir las imágenes que contiene el servidor
	- comments: esta carpeta va a contener los comentarios de cada foto, hay uno de ejemplo para la imagen MickeyMouse.

- client:
	- main.py: ejecuta la  (frontend). Primero se pregunta por el nombre, al pasar esta interfaz se inicia la conexión del cliente al servidor
	- cliente.py: tiene la clase Cliente que es el socket que se conectará. Es importado por el módulo main
	- handle_image.py: es una especie de backend para el manejo de imagenes (blurry, balde, recorte) y otras funciones útiles de manejo de bytes.
	- eventos.py: contiene las clases de eventos que se envían entre cliente.py y main.py mediante las señales.
- IMPORTANTE: no sé por qué pero la primera vez que lo ejecutaba después de harto tiempo me tiraba un error y no se enviaban todas las imágenes correctamente. Así que reiniciaba el server y el cliente y ahí sí funcionaba perfectamente. Por lo tanto recomiendo ejecutarlo una vez (ambos main), ingresar al Dashboard con el cliente y después reiniciar todo para que funcione bien y no esté el error.

# Alcance
- Si hay alguien editando una foto, al apretar un botón de edición este se va a bloquear para que se de cuenta de que está en ese modo (ej.: modo "blurry")
- Si alguien ingresa al editor y ya hay otra persona editando la foto, va a tener todos los botones de edición (recorte, blurry, balde) bloqueados y no va a poder hacer nada
- El blurry y algunos baldes pueden tardar más de lo normal (10 segundos aprox.) porque recorre muchos pixeles. Si bien esta función la realiza un Thread y el programa no se frena (uno puede hacer click en  otros botones, etc.) se recomienda no hacer otras funciones hasta que termina el blurry, para que no interfiera con los bytes de la imgagen
- Las imágenes se actualizan tanto en el Dashboard de todos, como en el editor de los que están mirando.
- Si un usuario quiere cambiar de color el balde, tiene que apretar el cursor y luego nuevamente el botón de balde ya que pregunta por color solo al ingresar a esa función
- Cuando un usuario sube una imagen al sistema, este no se la pone en su dashboard automáticamente (porque se asumió que va a tener otras 6 ya en esa posición). Así que lo que debería hacer es salir y volver a entrar al sistema para que le aparezca.
- Para los comentarios no se implementó que se evitara mostrar los emojis entre '<' '>'
- Todas las funcionalidades deberían estar funcionando bien

# Aclaraciones o supuestos
- Se asumió que las imágenes no iban a tener un tamaño demasiado grande, por lo que al abrir el editor este las va a mostrar del mismo tamaño que son. Esto se hizo así, porque éra más fácil trabajar con  los pixeles que se seleccionaban para las ediciones.
- Los comentarios si son muy largos van a tener scroll horizontal también (espero que no sea tan molesto)
- Al principio él servidor le envía los bytes completos de la imagen a los clientes (cuando ingresan), pero luego de esto las modificaciones enviadas son menores, ya que solo se envía la nueva información del idat.
- Asumí que un usuario iba a estar en solo una ventana de edición al mismo tiempo, no más.
- Cuando se trata de ingresar con el mismo nombre que otro que está conectado, se ingresa al Dashboard pero con una advertencia (pop up). Ahí hay un QLineEdit donde uno debería escribir su nuevo nombre para que logre entrar correctamente.
- No alcancé a hacer más bonita la interfaz, sorry si está muy desordenada